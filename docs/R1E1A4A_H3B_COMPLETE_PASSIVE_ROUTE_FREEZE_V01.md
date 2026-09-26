# H3B Complete Passive Unit Route Freeze V0.1

Status: SCIENTIFIC ROUTE FROZEN — AWAIT BUILD AUTHORIZATION
SimulationOps: 0.2.8

## 1. Purpose

H3B closes the first physically credible passive antenna element by integrating:
- the qualified P094 periodic radiator source;
- accepted H3A V0.2 orthogonal-stalk mechanics;
- the frozen H3B-T01A local 90-degree post-LNA transition technology.

H3B is an integration/physics gate, not a new nominal optimizer.

Mainline:
H3B-C0 BUILD-ONLY -> H3B-I01 six-state A/B passive pilot -> H3B PASSIVE UNIT V1 FREEZE -> LNA-on-stalk A0.

No LNA device model or LNA input match is authorized in H3B.

## 2. Parent authorities

H3A V0.2 protected artifact:
- SHA256 9e810560fc8fc759a88d4ac5fc39067863a1e078b6f01e6e343b004891201db5
- 94-mm unit-cell metadata
- accepted FR4 bridge/mortise/stalk/interlock/shield/mechanical topology.

T01-A freeze:
- Wsig = 1.50 mm
- Gcpw = 0.40 mm
- signal pad width = 2.00 mm
- pad gap = 0.30 mm
- transition extension = 0.30 mm
- copper engineering model sigma = 5.8e7 S/m
- solder proxy sigma = 7.0e6 S/m
- O3 nominal solved SHA256 5a3ec0b2a9eca4bc0253d0e1fd5ab5f512d6d0fb63944bbd7b932505c1f5f82f
- T01-A status PASS_R1E1A4A_H3B_T01A_FREEZE.

## 3. Important integration rule: coupon is not product routing

The long straight horizontal/vertical fixture lines and coupon FR4 boards are test-fixture geometry.
They SHALL NOT be copied wholesale into the antenna product model.

H3B inherits from T01-A only:
- local GCPW cross-section;
- local 90-degree transition pads;
- edge/castellation geometry;
- solder geometry;
- local backing-ground rule;
- first via-fence station/topology;
- conductor/material model;
- the physical-reference-plane concept.

H3A radiator/stalk FR4 solids remain the substrate authority.

The local integration slice terminates at uniform controlled-line handoff planes 3.0 mm from the junction on both sides. This coincides with the first frozen T01 via-fence station and avoids importing the long coupon fixture.

The downstream product routing between the LNA package and the local handoff plane is NOT frozen by H3B. It belongs to A0. This preserves the project policy that ordinary microstrip is the preferred mainline while T01-A GCPW remains a local transition technology.

## 4. Four transition instances

Junction height reference:
z0 = 57.1428571428 mm.

Nominal branch centers:
- X+ = (+9.4, 0, z0), associated with NE LNA/route corridor;
- X- = (-9.4, 0, z0), associated with SW LNA/route corridor;
- Y+ = (0, +9.4, z0), associated with NW LNA/route corridor;
- Y- = (0, -9.4, z0), associated with SE LNA/route corridor.

The local T01 +line coordinate points from junction toward its associated LNA corridor.

Transforms:
- X+ / NE: global x = +9.4 + xl; global y = +yl; global z = z0 + zl.
- X- / SW: global x = -9.4 + xl; global y = -yl; global z = z0 + zl.
- Y+ / NW: global x = -yl; global y = +9.4 + xl; global z = z0 + zl.
- Y- / SE: global x = +yl; global y = -9.4 + xl; global z = z0 + zl.

Therefore the vertical-stalk RF faces are:
- X+: +Y face;
- X-: -Y face;
- Y+: -X face;
- Y-: +X face.

This face assignment is authoritative and supersedes the schematic H3A RF-placeholder face placement. It restores the intended C4 relation to the accepted NE/SW/NW/SE route corridors without reopening the stalk mechanical architecture.

