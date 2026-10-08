# R1E1A3-R1 S1 Bonded C60P135 Science-Gate HOLD

Status: `HOLD_R1E1A3_SUPPORT_SCIENCE_GATE_S1_C60P135_DELTA_Z`.

Numerical solver qualification: PASS.
Adaptive Delta-S: 0.0576475 -> 0.0487832 -> 0.0197116 -> 0.0172116.
Desired-accuracy termination: PASS. Broadband convergence: PASS. Solver errors: NONE.

Frozen physical gate: max complex |Delta S11| <= 0.05 AND max |Delta Z_active| <= 10 ohm AND no severe mismatch alerts.

Observed versus qualified bare C60P135 over 1.15–1.65 GHz:
- max complex |Delta S11| = 0.02868632 -> PASS;
- RMS complex |Delta S11| = 0.01866250;
- max |Delta Z_active| = 15.09084 ohm -> FAIL;
- RMS |Delta Z_active| = 10.30755 ohm;
- severe mismatch alerts: NONE.

The 10-ohm threshold was frozen before results and is not changed after the fact.

Read-only localization:
- |Delta Z_active| > 10 ohm at 297/625 science-band samples (47.5%);
- exceedance range: 1.4128–1.6496 GHz;
- peak at 1.5520 GHz;
- bare Z_active = 255.2453 - j8.4874 ohm;
- supported Z_active = 250.2196 - j22.7168 ohm;
- Delta Z = -5.0257 - j14.2294 ohm;
- |Delta S11| at the peak-|Delta Z| frequency = 0.024201.

This is a broad upper-band support perturbation, not a single-frequency numerical glitch.

Solved artifact SHA256: `e909469daa31db7bf8d8c9c8c0d33844ace3c46bd38f3c2b8c4c1ee86713fd7a`.
Protected build-evidence rewrites were detected, restored, and verified.

Per the frozen sequence, S4_PEC_B0 was NOT started after this science HOLD.
