# H3B-T01A O2B Local Junction DOE Freeze V0.1

Status: AUTHORIZED BUILD + TWO-LEVEL SOLVE ON NW

Baseline: O2A with O1 line cross-section Wsig=1.50 mm / Gcpw=0.40 mm.

Released variables:
- transition signal-pad width: 2.0 / 2.4 mm;
- transition signal-to-ground pad gap: 0.20 / 0.30 mm;
- transition-region extension: 0.00 / 0.30 mm.
Also include unchanged O2A baseline 2.2 / 0.25 / 0.00 as reference.

The extension moves the pad-to-normal-GCPW boundary and backing-ground boundary together, preserving electrical continuity and RP spacing.

Frozen:
- transition ground-pad width = 2.4 mm;
- solder envelope in y/z and via geometry/locations;
- edge/castellation concept;
- boards, FR4, W15/G40 normal GCPW, RP1/RP2 and ports;
- T01-C and all active/LNA work.

All 9 geometries must pass build-only fresh-reopen/intersection checks before any solve.
Screen all 9 at exactly four adaptive passes. Screening cannot become final PASS.
Select three finalists using normalized maximum shortfall from preferred gates (15 dB worst-core return, 0.10 dB max junction excess); ties: better return, lower excess, larger gap, smaller extension.
Fresh-run only the three finalists at full O0 fidelity, DeltaS<=0.02 twice, MaxPasses16, no silent retry.

Preferred final gate: worst-core return >=15 dB AND max junction excess <=0.10 dB.
Acceptable gate: worst-core return >=12 dB AND max junction excess <=0.15 dB.
Also require no S21 notch below -3 dB and reciprocity <=0.05 dB.
Stop after O2B qualification.
