# Cui 2023 Provenance

Source:
- Yuehui Cui, Zhenxing Tu, Yue Qin, RongLin Li
- "A compact broadband antenna for ultra high frequency and L band on 5G new radio base stations"
- IET Microwaves, Antennas & Propagation 17(5), 361-368 (2023)
- DOI: 10.1049/mia2.12343
- Open-access publisher page: https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/mia2.12343

## Why it is in this project

Unlike the short CHARTS proceeding, Cui 2023 publishes:
- explicit substrate,
- explicit substrate thickness,
- a complete geometry-parameter table,
- dual-polarized feed topology,
- measured and simulated S-parameters,
- radiation patterns,
- physical explanation of the square-loop lower resonance and open-slot upper resonance.

The project uses REF-CUI to validate:
- CST geometry construction,
- dielectric/material handling,
- square-loop coupling physics,
- dual-polarized port handling,
- bandwidth / isolation post-processing,
- solver reproducibility.

It is **REFERENCE_ONLY** and does not replace the CHARTS-inspired mainline.

## Paper-explicit material stack

| Item | Value | Provenance |
|---|---:|---|
| Substrate | Rogers 4350B | PAPER_EXPLICIT |
| Relative permittivity | 3.48 | PAPER_EXPLICIT |
| Substrate thickness | 0.76 mm | PAPER_EXPLICIT |
| Polarizations | +/-45 deg | PAPER_EXPLICIT |
| Feed | two orthogonal broadband baluns | PAPER_EXPLICIT |

## Paper-explicit geometry table

Table 1 of the open-access article gives:

| Parameter | Value (mm) | Parameter | Value (mm) |
|---|---:|---|---:|
| Lg | 260 | H | 80 |
| Lr | 115 | Wr | 5.9 |
| Ld | 97 | Ws | 2.2 |
| Ls | 26.6 | Wg1 | 1.7 |
| Wg2 | 3.9 | Wp | 8.4 |
| Lp1 | 36.3 | Lp2 | 8.2 |
| Lp3 | 36.8 | Lb1 | 21 |
| Lb2 | 10 | Lb3 | 20.5 |
| Lb4 | 24.5 | Lb5 | 73 |
| Wb1 | 1.5 | Wb2 | 0.65 |
| Wb3 | 0.95 | Wb4 | 13 |
| Wb5 | 28.5 | Wb6 | 3.6 |
| Wb7 | 4.8 | Wb8 | 3.6 |

These values are source facts.
Their geometric mapping must still be audited against the publisher figures before a CST macro is written.

## Paper-explicit operating behavior

The article reports:
- broadband dual-polarized antenna composed of two +/-45-degree dipoles surrounded by a square loop,
- lower resonance around 0.7 GHz produced by the square loop,
- higher resonance around 1.5 GHz produced by open slots in the dipoles,
- impedance bandwidth ~0.69-1.52 GHz for return loss >15 dB,
- stable radiation patterns,
- reported inter-port isolation >35 dB,
- antenna above a ground plane for unidirectional radiation.

The square loop is explicitly stated to be tightly coupled but **not attached** to the dipoles in the underlying compacting principle.

## Physics reference

The paper states:
- the surrounding loop generates a resonance below the isolated half-wave-dipole resonance,
- for the square-loop case, neighboring sides of the square loop act approximately as a folded half-wave path,
- the open slots in the dipole arms create the upper resonance.

This is directly relevant to CHARTS because CHARTS cites Cui 2023 for the passive-ring compacting/bandwidth mechanism.

## Important non-transfer rule

The Cui broadband baluns are not automatically accepted for this project's low-noise active architecture.

REF-CUI validates passive EM and square-loop physics.

The eventual GNSS active element still follows the project requirement:
- minimize pre-LNA passive loss,
- feed-point active electronics,
- LNA/feed co-design.

## Current next step

Before CST BUILD_ONLY:
1. audit publisher Figure 7 and related figures,
2. map each Table-1 symbol to an unambiguous geometric feature,
3. create a parameter manifest with no guessed symbol mapping,
4. only then authorize a deterministic REF-CUI build.

No solver is authorized merely from this table extraction.
