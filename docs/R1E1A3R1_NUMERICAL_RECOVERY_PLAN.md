# R1E1A3-R1 Numerical Recovery Plan

Status: DESIGN ONLY — RECOVERY SOLVE NOT AUTHORIZED

Trigger:
`HOLD_R1E1A3_S1_BONDED_B0_NUMERICAL_MAXPASSES`

The first S1 broadside solve completed its broadband sweep and showed small support-vs-bare movement, but adaptive meshing terminated at MaxPasses=8. This is a numerical qualification HOLD, not a physics failure.

## Frozen recovery principle

Do not change geometry, materials, port, scan state, unit-cell pitch, frequency range, MaxDeltaS, Delta-S check count, tetrahedral order, or solver method.

Only proposed numerical change:
- `MaxPasses: 8 -> 12`.

Reason:
- pass 6 reached Delta-S=0.0130842;
- passes 7 and 8 rose slightly to 0.0202292 and 0.021505;
- the run therefore missed the frozen two-consecutive-passes <=0.02 rule by a small margin;
- extra adaptive passes are the least invasive recovery test.

R1 must use the same immutable S1_BONDED_B0 source SHA256:
`addcd7a30fabdac49227b9f8ab8f05a6832266f0e00b58d288982abec13bae95`.

R1 is one fresh one-shot invocation only. No reuse of the HOLD result directory.

If R1 reaches desired accuracy with the final two Delta-S values <=0.02, compare its science-band result to the existing HOLD run as a numerical-consistency check and then resume the remaining support matrix under the same recovery solver ceiling.

If R1 again terminates by MaxPasses, stop. Do not automatically increase passes again. Return to DESIGN to consider local mesh strategy or a physically justified thin-bond representation.

The pre-frozen physical benign gate remains unchanged:
- max complex |Delta S11| <= 0.05;
- max |Delta Z_active| <= 10 ohm;
- no severe mismatch alerts.

No threshold changes are allowed because results have already been viewed.
