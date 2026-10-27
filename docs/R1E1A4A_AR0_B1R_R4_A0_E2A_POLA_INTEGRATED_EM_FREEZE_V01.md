# R4-A0-E2 Pol-A Integrated Antenna / Landing-Zone Freeze V0.1

Status: DESIGN / PORT / METRIC FREEZE COMPLETE — BUILD SOURCE NOT YET FROZEN  
Date: 2026-09-28  
SimulationOps minimum: 0.2.11

## 1. Purpose

E2 is the first stage that reconnects the qualified QPL9547 landing-zone geometry to the accepted radiator / RF-tenon / stalk architecture.

The Pol-A pilot answers:

1. can the accepted radiator / tongue / stalk geometry and two qualified E1 landing zones coexist as one manufacturable EM structure;
2. does the integrated passive assembly remain numerically well behaved;
3. what passive multiport environment exists around the two first-stage device sites before inserting the QPL9547 active two-ports;
4. does the real radiator / stalk integration create unexpected branch-to-branch, bias-to-RF, or input-to-output coupling;
5. is Pol-A clean enough to justify building the mechanically complementary Pol-B sentinel without first opening a mechanism-recovery branch.

This stage is **characterization, not impedance optimization**.

## 2. Authority and supersession

### 2.1 Mechanical / radiator parent

Canonical corrected active-feed mechanical/RF parent:

`R1E1A4A_AR0_B1R_T1R1_GROUND_PLACEMENT_CORRECTED_BUILD_ONLY_V01.cst`

SHA256:

`fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e`

This parent is a geometry donor only. Its old passive-fixture RF interpretation is not product authority.

### 2.2 Landing-zone donor

Qualified one-LNA E1 geometry:

`source/cst/R1E1A4A_AR0_B1R_R4_A0_E1_ONE_LNA_LANDING_ZONE_BUILD_ONLY_V03.mcr`

Git blob:

`8066f693f7a3ba980cf015ef5d9554fd31dc7549`

Qualified E1 solved artifact:

SHA256 `bd487a52e342284fe7cdf4b6a35c0a7fc23296e97560f9603451bbf6f0b6349c`

E1 status:

`PASS_R1E1A4A_AR0_B1R_R4_A0_E1_PASSIVE_EM_CHARACTERIZED`

The E1 coupon is a **pattern/dimension donor**, not a literal substrate object to be pasted into E2.

### 2.3 Grounding authority

E2 Pol-A baseline uses:

`G-L0_BRANCH_LOCAL`

Each QPL9547 site owns its own finite branch-local backside RF ground and four plated ground vias (three paddle vias + one C_RF ground via).

Not allowed as E2 baseline:
- D2-M0/M1 remote lower-stalk common-ground merge;
- unsupported copper bridge;
- silent G-L1 local common-ground merge;
- any ground-to-radiator galvanic connection.

The old D2 remote merge remains sentinel/history only.

### 2.4 Four device-plane authority vs raw EM extraction

The earlier A0 pre-simulation plan froze four QPL9547 device-lead reference planes per polarization:

- P1A_IN
- P1A_OUT
- P1B_IN
- P1B_OUT

That **device-plane contract remains authoritative**.

However, a pure CST four-port extraction is **not** sufficient while C_IN / C_OUT / L1 / decoupling / R4 remain circuit-domain elements. If only the four device ports were retained, the physical C_IN gaps would leave the radiator electrically disconnected from P_IN and a claimed source impedance would be meaningless.

Therefore E2 V0.1 refines the implementation:

- external device-reference contract: four immutable QPL9547 lead planes;
- raw CST EM extraction: twelve single-ended auxiliary/device nodes;
- passive component insertion / node reduction: circuit-domain follow-on;
- active QPL9547 insertion: A0-C1.

This supersedes only the old assumption that E2 raw CST itself must be a literal four-port. It does not change the four QPL9547 device reference planes.

