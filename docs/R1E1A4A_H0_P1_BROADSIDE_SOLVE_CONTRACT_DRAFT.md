# R1E1A4A H0/P1 Broadside Mixed-Mode Solve Contract — Draft

Status: SOLVE CONSUMED — NUMERICAL/MIXED-MODE PASS, CANONICAL HOLD_GATE_R_RNF0; NO FOLLOW-ON SCAN/CARRIER SOLVES

## Input

Only qualified build artifact:
`D:\GNSS_Lband_Active_Array\_r1e1a4a_h0_p1_build_work\R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_V01.cst`

SHA256:
`d1ebb6f4a6e8b48f3484cc5459790dd5c9bbd29482832c491076c84f783b3deb`

Canonical build status:
`PASS_R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_READONLY_RECOVERY`

Do not rebuild H0/P1 before this solve.

## First solve scope

Broadside only: theta=0 deg.
No support carrier.
No package, feed trace, shield, bias network, output network, transistor or optimization.

Numerical formulation:
- CST 2022.5 HF Frequency Domain;
- tetrahedral, second order;
- curvature order 3;
- 1.0–1.8 GHz solver band;
- HighFrequencyTet / ExpertSystem adaptation;
- MinPasses=3;
- MaxPasses=12;
- MaxDeltaS=0.02;
- NumberOfDeltaSChecks=2.

This is the already qualified recovery ceiling; no new numerical tuning is introduced.

## Required raw results

Extract all four complex single-ended S-parameters at 50-ohm references:
- S11;
- S12;
- S21;
- S22.

Do not infer mixed-mode behavior from S11 alone.

For equal 50-ohm single-ended references, form the power-wave mixed-mode S matrix with the standard orthonormal transform.
Required outputs:
- Sdd;
- Sdc;
- Scd;
- Scc.

Differential reference impedance is 100 ohm; common-mode reference impedance is 25 ohm.

Frozen mixed-mode convention for equal 50-ohm single-ended references:
- d = (port1 - port2)/sqrt(2);
- c = (port1 + port2)/sqrt(2);
- Sdd = (S11-S12-S21+S22)/2;
- Sdc = (S11+S12-S21-S22)/2;
- Scd = (S11-S12+S21-S22)/2;
- Scc = (S11+S12+S21+S22)/2.

For the branch-symmetry diagnostic, convert the 50-ohm single-ended S matrix to Z. Under an imposed odd branch-current pair I1=+I and I2=-I:
- Zbranch1 = Z11-Z12;
- Zbranch2 = Z22-Z21.
Branch magnitude imbalance is 20log10(|Zbranch1|/|Zbranch2|); branch phase error is the wrapped phase difference between Zbranch1 and Zbranch2. These definitions are frozen before the solve result is viewed.

## Reference-plane questions

The solve must answer, before any carrier study:
1. how much the 10x10-mm H0 local ground changes broadside differential Sdd/Zdd relative to the old ideal P0 differential model;
2. whether nominal mode conversion passes the frozen Gate-R `|Sdc|,|Scd| <= -30 dB` requirement;
3. whether P1A/P1B branch symmetry passes amplitude <=0.20 dB and phase <=2 deg limits;
4. whether the nominal virtual-ground approximation is good enough that each branch source can be approximated by `Zdiff/2`;
5. whether common-mode response shows a resonance requiring H0/local-ground redesign before package/shield/carrier work.

No Gate-T support comparison is performed in this solve because no carrier is present.

## Numerical gate

PASS only if:
- CST terminates by desired accuracy rather than MaxPasses;
- final two adaptive Delta-S values <=0.02;
- broadband sweep converges;
- all four S-parameter traces are present and nonempty;
- no solver error lines.

Any numerical HOLD stops. No silent retry or pass-count increase.

## Stop boundary

After a successful broadside solve, perform read-only mixed-mode qualification and compare to P0.
Do NOT proceed automatically to C60P45/C60P135, support carrier, shield/package, or active transistor.

Separate explicit solver authorization is required before this contract can execute.

## Pre-result mapping / receiver-shadow predicates

These are frozen before the solve result is viewed.

### R-MAP — virtual-ground mapping qualification
For each branch under pure differential incident excitation over 1.15–1.65 GHz:
- `max |2*Zbranch_A - Zdd| <= 1.0 ohm`;
- `max |2*Zbranch_B - Zdd| <= 1.0 ohm`;
- max relative error for each branch <= 1.0%.

Rationale: mapping uncertainty must remain at least an order of magnitude below the 10-ohm Gate-T support scale before `Zdiff/2` is used as a simplified receiver model.

### R-NF0 broadside shadow
Use the actual odd-mode branch source impedances from the solved two-port, not an assumed `Zdiff/2`, with the frozen QPL9547 G0 noise parameters.

Each branch must satisfy:
`NF_device_shadow <= 0.40 dB`
for every science-band sample.

This checks only source-conditioned device noise at P1. R-LOSS and integrated R-NF1 remain unqualified because physical feed/via/package loss is not yet present.

### Common-mode resonance diagnostic
Report max |Scc| and its frequency over the science band. No new pass/fail threshold is invented here; any near-unity or sharp common-mode resonance is escalated for design review before shield/carrier integration.
