# R1A3 Materialized FR4 BUILD-ONLY Runbook

Status: AUTHORIZATION DOCUMENT — solver forbidden.

## Gate question

Can the frozen R1A1 visible aperture plus the R1A2 exact-rotation center-isolation rule be materialized as one mechanically continuous PCB with a physically separated RF copper topology, deterministically and without introducing ports or solver assumptions?

## Source bundle

- source/cst/R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr
- scripts/audit_r1a3_materialized_fr4.py
- scripts/run_r1a3_build_only_dc.py
- em/cst/R1_CHARTS_LBAND/parameters_r1a3_materialized_fr4.csv
- docs/R1A3_MATERIALIZED_APERTURE_DESIGN.md
- docs/R1A3_SCIENTIFIC_FREEZE.md
- execution/stage_contract.json

## Authorized execution

Host: NW / DESKTOP-GBTI6Q4.
Interpreter: CST 2022 bundled Python 3.6.
Mode: BUILD_ONLY.
Run static audit first. If it does not report PASS_R1A3_STATIC_AUDIT, stop HOLD.

Then create a fresh CST project through the harness, save, close, fresh reopen, enumerate shapes/parameters, export top and perspective evidence, and hash the CST project.

## Hard prohibitions

- no ports
- no solver
- no monitors
- no optimization
- no LNA
- no CST251 staging
- no material comparison sweep
- no hand edits to the saved canonical CST artifact

## Manual-review artifact gate

The resulting canonical CST file is a required user-review artifact.
It must remain on NW with lifecycle state PROTECTED (or CHECKPOINTED with purge_allowed=false) until the user explicitly completes review.
Record:
- absolute path
- SHA256
- bytes
- source HEAD
- macro SHA256
- fresh-reopen status

Do not make a display copy with manual edits. The reviewed CST must be the canonical build artifact.

## Allowed return status

- PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW
- HOLD_R1A3_STATIC_AUDIT
- HOLD_R1A3_CST_RUNTIME
- HOLD_R1A3_RUNTIME_AUDIT
- FAIL_R1A3_REPLAY

A build PASS does not authorize solver.
