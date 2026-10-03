# SIM_EXECUTION

SimulationOps: 0.2.17 @ d4d2e53055ec5745eadeb11367332151e80d090c

Current stage:\nR1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_ONLY_AUTHORIZED

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false

PRE-REMOTE STATUS:
PASS_R4_A0_E1_PREBUILD_READY_AWAIT_BUILD_AUTH

Remote calls in R4-A0 prebuild:
0

Mainline:
- passive D1/M1 fixture S11 = diagnostic only
- Architecture B retained
- two single-ended first-stage LNAs per polarization
- QPL9547 = G0 reference, not final-production device
- active device remains outside CST
- co-simulation reference planes = QPL9547 device leads
- local package ground + vias mandatory
- remote lower-stalk-only LNA ground forbidden as baseline

A0-E1:
one-LNA landing-zone coupon only
no radiator
no second LNA
no full lower stalk
no remote ground merge
no solver

Frozen coupon:
q=-2..+2 mm
v=3..13 mm
FR4 thickness=1.00 mm
finite backside local ground

Frozen package:
Rev-D QPL9547 land pattern
3 paddle vias
5 grounded side-pin spokes to exposed paddle
pin1 Vbias remains isolated EM node
pin2 RF-IN
pin7 RF-OUT/VDD

Frozen circuit seed:
C_IN=100 pF
C_OUT=100 pF
L1=18 nH
C_RF=100 pF
R4=3.32 kOhm circuit-domain in E1

Six EM nodes:
E_UP
P_IN
P_OUT
E_DN
B_VDD
B_VBIAS

All single-ended 50-ohm normalized to finite local backside ground.
No differential port.

Static arithmetic audit:
PASS_R4_A0_E1_STATIC_PREBUILD_ARITHMETIC_AUDIT

Narrowest planned unrelated-copper clearance:
0.20 mm
downstream RF trace vs right-side decoupling lane.
If CST build fails this clearance, widen/rework the active-region stalk; do not shrink vendor/package lands.

Build source:
source/cst/R1E1A4A_AR0_B1R_R4_A0_E1_ONE_LNA_LANDING_ZONE_BUILD_ONLY_V02.mcr

V01 source:
PRE-EXECUTION SUPERSEDED
never authorized/executed.
Reason: plated-via barrel required explicit FR4 drill-hole subtraction first.

V02 plated-via rule:
0.35-mm drill
0.25-mm finished hole
FR4 hole subtracted first
annular copper barrel second

V02 static source audit:
PASS_R4_A0_E1_BUILD_SOURCE_STATIC_AUDIT_RECOVERY

Expected postbuild:
36 solids
6 ports
4 plated vias total
0 via drill-tool solids remaining
0 result tree
0 solver invocations

Deterministic runner:
scripts/run_r1e1a4a_ar0_b1r_r4_a0_e1_build_only.py

Authorized 2026-09-28 for exactly one BUILD-ONLY invocation:
fresh MWS
-> execute V02 macro once
-> save
-> fresh reopen
-> exact inventory/port/material audit
-> critical pairwise Boolean checks
-> human 3D review
-> STOP

No solve follows automatically.
SOLVE_AUTHORIZED remains false.


## 2026-09-28 formal A0-E1 build-only attempt 1

Status:
HOLD_R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_ONLY

Formal build invocations consumed: 1
Solver invocations: 0
Retry authorized: false

PASS:
- 36 solids and exact component counts
- exact material identities
- four via drill tools consumed / four plated vias remain
- empty result tree
- fresh-reopen artifact hash stable

HOLD:
- expected 6 ports, observed 0 after fresh reopen
- ten pairwise Solid.Intersect audits uniformly returned CST automation error -2147418113
- zero reported intersection volumes are not accepted as PASS because the Boolean operation errored

Protected NW artifact SHA256:
f5ee6fceab2c26db5d4d63365e37abec65b87698633c577e1ca87613b86a9745

Next boundary:
R4_A0_E1_BUILD_HOLD_RECOVERY_CONTRACT_FREEZE

No rebuild/retry/solve is authorized.

## V03 recovery source freeze

Recovery freeze:
docs/R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_HOLD_RECOVERY_FREEZE_V01.md

V03 source:
source/cst/R1E1A4A_AR0_B1R_R4_A0_E1_ONE_LNA_LANDING_ZONE_BUILD_ONLY_V03.mcr

Static equivalence:
PASS_R4_A0_E1_V03_STATIC_NO_GEOMETRY_REDESIGN

V03 changes only build persistence semantics: production source must enter the CST 3D History List. Geometry/material/via/pad/port coordinates remain frozen.

Next required action is a non-formal CST 2022 tooling/API probe on temporary copies. BUILD_AUTHORIZED remains false; SOLVE_AUTHORIZED remains false.

## Tooling root-cause closeout