## 3. Pol-A pilot geometry scope

### 3.1 Retained full radiator

Retain the accepted complete radiator substrate and radiator copper unchanged, including the orthogonal polarization radiator geometry.

Reason:
the orthogonal radiator metal is part of the physical antenna and contributes real EM loading/coupling even in a Pol-A pilot.

No new ground may touch radiator copper.

### 3.2 Mechanical environment

Retain the accepted orthogonal two-stalk mechanical/dielectric architecture and lower interlock geometry needed to represent the real Pol-A half-lap environment.

For the **inactive Pol-B electrical feed** in the Pol-A pilot:
- retain only the accepted signal-only radiator-to-stalk launch / short pre-LNA stub through the common handoff region;
- do not retain legacy remote-return ground or old passive-fixture RF network;
- do not add Pol-B E1 landing zones in the Pol-A pilot;
- the inactive Pol-B electrical state is therefore an open-stub pilot condition, not final dual-pol active authority.

This is deliberate. E2 Pol-A is an integration pilot, not the final eight-device-plane dual-pol block.

### 3.3 Pol-A upstream handoff

Freeze the Pol-A active-feed handoff plane at:

`v = 3.000 mm`

Per branch:
- retain radiator terminal / RF tenon / signal tongue / upstream signal path through v=3 mm;
- retain no radiator-side ground contact;
- for v >= 3 mm, the E1 landing-zone donor controls the active-region signal/ground geometry.

The E1 donor starts with a 1.90-mm upstream MSL at v=3 mm, matching the architecture seed.

### 3.4 Replace, do not overlay

For Pol-A and v >= 3 mm:
- legacy B0/T1R1 branch MSL geometry that conflicts with the E1 donor is removed/rebuilt;
- legacy T1R1 feed-head backside-ground taper is not overlaid with E1 ground;
- the E1 branch-local G-L0 ground replaces the old first-stage ground representation;
- no duplicate FR4 coupon is created.

The parent stalk FR4 is the only dielectric substrate.

The E1 `FR4_COUPON` solid is therefore **not copied** into E2.

### 3.5 Two E1 cells

Pol-A branch centers remain:

- branch A / “+”: u = +3.000 mm
- branch B / “-”: u = -3.000 mm

Use the E1 branch-local q/v/n dimensions exactly.

For both branches freeze the same local orientation:

`+q -> +u`  
`+v -> downstream`  
`+n -> front/top copper normal`

Transforms:

branch A:
`u = +3.000 mm + q`

branch B:
`u = -3.000 mm + q`

This preserves the frozen “same package rotation, do not mirror package pinout” rule.

Consequence:
the side bias lanes are not exact mirror images in global u. This is intentional baseline geometry and may produce a measurable branch asymmetry. Do not silently mirror the package or side-lane geometry to make the result look more symmetric.

### 3.6 Branch envelopes

Each E1 cell occupies:

`q = -2 .. +2 mm`

Therefore:

branch A active envelope:
`u = +1 .. +5 mm`

branch B active envelope:
`u = -5 .. -1 mm`

Both remain outside the nominal central feed-head slot.

The E1 active-region v span is:

`v = 3 .. 13 mm`

### 3.7 Device placement after transform

Branch A:
- package center u = +3.25 mm, v = 7.00 mm
- RF-IN center u = +3.00 mm, v = 6.085 mm
- RF-OUT center u = +3.00 mm, v = 7.915 mm
- B_VDD line u = +4.45 mm
- B_VBIAS node u = +2.50 mm

Branch B:
- package center u = -2.75 mm, v = 7.00 mm
- RF-IN center u = -3.00 mm, v = 6.085 mm
- RF-OUT center u = -3.00 mm, v = 7.915 mm
- B_VDD line u = -1.55 mm
- B_VBIAS node u = -3.50 mm

No coordinate may move merely to improve a post-build visual or S-parameter result. Any required move is a new placement-contract revision.

