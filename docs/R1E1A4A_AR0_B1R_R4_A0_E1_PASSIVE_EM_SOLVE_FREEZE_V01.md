# R4-A0-E1 Passive 6-Port EM Solve Contract V0.1

Status: PRE-SOLVE FREEZE READY — NO SOLVE AUTHORIZATION  
Date: 2026-09-28  
SimulationOps minimum: 0.2.10

## 1. Purpose

This stage qualifies the one-LNA landing-zone as a passive six-port EM network before radiator integration and before QPL9547/circuit co-simulation.

It answers:
- whether the frozen V03 landing-zone solves numerically and produces a complete stable 6x6 passive network;
- whether the network is reciprocal/passive within numerical tolerance;
- how much parasitic coupling exists across the intentional circuit-domain gaps and around the omitted active device;
- whether any unexpected bypass/coupling is strong enough to justify a later field/current mechanism probe.

It does **not** optimize RF layout and does **not** establish final product input match.

## 2. Frozen source authority

Protected V03 artifact:
`D:\GNSS_R4A0E1_20260928_RECOVERY_ARTIFACTS\R1E1A4A_AR0_B1R_R4_A0_E1_ONE_LNA_LANDING_ZONE_BUILD_ONLY_V03.cst`

Source SHA256:
`a0e4bda5c64ea712564db76441721ca6dc147c97c061360a16a7d21f272f787a`

Source status:
`PASS_R4_A0_E1_V03_BUILD_AND_HUMAN_GEOMETRY_REVIEW`

The source artifact and its same-stem companion directory are protected and must remain unchanged.

## 3. Six-port node map

All ports are existing single-ended 50-ohm discrete ports referenced to the finite local backside ground.

| Port | Node | Role |
| --- | --- | --- |
| 1 | E_UP | upstream landing-zone line / input-cap upstream side |
| 2 | P_IN | QPL9547 RF-IN device-lead plane |
| 3 | P_OUT | QPL9547 RF-OUT/VDD device-lead plane |
| 4 | E_DN | downstream line / output-cap downstream side |
| 5 | B_VDD | post-L1 VDD/bias node |
| 6 | B_VBIAS | QPL9547 Vbias control node |

The following circuit-domain elements are intentionally absent from the EM model:
- C_IN = 100 pF G0 seed;
- QPL9547 active two-port;
- C_OUT = 100 pF G0 seed;
- L1 = 18 nH G0 seed;
- R4 = 3.32 kOhm.

Therefore the EM model contains intentional electrical gaps. A direct E_UP-to-E_DN S-parameter is **not** an insertion-loss measurement of the final signal chain.

## 4. Solver configuration

Solver source:
`source/cst/R1E1A4A_AR0_B1R_R4_A0_E1_PASSIVE_EM_SOLVER_CONFIG_V01.mcr`

Solver source blob:
`14554ad16fb7cb982ed7d9c03d0dc662bb4dec88`

Frozen configuration:
- frequency range: 1.0–1.8 GHz;
- decision band: 1.15–1.65 GHz;
- all boundaries open, no symmetry;
- 30 mm background space in all directions;
- HF Frequency Domain;
- tetrahedral mesh;
- curvature order 3;
- second-order tetrahedral formulation;
- General purpose frequency-domain method;
- adaptive mesh enabled;
- MinPasses = 3;
- MaxPasses = 16;
- MaxDeltaS = 0.02;
- NumberOfDeltaSChecks = 2;
- linear growth limitation = 40;
- Y/Z matrix post-processing enabled.

No geometry, material, port, boundary topology, or circuit element is modified other than solver/boundary/mesh settings.

## 5. Execution route

Solve host: **NW**.

Reason:
- the coupon is physically small;
- six-port frequency-domain qualification is modest compared with full antenna/array production solves;
- the protected V03 source already resides on NW;
- no XW or 251 dependency is required for this stage.

If NW execution is unavailable or drifts from the frozen environment, stop at infrastructure HOLD. Do not silently reroute to XW/251.

Execution runner:
`scripts/run_r1e1a4a_ar0_b1r_r4_a0_e1_passive_em_solve.py`

Runner blob:
`81379f68d79d229b713edd2ee2d06b3cec1853f4`

The runner must:
1. hash-verify the protected V03 source;
2. copy the complete CST project state (.cst + same-stem companion directory) to a fresh solve path;
3. add only the frozen solver configuration through History List;
4. fresh-reopen and verify six exact ports, solver history, and empty pre-solve result tree;
5. record one solver invocation;
6. invoke the solver exactly once;
7. never retry automatically;
8. extract all 36 complex Sij paths from one common valid run;
9. extract adaptive convergence;
10. preserve native logs and output a compact result packet.

## 6. Hard qualification gates

These gates decide PASS/HOLD.

### 6.1 Numerical convergence

PASS only if the final two adaptive `DeltaS` values are both <= 0.02.

MaxPasses 16 is the one-shot numerical budget. Reaching MaxPasses without two consecutive <=0.02 checks is a numerical HOLD, not permission to auto-rerun.

### 6.2 Complete network

All 36 Sij terms for ports 1–6 must exist on a common solver run and share the same native frequency grid.

Missing terms, incompatible run IDs, or frequency-grid mismatch => HOLD.

### 6.3 Reciprocity

