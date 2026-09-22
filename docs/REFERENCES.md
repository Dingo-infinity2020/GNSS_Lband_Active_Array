# Reference Map

This repository tracks reference ideas separately from project-owned geometry.

## Primary R0 source

**Lau, A. W. K. et al. (2025), "Active Planar Antenna Design for CHARTS Array", ISAP 2025.**  
DOI: 10.34385/proc.98.1571143655  
Role: primary topology and active-feed reference for R0.

Important known features:
- 300–500 MHz
- low-cost PCB / mostly 2D design
- 4-petal planar radiator
- passive surrounding ring
- 200 mm height over ground
- balanced output directly feeding a pair of LNAs
- local active electronics and clip-on RF shield
- incomplete published geometry; must be reconstructed honestly.

## Fully specified geometry reference

**Cui, Y. et al. (2023), "A compact broadband antenna for ultra high frequency and L band on 5G new radio base stations", IET Microwaves, Antennas & Propagation.**  
DOI: 10.1049/mia2.12343  
Role: validation/reference for square-loop loading, dual polarization, and a geometry with published dimensions/materials.

Key reported behavior:
- two +/-45-degree dipoles surrounded by square loop,
- Rogers 4350B, er 3.48, 0.76 mm,
- square loop creates a lower resonance,
- open slots create an upper resonance,
- measured/simulated 0.69–1.52 GHz bandwidth for return loss >15 dB,
- reported isolation >35 dB.

Its input baluns are **not** copied into the low-noise mainline architecture.

## Differential-LNA reference

**Da Costa, S., Lau, A. W. K., Vanderlinde, K. (2026), "Low-cost, ultra-wideband, differential low-noise amplifier for interferometric radio telescopes", arXiv:2607.21715.**  
Role: circuit reference for using commercial single-ended LNAs as a balanced first stage without a pre-amplification balun.

Reported:
- commercial SMT implementation,
- approximately 0.3 dB NF when matched to a 130-ohm source,
- feed-coupled system noise as low as ~25 K with a 300–1500 MHz Vivaldi feed.

Preprint status must remain explicit.

## Other architecture references

ASKAP active balun / connected-array work:
- informs "gain before balun" architecture and active-impedance-aware noise design.

C-ORA / SKA MFAA:
- informs coincident-phase-center dual polarization and locally integrated LNA concepts.

PUMA / unbalanced TCDA:
- first backup architecture if the balanced active-hub path becomes too costly or unstable.

ASTRON / EMBRACE / low-noise tiles:
- benchmark for integrated antenna/LNA receiver-noise methodology.

## Citation rule

Do not copy copyrighted PDFs or large source extracts into this repository.
Store metadata, source URLs/DOIs, project notes, and parameter provenance.
