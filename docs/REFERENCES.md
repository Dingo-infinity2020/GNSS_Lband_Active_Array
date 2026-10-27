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

## Receiver co-design references added for R1E1A4

**Warnick, K. F. et al. (2011), "Design and Characterization of an Active Impedance Matched Low-Noise Phased Array Feed", IEEE Transactions on Antennas and Propagation 59(6), 1876-1885.**
DOI: 10.1109/TAP.2011.2122223
Role: L-band radio-astronomy precedent for optimizing array/LNA performance around active impedance rather than isolated passive match.

**Maaskant, R. et al. (2007), "Applying the active antenna impedance to achieve noise match in receiving array antennas", IEEE APS.**
DOI: 10.1109/APS.2007.4396892
Role: theoretical/array-receiver precedent that active antenna impedance is the relevant low-noise source condition in coupled receiving arrays.

**Alekseev, K. et al. (2025), "Q-Band LNA-Antenna Co-Design: Exploiting Antenna Matching for System Noise Figure Optimization", IEEE Journal of Microwaves 5(5), 1107-1119.**
DOI: 10.1109/JMW.2025.3588491
Role: modern antenna/LNA co-design workflow showing that eliminating an arbitrary 50-ohm interface can improve receiver-level noise performance.

## Mechanical-support / low-density-foam evidence added for R1E1A4

**"Design, Development, and Qualification of a Broadband Compact S-Band Antenna for a CubeSat Constellation" (Sensors, 2025).**
DOI: 10.3390/s25041237
Role: peer-reviewed example of Rohacell spacers providing structural integrity while acting approximately as an air-like dielectric in a multilayer antenna stack.

**Ghalib et al. (2021), "Collocated MIMO travelling wave SIW slot array antennas for millimetre waves", IET Microwaves, Antennas & Propagation.**
DOI: 10.1049/mia2.12110
Role: explicit Rohacell 51 IG-F plus thin 3M VHB adhesive fabrication example; confirms foam+adhesive is a real antenna assembly technique, though in a laminated/sandwich form rather than the project's discrete-post geometry.

**"High-Efficiency Broadband Planar Array Antenna with Suspended Microstrip Slab for X-Band SAR Onboard Small Satellites" (Sensors, 2022).**
DOI: 10.3390/s22010252
Role: Rohacell plus adhesive-film multilayer array example and reminder that foam/support layers can be part of the intended EM stack rather than merely invisible mechanics.
