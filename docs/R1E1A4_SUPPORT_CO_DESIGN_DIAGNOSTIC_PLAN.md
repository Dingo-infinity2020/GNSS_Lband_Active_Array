# R1E1A4 Support Co-Design Diagnostic Plan

Status: DESIGN ONLY — NO NEW BUILD OR SOLVE AUTHORIZATION

Trigger:
`HOLD_R1E1A3_SUPPORT_SCIENCE_GATE_S1_C60P135_DELTA_Z`

The four-post bonded S1 assembly is numerically valid and benign at broadside and C60P45, but fails the pre-frozen 10-ohm Delta-Z gate at C60P135 over a broad upper-band region. The threshold is not relaxed.

Primary question:
**Is the C60P135 perturbation dominated by the foam support body, by the conservative adhesive surrogate / bond volume, or by support placement relative to the scanned near field?**

## Minimal diagnostic sequence

Use C60P135 first because it is the failing sentinel. Do not re-run broadside or C60P45 until a candidate passes C60P135.

D1 — FOAM_ONLY attribution:
- same four 4x4-mm posts at (+/-30,+/-30) mm;
- same ROHACELL baseline;
- remove the dielectric adhesive surrogate from the EM model while keeping the same nominal support height/contact geometry;
- purpose: isolate bulk foam/placement loading from the pessimistic glue model.

D2 — REDUCED_BOND attribution:
- same foam posts;
- reduce adhesive volume only, with geometry frozen before results;
- purpose: test whether the current 5x5x0.10-mm, epsilon_r=4, tan_delta=0.03 bond surrogate drives the upper-band shift.

Decision logic:
- if D1 fails the unchanged 10-ohm gate, the support body/placement itself is not benign and placement/body geometry must be redesigned;
- if D1 passes but D2/full S1 fail, adhesive/bond implementation is the dominant design variable;
- if a modified candidate passes C60P135, then qualify that exact assembly at B0 and C60P45 before freezing it for the six-pitch screen.

Do not use the metal sentinel as a substitute for this attribution. S4 remains an optional high-risk reference after the passive support baseline question is resolved.

## Geometry discipline

No post placement or cross-section optimization may use the current result to tune against individual frequency points. Candidate geometry must be mechanically credible and frozen before its solve.

If later placement redesign is needed, prefer a small discrete set of mechanically plausible symmetric locations or a field-informed placement study rather than continuous optimizer fitting.

## Gates

Keep the existing R1E1A3 physical benign gate unchanged:
- max complex |Delta S11| <= 0.05;
- max |Delta Z_active| <= 10 ohm;
- no severe mismatch alerts.

Use the numerically qualified MaxPasses=12 recovery solver ceiling as the current solver baseline unless a new numerical HOLD occurs.

## Stop boundary

DESIGN ONLY.
No R1E1A4 build.
No R1E1A4 solve.
No S4 sentinel solve.
No R1E1B pitch screen.
No material A/B or LNA integration.
