# AR0-B1R-T2S HOLD Report

Final status: **HOLD_R1E1A4A_AR0_B1R_T2S_LINUX_HISTORY_REPLAY**

## What happened

- Authorized formal CST launch count: 1
- Actual formal cst_design_environment launches: 1
- Automatic retries: 0
- Solver_HF_Tet numerical-kernel starts: 0
- S-parameter result produced: no
- Configured source SHA256: ab8a61cc781880ba938b729f44862d1d79f36dbb959288fc57ede5e61b4d2858
- Post-run project SHA256: ab8a61cc781880ba938b729f44862d1d79f36dbb959288fc57ede5e61b4d2858
- Outer exit code after controlled termination: 137

## Root cause

CST251 headless cst_design_environment -m/-f attempted to replay the inherited legacy parametric history of the copied T2F project before Solver_HF_Tet started. Replay failed at the historical Transform command .AutoDestination "True" with ActiveX Automation error 10091. The configured project SHA remained unchanged and no S-parameter result tree was produced.

The solver log was stable for at least 30 seconds with no Solver_HF_Tet/TetMesh process.
The remaining cst_design_environment processes were terminated after HOLD was proven.

## Interpretation

This is a solver-fixture packaging/history compatibility failure, not a measured RF failure.
No return-loss, balance, common-mode or loss conclusion may be drawn.

## Required recovery

Create a fresh, history-independent/flattened T2F-R1 fixture that contains only the accepted six T1 solids and the accepted three ports, with deterministic geometry/volume/endpoint equivalence to T2F.
Do not inherit the original radiator project's legacy history.
That recovery is a new BUILD-ONLY node and requires separate authorization before a new solve can be authorized.

Remote run root is PROTECTED_IN_PLACE:
/data/jlding/gnss_ar0_b1r_t2s_20260927
