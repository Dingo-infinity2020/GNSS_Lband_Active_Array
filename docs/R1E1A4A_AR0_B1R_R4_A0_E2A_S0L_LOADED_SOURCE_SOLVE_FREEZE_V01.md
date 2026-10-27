# R4-A0-E2A Pol-A Loaded Source-Side Passive Solve Freeze V0.1

Status: SOLVE CONTRACT FROZEN — ACTIVATION BLOCKED UNTIL HUMAN 3D REVIEW PASS — NO SOLVE AUTHORIZATION  
Date: 2026-09-28  
SimulationOps minimum: 0.2.12

## 1. Purpose

The first E2A electromagnetic solve shall **not** compute or promote the full raw 12x12 network.

Instead it shall characterize the Pol-A integrated radiator / stalk / twin-LNA landing-zone structure under a deliberately simple output condition:

- four source-side nodes remain exposed and are the only formal excitations;
- each QPL9547 RF-output device plane is terminated in a single-ended 50-ohm matched load to its branch-local RF ground;
- downstream C_OUT-side, VDD and Vbias auxiliary pads remain physically present but electrically open because their circuit-domain components are still absent.

This stage is named:

`E2A-S0L = loaded source-side passive pilot`

The suffix `L` means **50-ohm output-loaded**.

The goal is to answer the source-side question with the smallest network that preserves the relevant physics, without forcing a full 12-port characterization before it is needed.

## 2. Build authority

Protected build artifact:

`D:\GNSS_R4A0E2A_20260928_BUILD_R2\R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_INTEGRATED_BUILD_ONLY_V02_RECOVERY.cst`

SHA256:

`78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804`

Build status:

`PASS_R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_ONLY`

The canonical artifact remains protected. All solver configuration occurs on a complete-project copy.

## 3. Why this supersedes the original 12x12 first-solve plan

The original E2 freeze required all 144 Sij terms from the twelve raw EM nodes.

That remains a valid **full-network contingency**, but it is no longer the first-solve requirement.

Reason:

1. E2A first needs the source-side environment, not arbitrary excitation of every downstream pad;
2. QPL9547 RF output is naturally referenced to a 50-ohm environment in the G0 device model, so a 50-ohm output-load baseline is a useful first condition;
3. C_OUT, L1, decoupling and R4 are still circuit-domain elements, therefore E_DN / B_VDD / B_VBIAS should not be promoted into mandatory S-parameter excitations simply because they were useful build/audit reference planes;
4. a full 12x12 network is only required when arbitrary output/bias-network reconnection, reverse-feedback analysis or full active stability co-simulation becomes the scientific question.

The twelve build ports are still valid geometry/reference-plane evidence. This solve contract changes only the **solve copy port role**, not the production geometry.

## 4. Frozen loaded solve topology

### 4.1 Source-side exposed nodes

The four authoritative source-side nodes are:

- `A_E_UP`   = build raw port 1
- `A_P_IN`   = build raw port 2
- `B_E_UP`   = build raw port 7
- `B_P_IN`   = build raw port 8

These four nodes are the **only formal source excitations**.

They remain single-ended and referenced to the actual branch-local RF ground.

### 4.2 Output-load nodes

The two QPL9547 output device planes are:

- `A_P_OUT` = build raw port 3
- `B_P_OUT` = build raw port 9

For E2A-S0L they remain as single-ended 50-ohm ports referenced to branch-local ground but are **never excited**.

They act only as matched output loads and response/power-sink monitors.

This is an explicit baseline load condition, not a claim that the final output network is exactly 50 ohms under all operating conditions.

### 4.3 Auxiliary nodes left physically open

The following build-audit ports are removed from the solver copy:

- `A_E_DN`     = build raw port 4
- `A_B_VDD`    = build raw port 5
- `A_B_VBIAS`  = build raw port 6
- `B_E_DN`     = build raw port 10
- `B_B_VDD`    = build raw port 11
- `B_B_VBIAS`  = build raw port 12

Their copper pads/geometry remain unchanged.

With C_OUT / L1 / C_RF / R4 absent, these pads are intentionally open in E2A-S0L.

Do not replace them with arbitrary 50-ohm loads.

## 5. Solve-copy six-port mapping

After solver-copy port-role reduction, freeze the semantic six-port order as:

