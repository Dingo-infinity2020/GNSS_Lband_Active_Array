# R1E0B Read-Only Result Recovery

**RECOVERY_STATUS = PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE_READONLY_RECOVERY**

Recovery source HEAD:
e7971d5ff82608351eac7bb81286469a76b58e9b

Solver rerun:
NO

Artifact modified:
NO

Original formal status:
HOLD_R1E0B_RESULT_PATH_QUALIFICATION

Original HOLD classification:
PERIODIC_RESULT_PATH_NAMING_MISMATCH

## Solved artifact

D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work\R1E0B_POLA_PERIODIC_BROADSIDE_SMOKE_V01.cst

SHA256:
339021e580efa6aae6dfcfa229e4194b4dcf0bbef854398d44a0efed65aac7ad

Bytes:
43620

## Actual periodic result path

Driven-port self-reflection:

1D Results\S-Parameters\S1(1),1(1)

Point count:
1001

All S11 values finite:
PASS

All derived Z_active values finite:
PASS

## Native convergence

Delta-S:
0.0453805 -> 0.0552784 -> 0.0530417 -> 0.0204615 -> 0.0179226 -> 0.0185901

Final two values <= 0.02:
PASS

Termination:
desired accuracy limit reached

Max-pass termination:
NO

Broadband sweep:
PASS after 7 frequency samples

Error lines:
0

The YZ-matrix postprocessing warning is retained as non-fatal evidence; it is not required for the one-port active-impedance objective.

## Broadside periodic active impedance

Reference impedance:
100 ohm differential

Z_active = 100 * (1 + S11) / (1 - S11)

Best S11 over 1.0–1.8 GHz:
-9.7406 dB at 1.6736 GHz

Science band 1.15–1.65 GHz:
- Re(Z_active): 85.05 to 264.39 ohm
- Im(Z_active): -84.19 to +141.95 ohm
- |Z_active|: 105.33 to 266.79 ohm
- S11: -5.24 to -9.70 dB

Representative GNSS anchors:
- 1.1768 GHz: S11=-5.47 dB, Z_active=132.0+j141.1 ohm
- 1.2272 GHz: S11=-5.88 dB, Z_active=182.8+j136.5 ohm
- 1.2784 GHz: S11=-6.28 dB, Z_active=234.1+j104.2 ohm
- 1.4000 GHz: S11=-7.34 dB, Z_active=243.8-j37.5 ohm
- 1.5608 GHz: S11=-9.03 dB, Z_active=125.3-j80.8 ohm
- 1.5752 GHz: S11=-9.17 dB, Z_active=117.4-j78.5 ohm
- 1.6024 GHz: S11=-9.42 dB, Z_active=104.1-j73.2 ohm

## Context versus isolated element

Maximum complex S11 difference versus clean isolated Pol-A over 1.15–1.65 GHz:
0.70508

Maximum dB difference:
10.30 dB

This difference is not a failure. It is direct evidence that the periodic array environment materially changes the source impedance seen by the feed/LNA.

## Scientific conclusion

The 94-mm infinite periodic array broadside model is numerically stable and produces a valid active-impedance curve.

The project has now crossed from isolated-element qualification into actual array physics.

The broadside active-impedance locus is already far wider than the isolated 100-ohm-centered intuition, confirming the mainline rule that LNA input matching must not be frozen before scan-dependent active impedance is mapped.

## Canonical stage conclusion

PASS_R1E0B_BROADSIDE_PERIODIC_SMOKE

Next stage:
R1E0C first-scan DESIGN ONLY.
