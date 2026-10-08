# R1E0C-B C45P45 Scan Solve — Final Report

**FINAL_STATUS = PASS_R1E0C_B_C45P45_SCAN_SOLVE**

Source HEAD:
`8b45ac4aad13d61cf8cb9494fb232f0eca22db41`

Formal invocation count:
1

Exit code:
0

Runtime:
114.18 s

## Immutable input

State:
C45P45

Theta/Phi:
45 / 45 deg

Source SHA256:
`ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed`

## Solved artifact

`D:\GNSS_Lband_Active_Array\_r1e0c_b_c45p45_scan_solve_work\R1E0C_B_C45P45_SCAN_SMOKE_V01.cst`

SHA256:
`c36861d616af18d06ad3dddba11ef50112646bc77181aeb54e7a23a1052eb7f1`

Bytes:
43564

## Native convergence

Delta-S:
0.0451306 -> 0.0302095 -> 0.0382559 -> 0.0277872 -> 0.0182843 -> 0.0148265

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
100.78 to 123.59 ohm

Im(Z_active):
+29.23 to +58.09 ohm

Maximum |Z_active|:
129.84 ohm

Maximum |S11|:
0.27618

## GNSS anchors

- 1.1768 GHz: S11=-11.53 dB, Z_active=106.3+j56.4 ohm
- 1.2272 GHz: S11=-12.11 dB, Z_active=112.9+j52.9 ohm
- 1.2784 GHz: S11=-12.66 dB, Z_active=118.2+j48.8 ohm
- 1.4000 GHz: S11=-14.19 dB, Z_active=123.6+j37.4 ohm
- 1.5608 GHz: S11=-16.58 dB, Z_active=112.2+j29.3 ohm
- 1.5752 GHz: S11=-16.61 dB, Z_active=110.5+j29.6 ohm
- 1.6024 GHz: S11=-16.44 dB, Z_active=107.0+j30.7 ohm

## Movement versus broadside

Maximum complex Delta S11:
0.49334 at 1.6496 GHz

Maximum |Delta Z_active|:
143.69 ohm at 1.3656 GHz

## Physics-alert gate

|S11| >= 0.90:
NO

Re(Z_active) <= 0:
NO

|Z_active| >= 1000 ohm:
NO

Therefore:
NO_R1E0C_PHYSICS_ALERT_C45P45

## Preserved warning

CST retained the known parameter-history warning about an earlier attempt to restore R1E0_scan_theta_deg to 0 during history rebuild.

This does not invalidate the solve because the hash-locked source, pre-solver audit and solver log all identify theta=45/phi=45, and the periodic result is finite and converged.

## Scientific conclusion

The 94-mm periodic array remains numerically stable at 45-deg scan in the Pol-A principal plane.

The active-impedance trajectory moves substantially relative to broadside but occupies a tighter, positive-real impedance region across the required science band.

No radiator optimization is justified from C45P45 alone.

Next state:
C60P45, separate authorization required.
