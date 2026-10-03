# R4-A0-E2A-S0L Coupling Review and Mechanism Classification V0.1

Status: PASS — NO NARROW MECHANISM PROBE REQUIRED  
Date: 2026-09-29  
SimulationOps minimum: 0.2.12

## 1. Input authority

Qualified solved artifact:

`D:\GNSS_R4A0E2A_S0L_SOLVE_20260929\R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_SOLVED_V01.cst`

SHA256:

`811a31eabcd193bcf5f9cbecdf05f8aab1b1ab945bad4bda51a94d21d57b04b3`

Qualification disposition:

`PASS_LOADED_SOURCE_WITH_REVIEW`

The review trigger was the single-ended source-side term A_E_UP <-> B_E_UP exceeding -20 dB in part of the decision band.

Peak:
-16.2516 dB at approximately 1.5736 GHz.

Representative:
- L5: -20.9997 dB
- L2: -19.9872 dB
- L1: -16.2517 dB

## 2. First-principles interpretation

A_E_UP and B_E_UP are the two source-side terminals of the balanced Pol-A feed system.

Therefore a large single-ended mutual S-parameter between the two terminals is not, by itself, evidence of pathological crosstalk.

For a symmetric balanced two-terminal network, the physically relevant quantities are the differential/common-mode combinations.

Using the unitary transform

`a_d = (a_A-a_B)/sqrt(2)`

`a_c = (a_A+a_B)/sqrt(2)`

and likewise for b, the existing 1001-point single-ended source-side network was transformed offline.

No CST solve or geometry change was used.

## 3. Mixed-mode evidence

Across 1.15..1.65 GHz:

- E differential -> common conversion peak: -30.7106 dB
- E common -> differential conversion peak: -30.7117 dB
- E differential -> P_IN common peak: -67.6151 dB
- E common -> P_IN differential peak: -69.4570 dB
- P_IN differential -> common peak: -73.5334 dB
- P_IN common -> differential peak: -73.5338 dB

At L1:
- E differential -> common: -31.3040 dB
- E differential -> P_IN common: -68.2627 dB
- P_IN differential -> common: -73.9456 dB

At L2:
- E differential -> common: -35.6225 dB
- E differential -> P_IN common: -73.1249 dB
- P_IN differential -> common: -76.2015 dB

At L5:
- E differential -> common: -36.6487 dB
- E differential -> P_IN common: -74.1640 dB
- P_IN differential -> common: -76.5760 dB

Interpretation:

The single-ended A_E_UP <-> B_E_UP term is substantially stronger than the actual differential/common-mode conversion.

The loaded network therefore behaves much more like a balanced two-terminal structure with expected mutual terminal coupling than a local-ground-induced common-mode leakage path.

## 4. Smoothness / resonance evidence

For A_E_UP -> B_E_UP across 1.15..1.65 GHz:

- minimum magnitude: approximately -21.293 dB
- maximum magnitude: approximately -16.252 dB
- largest adjacent 0.8-MHz-grid step: approximately 0.0165 dB
- largest excursion in any <=50 MHz window: approximately 1.009 dB

Frozen resonance sentinel:

>=10 dB change over <=50 MHz.

Result:

NO RESONANCE SENTINEL.

There is no narrow feature, abrupt step or sharp local resonance requiring a dedicated mechanism probe.

## 5. Branch symmetry

Across the decision band:

- max |S11-S44| complex magnitude: 0.05827
- max single-ended return-magnitude difference: approximately 0.225 dB

This is compatible with the known finite geometric asymmetry and does not indicate a gross branch imbalance.

## 6. PEC-wire warning localization

CST warning:

`Some edges which are part of lossy conductor surfaces are the intersection of otherwise disjoint regions. These edges will be treated as infinitely thin PEC wires.`

The warning geometry file:

`Result\TetMesherError.axg`

contains problematic positions concentrated around:
- z = 57.1428566 mm
- z = 58.1428566 mm
- z = 58.4278564 mm

These coordinates map to the frozen RF tongue / solder-bridge joint.

Examples:

### Solder bridge

Frozen A_P solder bridge:
- origin z = 58.1428571428 mm
- height = 0.285 mm
- local edge begins at u=3.95, v=0.035

Global warning point:

`(2.76832294, 2.81782055, 58.1428566)`

Using the frozen A basis:
- U=(1/sqrt(2),1/sqrt(2),0)
- V=(-1/sqrt(2),1/sqrt(2),0)

maps to approximately:
- u=3.95
- v=0.035

The corresponding z=58.4278564 point is exactly the top of the 0.285-mm solder bridge.

### RF tongue

The z=57.1428566 warning points lie along the frozen RF tongue copper edge/range, including the u=2.05..3.95 terminal tongue interval.

Therefore the warning is not located in:
- P_IN landing zone;
- P_OUT landing zone;
- local backside ground;
- paddle-via cluster;
- CRF ground via;
- downstream LNA/bias section.

It is an intentional feed-joint contact seam.

## 7. Warning classification

Classification:

`KNOWN_INTENTIONAL_EDGE_CONTACT_MESH_WARNING`

It is **not** evidence of a hidden LNA/local-ground interference mechanism.

However it remains a model-quality debt.

Because CST converts the edge contact between lossy conductor regions into an ideal PEC wire, this seam is not suitable as final authority for:
- sub-dB conductor/solder loss;
- insertion-loss budgeting;
- noise-temperature contribution;
- final manufacturable solder-joint loss.

Before those quantities become authoritative, the RF tongue / solder joint should be represented as a finite-area overlap/union or otherwise qualified electrically continuous joint, rather than relying on edge-only contact.

This debt does not invalidate the present coupling classification.

## 8. Mechanism decision

The >-20 dB single-ended review sentinel is classified as:

`BALANCED_RADIATOR_TERMINAL_COUPLING_NOT_ABNORMAL_COMMON_MODE_MECHANISM`

Reasons:
1. differential/common-mode conversion is <= about -30.7 dB at E_UP and far lower at P_IN;
2. P_IN-to-P_IN coupling is extremely small;
3. A_E_UP <-> B_E_UP response is broadband and smooth;
4. no frozen resonance sentinel is triggered;
5. branch symmetry is acceptable;
6. mesh warning is localized to the intentional tongue/solder joint, not the LNA/local-ground region.

Decision:

**No narrow Pol-A mechanism probe is required before promotion.**

## 9. Promotion consequence

The previous REVIEW hold is resolved by offline classification.

Pol-B promotion may proceed to its offline geometry/port/solve-contract freeze.

This does not authorize:
- Pol-B build;
- Pol-B solve;
- LNA transistor integration.

Current:
- BUILD_AUTHORIZED = false
- SOLVE_AUTHORIZED = false
- LNA_INTEGRATION_AUTHORIZED = false

Next:

`R1E1A4A_AR0_B1R_R4_A0_E2B_POLB_PROMOTION_CONTRACT_FREEZE`
