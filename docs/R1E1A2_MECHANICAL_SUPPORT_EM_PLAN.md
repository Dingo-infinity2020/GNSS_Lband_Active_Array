# R1E1A2 Mechanical Support / Standoff EM Baseline Plan

Status: DESIGN ONLY — NO BUILD OR SOLVER AUTHORIZATION

## Why this gate exists

The current radiator is a mechanically continuous 70.714-mm PCB suspended approximately 57.143 mm above the ground/backplane. The PCB itself is structurally continuous, but the model does not yet contain the standoffs/frame that hold it at this height.

Any support placed in this volume is an electromagnetic object. Metal can carry induced current and act as a parasitic/ground extension; ordinary PCB/plastic can load the near field; low-density RF foam may be weakly perturbing but is not assumed perfectly transparent.

Therefore the support concept must be defined before the 18-case R1E1B pitch screen.

Primary question:
**Can a mechanically credible support be chosen whose EM perturbation is small and controlled enough to freeze before pitch screening?**

## Candidate classes

### S0 — bare reference
Existing R1E1A1 support-free P094 artifact. This remains the immutable electromagnetic reference.

### S1 — low-density RF foam support — preferred first candidate
Use a symmetric, minimal-volume foam pedestal or posts. Material properties must come from an actual candidate datasheet or measured coupon; do not treat foam as epsilon_r = 1 by definition.

### S2 — small-section dielectric standoffs
Candidate engineering plastics or fiberglass-family posts. These are manufacturable but may have appreciably higher epsilon_r than RF foam; exact material data are required before solve.

### S3 — FR4 ribs / PCB support
Useful as a manufacturability reference, but expected to perturb the field more strongly because of dielectric constant and loss. Not preferred by default.

### S4 — aluminium/metal posts or tubes
Treat as a high-risk reference, not a benign support. A roughly 57-mm conductive member is electrically substantial across 1.15–1.65 GHz. If metal is ever used, grounding, symmetry and exact geometry are part of the RF design.

## Geometry philosophy

Support must preserve fourfold symmetry unless a quantified reason requires otherwise.

Two low-risk placement families should be designed first:
1. four small symmetric supports under mechanically robust board bridge/corner regions;
2. a compact central low-density support integrated conceptually with the future active-hub region.

Do not put an arbitrary metal frame through the radiator aperture or between neighbouring cells.
Do not assume a support outside the copper outline is harmless; periodic fringing fields extend beyond the board edge.

The support must fit inside the minimum 88-mm cell without crossing periodic boundaries unless the real mechanical architecture itself is periodic across cells.

## Proposed execution sequence

R1E1A2-DESIGN:
- freeze candidate geometry families and real material-property sources;
- no CST build or solver.

R1E1A2-BUILD-ONLY, only after a separate authorization:
- derive support-inclusive P094 variants from the qualified bare P094 source;
- fresh reopen and geometry/material audit;
- no solver.

R1E1A3-SUPPORT-SENSITIVITY, only after a separate solver authorization:
- compare S0/S1 and only the most useful alternative(s) at P094;
- use broadside, theta=60 phi=45, and theta=60 phi=135 as the minimum three-state set;
- compare complex active reflection and Z_active against the bare reference;
- preserve the existing severe-mismatch diagnostics;
- freeze quantitative transparency/acceptance thresholds before results are viewed.

If the preferred low-density support is benign, freeze it and generate support-inclusive six-pitch sources before R1E1B. If it is not benign, support geometry becomes a co-design variable and the 18-case pitch screen remains blocked.

## Relationship to later active hardware

This gate is only the passive mechanical support baseline. The central active-hub PCB, local ground, RF shield, package launch and bias structures remain later full-wave EM objects under R2C.

The support baseline must not pre-emptively freeze the final LNA input match.

## Current stop boundary

DESIGN ONLY.
BUILD_AUTHORIZED = NO.
SOLVE_AUTHORIZED = NO.
No R1E1B pitch solver.
No material A/B solver.
No LNA integration.
