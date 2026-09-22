# Cui 2023 Provenance

Source:
- Yuehui Cui, Zhenxing Tu, Yue Qin, RongLin Li
- "A compact broadband antenna for ultra high frequency and L band on 5G new radio base stations"
- IET Microwaves, Antennas & Propagation (2023)
- DOI: 10.1049/mia2.12343

## Why it is in this project

Unlike the short CHARTS proceeding, Cui 2023 provides a much more completely specified dual-polarized antenna and a full geometry table.

The project uses it to validate:
- square-loop compacting mechanism,
- dual-polarized planar-dipole modeling,
- material and dimension handling,
- bandwidth / isolation post-processing.

## Reported reference facts

- two +/-45-degree dipoles,
- square loop surrounding dipoles,
- broadband baluns in the published design,
- Rogers 4350B,
- relative permittivity 3.48,
- substrate thickness 0.76 mm,
- lower resonance ~0.7 GHz from square loop,
- upper resonance ~1.5 GHz associated with open slots,
- 0.69–1.52 GHz bandwidth for return loss >15 dB,
- isolation reported >35 dB.

## Important non-transfer rule

The published input baluns are not automatically accepted for this project's low-noise architecture because pre-LNA passive loss is a first-order receiver-noise concern.

REF-CUI is a geometry / physics validation reference, not the active-front-end architecture.