### 3.8 Ground / via geometry

Per branch retain E1 G-L0 exactly:
- finite backside local ground over the active-region branch envelope;
- three QPL9547 paddle vias;
- one C_RF dedicated ground via;
- five grounded side-pin spokes / package local-ground geometry;
- no local common bridge between branch-A and branch-B grounds.

Two branches therefore contain:
- 6 paddle vias total;
- 2 C_RF ground vias;
- 8 plated ground vias total.

All eight via holes must be drilled through real parent stalk FR4 before copper barrels are created.

### 3.9 Ground extent boundary

For E2 V0.1, G-L0 remains a **local first-stage ground** and is not extended into the historical D2 remote common-ground network.

Nominal E1 local-ground physical extent remains v=3..13 mm.

A sharp resonance or suspicious coupling associated with the v=13 truncation may trigger a separately frozen ground-extent mechanism sentinel. It does not authorize an in-place redesign.

## 4. Raw twelve-node EM port contract

All raw CST ports are single-ended 50-ohm conductor-interface ports.

Port line rule:
- signal endpoint: local n=0;
- local ground endpoint: local n=-1 mm;
- segment through FR4 only;
- endpoint inside intended copper footprint;
- no port crosses finite-thickness copper.

### Branch A / + ports

1. A_E_UP  
   q=0, u=+3.000, v=4.650

2. A_P_IN  
   q=0, u=+3.000, v=6.085  
   **QPL9547 device RF-IN plane**

3. A_P_OUT  
   q=0, u=+3.000, v=7.915  
   **QPL9547 device RF-OUT/VDD plane**

4. A_E_DN  
   q=0, u=+3.000, v=9.350

5. A_B_VDD  
   q=+1.45, u=+4.450, v=9.800

6. A_B_VBIAS  
   q=-0.50, u=+2.500, v=6.085

### Branch B / - ports

7. B_E_UP  
   q=0, u=-3.000, v=4.650

8. B_P_IN  
   q=0, u=-3.000, v=6.085  
   **QPL9547 device RF-IN plane**

9. B_P_OUT  
   q=0, u=-3.000, v=7.915  
   **QPL9547 device RF-OUT/VDD plane**

10. B_E_DN  
    q=0, u=-3.000, v=9.350

11. B_B_VDD  
    q=+1.45, u=-1.550, v=9.800

12. B_B_VBIAS  
    q=-0.50, u=-3.500, v=6.085

## 5. Frozen four QPL9547 device planes

The device/cosim authority is the subset:

- P1A_IN  = raw port 2 = A_P_IN
- P1A_OUT = raw port 3 = A_P_OUT
- P1B_IN  = raw port 8 = B_P_IN
- P1B_OUT = raw port 9 = B_P_OUT

Here “A/B” denote the two branches **within Pol-A**, not the two antenna polarizations.

QPL9547-A will connect between ports 2 and 3.
QPL9547-B will connect between ports 8 and 9.

No 100-ohm differential device port is created.

## 6. Circuit-domain topology preserved by the 12-node extraction

Branch A:
- C_IN_A: 1 <-> 2
- QPL9547-A: 2 <-> 3
- C_OUT_A: 3 <-> 4
- L1_A: 3 <-> 5
- C_RF_A / bulk: 5 <-> local RF ground
- R4_A: 5 <-> 6

Branch B:
- C_IN_B: 7 <-> 8
- QPL9547-B: 8 <-> 9
- C_OUT_B: 9 <-> 10
- L1_B: 9 <-> 11
- C_RF_B / bulk: 11 <-> local RF ground
- R4_B: 11 <-> 12

E2 raw EM solve inserts **none** of those circuit elements.

Passive component models are inserted only after their provenance is qualified. No ideal component is silently used to collapse the raw network into a four-port product claim.

## 7. Build-only acceptance

E2-PolA build-only must demonstrate:

