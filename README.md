# GNSS L-band Active Array

Low-noise, dual-polarized active antenna array development for full L-band GNSS reception.

## Start here on an execution host

Synchronize `project/r0-charts-scaffold`, then read **`PROJECT_HANDOFF.md`**. It is the canonical current task/return document; do not rely on copied chat prompts.


## Current phase

**R0-CHARTS-RECON-PASSIVE** — literature-traceable passive reconstruction only.

No solver-derived claims are accepted yet. Geometry provenance, assumptions, and build-only validation must be reviewed before any optimization or active-LNA integration.

## Target system envelope

- RF coverage: **1.15–1.65 GHz**
- Two independent linear-polarization outputs per element
- Digital RHCP/LHCP synthesis; no analog 90° hybrid in the first generation
- Array-aware design: active impedance and scan behavior are first-class requirements
- Core scan region: **0–60° from zenith**; 60–75° is an extended target
- Low-cost manufacturability: standard PCB/SMT, compact shielded active hub, Bias-Tee powering
- LNA must be placed as close to the balanced feed as practical; pre-LNA passive loss is minimized
- QPL9547 is a **reference LNA candidate**, not a frozen production choice

## Development gates

1. **R0** — CHARTS passive reconstruction at the published 300–500 MHz scale
2. **R1** — Maxwell-scaled L-band reference, initially ~1.05–1.75 GHz
3. **R2** — true dual-polarization model and mixed-mode validation
4. **R3** — periodic/finite-array active-impedance and scan study
5. **R4** — differential LNA study (QPL9547 reference + alternative candidates)
6. **R5** — CST/ADS antenna-array-LNA co-design
7. **R6** — full-EM central active hub, shield and real feed integration
8. **R7** — first hardware prototype

See `docs/REQUIREMENTS_v0.1.md` and `docs/R0_CHARTS_RECON_PASSIVE.md` for the frozen first-stage requirements and acceptance gates.
