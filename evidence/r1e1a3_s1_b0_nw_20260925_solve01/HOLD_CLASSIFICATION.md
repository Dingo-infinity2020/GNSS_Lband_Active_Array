# R1E1A3 S1 Bonded Broadside HOLD Classification

Status: `HOLD_R1E1A3_S1_BONDED_B0_NUMERICAL_MAXPASSES`

Formal invocation count: 1. No retry.

Source SHA256:
`addcd7a30fabdac49227b9f8ab8f05a6832266f0e00b58d288982abec13bae95`

Solved artifact SHA256:
`55a55f56ad4981fb30d31624cc656f2a6f4affc5438d3879176531b633480ce3`

Solved artifact is PROTECTED_IN_PLACE.

## Numerical evidence

Adaptive Delta-S sequence:
0.0344858 -> 0.0434797 -> 0.0306481 -> 0.0224755 -> 0.0130842 -> 0.0202292 -> 0.021505.

CST reached MaxPasses=8 rather than desired-accuracy termination.
Final two Delta-S values are not both <=0.02.
Broadband sweep nevertheless completed and no solver error lines were found.

Therefore this is `HOLD_NUMERICAL`, not a physics failure.

## Provisional physical observation — not a PASS claim

Versus the qualified bare broadside reference over 1.15–1.65 GHz:
- max complex |Delta S11| = 0.01111983;
- RMS complex |Delta S11| = 0.00592639;
- max |Delta Z_active| = 4.27463 ohm;
- RMS |Delta Z_active| = 2.92423 ohm;
- no severe mismatch alert fired.

These values are inside the pre-frozen 0.05 / 10-ohm benign thresholds, but the candidate cannot be declared EM_BENIGN until numerical qualification passes.

Remaining authorized matrix states were NOT started after this HOLD.

## Provenance side effect observed

Opening the copied solve project replayed a historical build-audit step containing absolute evidence paths and rewrote two committed R1E1A2 B0 text files. The immutable source CST SHA256 remained unchanged. Those two build-evidence files were restored exactly from the previous Git checkpoint before closeout.

Any recovery harness must protect or neutralize these historical absolute-output audit paths before the next solver invocation.
