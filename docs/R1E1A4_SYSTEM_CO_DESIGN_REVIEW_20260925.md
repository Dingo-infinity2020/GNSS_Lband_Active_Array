# R1E1A4 System Co-Design Review — Mechanical Support + Active Frontend

Status: DESIGN / LITERATURE REVIEW ONLY — NO BUILD OR SOLVER AUTHORIZATION

## Why the stage is being reframed

R1E1A3 proved that the current four-post bonded low-density-foam assembly is not electromagnetically transparent under the project's pre-frozen 10-ohm Delta-Z criterion at C60P135. That result remains valid and is not reclassified.

However, "not transparent" is not equivalent to "unusable in the final active antenna."

The final element contains:
- mechanical support;
- balanced feed transition;
- local active-hub PCB;
- local ground / RF shield;
- two first-stage LNA branches per polarization in the balanced mainline;
- scan-dependent mutual coupling.

These objects jointly determine the source impedance presented to the first-stage LNAs. Therefore the production architecture must ultimately be judged by receiver noise, stability, loss, scan behavior and manufacturability rather than by support-only Delta-Z.

R1E1A4 is therefore elevated from a support-only diagnostic into a mechanical / receiver-interface co-design stage.

## Literature review — mechanical support

The literature check does NOT support a claim that low-density microwave foam is an exotic or invalid antenna material.

Examples found:
- Rohacell is used as a structural spacer in multilayer antennas and arrays; a 2025 Sensors CubeSat antenna explicitly describes Rohacell spacers as providing structural integrity while behaving nearly like air.
- A 2021 IET MIMO SIW array bonded flexible copper/polyimide layers to Rohacell 51 IG-F using thin 3M VHB adhesive.
- A 2021/2022 X-band SAR planar array used Rohacell between dielectric boards with adhesive films as the bonding agent.
- TCDA / array structural concepts also exist with low-dielectric foam or resin as non-conductive mechanical support.

The important nuance is packaging form:
foam is commonly used as a continuous spacer, sandwich core, sheet or filled support volume. The project's present architecture — four discrete 4x4-mm foam posts with local adhesive pads beneath a large suspended PCB — is much less representative of the mainstream examples reviewed.

Therefore S1 remains a useful low-dielectric EM reference, but it should no longer be assumed to be the most likely production mechanical architecture.

## Architecture decomposition for the next design phase

The active hub and the mechanical carrier are no longer treated as competing alternatives.

H0 is the mandatory source-facing receiver interface: a centered backside active-hub/local-ground architecture.
The support design then chooses one carrier family from H0/radiator to the main backplane.

### C0 — bonded low-density foam reference
Role:
- lowest-permittivity support reference;
- attribution / physics diagnostic;
- possible hardware path only if bonding, creep and serviceability are acceptable.

Do not discard it merely because it is less conventional.

### C1 — serviceable dielectric tube / standoff
Representative family:
- PTFE-class or other characterized low-loss engineering dielectric standoff;
- mechanically repeatable geometry;
- preferably non-conductive fastener above the ground plane;
- any metal nut/retainer kept behind the continuous backplane where practical.

This family is more conventional mechanically, but its dielectric constant is materially higher than low-density foam and it is not assumed EM-transparent.

### C2 — structural PCB / printed frame
Use one or more symmetric PCB ribs / printed frame pieces for support and registration only where they provide a clear assembly or routing advantage.

The H0 active hub remains source-facing and mandatory; S2 is the mechanical carrier beneath it, not a replacement for H0.

FR4 or another PCB laminate is not treated as invisible; any copper on the structural frame is an RF object.

### C3 — grounded metal support / tube / post
A metal support above the ground plane is an RF element, not a neutral fastener.

It may still become a valid architecture if intentionally used as:
- a shorting / common-mode-control element;
- shield wall;
- feed return / structural ground;
- mechanically integrated RF feature.

It is not evaluated as a transparent-support candidate.

## LNA / antenna co-design evidence

The receiver literature supports bringing the LNA source environment into the design earlier than a final hardware-integration stage.

Relevant evidence:
- Warnick et al. (IEEE TAP, 2011) designed an L-band radio-astronomy phased-array feed around an active-impedance matching condition.
- Maaskant et al. (APS 2007) explicitly identify active rather than passive antenna impedance as the relevant quantity for low-noise matching in receiving arrays.
- Alekseev et al. (IEEE Journal of Microwaves, 2025) demonstrate antenna/LNA co-design in which the antenna participates in the LNA noise match rather than forcing a conventional 50-ohm interface.
- Da Costa, Lau & Vanderlinde (arXiv:2607.21715, 2026) report a low-cost differential radio-astronomy LNA with approximately 0.3-dB NF when matched to a constant 130-ohm source and feed-coupled system noise as low as about 25 K.