### Parent preservation
- exact T1R1 parent SHA before transformation;
- accepted radiator substrate/copper preserved exactly;
- no radiator ground contact;
- accepted mechanical/interlock FR4 retained except the eight intentional via holes;
- no D2 remote rails/bridge imported.

### Active-region replacement
- v=3 mm handoff exact;
- two 1.90-mm upstream signal paths connect continuously into the two E1 cells;
- legacy conflicting Pol-A MSL/ground geometry is removed, not overlaid;
- no duplicate E1 substrate;
- exact E1 land/pad/via dimensions for both branches;
- same package rotation on both branches;
- exactly eight plated active-region vias after drill tools are consumed.

### Geometry / interference
- every E1 copper feature lies on the intended parent stalk face;
- no finite copper embedded in FR4 except via barrel walls;
- zero unintended positive-volume signal/ground overlap;
- zero RF-IN/RF-OUT node overlap;
- zero C_IN/C_OUT/L1/C_RF pad-node short;
- zero package/via/slot collision;
- zero active-region collision with orthogonal stalk;
- no branch-local ground crosses the central slot;
- no ground touches radiator copper.

### Ports / persistence
- exactly 12 raw ports after fresh reopen;
- all properties/coordinates exact;
- persistent History List;
- empty result tree;
- solver invocation count = 0;
- artifact hash stable after fresh reopen.

### Human review
Mandatory:
- full radiator + orthogonal mechanical assembly;
- Pol-A feed head from radiator to both LNA sites;
- both package land patterns and side bias lanes;
- all eight via locations relative to real FR4;
- central slot / orthogonal-stalk clearance;
- proof that remote D2 ground merge is absent;
- proof that no E1 coupon substrate was duplicated.

Human PASS is geometry/assembly sanity only, not RF-layout signoff.

## 8. First E2 solve scope

The first E2-PolA solve is characterization only.

Frozen band:
- modeled: 1.0–1.8 GHz;
- decision: 1.15–1.65 GHz;
- explicit references: L5 1.17645 GHz, L2 1.22760 GHz, L1 1.57542 GHz.

Frozen numerical baseline:
- HF Frequency Domain;
- tetrahedral second order;
- adaptive mesh;
- final two native solver DeltaS <= 0.02;
- MaxPasses <= 16;
- open radiation boundaries;
- no optimizer / sweep / geometry tuning;
- one formal solver invocation unless separately re-authorized after HOLD.

Exact solver macro/background spacing is frozen only after the E2 build artifact exists and passes build review.

## 9. Raw 12-port hard solve gates

Hard PASS/HOLD gates:

1. native solver convergence:
   final two native mesh-adaptation DeltaS <= 0.02;

2. complete network:
   all 144 Sij terms exist on one common qualified run and share one native frequency grid;

3. reciprocity:
   max native-grid |Sij-Sji| <= 0.02 over 1.0–1.8 GHz;

4. passivity:
   for every excitation j,
   sum_i |Sij|^2 <= 1.02;

5. native solver integrity:
   no fatal solver failure;
   no mesh corruption;

6. source integrity:
   pre/post solve protected-source hash and configured-copy provenance remain qualified.

No isolated 50-ohm S11 threshold is a hard product gate.

## 10. E2 diagnostic / review metrics

Record, but do not silently convert to pass/fail:

### Same-branch local parasitics
Per branch:
- E_UP <-> P_IN bare C_IN-gap coupling;
- P_IN <-> P_OUT device-bypass coupling;
- P_OUT <-> E_DN bare C_OUT-gap coupling;
- P_OUT <-> B_VDD bare L1-gap coupling;
- B_VBIAS coupling to RF nodes.

### Cross-branch coupling
Track all branch-A to branch-B RF/control-node couplings.

Engineering sentinels:
- unintended coupling > -20 dB in 1.15–1.65 GHz => REVIEW;
- unintended coupling > -10 dB => SEVERE REVIEW.

