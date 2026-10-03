# R1E1A4A-H1 Local-Ground / Feed-Transition Redesign Plan

Status: H1A BUILD AUTHORIZED; ONE H1A BROADSIDE SOLVE PRE-AUTHORIZED CONDITIONALLY ON BUILD PASS

Trigger:
`HOLD_R1E1A4A_H0_P1_GATE_R_RNF0`

## What H0 V0.1 proved

Retain:
- the two-single-ended-port P1A/P1B receiver reference-plane concept;
- 50-ohm single-ended / 100-ohm differential mixed-mode convention;
- Gate R V0.1;
- circuit-domain QPL9547 noise/stability co-simulation.

Reject as the next physical baseline:
- a continuous 10x10-mm local-ground island directly on the underside of the 1-mm radiator substrate.

Reason:
- numerical solve PASS;
- mixed-mode conversion and branch symmetry PASS;
- R-NF0 FAIL over roughly the upper half of the science band;
- differential loading relative to P0 reaches about 200 ohm.

## Physical interpretation

H0 V0.1 places grounded metal directly beneath the four center terminal/petal regions. The result behaves like substantial shunt capacitive loading of the source-facing structure.

A simple parallel-plate scale estimate is used only as a design heuristic, not as an EM result:
- 10x10 mm area across 1 mm FR4 with epsilon_r around 4.3 gives an upper-bound capacitance scale of about 3.8 pF;
- adding a 2.0-mm air spacing in series with the same 1-mm FR4 reduces that full-area scale to about 0.4 pF.

The actual antenna overlap/fringing is more complicated, but the order-of-magnitude reduction justifies a spacing diagnostic before changing several variables at once.

## H1A — OFFSET_GROUND_G2P0 — first next candidate

Purpose:
isolate the effect of vertical local-ground separation while preserving the already-qualified P1 topology and ground footprint.

Frozen design candidate for later BUILD review:
- parent = qualified bare P094 lineage;
- H0/P1 port topology retained;
- local-ground footprint = 10.0 x 10.0 mm, centered;
- local-ground copper thickness = 0.035 mm;
- radiator substrate underside remains z = 57.142857143 mm;
- local-ground top surface moves to z = 55.142857143 mm;
- air gap between radiator underside and local-ground top = 2.000 mm;
- P1A/P1B remain two 50-ohm single-ended lumped reference ports at the same x/y terminal centers;
- no support carrier, daughterboard dielectric, package, shield, bias, output, or active transistor.

This remains a reference-plane/loading diagnostic. The longer ideal port is not claimed to represent a physical signal pin or its inductance/loss.

## H1A gate sequence

1. BUILD-ONLY with fresh reopen; no solver.
2. After separate solve authorization: broadside only.
3. Reapply unchanged numerical and mixed-mode gates.
4. Reapply frozen R-NF0 <= 0.40 dB using actual branch impedances.
5. Compare H1A against H0 V0.1 and old P0 to quantify how much of the loading is recovered by spacing alone.

Do not run C60P45/C60P135 until H1A broadside R-NF0 passes.

## H1B — physical feed transition — only if H1A is promising

Add, in a separate stage:
- a manufacturable small daughterboard;
- signal pins/vias from radiator terminal regions to backside P1 pads;
- explicit local-ground clearance/antipad;
- package input pad geometry;
- copper/dielectric loss needed to evaluate R-LOSS;
- fourfold geometry rules for eventual dual polarization.

At H1B, P1 moves to the actual device input pad plane.

## H1C — shaped / perforated local ground — if spacing alone is insufficient

Do not immediately optimize arbitrary ground shapes.

First mechanically credible option:
- retain the 10x10-mm maximum hub envelope;
- remove ground beneath the terminal/contact projections using four exact-rotation clearances;
- route local ground preferentially through the existing center isolation-gap / low-field directions;
- freeze the clearance geometry before viewing its solve result.

H1C is not authorized automatically by an H1A failure.

## Stop boundary

DESIGN ONLY.
No H1A build.
No H1A solve.
No follow-on scan solve.
No carrier, shield, package or transistor integration.
