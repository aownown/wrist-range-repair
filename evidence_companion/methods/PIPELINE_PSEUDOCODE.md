# Operational pseudocode for the existing editor

This is a reading guide to the retained implementations, not executable code, a new algorithm, or a substitute for complete runtime dependencies. Main equations (1)–(6) and SI S1–S5 remain authoritative for numerical conventions.

## Inputs and fixed information

```
normal source = desired absolute poses and original gripper commands
normal trace = controller q, dq, filter_nominal_acceleration
fixed context = original initial arm reference and object observation
candidate bounds = the registered seven arm-bound pairs
```

The desired program is sampled at action boundaries (`goal_pos[::25]`, `goal_ori[::25]`); the geometric nominal posture is `control['q'][::25]`, not the single initial reference. The original physical initial state, 20 Hz action clock, controller settings and carry anchors are not changed.

## Source-side gate

```
for each stored normal controller sample:
    a0 = solve(M, clip(raw_nominal_OSC_torque, motor_bounds) - bias)
    # a0 is the recorded filter_nominal_acceleration, before correction
for each action:
    mark if any of its 25 a0[J7] samples violates Eq. (3) by > 1e-10
form five-action triangular padding b_t
form the unchanged original-carry taper h_t
w_t = max(b_t, h_t)
```

The recorded nominal acceleration is not simulator `qacc`, corrected acceleration or a future restricted rollout. Physical joint legality is evaluated separately.

## Geometric branch

```
previous = None
for action t in original order:
    if w_t == 0:
        keep source rotation and initial reference
        previous = None
        continue
    nominal = normal controller q at action t
    bounded_nominal = clip(nominal, inset bounds)
    first_start = nominal if previous is None else previous
    regularizer_reference = bounded_nominal if previous is None else previous
    starts = [first_start, nominal, inset-bound midpoint]
    solve three bounded least-squares problems with the fixed variant weight
    choose lowest recomputed objective; use start-order ties
    previous = chosen solution
    interpolate reference and source-to-FK rotation by w_t (SI S2)
```

At a segment start the first two starts intentionally coincide. Projecting optimizer starts is not projection of the physical state. A failed optimizer flag is not an infeasibility certificate; the retained validation rules and FK budgets still apply.

## Teacher construction and learned/retrieved branches

```
TRAIN only:
    if restricted source copy passes the strict criterion:
        retain its identity program
    otherwise:
        retain the first strictly successful old/position/free geometric program
        retain all failed candidate records and conditions without teachers
    fit from accepted materialized commands with the composed gate/map loss

Full:
    predict rotation/reference latents from source, context, bounds and time
Constant:
    replace only the pre-MLP 14-D capability feature by its frozen TRAIN mean
    retain real bounds, source-specific context, gate and span normalization
Both:
    materialize with Eqs. (1)–(2); do not gate the teacher a second time
Retrieval:
    choose first minimum descriptor distance in the frozen TRAIN bank
    align the stored ungated latents to query time and use query gates/bounds
```

The shared family/update is selected from original-clock Full DEV results in the two stages recorded in SI S13. Constant scores, the extra-action clock, fitting loss and FINAL results do not select it.

## Continuous execution and scoring

```
freeze each method's complete candidate before its restricted TEST execution
restore original physical initial state once
for every original action:
    inspect grasp before the action if in original carry window
    apply original gripper target, selected posture reference and absolute pose
    for its 25 physical steps:
        inspect all nine joint positions before the step
        native OSC -> nominal torque -> fixed arm correction or raw fallback
        advance simulator without assigning physical joint states
        inspect all nine joint positions after the step
    inspect grasp after the action if in original carry window
check native task goal at the original endpoint
strict = endpoint goal AND entire original carry check AND all-nine range check
hold last action for the separate +40 endpoint; extend range check, keep anchors
```

All-nine tolerance remains `1e-9` in each joint's original units. The +40 endpoint never replaces the original endpoint. No method is retrospectively chosen from test success. Normal qualification, restricted source success and edited strict success are different quantities. See the source listings for actual call order and checks; this guide does not assert new array-level timing alignment or dynamic verification.