These are mechanism sentinels, not retroactive hard RF acceptance targets.

### Resonance sentinel
Flag any narrow feature producing:
- >=10 dB change in an unintended coupling trace over <=50 MHz; or
- a sharp passivity-deficit / reflection feature coincident across multiple device/bias nodes.

A resonance sentinel triggers mechanism review before any geometry optimization.

### Branch symmetry
At L5/L2/L1 and over the decision band report:
- A-vs-B corresponding raw S-parameter magnitude/phase differences;
- device-bypass asymmetry;
- C_IN/C_OUT/L1 gap-parasitic asymmetry;
- Vbias/bias-lane coupling asymmetry.

Because the two package side lanes use the same rotation rather than mirror geometry, non-zero asymmetry is expected and must be measured, not edited away.

## 11. Mixed-mode handling

For the two branch input device planes (ports 2 and 8) and separately the two branch output planes (ports 3 and 9), derive mixed-mode quantities mathematically from the single-ended network.

Power-wave transform:

`a_d = (a_A - a_B)/sqrt(2)`

`a_c = (a_A + a_B)/sqrt(2)`

and equivalent for b waves.

Do not create a physical 100-ohm differential LNA port.

Any equivalent 100-ohm differential impedance is derived reporting only, not an optimization target.

## 12. Source-condition boundary

The **raw 12-port EM solve alone does not yet claim QPL9547 source impedance**, because C_IN/C_OUT/L1/bias components remain circuit-domain gaps.

The first authoritative device-plane source/load environment is produced only after:
1. the raw 12-port E2 network is qualified;
2. passive component models are provenance-qualified;
3. those passives are connected in circuit-domain packaging while QPL9547 remains omitted or replaced by device-plane test terminations.

Only then may the four frozen device planes be used to report:
- source reflection / source impedance at each P_IN;
- load reflection / load impedance at each P_OUT;
- mixed-mode input/output environment;
- branch-to-branch passive coupling seen by the device leads.

This avoids repeating the old passive-fixture mistake of assigning product meaning to a disconnected network.

## 13. Pol-A -> Pol-B promotion rule

Pol-B build is **not automatic** merely because Pol-A build exists.

### Clean promotion

Promote the frozen E2 geometry to the Pol-B sentinel only if Pol-A has:

- BUILD PASS + human geometry PASS;
- raw 12-port solve hard-gate PASS;
- no SEVERE coupling sentinel;
- no unresolved resonance sentinel;
- no geometry-specific Pol-A recovery still open.

If additionally no >-20 dB unintended-coupling REVIEW sentinel is present, promotion is direct.

### Review promotion

If Pol-A hard gates PASS but a >-20 dB REVIEW sentinel or a narrow resonance sentinel is present:
- do not redesign immediately;
- freeze a narrow Pol-A mechanism probe first;
- Pol-B remains blocked until the mechanism is classified.

### HOLD

If Pol-A fails a hard numerical/network/geometry gate:
- Pol-B remains blocked;
- attribution/recovery occurs on Pol-A first.

### Pol-B geometry rule

When promoted:
- preserve the exact E2 electrical layout dimensions and package orientation in Pol-B local coordinates;
- apply only the accepted 90-degree polarization transform and the real complementary half-lap mechanical handedness;
- do not retune W_MSL, component placement, via positions, local-ground extent, or package rotation before the A/B comparison.

This makes Pol-B a true mechanical/asymmetry sentinel rather than a separately optimized design.

## 14. What E2-PolA does not claim

E2-PolA is not:
- final dual-pol active source authority;
- final scan-dependent active impedance;
- final LNA noise match;
- final post-LNA load/stability model;
- final shield/bias-return model;
- proof that branch-local grounds can remain unconnected forever;
- proof that Pol-A and Pol-B are equivalent.

A later dual-pol integrated block / array source-condition stage remains required before hardware-release claims.

