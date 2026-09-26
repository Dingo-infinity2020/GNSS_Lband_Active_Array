# H3B-T01A to Active-Array Co-Design Master Plan V0.1

Status: PROJECT EXECUTION ROUTE — FROZEN / NO BUILD OR SOLVE AUTHORIZATION

SimulationOps minimum: 0.2.8

## 0. Post-O2B route amendment — authoritative

The post-O2B route is frozen by `docs/R1E1A4A_POST_O2B_ROUTE_FREEZE_V02.md`.
O2C nominal tuning is DEFERRED_CONTINGENCY_ONLY. The active mainline is O3 physical-fidelity verification → minimal O4 manufacturing sentinels → T01-A FREEZE → H3B Complete Passive Unit / H3B-I01 → LNA-on-stalk A0 → realistic periodic array → R1E2 active-impedance atlas → A1 final co-design → finite active array.

## 0A. H3B Complete Passive Unit amendment — authoritative

After T01-A freeze, H3B follows `docs/R1E1A4A_H3B_COMPLETE_PASSIVE_ROUTE_FREEZE_V01.md`.

Frozen route:
H3B-C0 build-only A/B sources → human 3D review → H3B-I01 six-state A/B passive pilot → Passive Unit V1 freeze → LNA-on-stalk A0.

Key integration rules:
- H3A visual-surrogate LNA/route/service solids are keepout predicates only and are excluded from formal EM.
- schematic H3A RFTransition/RFSolder/StalkRF placeholders are removed.
- four local T01-A integration slices use quadrant-specific stalk faces and 3-mm handoff planes.
- coupon long fixture lines/FR4 boards are not copied into the product model.
- ordinary microstrip remains the intended A0 product-mainline direction; local T01-A GCPW is not promoted into the whole post-LNA route.
- H3B does not optimize antenna-to-LNA matching.

## 0B. AR0 active-feed architecture fork — authoritative

The H3B-C0 grounded-T01 antenna integration is closed as architecture evidence after `HOLD_R1E1A4A_H3B_C0_GEOMETRY_OVERLAP`.

First-priority architecture is now:
`AR0-B0_STALK_TOP_TWIN_MSL_TWIN_LNA`

Authority:
- `docs/R1E1A4A_AR0_B0_STALK_TOP_TWIN_MSL_ARCHITECTURE_FREEZE_V01.md`
- `execution/R1E1A4A_AR0_B0_ARCHITECTURE_MANIFEST_V01.json`

Key change:
balanced radiator terminals connect only to signal tongues. Ground belongs to the stalk, begins below a frozen setback, and never becomes radiator copper. T01-A is retained only for possible post-LNA grounded-board use.

Architecture A (radiator-board electronics island) is deferred, not rejected.

## 1. Current proven state

H3A V0.2 mechanics are accepted. H3B-T01A GCPW 90-degree transition BUILD is accepted, and its maxpass16 numerical recovery converged at adaptive pass 12.

Protected T01-A solved SHA256:
928400031803e62665df0a17890b2158b8d56b2673e9af1a9e0c7a7d171266df

Qualified core-band baseline:
- S11/S22 approximately -15.37 to -9.77 dB;
- S21/S12 approximately -0.240 to -0.639 dB;
- no sharp destructive notch;
- reciprocity consistent.

Important: RP1-to-RP2 S21 contains straight FR4 GCPW loss plus the 90-degree junction. It is not junction-only insertion loss.

## 2. Immediate objective

Do not jump directly to H3B-I01. First close T01-A as a reusable local RF module:
1. separate straight-line mismatch/loss from junction behavior;
2. optimize only T01-A Class-B local variables;
3. re-qualify the winner at full numerical fidelity;
4. run a small manufacturing-tolerance sentinel set;
5. freeze geometry + RP1/RP2 + Touchstone N-port.

T01-C remains deferred.

## 3. T01A-O0 — straight reference-line calibration

Build a straight GCPW reference coupon using the same FR4, Wsig/gap/ground rails, backing ground, via fence and equivalent RP spacing.

Purpose:
- estimate line mismatch and line attenuation;
- separate line contribution from 90-degree junction excess loss;
- avoid optimizing the junction to compensate for a poorly chosen line impedance.

O0 is a reference calibration, not an alternative topology.

## 4. T01A-O1 — line cross-section optimization

Released variables only:
- Wsig;
- Gcpw.

Initial bounded screening domain:
- Wsig = 1.5 / 1.8 / 2.1 mm;
- Gcpw = 0.20 / 0.30 / 0.40 mm.

Do not automatically run all 9 cases at full fidelity. Prefer low-cost screening, select 2–3 finalists, then high-fidelity qualification.

Winner criterion is worst-case core-band match + manufacturability + tolerance robustness, not best single-frequency S11.

## 5. T01A-O2 — 90-degree junction optimization

Freeze the O1 line cross-section first.

Released variables only:
- transition signal-pad width;
- transition pad gap;
- transition pad length;
- ground-pad dimensions if needed;
- first via-to-junction distance;
- solder-envelope size within manufacturing limits.

