# R1E0C-B C60P45 Scan Solve — Final Report

**FINAL_STATUS = PASS_R1E0C_B_C60P45_SCAN_SOLVE**

Source HEAD:
`4df0ac815b4b0c4134634a3e540ff3c48f2061e0`

Formal invocation count:
1

Exit code:
0

Runtime:
76.68 s

## Immutable input

State:
C60P45

Theta/Phi:
60 / 45 deg

Source SHA256:
`94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01`

## Solved artifact

`D:\GNSS_Lband_Active_Array\_r1e0c_b_c60p45_scan_solve_work\R1E0C_B_C60P45_SCAN_SMOKE_V01.cst`

SHA256:
`58018c0ffa058c46a16fdca92948a6477ff77124960b027f0a2d071b4f368828`

Bytes:
43567

## Native convergence

Delta-S:
0.0500864 -> 0.0284443 -> 0.0175831 -> 0.0157380

Final two <= 0.02:
PASS

Termination:
desired accuracy limit reached

Max-pass termination:
NO

Broadband sweep:
PASS after 8 frequency samples

Error lines:
0

## Science-band active impedance

Band:
1.15-1.65 GHz

Re(Z_active):
55.42 to 77.84 ohm

Im(Z_active):
-13.42 to +103.03 ohm

Maximum |Z_active|:
129.13 ohm

Maximum |S11|:
0.51275

## GNSS anchors

- 1.1768 GHz: S11=-14.09 dB, Z_active=67.5-j6.2 ohm
- 1.2272 GHz: S11=-11.83 dB, Z_active=59.7+j7.4 ohm
- 1.2784 GHz: S11=-10.29 dB, Z_active=56.3+j20.3 ohm
- 1.4000 GHz: S11=-8.10 dB, Z_active=56.8+j47.9 ohm
- 1.5608 GHz: S11=-6.48 dB, Z_active=67.6+j82.4 ohm
- 1.5752 GHz: S11=-6.37 dB, Z_active=69.1+j85.6 ohm
- 1.6024 GHz: S11=-6.16 dB, Z_active=72.0+j91.8 ohm

## Movement versus broadside

Maximum complex Delta S11:
0.82410 at 1.6496 GHz

Maximum |Delta Z_active|:
209.36 ohm at 1.3552 GHz

## Physics-alert gate

|S11| >= 0.90:
NO

Re(Z_active) <= 0:
NO

|Z_active| >= 1000 ohm:
NO

Therefore:
NO_R1E0C_PHYSICS_ALERT_C60P45

## Preserved warning

CST retained the known parameter-history warning about an earlier attempt to restore R1E0_scan_theta_deg to 0 during history rebuild.

This does not invalidate the solve because the hash-locked source, pre-solver audit and solver log all identify theta=60/phi=45, and the periodic result is finite and converged.

## Scientific conclusion

The 94-mm periodic array remains numerically stable at the 60-deg core-scan boundary in the Pol-A principal plane.

The active-impedance locus moves very substantially relative to broadside, especially toward the high-frequency end, but no frozen scan-blindness or severe active-mismatch alert is triggered.

This clears the principal-plane 0-60 deg core scan numerically, pending the orthogonal-plane C60P135 sentinel.

Next state:
C60P135, separate authorization required.