## 15. Next implementation node

Next local/offline node:

`R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_SOURCE_IMPLEMENTATION`

Required before asking for BUILD authorization:
- source macro/runner;
- exact parent object keep/remove table;
- exact E1-to-PolA geometry transform audit;
- exact expected solid/component/via/port inventory;
- complete-project copy / history-persistence route;
- pairwise + whole-model interference predicates;
- static audit result packet.

## 16. Authorization boundary

`BUILD_AUTHORIZED = false`

`SOLVE_AUTHORIZED = false`

`LNA_INTEGRATION_AUTHORIZED = false`

No NW/XW/251 call is authorized by this freeze.


## 17. Build-source implementation addendum

Status:
`PASS_R4_A0_E2A_POLA_PREBUILD_READY_AWAIT_BUILD_AUTH`

Frozen build source:
`source/cst/R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_ONLY_V01.mcr`

Git blob:
`9931736f1129624d94aee1c9e983a1eaabca5f24`

Frozen build runner:
`scripts/run_r1e1a4a_ar0_b1r_r4_a0_e2a_pola_build_only.py`

Git blob:
`81f717ca5ef7aa4c4375618185aeb1723b0d50f1`

Frozen exact inventory contract:
`execution/R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_INVENTORY_V01.json`

Git blob:
`e10886a4c01d9aafd55a16d8126418b7e22025fd`

Static source accounting:
- parent solids = 45;
- superseded objects deleted = 12;
- final new objects = 74;
- final expected solids = 107;
- temporary drill tools created/consumed = 8;
- plated via barrels retained = 8;
- raw ports = 12;
- registered complete-project pairwise checks = 14.

The macro new-shape name set was parsed and compared against the inventory contract:
- missing = 0;
- extra = 0;
- duplicates = 0.

The macro contains:
- no solver invocation;
- no optimizer/sweep;
- no duplicate FR4 coupon;
- no historical D2 remote lower-ground rail/common bridge;
- no active QPL9547 / Touchstone insertion.

The runner contains zero `run_solver()` calls and requires:
- complete CST parent project copy;
- parent SHA and 45-shape gate;
- persistent History List build;
- exact 107-name / component-count gate;
- exact 12-port property/coordinate gate;
- two Pol-A prong drill-volume checks;
- eight via-volume checks;
- empty result tree;
- fresh-reopen hash stability;
- `CDCheckModelIntersections` command return;
- 14 destructive `Solid.Intersect` checks only on complete temporary project copies;
- human 3D review package.

Parent path is deliberately not guessed in the contract. At an authorized execution, NW must resolve the canonical T1R1 artifact by exact filename + SHA256 and require its same-stem companion directory.

Current authorization remains:
`BUILD_AUTHORIZED = false`
`SOLVE_AUTHORIZED = false`


## 18. E2A-S0L loaded source-side solve amendment

The original first-solve requirement for a full raw 12x12 / 144-term network is superseded by:

`docs/R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_SOLVE_FREEZE_V01.md`

New first-solve authority:
- source excitations: A_E_UP, A_P_IN, B_E_UP, B_P_IN;
- A_P_OUT and B_P_OUT become unexcited matched 50-ohm output loads;
- E_DN / B_VDD / B_VBIAS ports are removed from the solver copy and their physical pads remain open;
- minimum qualified result = 24 complex traces = 6 response rows x 4 source excitations;
- full 12x12 extraction is deferred until arbitrary output/bias-network reconnection, reverse-feedback, active stability or full transistor co-simulation requires it.

The four QPL9547 device planes remain unchanged.

C_IN remains absent from CST, so E2A-S0L alone does not directly claim final QPL9547 source impedance.

This amendment changes solve scope only. It does not change the qualified build geometry.

Activation remains blocked until explicit human 3D review PASS.

BUILD_AUTHORIZED = false  
SOLVE_AUTHORIZED = false
