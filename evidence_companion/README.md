# Numerical and method companion

This compact evidence package accompanies “Repairing manipulation programs under wrist range restrictions”. It is not a complete runnable reproduction bundle. The repository README records release scope and status.

## Included
- Can: all 840 declared condition-method cells (700 scored; 140 normal-qualification NA), original and separate +40 strict scores, original goal/carry/range components, source pairing, prior result/check hashes, 700 condition-level timing medians, and all ten source differences.
- Lift: all 300 scored cells, both clocks, failure components, repairs/regressions, timing medians, stored pairing summaries and original result/program hashes.
- TRAIN contributor/teacher memberships, nominated expansion/DEV/FINAL roles, recorded exclusions, two-stage DEV family/update choices, selected model hashes and the 14-component Constant feature.
- Operational pseudocode in `methods/PIPELINE_PSEUDOCODE.md` and selected method source listings for inspection only. These are not the complete dependency graph, simulator runtime, source dataset, weights, dense control traces or timing-repeat payloads.

## Verification
Run `python3 verify_tables.py` with Python 3 standard library only. It re-aggregates stored tables and checks their consistency and included file hashes. It does not train, infer, execute physics/FK, recompute bootstrap intervals or prove hashes of external files still match. Results are retained in `VERIFICATION_RESULT.json`.

`SOURCE_HASHES.json` records the input bytes used to prepare this package. Hashes in data rows identify original external records but do not embed those records. Absolute internal paths have been omitted from the delivered tables; an internal provenance ledger is retained by the authors.

## Interpretation and access limits
The original endpoint is primary; +40 is separate. `damage` means success regression, not physical hardware damage. Blank/NA cells must not be counted as failures or removed. Methods/seeds/ROMs are correlated within source. Stored uncertainty is copied, not newly sampled. Can CPU numerical failure and finite reference-GPU checks are unchanged; no full-study dynamic reproduction is asserted. The earlier original-TRAIN prequalification nomination list remains incomplete here.

The package contains author-maintained numerical tables and inspection listings. It does not redistribute source datasets, checkpoints or simulator assets. Publication and reuse of third-party materials require their respective permissions. See the repository release-status and rights notices.
