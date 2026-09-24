# R1E0C-B C60P135 Scan Solve — Final Report

**FINAL_STATUS = PASS_R1E0C_B_C60P135_SCAN_SOLVE**

Source HEAD:
`b7768b99848da9053a52ac1b1a7cefe2fe782c59`

Formal invocation count:
1

Exit code:
0

Runtime:
115.29 s

## Immutable input

State:
C60P135

Theta/Phi:
60 / 135 deg

Source SHA256:
`c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1`

## Solved artifact

`D:\GNSS_Lband_Active_Array\_r1e0c_b_c60p135_scan_solve_work\R1E0C_B_C60P135_SCAN_SMOKE_V01.cst`

SHA256:
`8107aff4f656c5013e9d6cf422f7d258ee4e045affa0311b7273c2889918d16c`

Bytes:
43575

## Native convergence

Delta-S:
0.0678618 -> 0.0451358 -> 0.0260878 -> 0.0274831 -> 0.0165357 -> 0.0145798

Final two <= 0.02:
PASS

Termination:
desired accuracy limit reached

Max-pass termination:
NO

Broadband sweep:
PASS after 9 frequency samples

Error lines:
0

## Science-band active impedance

Band:
1.15-1.65 GHz

Re(Z_active):
73.43 to 263.32 ohm

Im(Z_active):
-63.82 to +137.07 ohm

Maximum |Z_active|:
266.40 ohm

Maximum |S11|:
0.53690

## GNSS anchors

- 1.1768 GHz: S11=-5.48 dB, Z_active=82.8+j113.1 ohm
- 1.2272 GHz: S11=-5.61 dB, Z_active=104.5+j125.7 ohm
- 1.2784 GHz: S11=-5.74 dB, Z_active=132.3+j134.8 ohm
- 1.4000 GHz: S11=-6.17 dB, Z_active=218.1+j117.5 ohm
- 1.5608 GHz: S11=-7.26 dB, Z_active=251.8-j15.7 ohm
- 1.5752 GHz: S11=-7.40 dB, Z_active=245.3-j26.8 ohm
- 1.6024 GHz: S11=-7.69 dB, Z_active=230.1-j44.3 ohm

## Movement versus broadside

Maximum complex Delta S11:
0.38231 at 1.6496 GHz

Maximum |Delta Z_active|:
161.85 ohm at 1.4480 GHz

## Physics-alert gate

|S11| >= 0.90:
NO

Re(Z_active) <= 0:
NO

|Z_active| >= 1000 ohm:
NO

Therefore:
NO_FROZEN_SEVERE_MISMATCH_ALERT_C60P135

## Preserved warnings

CST retained the known parameter-history warnings for theta and phi history restoration attempts.

This does not invalidate the solve because the hash-locked source, pre-solver audit and solver log all identify theta=60/phi=135, and the periodic result is finite and converged.

## Scientific conclusion

The 94-mm periodic array remains numerically stable at the 60-deg orthogonal-plane sentinel.

The source-impedance region differs materially from the 60-deg principal-plane result; a read-only plane comparison is required before closing R1E0C.

No post-hoc numerical threshold is introduced for the plane-divergence observation.
