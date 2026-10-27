# M7B Diagnostic SOLVE Freeze V0.1

M7B `CIN_PAD_PROJECTION_CLEARANCE` passed user manual CST 3D geometry review. The protected reviewed build is the only allowed source for a future diagnostic solve.

The solve reuses the proven full-E2C/M7A 12-port coexistence semantics: source ports 1/2/4/5/7/8/10/11, load-only ports 3/6/9/12, 1.0-1.8 GHz, second-order tetrahedral adaptive mesh, MaxDeltaS 0.02 for two consecutive checks, max 16 passes, no automatic retry, and no H-field monitor.

Frozen before result:
- raw primary: >=30% reduction at 1.3432 GHz;
- mode primary: >=6 dB improvement at the full-E2C-selected worst diff-to-common anchor inside 1.20-1.40 GHz;
- secondary: >=30% branch-imbalance reduction at 1.2984 GHz;
- guard: no new >6 dB off-diagonal excursion within <=50 MHz;
- reject controlling CIN-shunt mechanism only if both primary improvements are <10% and secondary fails.

BUILD_AUTHORIZED = false.
SOLVE_AUTHORIZED = false.
Formal solver budget = one future invocation only if separately authorized.
Before any SOLVE grant, the frozen host static audit must PASS.