## 5. H3A component disposition in formal H3B EM geometry

KEEP as physical geometry:
- UnitCellGround;
- Substrate / TopCopper;
- H3A_Stalk;
- H3A_HubGround;
- H3A_Shield;
- H3A_MechLand;
- H3A_MechSolder;
- the accepted FR4 bridge/mortise/tenon/interlock geometry.

REMOVE from formal EM solids, but retain their coordinates as keepout/audit predicates:
- H3A_LNAEnvelope;
- H3A_RouteEnvelope;
- H3A_ServiceEnvelope.

REMOVE and replace:
- H3A_RFTransition;
- H3A_RFSolder;
- H3A_StalkRF.

Reason: the latter are schematic PEC placeholders and are not qualified product RF geometry.

## 6. Physical material policy

For the A/B pilot, both models use the same physicalized material assumptions.

Copper-like physical conductors:
- radiator copper;
- unit-cell ground/backplane;
- hub ground;
- shield;
- mechanical lands;
- T01 line/pads/edge caps/backing grounds/vias;
use sigma = 5.8e7 S/m engineering copper model.

Solder solids:
- mechanical solder;
- T01 RF solder;
use sigma = 7.0e6 S/m solder proxy.

FR4 remains the project cost-baseline dielectric already used by the parent.

Visual surrogate dielectrics are forbidden in formal I01 EM solves.

## 7. H3B-C0 build-only products

C0 creates two fresh, independently audited P094 artifacts from the same parent authority.

A — H3A_MECH_ONLY_PHYSICALIZED:
- accepted H3A physical mechanics;
- visual surrogates removed;
- schematic RF placeholders removed;
- physical conductor/solder materials applied;
- no T01 local slice;
- zero RF ports;
- no solver.

B — H3B_COMPLETE_PASSIVE_V1:
- byte-equivalent A parent before T01 insertion;
- four frozen local T01 integration slices placed by the transforms above;
- existing H3A radiator/stalk FR4 is reused; no coupon board solid is inserted;
- local T01 geometry is clipped only at the two frozen 3.0-mm handoff planes;
- zero RF ports;
- no solver.

C0 is a geometry/material authority gate only.

## 8. C0 build gate

Both A and B must pass:
- fresh CST MWS / deterministic parent provenance;
- source/hash identity recorded;
- fresh reopen;
- positive-volume shape audit;
- exact component disposition audit;
- no forbidden visual-surrogate EM solid;
- no schematic RF-placeholder solid in B;
- no duplicate coupon FR4 board;
- all four T01 instances present at the frozen branch centers/faces;
- C4 transform audit;
- CST EM auto-intersection check;
- CDCheckModelIntersections return;
- explicit allowlist for intentional conductor/FR4/solder face contacts;
- all other overlap/interference = HOLD;
- zero RF ports;
- zero lumped loads;
- zero solver results.

Human 3D review is required after C0 PASS and before I01 solve.

## 9. H3B-I01 passive A/B pilot

Only after separate SOLVE authorization.

Pitch:
- P094 only.

Models:
- A = H3A_MECH_ONLY_PHYSICALIZED;
- B = H3B_COMPLETE_PASSIVE_V1.

Pilot scan states:
- BROAD: theta=0 deg, phi=45 deg;
- C60P45;
- C60P135.

Pol-A is the formal first-pilot feed because the B geometry must pass an exact C4 transform audit.
Pol-B becomes mandatory in this stage only if C4 audit fails or a physics result breaks the expected rotational equivalence. Full dual-pol coverage remains mandatory for the later realistic periodic atlas.

Each A/B/state combination is a separate one-shot formal solve:
3 states x 2 models = 6 formal solves.

Existing older bare-P094 scan data are context only and are not substituted for the new physicalized A baseline.

## 10. I01 passive termination policy

H3B must not force the antenna input to 50 ohms.