Status:
PASS_R4_A0_E1_V03_RECOVERY_PREBUILD_READY_AWAIT_BUILD_AUTH

Confirmed:
- direct schematic.execute_vba_code Port99 fresh-reopens with PORT_COUNT=0;
- modeler.add_to_history Port99 fresh-reopens with PORT_COUNT=1 and persistent Model.mod history;
- CST 2022.5 current VBA surface does not expose Solid.DoTheseGeometricallyIntersect;
- .cst-only temporary pair copy can lose the required model state for a history-less artifact;
- complete project copy restores the target solid and makes Solid.Intersect return Err.Number=0 for the known zero-overlap test.

Recovery freeze:
docs/R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_HOLD_RECOVERY_FREEZE_V02.md

Recovery runner:
scripts/run_r1e1a4a_ar0_b1r_r4_a0_e1_v03_recovery_build.py

BUILD_AUTHORIZED remains false.
SOLVE_AUTHORIZED remains false.
Next boundary is a new one-shot V03 recovery BUILD-ONLY authorization.


## V03 recovery build authorization — 2026-09-28

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: false
Formal build budget: 1
Solver launch budget: 0
Silent retry: forbidden
Stop after persistent-history build + fresh reopen + port/history/intersection audit.


## V03 formal recovery build result

Automated status:
PASS_R1E1A4A_AR0_B1R_R4_A0_E1_V03_BUILD_ONLY

Artifact SHA256:
a0e4bda5c64ea712564db76441721ca6dc147c97c061360a16a7d21f272f787a

PASS:
- persistent model history
- exact 36 solids/materials
- six persistent 50-ohm ports with frozen coordinates
- four plated vias / drill tools consumed
- CDCheckModelIntersections returned
- 10/10 forbidden pairwise positive-volume overlaps = 0
- empty result tree
- fresh-reopen hash stable
- solver invocations = 0

BUILD authorization consumed and closed.
SOLVE_AUTHORIZED remains false.
Next gate: human 3D review using docs/R1E1A4A_AR0_B1R_R4_A0_E1_V03_HUMAN_3D_REVIEW_20260928.md.


## V03 human geometry review result

Status:
PASS_R4_A0_E1_V03_HUMAN_3D_REVIEW

Scope:
visual geometry / assembly sanity only.

Reviewer noted limited RF-layout expertise, therefore this PASS does not qualify RF performance, impedance, passive loss, local-ground RF quality, coupling, or stability.

A0-E1 build/human-geometry stage is closed PASS.

Next stage:
R1E1A4A_AR0_B1R_R4_A0_E1_PASSIVE_EM_SOLVE_CONTRACT_FREEZE

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
No solver invocation follows automatically.


## E1-S0 passive EM solve contract freeze

Status:
PASS_R4_A0_E1_PASSIVE_EM_PRESOLVE_FREEZE_READY_AWAIT_SOLVE_AUTH

Freeze:
docs/R1E1A4A_AR0_B1R_R4_A0_E1_PASSIVE_EM_SOLVE_FREEZE_V01.md

Protected V03 source SHA256:
a0e4bda5c64ea712564db76441721ca6dc147c97c061360a16a7d21f272f787a

Solver config:
source/cst/R1E1A4A_AR0_B1R_R4_A0_E1_PASSIVE_EM_SOLVER_CONFIG_V01.mcr
blob 14554ad16fb7cb982ed7d9c03d0dc662bb4dec88

Runner:
scripts/run_r1e1a4a_ar0_b1r_r4_a0_e1_passive_em_solve.py
blob 81379f68d79d229b713edd2ee2d06b3cec1853f4

Route:
NW only for this stage.
Complete-project copy of protected V03 source.
One formal solver invocation.
Zero automatic retries.

Hard gates:
- final two DeltaS <= 0.02
- complete common-run 6x6 S matrix
- max |Sij-Sji| <= 0.02
- max sum_i |Sij|^2 <= 1.02
- no fatal solver error
- no mesh corruption

Interpretation:
S11 is diagnostic only.
E_UP-to-E_DN transmission is not final insertion loss because C_IN/QPL9547/C_OUT/L1 remain circuit-domain gaps.
Unintended coupling > -20 dB is a review sentinel, not a hard physics FAIL.

If hard gates PASS with no coupling review:
next = A0-E2 integrated antenna EM contract freeze.

If hard gates PASS with coupling review:
next = narrow E1-M1 field/current/loss mechanism probe.

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false

No remote calls were used for this contract freeze.


## E1-S0 solve authorization — 2026-09-28

SOLVE_AUTHORIZED: true
BUILD_AUTHORIZED: false
Formal solver budget: 1
Automatic retry budget: 0
Solve host: NW
Stop after read-only six-port qualification; no retry.


## E1-S0 post-human provenance rebaseline

Pre-solve source hash drift was detected before any solver invocation.
Dedicated identity audit PASSed: exact 36 solids/materials, exact six ports/coordinates, persistent V03 History, empty result tree, stable current hash.