Because the E1 coupon is passive and reciprocal, require over the full 1.0–1.8 GHz native grid:

`max |Sij - Sji| <= 0.02`, for all i != j.

This is a numerical-integrity gate, not an RF-layout target.

### 6.4 Passivity

For every native frequency and every excitation port j:

`sum_i |Sij|^2 <= 1.02`.

The 2% allowance is numerical tolerance. Values above this threshold are a network-integrity HOLD.

A value below unity is not interpreted as pure insertion loss; the deficit can include conductor loss, dielectric loss, and radiation/open-boundary power.

### 6.5 Native solver integrity

Hard HOLD on fatal solver failure or mesh corruption.

Large-reflection or disconnected-conductor warnings are recorded for interpretation but are not automatically physics FAIL because the network intentionally contains high-impedance/open circuit-domain gaps.

## 7. Diagnostic coupling sentinels

These are **review flags, not PASS/HOLD gates**.

Tracked couplings:
- P_IN <-> P_OUT: active-device bypass;
- E_UP <-> E_DN: end-to-end bypass;
- E_UP <-> P_IN: C_IN bare-gap parasitic;
- P_OUT <-> E_DN: C_OUT bare-gap parasitic;
- P_OUT <-> B_VDD: L1 bare-gap parasitic;
- B_VBIAS coupling to E_UP/P_IN/P_OUT/E_DN/B_VDD.

For unintended bypass/control-node coupling:
- > -20 dB anywhere in 1.15–1.65 GHz => REVIEW sentinel;
- > -10 dB => SEVERE REVIEW sentinel.

These thresholds are engineering sentinels only. They must not be re-labeled after seeing the result as formal pass/fail criteria.

The three intentional C/L gaps are reported but excluded from the unintended-coupling PASS/HOLD interpretation.

## 8. Frequency sampling rule

Hard numerical/reciprocity/passivity gates use **native solver samples only**.

Reference reporting at:
- L5 = 1.17645 GHz;
- L2 = 1.22760 GHz;
- L1 = 1.57542 GHz;

uses linear interpolation of the complex S-parameter, not interpolation of dB magnitude. The nearest native frequency and offset are retained as audit evidence.

## 9. Required outputs

The result package must contain:
- configured and solved CST artifact hashes;
- selected common S-parameter run ID;
- all S-parameter run IDs;
- convergence run ID and DeltaS sequence;
- full native 6x6 complex S matrix CSV;
- reciprocity extrema;
- passivity column-power extrema;
- coupling sentinels and their peak frequencies;
- exact L5/L2/L1 interpolated reference samples;
- native solver logs/warning flags;
- formal solver invocation count = 1;
- automatic retry count = 0.

A Touchstone S6P export is intentionally deferred until a writer/export path is separately qualified. The full complex 6x6 native matrix is sufficient for this stage and preserves the information required for later packaging.

## 10. Interpretation boundary

Do not use any single S11/S22 value as product input-match authority.

Do not call E_UP-to-E_DN transmission "insertion loss": the circuit-domain C_IN, QPL9547, C_OUT and L1 are absent.

Do not redesign geometry from one unusual coupling trace without first classifying whether the feature belongs to:
- the intentional component gap;
- device bypass;
- bias/control coupling;
- radiation/loss;
- or numerical artifact.

## 11. Next-stage rule

If all hard gates PASS and no unintended coupling REVIEW sentinel is raised:
- close E1 passive network qualification;
- proceed to **A0-E2 integrated antenna EM contract freeze**;
- do not optimize the isolated landing-zone further.

If hard gates PASS but a coupling REVIEW sentinel is raised:
- retain E1 geometry;
- freeze a narrow **E1-M1 mechanism probe** using field/current/loss observables at the offending peak and L5/L2/L1;
- do not immediately redesign geometry.

If any hard gate fails:
- HOLD and perform numerical/tooling attribution before any new solve.

## 12. Authorization boundary

`BUILD_AUTHORIZED = false`  
`SOLVE_AUTHORIZED = false`  
`LNA_INTEGRATION_AUTHORIZED = false`

No remote execution is authorized by this freeze.

The next formal action, if separately authorized, is exactly one NW E1-S0 passive EM solver invocation with zero automatic retries.


## 13. Post-human source provenance addendum

Before the authorized E1-S0 solve, the protected V03 .cst container no longer matched the build-pass SHA256.

Build-pass SHA256:
`a0e4bda5c64ea712564db76441721ca6dc147c97c061360a16a7d21f272f787a`

Post-human current SHA256:
`aee6bc30085c002b6063de80f110096f6b62911bf897007d133b309e5a962b36`

A dedicated complete-project-copy identity audit returned:
`PASS_R4_A0_E1_V03_POST_HUMAN_SOURCE_IDENTITY`

Verified unchanged:
- exact 36-solid inventory;
- exact component counts and materials;
- exact six ports, properties and coordinates;
- persistent V03 History;
- empty solver result tree;
- current source hash stable during the audit.

Therefore the post-human SHA256
`aee6bc30085c002b6063de80f110096f6b62911bf897007d133b309e5a962b36`
is the canonical source authority for the authorized E1-S0 solve.

This is a provenance-only re-baseline. No geometry, material, port, solver threshold, diagnostic threshold, or scientific interpretation rule changed. The formal solver budget remains unconsumed.
