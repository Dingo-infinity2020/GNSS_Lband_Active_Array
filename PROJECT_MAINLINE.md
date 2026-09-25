# PROJECT_MAINLINE.md

> Highest-level scientific and simulation mainline for the GNSS L-band Active Array project.
>
> This document is the long-horizon authority for **what the project is trying to prove and in what order**.
> It is intentionally more stable than `PROJECT_HANDOFF.md`, which controls only the current execution baton.

## Authority and anti-drift rule

Every new design/execution session must read this file **before** the current handoff.

The project must not silently drift back toward optimizing an isolated antenna element as the final objective.

The system being designed is:

> **a low-cost dual-polarized active GNSS array element whose antenna, periodic-array environment, and first-stage LNA are co-designed around scan-dependent active impedance and receiver noise.**

Current mainline architecture:

- CHARTS-inspired planar balanced radiator;
- two independent linear-polarization channels;
- digital RHCP/LHCP synthesis;
- feed-point low-noise active frontend;
- periodic-array behavior treated as a first-class design constraint;
- finite-array validation before final system release.

First backup remains:
- PUMA / unbalanced tightly-coupled element with LNA behind the ground plane.

No architecture replacement is allowed without explicit human approval and the replacement test in `docs/PROJECT_RULES.md`.

## Non-negotiable design principles

1. **The isolated-element return loss is not the system objective.**
2. **Periodic/unit-cell active impedance must be understood before the LNA input match is frozen.**
3. The antenna must not be forced to 50 ohm or 100 ohm merely for convenience.
4. LNA design is judged against the source-impedance locus seen under frequency and scan, not one broadside impedance point.
5. Pre-LNA passive loss is minimized; a lossy passive balun is not introduced merely to obtain a nominal single-ended interface.
6. Material decisions must consider array scan, dielectric loss and pre-LNA efficiency, not isolated S11 alone.
7. Infinite periodic-array results must later be checked against finite-array center/edge/corner behavior.
8. Cross-polar isolation claims require a physically meaningful multi-conductor/feed representation; the historical crossed discrete-edge-port model is diagnostic only.
9. Production EM/circuit work must preserve deterministic provenance and SimulationOps build/solve separation.
10. Mechanical supports, standoffs, shields and frames that occupy the element near field are electromagnetic objects and must be qualified before the array baseline is frozen.
11. Stop once a gate answers its scientific question; do not optimize unrelated variables inside that gate.

## System requirements carried through the mainline

RF band:
- required continuous design band: 1.15–1.65 GHz.

Polarization:
- two independent linear channels;
- digital RHCP/LHCP synthesis;
- no generation-1 analog 90-degree hybrid.

Scan:
- core region: 0–60 deg from zenith;
- extended investigation: 60–75 deg.

Pitch search:
- exploratory square-lattice range: 88–100 mm;
- 94 mm is the first periodic baseline, not a frozen winner.

Low-noise frontend:
- first gain stage at/near the balanced feed;
- QPL9547 is a reference G0 candidate, not a frozen final device;
- final input network is not frozen until the array active-impedance locus is known.

## Simulation / design mainline

### M0 — Proven passive radiator baseline — CLOSED

Already established:
- project-owned CHARTS-inspired L-band radiator;
- human-reviewed materialized geometry;
- differential-feed diagnostic model;
- crossed-port limitation characterized;
- second-order adaptive tetrahedral passive solution numerically converged.

Canonical converged diagnostic evidence:
`R1A5M2 = PASS_R1A5M2_NATIVE_AND_ABSOLUTE_CONVERGED`.

This result is a **baseline**, not a reason to keep optimizing the isolated element.

### M1 - Clean non-crossing passive feed representation - CLOSED

Current gate family:
`R1A5F`.

Goal:
- build two deterministic single-differential-port variants from the same reviewed geometry;
- Pol-A = NE<->SW;
- Pol-B = NW<->SE;
- eliminate simultaneous crossed discrete-edge ports;
- prove exact rotational equivalence and geometry identity.

After build-only qualification, run only a short equivalence solve if needed to prove that the clean feed reproduces the converged isolated passive baseline.

**Do not start an isolated-element optimization campaign here.**

### M2 - Periodic unit-cell baseline - CLOSED PASS

Working stage:
`R1E0`.

Purpose:
move the scientific mainline from an isolated radiator to the infinite array environment.

Initial baseline:
- square lattice;
- pitch = 94 mm;
- existing FR4 baseline;
- one clean differential polarization at a time;
- periodic phase boundaries in x/y;
- open/radiating boundary in z;
- active differential impedance under scan.

First qualification set should be deliberately small:
- broadside;
- theta = 30, 45, 60 deg;
- representative frequencies spanning low/mid/high L-band.

Questions:
- does the periodic workflow reproduce a sensible broadside limit;
- how far does active impedance move with scan;
- is there scan blindness or a strong impedance anomaly;
- is the current pitch viable to 60 deg.

### M3 - Periodic pitch/material trade - CURRENT PRIMARY PHYSICS GATE

Working stage:
`R1E1`.

Use the validated unit-cell workflow to compare a compact candidate matrix.

Primary pitch candidates:
- 88, 90, 92, 94 mm.

Upper-bound/failure references:
- 96, 100 mm.

Materials:
- FR4 cost baseline;
- low-loss 4350B-class reference.