Build-pass SHA256:
a0e4bda5c64ea712564db76441721ca6dc147c97c061360a16a7d21f272f787a

Canonical post-human source SHA256:
aee6bc30085c002b6063de80f110096f6b62911bf897007d133b309e5a962b36

Classification: provenance-only rebaseline; no scientific model or solve-gate change.
Formal solver budget remains 0/1 consumed.
SOLVE_AUTHORIZED remains true for exactly one E1-S0 solve.


## E1-S0 passive EM solve result

Status:
PASS_R1E1A4A_AR0_B1R_R4_A0_E1_PASSIVE_EM_CHARACTERIZED

Disposition:
PASS_CHARACTERIZED_NETWORK_CLEAN_SENTINELS

Formal solver invocations: 1
Automatic retries: 0

Solved artifact SHA256:
bd487a52e342284fe7cdf4b6a35c0a7fc23296e97560f9603451bbf6f0b6349c

Native CST mesh-adaptation authority:
- pass 3 DeltaS = 0.00772936
- pass 4 DeltaS = 0.00465735
- CST terminated adaptation because desired accuracy was reached

Network integrity:
- complete 6x6 network: PASS
- native frequency grid: 1001 points, 1.0–1.8 GHz
- max |Sij-Sji| = 4.233e-7: PASS
- max sum_i |Sij|^2 = 0.999045: PASS
- fatal solver error: false
- mesh corruption: false

Coupling:
- strongest P_IN/P_OUT bypass = -68.99 dB
- E_UP/E_DN bypass = -49.44 dB
- no unintended coupling exceeded -20 dB
- no E1-M1 mechanism probe required

Native warning:
large input reflection at 1.8 GHz.
This is interpretation-only because the passive EM coupon intentionally leaves C_IN/QPL9547/C_OUT/L1 in the circuit domain. It is not product input-match authority.

The cst.results convergence series is retained as secondary evidence; native output.txt is the primary mesh-adaptation authority because the two representations are numerically different though both independently pass the 0.02 threshold.

SOLVE_AUTHORIZED: false
BUILD_AUTHORIZED: false

Next:
R1E1A4A_AR0_B1R_R4_A0_E2_INTEGRATED_ANTENNA_EM_CONTRACT_FREEZE


## SimulationOps sync after E1-S0

Next-stage minimum: SimulationOps 0.2.11.
New global rules captured from E1-S0: post-human/GUI CST source-hash integrity and native-vs-result-tree convergence authority.


## E2A Pol-A integrated EM contract freeze

Status:
PASS_R4_A0_E2A_POLA_CONTRACT_FROZEN_SOURCE_IMPLEMENTATION_NEXT

Authority:
- docs/R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_INTEGRATED_EM_FREEZE_V01.md
- execution/R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_INTEGRATED_EM_MANIFEST_V01.json

Key correction:
the four QPL9547 device-lead planes remain frozen, but raw CST E2 extraction is twelve-node, not a literal four-port. This is required because C_IN/C_OUT/L1/decoupling/R4 remain circuit-domain elements; collapsing the raw EM model to four ports before inserting those passives would disconnect the radiator from P_IN and destroy source-condition meaning.

Pol-A pilot:
- full radiator retained;
- accepted orthogonal mechanical/dielectric environment retained;
- inactive Pol-B feed held as open signal stub only through the v=3 handoff;
- two Pol-A E1 cells inserted from v=3..13 on u=+/-3 branches;
- same package rotation on both branches;
- G-L0 branch-local grounds only;
- no G-L1 merge;
- no historical D2 remote ground merge;
- eight active-region plated vias total;
- exactly twelve raw single-ended 50-ohm ports after build.

Frozen device planes:
raw ports 2/3/8/9 = P1A_IN / P1A_OUT / P1B_IN / P1B_OUT.

Pol-A -> Pol-B:
Pol-B is blocked until Pol-A build + human geometry + raw 12-port hard solve PASS. Any unresolved >-20 dB coupling review or resonance mechanism blocks direct promotion.

Current stage:
R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_SOURCE_IMPLEMENTATION

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false

No remote calls were used for this freeze.


## E2A Pol-A prebuild implementation result

Status:
PASS_R4_A0_E2A_POLA_PREBUILD_READY_AWAIT_BUILD_AUTH

Frozen source:
- macro blob 9931736f1129624d94aee1c9e983a1eaabca5f24
- runner blob 81f717ca5ef7aa4c4375618185aeb1723b0d50f1
- inventory blob e10886a4c01d9aafd55a16d8126418b7e22025fd

Exact build accounting:
45 parent - 12 superseded + 74 final new = 107 final solids.

The macro additionally creates eight drill-tool solids, consumes all eight by FR4 subtraction, and retains eight plated via barrels.

Raw ports:
12 exact 50-ohm single-ended ports.
Device planes remain raw ports 2/3/8/9.

