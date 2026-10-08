# R4-A0-E2B Pol-B Rigid-Transfer Build + Loaded Solve Freeze V0.1

Status: BUILD AUTHORIZED; SOLVE PREAUTHORIZED BUT GATED  
Date: 2026-09-29  
SimulationOps minimum: 0.2.12

## Purpose

Promote the proven E2A active-feed architecture to Pol-B as a mechanical/asymmetry sentinel.

No RF retune is allowed before the A/B comparison.

## Parent authority

Canonical pre-E2 parent:
R1E1A4A_AR0_B1R_T1R1_GROUND_PLACEMENT_CORRECTED_BUILD_ONLY_V01.cst

SHA256:
fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e

Using the same pre-E2 parent keeps the non-tested orthogonal polarization in the same v=0..3 mm open-stub condition as the E2A pilot.

## Frozen transfer

Pol-B local basis:
- u = (-1,+1,0)/sqrt(2)
- local board normal = (-1,-1,0)/sqrt(2)
- downstream v = global -z

Rigidly transferred from E2A:
- all signal polygons;
- package lands;
- QPL9547 package rotation/pinout;
- top local ground;
- eight via centers, OD/ID and plating;
- bias polygons;
- P-branch backside ground;
- all 12 raw port local reference planes.

No LNA/circuit components are inserted.

## Sole released mechanical geometry

The B lower-body half-lap cut occupies local u=-1.125..+0.125 and reaches the upper/lower-body handoff at downstream v=12 mm.

All signal/top-ground/via geometry is outside this cut.

Only E2A's N-branch full-width backside ground would overhang the half-lap for the last 1 mm.

Therefore the only released geometry is:

E2B_N_BackGround:LOCAL_BACK_GROUND

- v=3..12 mm: u=-5..-1
- v=12..13 mm: u=-5..-1.125

Removed copper footprint area: 0.125 mm^2.

This is a support/clearance notch, not an RF optimization variable.

## Build contract

Parent solids: 45  
Delete superseded objects: 12  
Final new solids: 74  
Expected final solids: 107

Temporary drill tools: 8, all consumed.  
Plated via barrels: 8.  
Raw ports: 12.  
Device planes: 2/3/8/9.

CST-native drill-kernel reference is required on a disposable complete-project copy before production History.

Hard build gates:
- exact parent SHA and companion directory;
- exact 107-name set / component counts;
- only B_P/B_N prong volume changes, matching the CST-native drill reference;
- 8 via barrels with frozen geometry;
- 12 exact B-basis ports;
- persistent History;
- empty result tree;
- fresh-reopen hash stability;
- whole-model intersection command returns cleanly;
- 14 registered destructive-on-complete-copy pairwise checks show zero positive-volume overlap;
- analytic half-lap support audit passes.

Build failure => HOLD and solve blocked.

## Human 3D review

Required before solver activation.

Inspect:
- Pol-B has the two complete E1 cells;
- Pol-A stops at v=3 mm stubs;
- same package rotation, not mirrored pinout;
- all 8 vias pass through real B FR4;
- N backside-ground notch follows the half-lap and does not alter signal/top-ground geometry;
- no local ground touches radiator or Pol-A stalk;
- no D2 remote common-ground structure is present;
- 12 raw ports are at the intended planes.

## Loaded solve after build + human PASS

Same E2A-S0L contract:
- reduce 12 raw ports -> six solver ports;
- sources = 1,2,4,5;
- P_OUT load-only = 3,6 at 50 ohm;
- E_DN/VDD/VBIAS audit ports removed from solve copy;
- 24 complex responses = rows 1..6 x source columns 1,2,4,5;
- 1.0..1.8 GHz; decision band 1.15..1.65 GHz;
- second-order tetrahedral adaptive;
- MaxDeltaS 0.02, two consecutive native checks, MaxPasses16;
- exactly one formal solver invocation;
- no automatic retry.

Hard solve gates remain:
- native convergence;
- 24/24 response completeness on one grid/run;
- source-side reciprocity <=0.02;
- loaded column power <=1.02;
- no fatal error / mesh corruption.

## Pol-A / Pol-B comparison

Pol-B is not retuned before comparison.

Report:
- differential/common-mode source-side network;
- E diff->common and P_IN diff->common conversion;
- branch return asymmetry;
- C_IN-gap parasitics;
- output-load pickup;
- resonance sentinel;
- A/B delta at L5/L2/L1 and across the decision band.

Pre-frozen comparative review:
- >6 dB degradation in corresponding diff/common conversion vs E2A => REVIEW;
- >10 dB degradation => SEVERE REVIEW;
- branch return-magnitude imbalance >1 dB => REVIEW;
- >=10 dB change over <=50 MHz => resonance REVIEW.

These are review triggers, not post-hoc tuning targets.

## Authorization

User explicitly authorized Pol-B BUILD and SOLVE on 2026-09-29.

BUILD_AUTHORIZED = true  
SOLVE_AUTHORIZED = true

Solve activation additionally requires:
1. automated build PASS;
2. explicit human 3D review PASS.

No build failure, HOLD or missing review may be bypassed by the preauthorization.
