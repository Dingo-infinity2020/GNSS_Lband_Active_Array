# H3B-T01A O2A W15/G40 Junction Baseline Freeze V0.1

Status: AUTHORIZED BUILD + ONE-SHOT SOLVE ON NW

Purpose: determine whether the original 90-degree junction already meets the frozen O2 targets after applying the O1 winning line cross-section.

Only released change versus the qualified T01-A geometry:
- straight GCPW Wsig: 1.8 -> 1.5 mm;
- straight GCPW gap: 0.30 -> 0.40 mm;
- corresponding straight-line signal/ground rail x extents change deterministically.

Frozen without change:
- transition signal pad width 2.2 mm;
- transition pad gap 0.25 mm;
- transition pad lengths;
- transition ground pads;
- edge caps;
- solder envelopes;
- via locations/pitch/diameters;
- both boards, FR4, backing grounds;
- RP1/RP2, 50-ohm discrete ports;
- 1.0-2.0 GHz solve / 1.15-1.65 GHz decision band;
- second-order tetrahedral, MaxDeltaS 0.02, two checks, MaxPasses 16.

Reference authority: O1 W15_G40 high-fidelity straight line, SHA256 2050bba69d0a21a2a295c378d0a36a5408ad80e7399ba7403025a94a5694a604.

Decision:
- preferred: worst-core return >=15 dB AND max junction excess loss <=0.10 dB;
- acceptable: worst-core return >=12 dB AND max junction excess loss <=0.15 dB;
- reciprocity <=0.05 dB; no S21 notch below -3 dB.
If preferred is already met, do not automatically launch a broad O2 DOE.