Static audit:
- exact 74-new-shape name set matches manifest;
- no missing / extra / duplicate shape names;
- port numbers exactly 1..12;
- no solver tokens;
- no active QPL9547;
- no circuit passives;
- no duplicate E1 FR4 coupon;
- no D2 remote ground merge;
- runner run_solver() count = 0;
- complete project copy + History build required;
- whole-model intersection check + 14 complete-copy pairwise checks frozen.

Current:
BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false

Next:
one E2A Pol-A BUILD-ONLY authorization.


## E2A Pol-A build authorization — 2026-09-28

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: false
Formal build budget: 1
Solver invocation budget: 0
Automatic retry budget: 0
Stop after fresh-reopen / exact inventory / 12-port / via / interference / human-review package.


## E2A Pol-A formal build HOLD

Status:
HOLD_R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_ONLY

Classification:
HOLD_BUILD_AUDIT_CRITERION

Formal build invocations: 1
Solver invocations: 0
Automatic retries: 0

Artifact SHA256:
573e21e893a5b8fa9a76ae3c8d5dce641c672607c2747aa1ca39f9879b63c7fc

All structural/persistence/interference checks PASSed except the pre-frozen analytic prong drill-volume equality gate.

Observed four-hole prong losses:
- A_P 0.38483724205539716 mm3
- A_N 0.3848372420552977 mm3

Frozen analytic value:
0.3848451000647496 mm3

Historical E1-V03 accepted four-hole CST Boolean loss:
0.3848392442002009 mm3

Attribution:
the 1e-7 mm3 analytic pi*r^2*h equality gate is not qualified for CST/ACIS Boolean cylinder volume semantics.

SimulationOps no-post-result-gate-change rule applies:
this formal build remains HOLD.

Next:
NO_GEOMETRY_REDESIGN audit-recovery freeze.

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false


## E2A Pol-A V02 audit recovery ready

Status:
PASS_R4_A0_E2A_POLA_V02_RECOVERY_READY_AWAIT_BUILD_AUTH

Attempt-1 formal status remains:
HOLD_R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_ONLY

Root cause proof:
PASS_R4_A0_E2A_DRILL_KERNEL_REFERENCE

The disposable canonical-parent drill reference reproduced the formal HOLD artifact prong volumes exactly:
- A_P 47.6151627579446 mm3
- A_N 47.6151627579447 mm3
- hold-minus-reference = 0.0 mm3 for both branches

Recovery class:
NO_GEOMETRY_REDESIGN

Unchanged production authority:
- production macro blob 9931736f1129624d94aee1c9e983a1eaabca5f24
- inventory blob e10886a4c01d9aafd55a16d8126418b7e22025fd
- 107 solids / 12 ports / 8 vias / 14 pairwise predicates

New tooling authority:
- kernel reference blob e7fe96e2e763fcc025ce45e874162d9c8a771f77
- V02 runner blob a8f9183d7e4bb635ece3a5cc9e0edd30fb230502

V02 hard drill-volume gate:
production prong loss must match CST/ACIS-native canonical-parent drill reference within 1e-7 mm3.

Analytic 4*pi*r^2*h is diagnostic only.

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false

A new explicit BUILD authorization is required.


## SimulationOps sync after E2A audit HOLD

Current minimum: SimulationOps 0.2.12.
Global rule added: analytic primitive volume is diagnostic unless CST/ACIS Boolean equivalence is qualified; use CST-native kernel reference for tight volume gates.


## E2A Pol-A V02 recovery build authorization — 2026-09-28

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: false
Recovery class: NO_GEOMETRY_REDESIGN
Formal build budget: 1
Solver invocation budget: 0
Automatic retry budget: 0
Kernel-reference preflight must pass before the unchanged production History executes.


## E2A Pol-A V02 recovery build PASS

Status:
PASS_R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_ONLY

Recovery class:
NO_GEOMETRY_REDESIGN

Formal build invocations: 1
Solver invocations: 0
Automatic retries: 0

Artifact:
D:\GNSS_R4A0E2A_20260928_BUILD_R2\R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_INTEGRATED_BUILD_ONLY_V02_RECOVERY.cst

SHA256:
78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804

Kernel-reference gate:
- A_N production/reference loss delta = 0.0 mm3
- A_P production/reference loss delta = 0.0 mm3
- hard tolerance = 1e-7 mm3
- analytic 4*pi*r^2*h retained as diagnostic only

Build qualification:
- 107 exact solids PASS
- exact component/name set PASS
- 12 exact ports PASS
- device planes raw 2/3/8/9
- 8 plated vias PASS
- History persistence PASS
- empty result tree PASS
- fresh-reopen/hash stability PASS
- CDCheckModelIntersections return PASS
- 14/14 complete-project-copy pairwise zero-positive-volume PASS
- cross-pol envelope PASS

