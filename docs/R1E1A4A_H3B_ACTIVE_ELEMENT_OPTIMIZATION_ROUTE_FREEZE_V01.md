# H3B and Active-Element Optimization Route Freeze V0.1

Status: PROJECT-LEVEL OPTIMIZATION AUTHORITY — FROZEN

Scope: GNSS L-band dual-polarization active array element, 1.15–1.65 GHz, with H3A V0.2 orthogonal-PCB mechanics, radiator-backside first-stage LNA, periodic-array environment, and later post-LNA stalk networks.

## 1. Research conclusion

The project shall use hierarchical modular co-design with system-level closure.

It shall NOT use either extreme:
- SILOED_MODULE_OPTIMIZATION: separately perfect antenna, LNA, interconnect and support, then connect only at the end.
- MONOLITHIC_GLOBAL_OPTIMIZATION_FROM_DAY_ONE: expose all mechanical, EM, circuit, matching and array parameters to one optimizer before the submodels are validated.

Accepted method:
validate modules -> optimize local variables -> export physical interface models -> co-simulate coupled modules -> expose only a small set of cross-domain variables -> close the loop on system sensitivity over frequency and scan.

## 2. Objective hierarchy

### Tier 0 — hard constraints
- manufacturable geometry and assembly;
- CST geometry-intersection gate;
- proven stability over the required source/load domain;
- no destructive/common-mode resonance in the operating band;
- polarization topology preserved;
- mechanical/serviceability constraints;
- frozen scientific gates cannot be silently relaxed.

### Tier 1 — final system objective
The final objective is robust receiving sensitivity, represented by A_eff/T_sys or equivalently G/T.

Core domain:
- frequency 1.15–1.65 GHz;
- scan 0–60 degrees;
- both required scan-azimuth families and both linear polarizations.

Extended 60–75 degree scan is a diagnostic/sentinel domain and does not initially dominate the core objective.

The objective must emphasize worst-case / lower-tail core performance, not only the mean.

### Tier 2 — system contributors
When full G/T is not yet available, use:
- receiver noise temperature or source-conditioned NF;
- radiation efficiency / realized receive gain;
- active impedance under scan;
- branch amplitude/phase symmetry;
- polarization isolation / cross-pol response;
- passband gain and stability.

### Tier 3 — local proxy metrics
S11, insertion loss, 50-ohm return loss, line impedance and isolated coupon metrics are local engineering proxies only. They may optimize a module but may not overrule Tier-1/2 system performance.

## 3. 50-ohm policy

- Antenna -> first-stage LNA: do NOT force 50 ohms. Optimize the source impedance seen by the LNA against noise, gain and stability.
- Post-LNA interconnect / measurement / service interfaces: 50-ohm-class reference planes are preferred for testability and because first-stage gain has already reduced NF sensitivity to downstream loss.

## 4. Active-impedance policy

The final authoritative LNA source condition is scan-dependent active/embedded array impedance, not isolated-element passive S11.

Required closure loop:
array EM -> source impedance into LNA -> LNA loading/noise -> back-annotated array EM -> system sensitivity.

Broadside/isolated impedance is only an early model. Z_active(f, theta, phi, pol) becomes mandatory before final active-front-end optimization.

## 5. Module partition and reference planes

### M0 — radiator + H3A mechanics + local hub EM
Contains radiator copper, FR4 bridges/mortises, stalk dielectrics, local ground/shield, backplane and array boundary environment.
Exports active/embedded impedances, patterns, losses and coupling data.

### M1 — first-stage LNA
Contains active device/package/bias/input network that materially affects the antenna source plane.
Exports S-parameters, noise parameters, stability, gain and impedances.

### M2 — H3B post-LNA orthogonal transition
Contains radiator-backside output line, horizontal-to-vertical PCB transition, solder/edge-plating geometry and first controlled stalk line.
Reference planes:
- RP1: first-stage LNA output / horizontal-board side;
- RP2: qualified vertical-stalk line after the transition.

### M3 — stalk downstream RF network
May later contain branch routing, bias injection, filtering, second gain, differential-to-single-ended conversion and service connector.

### M4 — periodic / finite array environment
Provides scan-dependent mutual coupling and active impedance. M4 is the authority for final source conditions.

## 6. Variable ownership

### Class A — hard-frozen mechanical/manufacturing variables
Examples after H3A acceptance: stalk orientation, tenon/mortise topology, basic assembly sequence, electronics-cavity topology, orthogonal-stalk architecture.
These are not optimizer variables unless architecture is formally reopened.

### Class B — module-local variables
Examples: H3B GCPW width/gap, transition pads, edge plating/castellation, solder geometry within manufacturing bounds, downstream line widths, local matching component values.
Optimize locally, tolerance-check, then temporarily freeze.

### Class C — cross-domain co-design variables
A deliberately small set remains available for later system closure:
- selected radiator feed-region dimensions controlling source impedance;
- local backside ground/shield dimensions;
- first-stage LNA input/noise-match network parameters;
- selected stalk RF-ground bond/jumper state;
- limited array/pitch/material variables when their stage is reached.

