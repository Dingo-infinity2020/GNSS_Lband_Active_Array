# CHARTS 2025 Provenance

Source:
- Albert Wai Kit Lau et al.
- "Active Planar Antenna Design for CHARTS Array"
- ISAP 2025
- DOI: 10.34385/proc.98.1571143655

## Paper-explicit parameters used by R0

| Item | Value | Provenance |
|---|---:|---|
| Frequency band | 300–500 MHz | PAPER_EXPLICIT |
| Radiator concept | planar 4-petal square antenna | PAPER_EXPLICIT |
| Passive loading | surrounding ring, lower-band resonance / inductive load | PAPER_EXPLICIT |
| Height above ground | 200 mm | PAPER_EXPLICIT |
| Center impedance design region | (100 +/- 40) + j(0 +/- 40) ohm | PAPER_EXPLICIT |
| S11 @ 300 MHz | -20 dB | PAPER_EXPLICIT |
| S11 @ 400 MHz | -18 dB | PAPER_EXPLICIT |
| S11 @ 500 MHz | -18 dB | PAPER_EXPLICIT |
| E HPBW @ 300/400/500 | 92/108/120 deg | PAPER_EXPLICIT |
| H HPBW @ 300/400/500 | 66/74/87 deg | PAPER_EXPLICIT |
| Gain @ 300/400/500 | 8.7/7.75/7 dBi | PAPER_EXPLICIT |
| Simulated efficiency | 98.5% | PAPER_EXPLICIT |
| Active input | balanced output directly into pair of LNAs | PAPER_EXPLICIT |
| Active mounting | small ground plane beneath petal feed point | PAPER_EXPLICIT |
| Shield | clip-on metallic shield | PAPER_EXPLICIT |
| Scaled measurement | 1:5.5 at 1.65–2.75 GHz | PAPER_EXPLICIT |

## Geometry not fully specified by text

The proceeding does not include a complete numerical geometry table for:
- outer radiator PCB side,
- exact petal polygon vertices / curvature,
- exact ring side/width/gaps,
- detailed central cutout and feed-terminal dimensions,
- ground-plane lateral size,
- conductor/substrate stack and dielectric parameters for the full-scale unit.

Some dimensions are visibly annotated in Fig. 1(a), but values read from the figure must remain `FIGURE_DERIVED_UNVERIFIED` until independently checked at sufficient resolution.

## Modeling rule

A parameter inferred only by image scaling must never overwrite a paper-explicit parameter.

Every R0 CAD parameter must appear in `em/cst/R0_CHARTS_300_500/parameters.csv`.
