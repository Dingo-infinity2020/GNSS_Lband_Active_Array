# R1E1A3 Support Sensitivity Gate Closeout

Canonical status: `HOLD_R1E1A3_SUPPORT_SCIENCE_GATE_S1_C60P135_DELTA_Z`.

R1E1A2 build canonical status: `PASS_R1E1A2_SUPPORT_BUILD_ONLY_READONLY_RECOVERY`.
The S1 bonded assembly was then qualified at three required scan states under the MaxPasses=12 recovery solver baseline.

| State | Numerical | max |Delta S11| | max |Delta Z| | Benign gate |
| --- | --- | ---: | ---: | --- |
| S1 B0 | PASS | 0.02950756 | 5.58606 ohm | PASS |
| S1 C60P45 | PASS | 0.00697213 | 0.982821 ohm | PASS |
| S1 C60P135 | PASS | 0.02868632 | 15.09084 ohm | FAIL |

The C60P135 failure is not a severe mismatch event and not a numerical failure. It is a failure of the pre-frozen support-transparency criterion max |Delta Z_active| <= 10 ohm.

At C60P135, |Delta Z| > 10 ohm for 297/625 science-band samples, spanning approximately 1.4128–1.6496 GHz. Peak |Delta Z|=15.09084 ohm occurs at 1.5520 GHz, with Delta Z approximately -5.03 - j14.23 ohm.

Therefore the S1 assembly is not frozen as the production passive support baseline. The threshold is not relaxed after viewing results.

The authorized S4_PEC_B0 sentinel was NOT started because the sequence stop rule requires any HOLD to stop subsequent solves.

R1E1B pitch screening remains blocked.
Next design stage: `docs/R1E1A4_SUPPORT_CO_DESIGN_DIAGNOSTIC_PLAN.md`.
