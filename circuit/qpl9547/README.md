# QPL9547 reference model workspace

QPL9547 is the project's G0 reference LNA, not a frozen production choice.

## R1E1A4 receiver-shadow reference

`QPL9547_NOISE_REFERENCE_1P1_1P7.csv` contains a small project-owned transcription of in-band Qorvo Rev-D noise-parameter anchors plus the deterministic 50-ohm GammaOpt-to-Zopt conversion.

`illustrative_2xzopt_*` is NOT a frozen differential design target. It is only twice the single-ended Zopt and may be used only after the balanced antenna / two-LNA virtual-ground and reference-plane assumptions are explicitly qualified.

Source: Qorvo QPL9547 Data Sheet Rev. D, 2023-10-11.
