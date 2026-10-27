# H3B-T01A O1 Line Cross-Section Freeze V0.1

Status: AUTHORIZED TWO-LEVEL DOE ON NW

Released variables only:
- Wsig = 1.5 / 1.8 / 2.1 mm
- Gcpw = 0.20 / 0.30 / 0.40 mm

All other O0 geometry, FR4, RP spacing, ground-rail width, backing ground, via rule, ports, boundary and frequency range are frozen.

Screening:
- build and fresh-reopen audit all 9 candidates before solving;
- second-order tetrahedral, exactly 4 adaptive passes;
- screening results are ranking-only and can never be promoted to final PASS;
- select 3 finalists by lowest worst-case core-band S11/S22 dB; tie-break by S21, then larger gap.

Qualification:
- finalists are fresh-run from their clean build artifacts;
- second-order tetrahedral, DeltaS <= 0.02 for two checks, MaxPasses 16;
- no silent retry;
- an O1 winner must be numerically qualified and achieve at least 12 dB worst-case return loss across 1.15-1.65 GHz;
- 15 dB or better is preferred.
- no S21 notch below -3 dB and reciprocity <=0.05 dB.

Stop after O1 line-cross-section freeze. No junction optimization, T01-C, H3B integration or LNA work is authorized.