Runner summary contains inherited display field simulationops=0.2.11; project/global execution authority is 0.2.12. Metadata-only.

Current stage:
R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_HUMAN_3D_REVIEW

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false


## E2A-S0L loaded source-side solve contract

Status:
PASS_R4_A0_E2A_S0L_LOADED_SOURCE_SOLVE_CONTRACT_FROZEN_BLOCKED_BY_HUMAN_REVIEW

Authority:
- docs/R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_SOLVE_FREEZE_V01.md
- execution/R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_SOLVE_MANIFEST_V01.json

First E2A solve is no longer a mandatory 12x12/144-term extraction.

Loaded pilot:
- formal source excitations: A_E_UP, A_P_IN, B_E_UP, B_P_IN
- matched 50-ohm output loads: A_P_OUT, B_P_OUT
- E_DN / B_VDD / B_VBIAS audit ports removed from solve copy; physical pads remain open
- minimum qualified response: 24 complex traces = 6 response rows x 4 source excitations
- loaded source-side reciprocity gate only
- loaded column-power closure includes both output-load response rows

Interpretation:
C_IN remains absent from CST. Raw S0L is not direct final QPL9547 source impedance authority.
After qualified C_IN insertion, derived result is labeled 50OHM_OUTPUT_LOADED_SOURCE_CONDITION.
Full network is deferred until arbitrary output loading / reverse feedback / active stability / full transistor co-sim requires it.

Current stage remains:
R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_HUMAN_3D_REVIEW

Activation requires explicit human geometry PASS.

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false

No remote calls were used for this freeze.


## E2A-S0L selected-excitation implementation

Status:
PASS_R4_A0_E2A_S0L_STATIC_IMPLEMENTATION_READY_BLOCKED_BY_HUMAN_REVIEW

No remote calls were used.

CST 2022 implementation:
- delete raw audit ports 12/11/10/6/5/4
- rename raw 7/8/9 -> solve 4/5/6
- six-port semantic map retained
- FDSolver source type = List/List
- selected source excitations = 1/2/4/5
- ports 3/6 = passive 50-ohm matched output loads, never sources
- no high-Z open surrogate
- no geometry rebuild
- no six-source fallback

Frozen sources:
- config macro blob a42d59e0aa6dae84c0d6ff4b5bf20193a71a9bf5
- presolve runner blob ca520ccbc48fb56baf725c0216c3b32cd718af0c
- formal solve runner blob 9b944002dc65b5b21cad00c230ba041833c4de5e

Static audit:
- config solver-start count = 0
- presolve runner run_solver() count = 0
- formal solve runner run_solver() count = 1
- response contract = 24 complex traces
- no full 6x6/12x12 first-solve requirement

Current stage remains:
R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_HUMAN_3D_REVIEW

After explicit human PASS:
next = R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_PRESOLVE_CONFIG_AWAIT_AUTH

That next node runs configuration only and must STOP before solver invocation.

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false


## E2A-S0L presolve configuration authorization — 2026-09-29

PRESOLVE_CONFIG_AUTHORIZED: true
BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
Formal solver budget: 0
Automatic retry budget: 0
Configure disposable complete-project copy only; stop after fresh-reopen 107-solid/6-port/selected-excitation/empty-result-tree qualification.


## E2A-S0L presolve configuration PASS

Status:
PASS_R4_A0_E2A_S0L_PRESOLVE_CONFIG_READY

Formal solver invocations: 0
Formal build invocations: 0

Configured artifact:
D:\GNSS_R4A0E2A_S0L_PRESOLVE\R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_PRESOLVE_CONFIGURED_V01.cst

SHA256:
ad549cb2743a425c21e602469010836f43a16e8fec99d32f4c28369bc47a381f

Runtime fresh-reopen proof:
- 107 solids unchanged
- exact shape/component/material/volume signature unchanged
- exactly 6 ports
- source excitations = 1,2,4,5
- ports 3,6 = 50-ohm S-parameter ports, load-only, not excited
- exact selected-excitation History persists
- result tree empty
- configured hash stable

Load interpretation:
An unexcited 50-ohm S-parameter port is the matched passive termination for the S0L EM baseline. No separate physical 50-ohm lumped resistor is inserted.

Current human 3D review is not retroactively marked PASS by this configuration run.

PRESOLVE_CONFIG_AUTHORIZED: false
BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false


## E2A human review PASS and S0L solve authorization — 2026-09-29

Human review status: PASS_R4_A0_E2A_POLA_HUMAN_3D_REVIEW
User also confirmed the S0L presolve review copy.

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true
Formal solver budget: 1
Automatic retry budget: 0
Selected sources: 1,2,4,5
Matched-load-only ports: 3,6
No full 6x6 or 12x12 fallback.


## E2A-S0L solve qualification recovery PASS

Formal solve runner status remains:
HOLD_R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_QUALIFICATION

