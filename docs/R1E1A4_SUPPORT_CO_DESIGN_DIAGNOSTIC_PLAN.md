# R1E1A4 Support Co-Design Diagnostic Plan

Status: DESIGN ONLY — NO NEW BUILD OR SOLVE AUTHORIZATION

Trigger:
`HOLD_R1E1A3_SUPPORT_SCIENCE_GATE_S1_C60P135_DELTA_Z`

The four-post bonded S1 assembly is numerically valid and benign at broadside and C60P45, but fails the pre-frozen 10-ohm Delta-Z gate at C60P135 over a broad upper-band region. The threshold is not relaxed.

This file now serves as the EM-diagnostic sub-plan under the higher-level system review:
`docs/R1E1A4_SYSTEM_CO_DESIGN_REVIEW_20260925.md`.

The immediate next task is NOT a CST solve. R1E1A4A first freezes the balanced antenna-to-LNA reference plane, receiver shadow model and system-level Gate R.

After R1E1A4A, the first EM question remains:
**At the known failing C60P135 sentinel, how much of the S1 perturbation comes from the conservative adhesive surrogate versus the foam body / support placement, and how do more conventional serviceable support architectures compare at receiver level?**

## Prerequisite — R1E1A4A receiver shadow

Before any new EM solve:
- freeze differential-to-per-LNA impedance mapping;
- import QPL9547 reference S/noise parameters;
- replay existing bare/S1_BONDED impedance loci;
- freeze receiver-level Gate R;
- freeze H0 plus C0/C1/C2 carrier envelopes.

## Minimal EM diagnostic sequence — R1E1A4B

Use C60P135 first because it is the failing sentinel. Do not re-run broadside or C60P45 until a candidate survives C60P135.

D1 — FOAM_ONLY attribution:
- same four 4x4-mm posts at (+/-30,+/-30) mm;
- same ROHACELL baseline;
- remove the dielectric adhesive surrogate from the EM model while keeping the same nominal support height/contact geometry;
- purpose: isolate bulk foam/placement loading from the pessimistic glue model.

D2 — REDUCED_BOND attribution:
- same foam posts;
- reduce adhesive volume only, with geometry frozen before results;
- purpose: test whether the current 5x5x0.10-mm, epsilon_r=4, tan_delta=0.03 bond surrogate drives the upper-band shift.

C1 — central dielectric-tube / serviceable standoff candidate:
- PTFE-class, PEEK-class, or another characterized engineering dielectric;
- actual material grade/properties frozen before build;
- hollow symmetric carrier preferred if mechanically adequate;
- no assumption of EM transparency.

C2 — structural PCB / printed-frame carrier candidate:
- mechanically support the H0/radiator assembly;
- any copper on the frame is an explicit RF object;
- no transistor or active circuit inside CST;
- preserve source-facing terminal symmetry unless a quantified exception is frozen.

Decision logic:
- if D1 fails the unchanged 10-ohm gate, the support body/placement itself is not benign and placement/body geometry must be redesigned;
- if D1 passes but D2/full S1 fail, adhesive/bond implementation is the dominant design variable;
- if a modified candidate passes C60P135, then qualify that exact assembly at B0 and C60P45 before freezing it for the six-pitch screen.

Do not use the metal sentinel as a substitute for this attribution. S4 remains an optional high-risk reference after the passive support baseline question is resolved.

## Geometry discipline

No post placement or cross-section optimization may use the current result to tune against individual frequency points. Candidate geometry must be mechanically credible and frozen before its solve.

If later placement redesign is needed, prefer a small discrete set of mechanically plausible symmetric locations or a field-informed placement study rather than continuous optimizer fitting.

## Gates

Keep the existing R1E1A3 transparency gate (Gate T) unchanged:
- max complex |Delta S11| <= 0.05;
- max |Delta Z_active| <= 10 ohm;
- no severe mismatch alerts.

Gate T answers whether the support can be treated as electromagnetically negligible. It is not the sole production-architecture gate.

R1E1A4A must freeze a receiver/system gate (Gate R) using the actual balanced-to-LNA reference plane and QPL9547 reference noise/stability model before new candidate results are viewed.

A mechanically credible candidate may fail Gate T yet remain viable under Gate R; such a candidate is classified as a co-designed RF/mechanical structure, not as a transparent support.

Use the numerically qualified MaxPasses=12 recovery solver ceiling as the current solver baseline unless a new numerical HOLD occurs.

## Stop boundary

DESIGN ONLY.
Next: R1E1A4A receiver-shadow / interface freeze.
No R1E1A4 build.
No R1E1A4 solve.
No S4 sentinel solve.
No R1E1B pitch screen.
No material A/B solve.
No physical LNA CST integration.
