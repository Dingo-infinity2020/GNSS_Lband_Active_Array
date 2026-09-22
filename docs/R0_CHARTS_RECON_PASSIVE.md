# R0-CHARTS-RECON-PASSIVE

Status: **PLANNED / BUILD-ONLY FIRST**

## Objective

Create a literature-traceable passive CST reconstruction of the 2025 CHARTS planar antenna at its original 300–500 MHz scale.

R0 is not an L-band design and is not an exact-replica claim.

## Why R0 exists

The CHARTS proceeding provides enough information to reconstruct the topology and several electrical/mechanical constraints, but does **not** publish a complete geometry table for the petal and ring.

Therefore R0 must distinguish:

- directly stated values,
- values read from figures,
- assumptions needed to close the CAD model.

## Explicit paper anchors

From Lau et al., ISAP 2025:

- operating band: 300–500 MHz
- planar 4-petal square configuration
- passive ring surrounding radiator
- ground-plane spacing: 200 mm
- center impedance tunable roughly within `(100 +/- 40) + j(0 +/- 40) ohm`
- simulated S11 at 300/400/500 MHz: -20/-18/-18 dB
- simulated E-plane HPBW at 300/400/500 MHz: 92/108/120 deg
- simulated H-plane HPBW at 300/400/500 MHz: 66/74/87 deg
- simulated gain at 300/400/500 MHz: 8.7/7.75/7 dBi
- simulated radiation efficiency: 98.5%
- balanced differential output can directly feed a pair of LNAs
- active implementation places a small ground plane beneath petal feed points
- LNA circuitry is mounted at the feed region
- clip-on metallic shield is used to suppress positive feedback / self-resonance
- 1:5.5 scaled beam-measurement model was tested at 1.65–2.75 GHz

## R0 stages

### R0.0 — provenance freeze
Deliver:
- parameter table,
- source classification,
- screenshot / page references,
- explicit list of unknown dimensions.

PASS condition: no geometry is presented as paper-explicit unless it is textually explicit or unambiguously dimensioned in the source.

### R0.1 — geometry build-only
Build:
- ground plane,
- planar four-petal conductor,
- passive square/ring conductor,
- differential ideal feed,
- 200 mm radiator-to-ground spacing.

No active PCB, no shield, no LNA.

PASS condition:
- valid solids/sheets,
- no accidental conductor overlap at the differential gap,
- symmetry checks,
- geometry hash / parameter manifest saved,
- solver not run.

### R0.2 — passive electromagnetic sanity run
Only after human review of R0.1.

Check:
- impedance trend over 300–500 MHz,
- broad hemispherical pattern,
- beamwidth trend against Table I,
- whether the chosen reconstruction can reproduce the published behavior without hidden fitting.

A mismatch is evidence, not permission to silently alter source-derived geometry.

### R0.3 — reconstruction uncertainty study
Vary only parameters marked `ASSUMPTION` or `FIGURE_DERIVED_UNVERIFIED`.

Goal:
- identify which unpublished dimensions materially control resonance and beamwidth,
- bound the family of plausible CHARTS-like geometries.

## Stop condition

R0 ends with a **reconstructed family**, not necessarily one falsely precise geometry.

Only after R0 closure may R1 apply an approximate /3.5 electromagnetic scaling toward an initial 1.05–1.75 GHz L-band model.
