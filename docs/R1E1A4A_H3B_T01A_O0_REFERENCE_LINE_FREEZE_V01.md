# H3B-T01A O0 Straight Reference-Line Freeze V0.1

Status: AUTHORIZED ONE-SHOT BUILD + SOLVE ON NW

Purpose: decompose straight-line mismatch/loss from the qualified 90-degree cross-board T01-A transition.

Frozen reference geometry:
- one FR4 board, 1.0 mm, epsilon_r 4.3, tan(delta) 0.02;
- PEC screening conductors, identical to current T01-A material assumption;
- GCPW Wsig 1.8 mm, gap 0.30 mm, ground rails 2.20 mm;
- local backing ground width 8.0 mm;
- same 0.40 mm OD / 0.30 mm ID via-barrel rule and 3 mm pitch pattern;
- straight RP1/RP2 spacing = 24.0 mm, equal to unwrapped T01-A reference-plane path;
- same 50-ohm discrete-port topology, 1.0-2.0 GHz range, 1.15-1.65 GHz decision band;
- same second-order tetrahedral solver, MaxDeltaS 0.02, two checks, MaxPasses 16.

O0 is calibration only. It does not authorize Wsig/gap optimization, T01-C, integrated H3B, or LNA work.
Build must pass fresh-reopen, zero-port build-only, positive-volume shape inventory, built-in intersection invocation, and no-solver-result checks before the one formal solve.
