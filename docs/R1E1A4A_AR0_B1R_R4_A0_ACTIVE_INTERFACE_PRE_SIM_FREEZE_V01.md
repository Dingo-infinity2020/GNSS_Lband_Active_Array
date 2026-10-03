# AR0-B1R-R4-A0 Active-Interface Pre-Simulation Freeze V0.1

Status: DESIGN FREEZE COMPLETE — NO REMOTE BUILD / NO SOLVE AUTHORIZATION
SimulationOps minimum: 0.2.8

## 1. Mainline correction

The project is no longer authorized to spend the mainline on explaining passive-fixture S11 differences such as the D1R1 local-closure ~-5.7 dB result versus the M1 remote-return ~-0.3 dB result.

Reason:
the passive fixtures do not contain the final continuous active signal chain.
They terminate / interrupt the signal path at artificial ports while allowing downstream ground structures to continue.

Those results remain valid for:
- geometry-integrity evidence;
- proof that ground topology matters electromagnetically;
- proof that remote return geometry can strongly load the passive fixture;
- qualitative A/B mechanical-asymmetry evidence.

They are NOT product input-match authority.

The proposed `D2-M2_RETURN_PATH_FIXTURE_MECHANISM_PROBE` is DEFERRED as a contingency, not the mainline.

## 2. Architecture-B active baseline

Retain:
`AR0-B0_STALK_TOP_TWIN_MSL_TWIN_LNA`

For each polarization:
balanced antenna terminal pair
-> two independent pre-LNA signal branches
-> two single-ended QPL9547-class first-stage LNAs
-> post-LNA single-ended branches
-> later combining / polarization-processing network.

No passive balun or combiner is inserted before first gain.

For the dual-pol element:
4 first-stage LNAs total.

QPL9547 is G0 reference only.

## 3. Electrical continuity rule

Any future RF-qualification model must contain an explicit connectivity graph.

A product-representative active branch is:

antenna terminal
-> RF solder tenon / tongue
-> continuous pre-LNA transmission line
-> mandatory input DC-block element
-> QPL9547 RF-IN device-lead plane
-> active QPL9547 two-port
-> QPL9547 RF-OUT/VDD device-lead plane
-> mandatory output DC-block / bias-feed network
-> continuous post-LNA route
-> defined load / downstream reference plane.

A passive CST model with the signal trace simply ending while the ground continues may be used only as a labeled mechanism probe.
It may not be promoted to product S11 authority.

## 4. EM / circuit partition

The active transistor remains OUTSIDE CST.

CST owns physical passive geometry:
- radiator;
- RF tenon / solder region;
- pre-LNA signal trace;
- local ground-acquisition geometry;
- exact QPL9547 PCB land pattern;
- backside-paddle ground region and vias;
- AC-block / bias-component pads;
- post-LNA trace;
- structural stalk / orthogonal-board mechanics;
- shield / grounded wall when later frozen;
- parasitic input-output coupling through the physical assembly.

Circuit/noise environment owns:
- QPL9547 S2P;
- QPL9547 noise parameters;
- ideal or vendor component models for DC blocks / bias choke / decoupling;
- source/load terminations;
- gain / NF / stability analysis.

## 5. Device-lead reference planes

QPL9547 Rev-D S/noise data are referenced on device leads.

Therefore the co-simulation interface shall use device-lead planes rather than arbitrary 50-ohm line planes.

For one polarization define four single-ended RF planes:
- P1A_IN: branch-A RF-IN device lead to local RF ground;
- P1A_OUT: branch-A RF-OUT device lead to local RF ground;
- P1B_IN: branch-B RF-IN device lead to local RF ground;
- P1B_OUT: branch-B RF-OUT device lead to local RF ground.

Circuit layer inserts:
QPL9547-A S2P between P1A_IN and P1A_OUT;
QPL9547-B S2P between P1B_IN and P1B_OUT.

For dual polarization the complete passive EM block may later expose 8 RF planes.

Do not force a 100-ohm differential port at the LNA interface.