The frozen native-log parser did not recognize CST 2022.5 lines of the form `All S-Parameters = value`.

Read-only recovery:
PASS_R4_A0_E2A_S0L_READONLY_QUALIFICATION_RECOVERY

No new solver invocation was used.

Recovered native DeltaS:
- 0.039114
- 0.00606905
- 0.00737333

Final two are both <= 0.02.

Other hard gates:
- 24/24 response traces PASS
- common 1001-point 1.0..1.8 GHz grid PASS
- source-side reciprocity max |Sij-Sji| = 1.7684e-5 PASS
- loaded column power max = 0.9999856 PASS
- fatal solver error = false
- mesh corruption = false

Disposition:
PASS_LOADED_SOURCE_WITH_REVIEW

Review sentinel:
A_E_UP <-> B_E_UP peaks at -16.2516 dB near 1.5736 GHz.
No severe > -10 dB sentinel.
Pol-B promotion is blocked pending mechanism classification.

Representative GNSS values:
- L5 A_EUP<->B_EUP: -20.9997 dB
- L2: -19.9872 dB
- L1: -16.2517 dB
- P_IN<->P_IN remains approximately -102 to -107 dB at L5/L2/L1.

Current:
BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false

Next:
R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_COUPLING_REVIEW_FREEZE


## E2A-S0L coupling review PASS

Status:
PASS_R4_A0_E2A_S0L_COUPLING_CLASSIFIED_NO_PROBE_REQUIRED

Classification:
BALANCED_RADIATOR_TERMINAL_COUPLING_NOT_ABNORMAL_COMMON_MODE_MECHANISM

Offline mixed-mode evidence from the qualified 1001-point solve:
- E diff->common peak: -30.7106 dB
- E common->diff peak: -30.7117 dB
- E diff->P_IN common peak: -67.6151 dB
- P_IN diff->common peak: -73.5334 dB
- A_E_UP<->B_E_UP max 50-MHz excursion: 1.009 dB
- frozen >=10 dB / <=50 MHz resonance sentinel: NOT TRIGGERED
- max single-ended return-magnitude branch difference: 0.225 dB

Therefore the single-ended A_E_UP<->B_E_UP peak (-16.2516 dB near 1.5736 GHz) is classified as balanced-radiator terminal coupling rather than an abnormal local-ground/LNA common-mode mechanism.

PEC-wire warning localization:
- Problematic Positions occur at z=57.1428566 / 58.1428566 / 58.4278564 mm.
- Coordinates map exactly onto the frozen RF tongue / solder-bridge contact seam.
- They do not map to P_IN, P_OUT, local backside ground, paddle-via cluster or CRF ground via.
- Classification: KNOWN_INTENTIONAL_EDGE_CONTACT_MESH_WARNING.

Model-quality debt:
edge-only contact is not final authority for conductor/solder loss or noise-temperature budgeting.
Before authoritative loss/NF work, replace it with a finite-area overlap/union or otherwise qualified continuous solder joint.

Decision:
- no narrow Pol-A mechanism probe required;
- Pol-B promotion is unblocked for offline contract freeze only;
- no Pol-B build or solve is authorized.

Current:
BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false

Next:
R1E1A4A_AR0_B1R_R4_A0_E2B_POLB_PROMOTION_CONTRACT_FREEZE


## E2B Pol-B build PASS

Status:
PASS_R1E1A4A_AR0_B1R_R4_A0_E2B_POLB_BUILD_ONLY

Artifact:
D:\GNSS_R4A0E2B_20260929_BUILD\R1E1A4A_AR0_B1R_R4_A0_E2B_POLB_INTEGRATED_BUILD_ONLY_V01.cst

SHA256:
002eb117b0716cf2a47856b4552dd96ef4567358c7dd5827cbe766d10a633f39

Human review copy:
D:\GNSS_R4A0E2B_20260929_BUILD\R1E1A4A_AR0_B1R_R4_A0_E2B_POLB_HUMAN_REVIEW_COPY.cst

Automated build qualification:
- 107/107 exact solids
- 12 exact B-basis ports
- 8 plated vias
- B_P/B_N drill losses exactly match CST-native kernel reference
- half-lap unsupported copper absent
- N backside-ground notch volume exactly 0.004375 mm3 relative to P baseline
- CDCheckModelIntersections command PASS
- 14/14 complete-copy pairwise checks zero positive-volume overlap
- result tree empty
- solver invocations 0

S0L solve source is already frozen and static-audited:
- config blob 07928d0412fb90dc439632c68c2d9375933157ca
- runner blob 5e55381d489665c9a930c78722e7ef65bf4450b3
- selected sources 1/2/4/5
- 50-ohm load-only ports 3/6
- formal runner run_solver() count = 1
- automatic retry = 0
- 24-response contract retained

User has already authorized the solve, but production solve activation remains blocked until explicit E2B human 3D review PASS.

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: true
production_solve_authorized: false