Keep board geometry, edge/castellation concept, antenna geometry, H3A mechanics, array pitch, LNA input matching, downstream filter/balun/connector and T01-C frozen.

Use a compact DOE of roughly 8–12 screening candidates, then 2–3 refined candidates.

## 6. T01A-O3 — full-fidelity winner qualification

Before the sweep, freeze these local targets:
- preferred worst-case return loss at both ports >= 15 dB across 1.15–1.65 GHz;
- minimum acceptable freeze target >= 12 dB across the core band;
- junction excess loss versus straight reference: preferred <= 0.10 dB, acceptable <= 0.15 dB;
- no S21 notch below -3 dB;
- reciprocity difference <= 0.05 dB.

Final candidate requires fresh-run provenance, geometry/intersection recheck if rebuilt, second-order tetrahedral adaptive convergence with two final DeltaS values <= 0.02, and the full 1.0–2.0 GHz result.

Screening may retain PEC conductors to isolate impedance/topology behavior, but final O3 qualification must add a frozen finite-conductivity copper model and a physically explicit solder-conductor assumption before claiming physical insertion loss.

Final O3 also requires a port-model sentinel: either straight-reference de-embedding with identical RP1/RP2 discrete ports or an equivalent waveguide-port/line-fixture cross-check, so that the selected transition is not an artifact of the discrete-port excitation.

If no candidate meets the acceptable target without poor manufacturability/tolerance, HOLD. Do not open T01-C automatically.

## 7. T01A-O4 — tolerance sentinels

Before T01-A freeze, check a small deterministic set:
- Wsig +/-0.10 mm;
- Gcpw +/-0.05 mm;
- board-to-board lateral alignment +/-0.20 mm;
- solder envelope small / nominal / large.

This is not Monte Carlo. The goal is to reject a sharp nominal optimum.

## 8. T01A-FREEZE

Freeze:
- geometry hash;
- RP1/RP2;
- converged Touchstone 2-port;
- straight-line reference result;
- junction excess-loss report;
- tolerance sentinel report;
- manufacturing dimensions.

Only then is T01-A a reusable M2 module.

## 9. H3B-I01 — integrated passive pilot

Insert qualified T01-A into accepted H3A V0.2 at P094 only.

First pilot conditions:
- broadside;
- C60P45;
- C60P135.

Questions:
1. Does the physical stalk/transition move antenna active impedance materially?
2. Does it create common-mode/stalk resonance?
3. Does it materially change efficiency/pattern/polarization?
4. Are branch pairs sufficiently symmetric?

If this fails, return to H3B physical integration. Do not compensate with LNA matching.

## 10. Re-enter array mainline

After H3B-I01:
- R1E1B: support/hub-inclusive pitch/material trade;
- R1E2: authoritative scan-dependent active-impedance atlas.

The earlier bare-source pitch work remains useful infrastructure, but the final pitch/material decision must use the real H3A/H3B architecture.

## 11. LNA sequencing

H3C-LNA0 device/model qualification may proceed in parallel when separately authorized: S/noise parameters, bias, stability, source-pull/noise sensitivity and package model.

H3C-C01 final antenna/LNA co-design is blocked until R1E2 exists. Do not freeze final input matching from broadside or isolated-element impedance.

After R1E2, H3C-C01 uses the active-impedance cloud; H3C-EMBACK then iterates EM <-> circuit until source/load conditions are self-consistent.

## 12. System closure

After H3C convergence:
- SYSOPT-1: limited Class-C robust optimization against A_eff/T_sys or G/T;
- SYSVERIFY: frequency x scan x polarization x noise x stability x radiation x tolerances x manufacturing;
- finite-array center/edge/corner validation remains mandatory.

## 13. Host routing

- NW: build-only, T01 reference/coupon work, lightweight explicitly authorized screening;
- CST251-C: heavy integrated periodic, pitch/material and finite-array production solves;
- XW: auxiliary Windows/Sonnet/circuit role when explicitly required.

Do not let heavy R1E1B/R1E2 work drift onto NW by inertia.

## 14. SimulationOps 0.2.8 optimization contract

Before any sweep/DOE, freeze:
- converged baseline;
- released variables and ranges;
- fixed variables;
- objective and hard constraints;
- screening fidelity;
- qualification fidelity;
- sample plan;
- winner rule;
- tolerance sentinels;
- stop boundary.

After results are visible, do not change thresholds, enlarge the variable set to rescue a candidate, or promote screening results directly to final PASS.

Every final winner requires fresh-run qualification and no-silent-retry semantics.

## 15. Immediate next execution node

R1E1A4A_AR0_B0G_FEED_HEAD_BUILD_ONLY_AWAIT_AUTH

Authority:
- docs/R1E1A4A_AR0_B0_STALK_TOP_TWIN_MSL_ARCHITECTURE_FREEZE_V01.md
- docs/R1E1A4A_AR0_B0G_FEED_HEAD_BUILD_ONLY_PLAN_V01.md
- execution/R1E1A4A_AR0_B0_ARCHITECTURE_MANIFEST_V01.json

No BUILD or SOLVE authorization is currently open.