The global optimizer is forbidden from opening all Class A/B variables simultaneously.

## 7. Frozen optimization sequence

### H3B-T01 — post-LNA 90-degree transition coupon
Purpose: qualify one physical horizontal-to-vertical PCB transition independently of antenna/LNA source matching.
Sequence:
1. Freeze coupon geometry and RP1/RP2.
2. BUILD-ONLY + CST intersection gate.
3. Passive solve over at least 1.0–2.0 GHz; 1.15–1.65 GHz is the decision band.
4. Optimize only M2-local variables.
5. Verify S-parameters, loss, no sharp resonance, surface/current-return behavior and tolerance sensitivity.
6. Freeze the transition as an EM N-port / geometry revision.

No antenna geometry or LNA input match may be tuned to rescue a bad T01 transition.

### H3B-I01 — integrate qualified transition into H3A passive element
Purpose: establish the passive penalty of the real mechanical/RF architecture.
Evaluate impedance/active-impedance change, radiation efficiency/pattern/polarization, common-mode/stalk current resonances and branch symmetry.
Do not yet optimize a real active device.

### H3C-LNA0 — first-stage LNA/noise model qualification (may proceed in parallel after H3B-I01)
Required data: S-parameters, noise parameters vs frequency, bias assumptions, stability and source-impedance sensitivity/source-pull where available.
QPL9547 remains a reference candidate, not final authority.

### H3C-C01 — antenna/LNA circuit co-design
Use real M0/M4 source-impedance sets and the M1 active model.
Primary variables: first-stage input/noise-match network plus explicitly released Class-C feed/local-ground variables.
Objectives: minimize robust receiver-noise penalty across core frequency/scan while maintaining gain and stability and avoiding narrow high-Q solutions.

### H3C-EMBACK — self-consistent EM/circuit closure
Back-annotate optimized LNA input reflection/loading into the EM/array model, recompute active impedance/pattern/coupling, and iterate with H3C-C01 until source/load conditions converge within frozen thresholds.

### SYSOPT-1 — limited robust system optimization
Expose only a small Class-C vector.
Final objective: maximize robust core-domain A_eff/T_sys or G/T subject to hard constraints.
Use weighted/worst-case multi-condition objectives, surrogate/interpolated EM data where appropriate, and periodic high-fidelity CST + circuit verification.

### SYSVERIFY — full integrated verification
Freeze geometry/circuit values, then verify frequency, scan, both polarizations, stability, noise, gain, radiation/polarization, tolerances, material/bond states and geometry integrity.

## 8. Rollback rules

- Bad transition cannot be hidden by antenna/LNA retuning: return to H3B-T01.
- LNA instability over realistic source/load domain: return to LNA design.
- Active impedance lies far from usable LNA noise region over much of scan: reopen only limited Class-C antenna/local-ground variables.
- Passive pre-LNA loss dominates NF: shorten/remove that passive structure before adding matching.
- Mechanically marginal global optimum: reject it; do not relax mechanical gates.

## 9. Tolerance / robustness policy

At module freeze, evaluate dominant tolerances: PCB epsilon/thickness, trace/gap etch, solder volume, board alignment, component/package parasitics and LNA model/noise uncertainty.
Prefer a broad robust basin over a sharper nominal optimum when system performance is comparable.

## 10. Tool partition

- CST: radiator, stalk mechanics, transitions, local ground/shield, periodic/finite-array EM, fields/currents.
- ADS/Sonnet/circuit environment: active device, noise/gain/stability, matching and circuit optimization.
- Python orchestration: data contracts, objective aggregation, provenance and routing.

Preferred bridge: physical reference planes + Touchstone/N-port/noise-parameter data.
Do not repeatedly rebuild a monolithic full-wave active model for every circuit-variable iteration when a validated EM block is sufficient.

## 11. Immediate next node

H3B_T01_POST_LNA_ORTHOGONAL_TRANSITION_COUPON_FREEZE

T01 may optimize the post-LNA 90-degree transition only. It shall not tune radiator geometry, LNA input matching, balun/combiner, filter, final connector or array pitch.

No BUILD or SOLVE authorization is implied by this route freeze.

## 12. Literature basis

- Sharawi et al., Miniaturised active integrated antennas: a co-design approach, IET MAP, 2016, DOI 10.1049/iet-map.2015.0588.
- Maaskant & Woestenburg, Applying the active antenna impedance to achieve noise match in receiving array antennas, IEEE APS 2007, DOI 10.1109/APS.2007.4396892.
- Warnick et al., Design and Characterization of an Active Impedance Matched Low-Noise Phased Array Feed, IEEE TAP 59(6), 2011, DOI 10.1109/TAP.2011.2122223.
- de Lera Acedo et al., SKALA/SKA-Low active-antenna work: system sensitivity and LNA noise match are coupled design drivers.
- Alekseev et al., Q-Band LNA-Antenna Co-Design: Exploiting Antenna Matching for System Noise Figure Optimization, IEEE Journal of Microwaves, 2025, DOI 10.1109/JMW.2025.3588491.