Before the production pitch screen, freeze a mechanically credible support/standoff baseline. Start from low-density RF foam or another minimal-volume symmetric dielectric support, but model its actual material properties; conductive aluminium/metal supports are not assumed benign. Use a small 94-mm support-sensitivity gate before propagating support geometry to all pitch candidates.

Do not declare a material winner from isolated return loss alone.

Metrics include:
- active differential impedance;
- scan robustness;
- radiation/total efficiency;
- realized gain;
- dielectric/pre-LNA loss implication;
- manufacturability/cost.

Freeze the first array pitch/material baseline only after this gate.

### M4 — Active-impedance and embedded-pattern atlas

Working stage:
`R1E2`.

Generate the source environment needed by the active frontend.

Core scan grid:
- theta = 0, 15, 30, 45, 60 deg.

Extended investigation:
- theta = 65, 70, 75 deg.

Representative azimuths:
- phi = 0, 45, 90 deg.

Required outputs:
- Z_active(f, theta, phi, pol);
- active reflection coefficient;
- embedded element pattern;
- efficiency and realized gain;
- co/cross-pol behavior;
- scan-blindness indicators;
- Pol-A/Pol-B symmetry.

The resulting active-impedance locus is the authoritative RF source environment for LNA co-design.

## When LNA work begins

There are two distinct start points.

### LNA circuit research may start in parallel during M2/M3

Allowed preliminary work:
- validate QPL9547 reference models;
- collect S/noise parameters;
- bias and stability analysis;
- broadband source-impedance/noise sweeps;
- compare plausible differential/active-balun frontend topologies;
- screen lower-cost alternatives.

Not allowed at this point:
- freezing the antenna input to 50 ohm or 100 ohm;
- freezing the final LNA input matching network;
- claiming final receiver NF from a broadside isolated impedance.

### True active-antenna co-design starts after M4 active-impedance locus exists

Working stages:
`R2A/R2B`.

Use the actual array source-impedance cloud to optimize:
- receiver noise temperature / NF;
- gain;
- stability;
- source mismatch robustness;
- common/differential mode behavior;
- out-of-band/RFI robustness.

The primary objective is receiver/system performance, not return loss.

Prefer objectives such as:
- T_rec(f, theta, phi);
- realized gain / T;
- stable low-noise operation over the active-impedance locus.

## M5 — Passive finite-array validation

Working stage:
`R1F`.

Before final active frontend freeze, compare periodic predictions against a finite passive array, nominally 5x5 or 7x7 if resources permit.

Inspect:
- center element;
- edge element;
- corner element;
- finite ground/backplane effects.

Compare their source-impedance loci to the infinite unit-cell result.

If finite-array edge/corner loci materially expand the source environment, that expanded locus must be included in LNA robustness analysis.

This is a likely CST251 production-scale task.

## M6 — Active frontend circuit design and co-design

Working stages:
`R2A/R2B`.

Circuit domain:
- ADS and/or CST Design Studio;
- LNA S/noise/nonlinear models;
- bias network;
- differential/common-mode stability;
- source-pull/noise optimization over the array impedance locus.

Architecture comparison should include, where practical:
- true differential first stage;
- symmetric two-LNA / active-balun concepts;
- alternatives that avoid lossy pre-LNA passive conversion.

## M7 — Full-EM active hub / feed transition

Working stage:
`R2C`.

CST EM includes only what truly requires field modeling:
- feed pads;
- vias;
- local ground;
- package launch/parasitics;
- RF shield;
- PCB traces and bias structures.

Transistor/LNA device physics remains in circuit-domain models.

Use EM-circuit co-simulation rather than embedding an active transistor directly into a large 3D FEM model.

## M8 — Active periodic-array validation

Working stage:
`R2D`.

Re-evaluate the periodic element with the selected frontend.

Required system metrics:
- receiver NF / T_rec vs scan;
- gain;
- stability;
- active mismatch;
- realized gain/T;
- polarization fidelity;
- sensitivity to process/component variation.

## M9 — Finite active array and digital polarization

Working stage:
`R3`.

Validate:
- finite active-array center/edge/corner behavior;
- digital X/Y calibration;
- RHCP/LHCP synthesis;
- axial ratio / polarization purity;
- system G/T;
- calibration repeatability.

Only after this stage should the design be treated as an array system rather than an antenna element.

## Host / SimulationOps routing

- NW: control plane, build-only, lightweight diagnostic/unit-cell solves when explicitly authorized.
- CST251-C: heavy periodic/finite-array production solves when explicitly authorized.
- XW: auxiliary Windows simulation host when required.
- ADS/circuit host routing must be recorded before active co-design execution.

No stage inherits solver permission from the previous stage.

## Current immediate route

As of the current handoff:

`R1E0 94-mm periodic scan qualification CLOSED PASS -> R1E1A1 six-pitch bare source set CLOSED PASS -> R1E1A2 mechanical-support EM baseline DESIGN -> R1E1 pitch/material trade -> R1E2 active-impedance atlas -> R2 active-front-end co-design`.

LNA model validation may proceed in parallel after the periodic workflow begins, but **final active-antenna input matching is blocked until R1E2 provides the scan-dependent active-impedance locus**.

This sequence is the default mainline. Deviations require explicit human approval and an update to this file.