## E2B S0L recovery + E2 A/B promotion PASS

Formal E2B runner remains HOLD due a postsolve Python regex exception. The scientific solve itself completed once; no retry occurred.

Read-only recovery:
PASS_R1E1A4A_AR0_B1R_R4_A0_E2B_S0L_READONLY_QUALIFICATION_RECOVERY

- formal solver invocations: 1
- recovery solver invocations: 0
- native final DeltaS: 0.00656218 / 0.00869598
- 24/24 traces on 1001-point 1.0..1.8 GHz grid
- reciprocity max: 2.199e-5
- max loaded column power: 0.9999873
- no fatal solver error
- no mesh corruption

A/B passive promotion:
PASS_R1E1A4A_AR0_B1R_R4_A0_E2AB_PASSIVE_PROMOTION

Pol-B conversion is slightly lower than Pol-A by about 1.4..2.2 dB for the frozen diff/common leakage metrics.
Pol-B branch return imbalance is 0.186 dB.
Pol-B max 50-MHz E-terminal coupling excursion is 0.990 dB.
No >6 dB conversion-degradation, >1 dB branch-imbalance, or >=10 dB/50MHz resonance review gate is triggered.

PEC-wire problematic positions remain on RF tongue / solder-bridge seams, not the half-lap.

Passive E2 mainline is closed. No build or solve is authorized.

Next:
R1E1A4A_AR0_B1R_R4_A0_C1_ACTIVE_COSIM_CONTRACT_FREEZE


## E2C dual-pol coexistence contracts frozen

Status:
PASS_R4_A0_E2C_ROUTE_GEOMETRY_AND_SENTINEL_CONTRACTS_FROZEN

This supersedes the previous immediate-C1 next step.

Frozen route:
E2C dual-pol coexistence
-> D0 device/component model authority
-> C1 full-network active feasibility
-> periodic/scan active-impedance atlas
-> final LNA/antenna co-design

E2C geometry:
- canonical pre-E2 parent, not A/B CST-container merge
- 45 parent solids - 12 superseded + 72 Pol-A + 72 Pol-B = 177 final solids
- 16 plated vias
- 24 raw audit/reference ports
- exact E2A geometry + exact E2B geometry including frozen half-lap notch
- no RF retune
- cross-pol A-vs-B conductor broad-phase + qualified pairwise positive-volume intersection audit required

E2C combined sentinel:
- reduced 12-port network
- 8 source ports: E_UP/P_IN for four branches
- 4 P_OUT 50-ohm load-only ports
- 96 required complex traces
- no full 24x24 first solve
- native DeltaS <=0.02 twice
- source-side reciprocity <=0.02
- loaded column power <=1.02

Frozen coexistence review:
- own-pol 4x4 max complex delta >0.10 REVIEW; >0.20 severe
- mode-conversion degradation >3 dB REVIEW; >6 dB severe
- branch return imbalance >1 dB REVIEW
- >=10 dB / <=50 MHz resonance REVIEW
- cross-pol device-side coupling >-20 dB REVIEW; >-10 dB severe

No active-stability claim may use this partial sentinel network. C1 still requires separately frozen full passive network authority.

Current:
BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false

Next:
R1E1A4A_AR0_B1R_R4_A0_E2C_BUILD_SOURCE_STATIC_PREPARATION


## E2C prebuild static implementation PASS

Status:
PASS_R4_A0_E2C_PREBUILD_STATIC_READY_AWAIT_AUTH

No NW/XW/251 simulation call was used.
Formal build invocations: 0
Solver invocations: 0

Frozen implementation:
- combined build macro blob: fb770258aa94106a2437320c29a2cd036990770a
- exact inventory blob: dcc33fc9236eb9e2a696bb90f43ce9e1bdc27bd2
- 16-via CST kernel-reference blob: fbaac4e894a5b5af3c3145a67e767b2a7c8e9c98
- cross-pol broadphase runner blob: ce09233173aea44783be8d87dc5e665ca07356e9
- cross-pol broadphase manifest blob: 8dd082aab1c1fd99495b0e773c1c987efd79e62c
- formal build runner blob: e62ae3982f39c67f1c369802792c2ec553c6788c

Static geometry closure:
- 12 parent deletes
- 16 temporary via drill tools
- 144 final new solids
- 177 expected final solids
- 16 plated vias
- 24 exact raw ports
- 16 drill subtract operations
- Pol-A via rotations +135 deg: 16 transform occurrences
- Pol-B via rotations -135 deg: 16 transform occurrences
- build runner run_solver() count = 0

Cross-pol coexistence broadphase:
- Pol-A new solids = 72
- Pol-B new solids = 72
- all A x B pairs = 5184
- source-AABB candidate pairs = 1
- candidate:
  E2C_A_P_BackGround:LOCAL_BACK_GROUND
  vs
  E2C_B_N_BackGround:LOCAL_BACK_GROUND