Mixed-mode quantities are derived from the single-ended matrix.

## 6. Local-ground policy

The prior Architecture-B rule "no common ground in the feed/LNA head" is superseded for the active-device region.

New hard rule:
each QPL9547 backside paddle must see a physically short local ground path using package-region ground copper and vias.

Remote lower-stalk-only ground closure is prohibited as the first-stage grounding baseline.

Still frozen:
- no stalk ground galvanically contacts radiator copper;
- radiator terminal has exactly one intended signal connection;
- ground belongs to the stalk / active electronics, not to the radiator arm.

Released A1 design variable:
whether the two twin-LNA local ground cells merge immediately into one local island or remain two tightly controlled cells for a short distance before merging.

This variable shall be decided by EM + stability evidence, not by visual preference.

## 7. Package / landing-zone seed

QPL9547 G0:
- 2 x 2 mm DFN;
- backside exposed paddle nominal 0.8 x 1.6 mm;
- 0.5-mm terminal pitch;
- package paddle requires short RF/DC ground connection and ground vias.

Datasheet via reference:
- 0.35-mm drill bit;
- 0.25-mm final plated-through diameter.

Current B0 LNA-envelope centers near local u=+/-3 mm, v~7 mm are retained only as a placement seed.

They are NOT final package-center authority.

Exact device orientation must:
- minimize antenna-terminal-to-RF-IN electrical length;
- leave input/output routing physically separable;
- permit paddle vias and local decoupling;
- preserve branch symmetry as far as mechanics allow;
- avoid the interlock / tenon keepouts.

## 8. DC-block / bias model

Mandatory:
- series input DC block before RF IN;
- series output DC block after RF OUT;
- VDD injection at RF OUT through the bias network;
- Vbias/current-setting network;
- local RF decoupling to the package ground.

G0 circuit reference starts from the QPL9547EVB-01:
- input/output 100-pF reference DC blocks;
- 18-nH reference RF choke;
- 3.32-kOhm reference current-setting resistor;
- 100-pF + 1-uF-class decoupling references.

These are topology/reference seeds only.
Do not freeze them as final stalk BOM yet.

Pads, microstrip transitions and vias are EM objects.
Ideal/component electrical behavior is circuit-domain until a vendor broadband model is selected.

## 9. Three-level validation route

### A0-C0 — circuit-only G0 sanity

No CST required.

Use the existing QPL9547 S/noise references to reproduce:
- datasheet-like 50-ohm gain / input-output match trend;
- NFmin / noise-parameter interpolation;
- K / mu / mu-prime / Delta;
- source-conditioned NF for arbitrary complex source impedance;
- transducer / available-gain calculation.

Then instantiate two identical QPL9547 branches for one polarization.

Do NOT use `Zbranch = Zdiff/2` as an authority assumption.

A0-C0 proves the circuit math/import chain only.

### A0-E1 — one-LNA landing-zone EM coupon

First remote/CST stage after a separate authorization.

Purpose:
qualify the physical device landing zone before attaching the radiator.

Include:
- exact package land pattern;
- local ground island;
- paddle-via cluster;
- RF-IN/RF-OUT pad launches;
- input/output DC-block pads;
- bias-choke / decoupling pads and ground vias;
- short controlled input/output line sections;
- stalk dielectric and nearby mechanical keepouts.

Active device omitted and replaced by device-lead reference planes.

Question:
does the local landing-zone create a sane, low-loss, non-resonant passive environment and a physically credible RF ground?

### A0-E2 — integrated antenna + landing-zone EM block

Attach the accepted radiator / tenon / stalk feed to the qualified landing zone.

For one polarization export the 4-port single-ended passive EM block:
P1A_IN / P1A_OUT / P1B_IN / P1B_OUT.

The antenna/radiation system is part of the passive EM block.

Then connect the two QPL9547 S2Ps in circuit co-simulation.

Pol-A pilot first.
Pol-B becomes an explicit sentinel because the half-lap mechanics are not perfectly C4 symmetric.

