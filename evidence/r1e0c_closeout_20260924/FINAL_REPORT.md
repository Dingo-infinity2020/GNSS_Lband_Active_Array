# R1E0C Scan Qualification — Final Closeout

**CANONICAL_STATUS = PASS_R1E0C_SCAN_QUALIFICATION**

## Scope

Validated the 94-mm infinite periodic array active-impedance workflow over:
- broadside reference: theta=0 deg, phi=45 deg;
- principal-plane scans: theta=30, 45, 60 deg, phi=45 deg;
- orthogonal-plane sentinel: theta=60 deg, phi=135 deg.

Required science band:
1.15-1.65 GHz

## Numerical status

All four R1E0C-B scan solves:
- used immutable hash-locked scan-state inputs;
- completed exactly one formal invocation per state;
- reached the frozen native adaptive convergence gate;
- terminated by desired accuracy;
- passed broadband sweep convergence;
- produced finite 1001-point periodic driven-port S11 and Z_active;
- produced no solver error lines.

Closed states:
- C30P45: PASS_R1E0C_B_C30P45_SCAN_SOLVE
- C45P45: PASS_R1E0C_B_C45P45_SCAN_SOLVE
- C60P45: PASS_R1E0C_B_C60P45_SCAN_SOLVE
- C60P135: PASS_R1E0C_B_C60P135_SCAN_SOLVE

## Frozen severe-mismatch alerts

Across all scan states, none of the frozen severe alerts were triggered:
- |S11| >= 0.90: NO
- Re(Z_active) <= 0: NO
- |Z_active| >= 1000 ohm: NO

Therefore the 94-mm baseline is numerically viable through the defined 0-60 deg core scan under the R1E0C alert contract.

## State-by-state science-band impedance regions

Broadside:
- Re: 85.05 to 264.39 ohm
- Im: -84.19 to +141.95 ohm
- max |Z|: 266.79 ohm

C30P45:
- Re: 93.21 to 191.35 ohm
- Im: -30.20 to +103.55 ohm
- max |Z|: 195.49 ohm

C45P45:
- Re: 100.78 to 123.59 ohm
- Im: +29.23 to +58.09 ohm
- max |Z|: 129.84 ohm

C60P45:
- Re: 55.42 to 77.84 ohm
- Im: -13.42 to +103.03 ohm
- max |Z|: 129.13 ohm

C60P135:
- Re: 73.43 to 263.32 ohm
- Im: -63.82 to +137.07 ohm
- max |Z|: 266.40 ohm

## 60-deg plane dependence

Read-only C60P45 versus C60P135 comparison:
- max complex Delta S11: 0.67023
- RMS complex Delta S11: 0.64286
- max |Delta Z_active|: 208.98 ohm
- RMS |Delta Z_active|: 173.71 ohm

Representative |Delta Z_active| between the two 60-deg planes:
- 1.1768 GHz: 120.22 ohm
- 1.2272 GHz: 126.47 ohm
- 1.2784 GHz: 137.47 ohm
- 1.4000 GHz: 175.60 ohm
- 1.5608 GHz: 208.74 ohm
- 1.5752 GHz: 208.97 ohm
- 1.6024 GHz: 208.53 ohm

No numerical PASS/FAIL threshold for plane divergence was frozen before results, so no post-hoc threshold is introduced.

Scientific observation:
the 60-deg active source impedance is strongly scan-plane dependent in a quantitative sense, even though neither plane triggers the frozen severe-mismatch alerts.

## System implication

The R1E0C result is sufficient to reject the idea of a single fixed nominal antenna source impedance for frontend design.

Final LNA input matching remains blocked.

Preliminary LNA circuit/model research may continue in parallel, but the authoritative source-impedance cloud must come from later R1E1/R1E2 array studies.

## Evidence

- `plane60_comparison.json`
- `scan_locus_summary.json`
- `scan_anchor_matrix.csv`
- per-state solver evidence directories for C30P45/C45P45/C60P45/C60P135

## Next mainline stage

R1E1 periodic pitch/material trade.

No R1E1 build or solve is authorized by this closeout.