This is highly relevant because the project's CHARTS-inspired architecture also uses a balanced antenna output feeding a pair of first-stage LNAs.

## QPL9547 preliminary receiver-shadow context

QPL9547 remains a reference device, not a selected final LNA.

The manufacturer's Rev-D noise-parameter table provides NFmin, GammaOpt and Rn through the project band.

Representative 50-ohm single-ended GammaOpt-to-Zopt conversions are approximately:
- 1.1 GHz: 63.5 + j14.0 ohm;
- 1.2 GHz: 62.7 + j11.3 ohm;
- 1.3 GHz: 62.2 + j11.7 ohm;
- 1.4 GHz: 56.3 + j14.8 ohm;
- 1.6 GHz: 54.9 + j12.8 ohm;
- 1.7 GHz: 50.8 + j13.2 ohm.

If — and only if — the future balanced topology presents two symmetric single-ended LNA source impedances with a virtual-ground symmetry plane, twice these values would correspond to an illustrative differential optimum near roughly 102–127 + j23–30 ohm across these anchors.

That "2 x Zopt" relation is NOT yet an architecture fact. The exact differential-to-per-device reference-plane mapping must be frozen before using the QPL9547 noise model against antenna Z_active.

The numerical proximity to the approximately 130-ohm source used by the recent differential-LNA reference is nevertheless a strong reason to build the receiver shadow now.

## New decision: two gates, not one

### Gate T — support transparency diagnostic
Existing metric remains valid:
- max complex |Delta S11| <= 0.05;
- max |Delta Z_active| <= 10 ohm;
- no severe mismatch alert.

Purpose:
classify whether a mechanical structure can be ignored as an RF design variable.

S1 is NOT transparent because C60P135 fails Gate T.

Gate T is not retroactively changed.

### Gate R — receiver / system acceptability
A non-transparent support may still be acceptable if the complete antenna/support/hub source environment produces acceptable:
- LNA noise penalty / receiver temperature;
- transducer gain / mismatch;
- stability;
- scan dependence;
- pre-LNA loss;
- polarization behavior;
- manufacturability and serviceability.

Gate R numerical limits must be frozen in R1E1A4A before any new support candidate result is viewed.

## Revised execution sequence

### R1E1A4A — receiver shadow + interface freeze — NEXT
No CST solve.

1. Freeze the balanced antenna / two-LNA electrical reference plane.
2. Define how differential Z_active maps to each LNA source reflection coefficient.
3. Import a traceable QPL9547 S/noise-parameter anchor set.
4. Build GammaOpt, Zopt, NF/noise-temperature penalty and mismatch/stability calculations.
5. Replay the existing bare and S1 B0/C60P45/C60P135 source-impedance data through the receiver shadow.
6. Freeze receiver-level acceptance metrics before any new mechanical candidate result is viewed.
7. Freeze mechanically credible geometry envelopes for C0/C1/C2; keep C3 as an intentional-RF architecture, not a transparent-support candidate.

### R1E1A4B — failing-plane attribution / architecture screen
Only after separate build/solve authorization.

Start only at C60P135:
- D1 FOAM_ONLY: current historical `S1_BONDED` post geometry with the conservative adhesive dielectric removed, to identify glue versus foam/placement loading;
- C1 central dielectric-tube / serviceable standoff candidate;
- C2 structural PCB / printed-frame carrier candidate, both used beneath the mandatory H0 active hub.

Do not spend three scan states on every candidate.
First eliminate candidates at the known failing C60P135 sentinel.

### R1E1A4C — three-state qualification
For surviving mechanically credible candidates only:
- B0;
- C60P45;
- C60P135.

Report both Gate T and Gate R.

### R1E1B and later
Only a support/hub architecture that is understood at the system level is propagated into the pitch screen.

The pitch screen should add receiver-shadow metrics to active S11 / Z_active rather than ranking pitch from antenna impedance alone.

The physical LNA transistor is still not inserted into CST at this point. Full active-hub PCB / local ground / shield geometry must, however, enter full-wave EM on the final pitch/material shortlist before the array baseline is frozen.

## Immediate stop boundary

The next task is R1E1A4A only.

No support build.
No support solve.
No S4 solve.
No pitch screen.
No material A/B solve.
No physical LNA CST integration.

The purpose of the next task is to define the correct receiver-level question before spending additional full-wave solves.
