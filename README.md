# Repairing manipulation programs under wrist range restrictions

Author-maintained supplementary information and numerical evidence for the paper by Yanming Liu, Pengyu Huo, Yusen Guo, Kaixiang Lai, Huijuan Liu, Huixian Ye and Qiliang Li.

**Status:** author-maintained evidence companion for a paper accepted at ICMIC 2026. Acceptance is not publication; no proceedings DOI is assigned here. This repository is not a SPIE-hosted supplement.

## What is included

- `supplement/Supplementary_Information.pdf`: 12-page supplementary methods and results, with the main paper's S1–S13 identifiers.
- `evidence_companion/results/`: all 840 declared Can cells (700 scored, 140 qualification NA), all 300 scored Lift cells, both clocks, recorded timing and uncertainty summaries.
- `evidence_companion/protocols/`: source roles, teacher memberships, exclusions and recorded model-selection rules.
- `evidence_companion/methods/`: pseudocode and 15 inspectable source listings. The `.py.txt` suffix is intentional: they are not a complete installable simulator or training runtime.
- `figures/`: complete Can and Lift cell matrices, as PDF and SVG. Main-paper artwork and scientific results are not altered by this packaging step.

## Verify the stored results

Python 3 standard library only, no GPU or datasets required:

```sh
python3 evidence_companion/verify_tables.py
```

This recounts the stored outcome tables, checks source-role separation, and verifies included file hashes. It writes `evidence_companion/VERIFICATION_RESULT.json`. It does not train, infer, run physics or FK, resample confidence intervals, or validate external files identified only by hashes.

## Interpretation

Can source-copy success is 12/50 on the primary clock, clipping is 36/50, geometry seeds are 46/47/43, and learned seeds are 45/43/43. Lift source-copy is 28/30, geometry and position-priority projection reach 30/30, and retrieval and learned policies reach 29/30. Keep the original and +40 clocks separate. These correlated cells do not constitute independent trials. NA is not failure; `damage` denotes success regression, not hardware damage.

The paper does not establish a consistent neural quality advantage, capability-token necessity, cross-morphology generalization or real-robot safety. The earlier Can CPU numerical mismatch and the limited reference-GPU check remain negative/finite evidence. Full-study dynamic reproducibility is not established by this package.

## Material boundaries

No raw demonstrations, model weights, dense physical trajectories, simulator assets, registration forms, payment records, private correspondence, server credentials or internal provenance paths are included. See `RIGHTS_AND_SCOPE.md`.

The supplementary PDF retains the scientific content of the review copy, with material-access notes updated for this repository. Scientific results, exclusions, thresholds and reproduction limitations are unchanged. This is an author-managed resource, not a SPIE-hosted publication supplement.
