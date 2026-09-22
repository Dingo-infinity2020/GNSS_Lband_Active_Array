# Agent Instructions

This repository is a staged scientific hardware project.

## Current gate

Current task: **R0-CHARTS-RECON-PASSIVE**

Do not skip gates.

## Hard rules for R0

- Do not run a CST solver unless the task explicitly authorizes it.
- Build-only means geometry construction and validation only.
- Do not add QPL9547, active PCB, shield, Bias-Tee, array periodic boundaries, or L-band optimization during R0.
- Do not claim an exact CHARTS replica.
- Never convert a visually inferred dimension into a paper-explicit dimension.
- Every geometry parameter must exist in the parameter manifest with one provenance class:
  - PAPER_EXPLICIT
  - FIGURE_DERIVED_UNVERIFIED
  - ASSUMPTION
  - OPTIMIZED (not allowed in initial R0 build)
- If a required dimension is unknown, keep it visibly unknown until a documented reconstruction assumption is approved.
- Preserve source/reference metadata; do not copy entire copyrighted papers into the repository.

## Expected engineering style

- parameterized scripts/macros over opaque manual edits,
- deterministic builds,
- small commits,
- build reports before solver reports,
- explicit PASS/HOLD status,
- no silent auto-tuning to match a paper plot.

## Primary tools

- CST: antenna/full-wave geometry and later periodic/finite-array EM
- ADS: later LNA/noise/stability and EM-circuit co-design
- HFSS: optional independent cross-check
- Python: post-processing and parameter bookkeeping

## Stop rule

When an ambiguity in the source geometry materially changes the model, stop and document it rather than guessing invisibly.