1. `A_E_UP` — source
2. `A_P_IN` — source / QPL9547 input device plane
3. `A_P_OUT_LOAD50` — 50-ohm matched load, never excited
4. `B_E_UP` — source
5. `B_P_IN` — source / QPL9547 input device plane
6. `B_P_OUT_LOAD50` — 50-ohm matched load, never excited

If CST 2022.5 requires port renumbering after copy mutation, this exact semantic mapping is authority.

The solver implementation must prove the final six-port properties/coordinates before the formal invocation.

## 6. Excitation contract

Formal excitation set:

`{1, 2, 4, 5}`

Matched-load-only set:

`{3, 6}`

A formal E2A-S0L runner must demonstrate before solver start that:
- only the four source ports are enabled as excitations;
- ports 3 and 6 remain passive matched terminations;
- no deleted auxiliary port survives;
- no solver has yet run.

If deterministic selected-port excitation cannot be proven in CST 2022.5, HOLD implementation.

Do **not** silently fall back to a six-source 6x6 solve.

A revised contract would be required before such a fallback.

## 7. Required response data

The authoritative result is not a 12x12 matrix.

Required common-run data are:

### Source-side reduced network

All 16 source-side terms for source/output indices in:

`{1,2,4,5} x {1,2,4,5}`

This is the loaded 4x4 source-side network.

### Output-load pickup rows

For every formal source excitation j in `{1,2,4,5}`, also retain:

- `S(3,j)` = power-wave response delivered to A output 50-ohm load
- `S(6,j)` = power-wave response delivered to B output 50-ohm load

Therefore the minimum qualified response set is:

**6 response rows x 4 source excitations = 24 complex traces**

on one common native frequency grid.

No S-column for output-load excitation is required.

## 8. Circuit-domain interpretation

C_IN remains absent from CST.

Therefore E2A-S0L **does not directly claim final QPL9547 source impedance at P_IN**.

Instead it produces a qualified loaded four-node passive source-side block:

`A_E_UP, A_P_IN, B_E_UP, B_P_IN`

with QPL9547 output planes terminated at 50 ohms.

After a provenance-qualified C_IN model is inserted in circuit domain:

- C_IN_A connects A_E_UP <-> A_P_IN
- C_IN_B connects B_E_UP <-> B_P_IN

the reduced loaded network may be collapsed to the two QPL9547 input device planes and used to derive:

- loaded source reflection coefficient;
- loaded source impedance;
- branch-to-branch input coupling;
- mixed-mode/common-mode input environment.

That derived source condition must be labeled:

`50OHM_OUTPUT_LOADED_SOURCE_CONDITION`

It is not final active-array source authority.

## 9. Deferred full-network trigger

The original twelve-node/full-network path is deferred, not deleted.

A full network becomes required before making claims about:
- arbitrary QPL9547 output load;
- reverse-feedback sensitivity involving the real downstream network;
- active stability with non-50-ohm output loading;
- C_OUT / L1 / VDD / Vbias network interaction;
- output-network co-design;
- full transistor two-port insertion with arbitrary external terminations.

A full-network solve may also be triggered if E2A-S0L shows a severe/unresolved coupling or resonance that cannot be attributed from the reduced loaded result.

It requires a separately frozen stage and separate solve authorization.

## 10. Frequency and numerical contract

Modeled band:

`1.0 .. 1.8 GHz`

Decision band:

`1.15 .. 1.65 GHz`

Reference frequencies:
- L5 = 1.17645 GHz
- L2 = 1.22760 GHz
- L1 = 1.57542 GHz

Frozen numerical baseline:
- CST HF Frequency Domain;
- second-order tetrahedral mesh;
- adaptive mesh;
- open radiation boundaries appropriate to the integrated antenna;
- MaxDeltaS = 0.02;
- require two consecutive native mesh-adaptation DeltaS <= 0.02;
- MaxPasses = 16;
- one formal solver invocation;
- automatic retry = 0;
- no optimizer / parameter sweep.

Native solver log remains convergence authority under SimulationOps 0.2.12.

## 11. Hard PASS / HOLD gates

### 11.1 Source identity

Before solver start:
- canonical build SHA exact;
- complete-project copy exact;
- solver-copy geometry inventory remains 107 solids;
- materials/shape names unchanged;
- only port role/configuration may change.

### 11.2 Six-port role