Formal build pairwise contract:
- inherited E2A checks = 14
- inherited E2B checks = 14
- new E2C A/B coexistence candidate = 1
- total required complete-copy pairwise checks = 29/29

Current boundary:
R1E1A4A_AR0_B1R_R4_A0_E2C_BUILD_AWAIT_AUTH

BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false
LNA_INTEGRATION_AUTHORIZED: false


## SimulationOps 0.2.15 runner migration for E2C build

Authority:
- SimulationOps main commit 7dfbeb7a44a82501a7a20bbe62230aa047e80af6
- GLOBAL protocol 0.2.15
- generic stage runner v0.1
- NW stable launcher runner/nw/simops.cmd

User authorization:
BUILD_AUTHORIZED = true
SOLVE_AUTHORIZED = false

Execution rule:
- use BUILD_ONLY runner packet;
- validate + dry-run before one-shot run;
- no Build->Solve chaining;
- automatic retry = 0;
- stop after project build/audit and human-review-copy boundary.

Compatibility finding:
NW stable launcher binds non-CST Python 3.13, while CST Studio Suite 2022 cst package supports Python 3.6/3.7/3.8/3.9 only.

Project adapter:
scripts/simops_cst_python_bridge_v01.py

The bridge contains no CST installation path. It receives CST_PYTHON_EXECUTABLE from runtime environment derived from SimulationOps HOSTS, records the exact child argv, and uses subprocess with shell=False.

Repository boundary:
the CST executable path remains host/runtime authority and is not copied into project scientific source.


E2C SimOps 0.2.15 final build transaction update:
- final build runner blob: 08adaf7ecac05832ee47916b566be80af63992d3
- review copy is part of the same BUILD_ONLY transaction
- interpreter bridge: scripts/simops_cst_python_bridge_v01.py
- generic runner remains responsible for authorization/preflight/one-shot/result packet
- project runner remains responsible for CST geometry/build/audit science


## E2C formal build attempt 01 HOLD

Generic runner packet:
GNSS-E2C-DUALPOL-BUILD-20260930-01

SimulationOps core:
- final_status = HOLD_ENTRYPOINT
- build_consumed = true
- solve_consumed = false
- no retry

Project exception:
TypeError: main() takes 6 positional arguments but 7 were given

Failure boundary:
before project main() entered; no CST kernel reference, production macro or solver started.

Recovery:
NO_GEOMETRY_REDESIGN
docs/R1E1A4A_AR0_B1R_R4_A0_E2C_BUILD_RECOVERY_FREEZE_V01.md

Corrected runner blob:
76b3e403a830d9736fc019303dc7f0b0e8b3ee0f

Entrypoint AST audit blob:
e2e761d54d263e52d7a7c90a910d9e5863d8251f

Current:
BUILD_AUTHORIZED: false
SOLVE_AUTHORIZED: false

Next:
R1E1A4A_AR0_B1R_R4_A0_E2C_BUILD_RECOVERY_AWAIT_AUTH


## SimulationOps 0.2.16 E2C recovery adoption

Current global authority:
- SimulationOps 0.2.16 @ 4a3af70c8f9a859bacf7cbc51e7b72fcf4e14d2a
- PROJECT_RUNNER_ADOPTION.md applies
- NW checkout authority: D:\quest_naoc_tarminal\SimulationOps
- control runtime != CST simulator runtime
- routine formal packet source is Git-first

Committed packet generator:
scripts/make_e2c_build_recovery_runner_packet_v01.py

Generator blob:
5cc98ff5f37fb69ca6b10c329ca4bf8c7d4774d8

Recovery authorization:
BUILD_AUTHORIZED = true
SOLVE_AUTHORIZED = false

Fresh production-entrypoint qualification is mandatory before the new recovery BUILD_ONLY packet is allowed to consume authorization.


## SimulationOps 0.2.17 observable E2C recovery

Authority:
- SimulationOps 0.2.17 @ d4d2e53055ec5745eadeb11367332151e80d090c
- PROJECT_OBSERVABILITY_PROTOCOL.md
- runner v0.2 status/event state

Project event protocol:
simops-project-event-v0.1

Production boundary:
immediately before frozen E2C `prj.modeler.add_to_history(HISTORY_LABEL, macro_body(macro))`.

Fresh user authorization:
BUILD_AUTHORIZED = true
SOLVE_AUTHORIZED = false

Before formal build:
1. fresh entrypoint/runtime qualification;
2. GENERIC_NONPRODUCTION canonical-parent smoke:
   copy -> open -> exact inventory -> result-tree empty -> close;
3. smoke must PASS.

Phase watchdog adapter:
scripts/e2c_simops_watchdog_adapter_v01.py

Smoke:
scripts/smoke_e2c_parent_inventory_v01.py

No process/window/directory polling is the normal progress API. If intermediate state is needed, use `simops.cmd status --packet ...`.
