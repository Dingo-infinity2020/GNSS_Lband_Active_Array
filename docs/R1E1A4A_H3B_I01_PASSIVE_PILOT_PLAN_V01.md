# H3B-I01 Passive Integrated Pilot Solve Plan V0.1

Status: FROZEN PLAN — SOLVE NOT AUTHORIZED

Authority: docs/R1E1A4A_H3B_COMPLETE_PASSIVE_ROUTE_FREEZE_V01.md

Prerequisite:
PASS H3B-C0 and human 3D review.

Formal matrix:
- A / BROAD
- B / BROAD
- A / C60P45
- B / C60P45
- A / C60P135
- B / C60P135

Six separate one-shot solve tickets.
No batch result may hide a failed case.

B-only post-LNA proxy:
four local T01 slices, each with 50-ohm-class matched passive loads at the two frozen 3-mm handoff planes.

The antenna periodic feed remains the original qualified active-impedance reference; no 50-ohm constraint is imposed on antenna-to-LNA source impedance.

Numerical formulation:
HF Frequency Domain / tet second order / curvature 3 / General purpose / ExpertSystem / MinPasses3 / MaxPasses16 / MaxDeltaS0.02 / two checks / growth40 / 1.0-1.8 GHz.

Required anchors:
L5 1.17645 GHz
L2 1.22760 GHz
L1 1.57542 GHz

Required comparisons:
complex S11 and Zactive B-A;
efficiency ratio B/A;
realized co-pol gain penalty B-A;
cross-pol/XPD change;
surface-current mechanism.

Automatic and human gates are frozen in the route-freeze document.

Stop after six-case qualification and current-map review.
Do not start A0 automatically.