### A0-C1 — active co-simulation

For each frequency / scan state calculate:
- branch source impedance;
- source-conditioned noise factor / equivalent noise temperature;
- transducer gain;
- branch gain/phase balance;
- differential/common-mode conversion;
- input/output match as diagnostics;
- source/load stability.

### A0-STAB — assembled feedback stability

Before hardware release extend the EM block to include the physical output route, shield, bias return and other output-to-input coupling paths that can create feedback.

A standalone QPL9547 K/mu PASS does not satisfy this gate.

## 10. Frequency policy

Science decision band:
1.15–1.65 GHz.

Initial local/integrated EM:
1.0–1.8 GHz.

Circuit gain/noise:
at minimum 1.0–1.8 GHz, with L5/L2/L1 explicitly sampled.

Stability:
wideband using the available valid S2P span.
For the current extended TRL reference, below ~0.6 GHz is sentinel-only.
Later hardware-release authority requires a production-quality wideband model.

## 11. Metrics and objective hierarchy

Primary active metrics:
- source-conditioned NF / Te;
- transducer gain;
- stability;
- pre-LNA passive loss;
- branch amplitude/phase balance;
- mixed-mode conversion;
- robustness over GNSS frequency and later scan-dependent source impedance.

Secondary diagnostics:
- S11;
- isolated 50-ohm return loss;
- local line impedance.

Do NOT optimize the product to 100+j0 ohm merely because the passive fixture used a 100-ohm differential reference.

Existing Gate-R receiver budgets remain the starting acceptance authority:
- device/source-conditioned NF shadow target <=0.40 dB;
- nominal integrated first-stage estimate <=0.45 dB;
- pre-LNA passive loss target <=0.05 dB;
- nominal Sdc / Scd target <= -30 dB;
- branch magnitude imbalance <=0.20 dB;
- odd-mode phase imbalance <=2 deg.

These thresholds are not relaxed by the D1/M1 passive-fixture results.

## 12. Array / source-condition closure

Final first-stage matching is still blocked from being frozen solely from an isolated-element result.

The eventual authority remains scan-dependent active / embedded array source conditions.

The active chain may be developed now in parallel using:
- ideal source sweeps;
- existing isolated / periodic source impedances;
- later R1E2 active-impedance clouds.

The design shall avoid a narrow high-Q match to one broadside source point.

## 13. Superseded / retained historical authority

Superseded for Architecture-B active mainline:
- H0 backside-radiator-board electronics-island geometry as default;
- the rule that no local common ground may exist near the first-stage LNA;
- passive M2 fixture S11 as product-match authority.

Retained:
- the reference-plane/cosim principle in `R1E1A4A_REFERENCE_PLANE_AND_COSIM_SPEC.md`;
- Gate-R receiver/noise/stability budgets;
- existing QPL9547 S/noise provenance;
- D1/M1 as diagnostic evidence;
- Architecture-B mechanical stalk / RF-tenon concept;
- local-ground-to-radiator galvanic isolation.

Architecture A remains a deferred sentinel, not rejected.

## 14. Open items before A0-E1 BUILD

Must be resolved without guessing:
1. machine-transcribe / audit Rev-D recommended PCB land pattern;
2. choose initial package orientation for + and - branches;
3. define initial local-ground island(s);
4. define paddle-via count and placement using vendor/manufacturing constraints;
5. choose G0 DC-block / choke / decoupling component models;
6. define exact input/output line handoff distances around the package;
7. define shield keepout but do not necessarily build the shield in E1;
8. freeze A0-E1 port coordinates and conductor endpoints;
9. freeze interference predicates and manufacturability clearances.

## 15. Current stop boundary

This document authorizes design/provenance work only.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
LNA_INTEGRATION_AUTHORIZED = false

Next execution node:
R1E1A4A_AR0_B1R_R4_A0_C0_CIRCUIT_REFERENCE_AND_A0_E1_LANDING_ZONE_FREEZE

Do not call NW/XW/251 until the A0-E1 geometry / port / footprint contract is frozen.