Fresh reopen must prove:
- exactly six solver-copy ports;
- exact semantic mapping;
- exact coordinates;
- exact 50-ohm reference impedance;
- only ports 1/2/4/5 are formal excitations;
- ports 3/6 are matched-load-only.

### 11.3 Numerical convergence

Native final two mesh-adaptation DeltaS <= 0.02.

### 11.4 Response completeness

Exactly 24 required complex traces exist on one common qualified run/native grid:
- 16 loaded source-side 4x4 terms;
- 8 output-load pickup terms.

### 11.5 Loaded source-side reciprocity

For source-side indices `{1,2,4,5}`:

`max |Sij - Sji| <= 0.02`

over 1.0–1.8 GHz.

No reciprocity gate is applied to unexcited load columns because those columns are intentionally not solved.

### 11.6 Loaded power closure

For each source excitation j in `{1,2,4,5}`:

`sum over i in {1,2,3,4,5,6} |S(i,j)|^2 <= 1.02`

Radiation and material loss account for power below unity.

### 11.7 Native integrity

- no fatal solver error;
- no mesh corruption;
- no unexpected port/excitation mutation;
- solved artifact/result tree readable read-only.

## 12. Diagnostics and review sentinels

Record across the decision band:

### Same-branch source gap parasitic

- A_E_UP <-> A_P_IN
- B_E_UP <-> B_P_IN

These are C_IN-gap parasitic baselines, not product insertion loss.

### Cross-branch source coupling

All A-source to B-source loaded terms.

Engineering sentinels:
- unintended coupling > -20 dB => REVIEW
- unintended coupling > -10 dB => SEVERE REVIEW

### Output-load pickup

For every source excitation:
- power-wave pickup into A 50-ohm output load;
- power-wave pickup into B 50-ohm output load.

Unexpected output-load pickup > -20 dB => REVIEW.
Unexpected output-load pickup > -10 dB => SEVERE REVIEW.

These are mechanism sentinels, not retroactive RF acceptance targets.

### Resonance sentinel

Flag:
- >=10 dB change in an unintended coupling/load-pickup trace over <=50 MHz; or
- a coincident sharp multi-source feature.

## 13. Branch comparison

At L5/L2/L1 and across the decision band report:

- A vs B E_UP return behavior;
- A vs B P_IN return behavior;
- A vs B C_IN-gap coupling magnitude/phase;
- cross-branch source coupling;
- A/B output-load pickup;
- mixed-mode source-side quantities derived from the two branch pairs.

The same-package-rotation asymmetry remains part of the baseline and shall not be tuned away inside this solve.

## 14. Mixed-mode reporting

For corresponding A/B source-side device-input waves:

`a_d = (a_A - a_B)/sqrt(2)`

`a_c = (a_A + a_B)/sqrt(2)`

and likewise for b.

Mixed-mode values are derived from the loaded single-ended source-side network.

No physical 100-ohm differential port is introduced.

## 15. Pol-A -> Pol-B promotion rule — supersession

This section supersedes the earlier requirement that Pol-A must first PASS a raw 12-port/full-144-term solve.

Pol-B promotion now requires:

- E2A build PASS;
- human 3D geometry review PASS;
- E2A-S0L loaded source-side solve hard-gate PASS;
- no SEVERE coupling/load-pickup sentinel;
- no unresolved resonance/mechanism review.

If hard gates PASS and no >-20 dB REVIEW sentinel remains, Pol-B promotion is direct.

If a >-20 dB REVIEW sentinel or unresolved resonance appears:
- freeze a narrow Pol-A mechanism probe first;
- Pol-B remains blocked until classification.

Pol-B must use the same 50-ohm output-load condition and the transformed equivalent source-side excitation contract for the A/B comparison.

## 16. Human-review dependency

This solve contract is frozen now, but it is **not active yet**.

Current E2A build stage still requires human 3D review.

Only after explicit human geometry PASS may project authority advance to:

`R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_SOLVE_IMPLEMENTATION`

Then the exact CST solver-copy port-reduction / selected-excitation source may be implemented and statically qualified.

No solve authorization is implied.

## 17. Authorization boundary

`BUILD_AUTHORIZED = false`

`SOLVE_AUTHORIZED = false`

`LNA_INTEGRATION_AUTHORIZED = false`

No NW/XW/251 call is authorized by this freeze.