The four post-LNA local T01 slices are instead terminated at their two 3-mm handoff planes with matched 50-ohm-class passive loads during B solves, because M2 is a post-first-stage-LNA interface by project policy.

This termination is an engineering passive proxy only:
- it suppresses artificial open-stub resonances;
- it does not represent the antenna-to-LNA input match;
- it is removed/replaced by the A0/A1 active-front-end model later.

A contains no corresponding T01 load because the T01 geometry is absent.

## 11. Numerical formulation

Reuse the proven R1E0C periodic formulation with increased adaptive budget for the larger geometry:
- CST 2022.5;
- HF Frequency Domain;
- tetrahedral second order;
- curvature order 3;
- General purpose;
- HighFrequencyTet / ExpertSystem;
- MinPasses 3;
- MaxPasses 16;
- MaxDeltaS 0.02;
- NumberOfDeltaSChecks 2;
- LinearGrowthLimitation 40;
- 1.0-1.8 GHz.

No silent retry.

## 12. Required outputs

For every A/B/state:
- complex active S11;
- complex Z_active referenced to the existing qualified periodic feed;
- native Delta-S sequence / termination / broadband convergence;
- radiation efficiency;
- realized co-pol gain in the intended scan direction;
- cross-pol or XPD metric where the parent formulation supports it.

Field/pattern anchors:
- 1.17645 GHz (L5);
- 1.22760 GHz (L2);
- 1.57542 GHz (L1).

B also requires surface-current evidence on:
- radiator;
- stalks;
- hub/shield;
- T01 local transitions.

If a new narrow feature appears, add one monitor at the feature frequency for diagnosis; this is evidence extraction, not a geometry retry.

## 13. Frozen automatic gates

Numerical PASS per solve:
- source hash / scan metadata match;
- required periodic S11 path exists;
- finite S11 and Z_active;
- final two Delta-S <= 0.02;
- desired-accuracy termination;
- not max-pass terminated;
- broadband sweep converged;
- no solver error lines.

Architecture HOLD if B newly triggers, while A does not:
- |S11| >= 0.90 in 1.15-1.65 GHz;
- Re(Z_active) <= 0 in 1.15-1.65 GHz;
- |Z_active| >= 1000 ohm in 1.15-1.65 GHz.

Relative A->B passive-penalty gates at L5/L2/L1:
- radiation-efficiency ratio B/A >= 0.85 required; >=0.90 preferred;
- intended-direction realized co-pol gain penalty <=1.0 dB required; <=0.5 dB preferred.

Active-impedance movement itself is record-only unless it coincides with one of the architecture alerts above. H3B shall not tune the radiator merely to keep Z_active near 50 ohms.

Cross-pol/XPD:
- report absolute values and A->B degradation;
- HOLD if a clear co-pol/cross-pol role inversion appears or if a new narrow polarization resonance is associated with stalk/T01 current;
- otherwise defer detailed dual-pol optimization to the later atlas.

## 14. Human mechanism gate

After all six numerical solves:
- inspect current maps at L5/L2/L1 and any new feature frequency;
- identify whether current is radiator-dominated or stalk/hub/T01 dominated;
- a new narrow efficiency/gain anomaly with stalk/T01-dominated current is H3B HOLD;
- smooth impedance movement without destructive efficiency/pattern behavior is not a failure.

## 15. Exit

If C0 and I01 PASS:
status = PASS_R1E1A4A_H3B_PASSIVE_UNIT_V1

Freeze:
- A/B source hashes;
- B exact geometry/material manifest;
- four T01 transforms;
- 3-mm handoff planes;
- P094 periodic metadata;
- six representative solve products;
- keepout predicates for future LNA/mainline routing.

Then proceed to:
LNA-on-stalk A0 engineering prototype.

If C0 or I01 HOLD:
do not open A0 and do not silently tune radiator/T01.
Return only to the implicated integration mechanism.

No BUILD or SOLVE authorization is implied by this document.
