# R1E0C-B C30P45 Scan Solve — Final Report

**FINAL_STATUS = PASS_R1E0C_B_C30P45_SCAN_SOLVE**

Source HEAD:
`046ccc660e70f4ab4c9ddfd6026111c6a140ad24`

Formal invocation count:
1

Exit code:
0

Runtime:
112.60 s

## Immutable input

State:
C30P45

Theta/Phi:
30 / 45 deg

Source SHA256:
`e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2`

## Solved artifact

`D:\GNSS_Lband_Active_Array\_r1e0c_b_c30p45_scan_solve_work\R1E0C_B_C30P45_SCAN_SMOKE_V01.cst`

SHA256:
`068665b01c0cdea5338662a43fd70f1675e623ef205dbf0b910f45b40526823c`

Bytes:
43583

## Native convergence

Delta-S:
0.0534035 -> 0.0428105 -> 0.0459950 -> 0.0447652 -> 0.0130888 -> 0.0198328

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
93.21 to 191.35 ohm

Im(Z_active):
-30.20 to +103.55 ohm

Maximum |Z_active|:
195.49 ohm

Maximum |S11|:
0.44294

## GNSS anchors

- 1.1768 GHz: S11=-7.40 dB, Z_active=126.2+j102.7 ohm
- 1.2272 GHz: S11=-8.00 dB, Z_active=154.9+j93.0 ohm
- 1.2784 GHz: S11=-8.64 dB, Z_active=178.6+j71.8 ohm
- 1.4000 GHz: S11=-10.57 dB, Z_active=184.1+j2.8 ohm
- 1.5608 GHz: S11=-15.53 dB, Z_active=122.9-j29.9 ohm
- 1.5752 GHz: S11=-16.21 dB, Z_active=117.5-j29.1 ohm
- 1.6024 GHz: S11=-17.57 dB, Z_active=107.9-j26.6 ohm

## Movement versus broadside

Maximum complex Delta S11:
0.22935 at 1.6496 GHz

Maximum |Delta Z_active|:
73.84 ohm at 1.3616 GHz

## Physics-alert gate

|S11| >= 0.90:
NO

Re(Z_active) <= 0:
NO

|Z_active| >= 1000 ohm:
NO

Therefore:
NO_R1E0C_PHYSICS_ALERT_C30P45

## Preserved warning

CST retained the known parameter-history warning about an earlier attempt to restore R1E0_scan_theta_deg to 0 during history rebuild.

This does not invalidate the solve because:
- the hash-locked source had theta=30/phi=45;
- the pre-solver audit passed;
- the solver log explicitly states Theta:30, Phi:45;
- the periodic result is finite and converged.

## Scientific conclusion

The 94-mm periodic array remains numerically stable at 30-deg scan in the Pol-A principal plane.

The active source impedance moves materially relative to broadside but remains finite, positive-real and well away from the frozen severe-mismatch alert thresholds.

No radiator optimization is justified from C30P45 alone.

Next state:
C45P45, separate authorization required.
