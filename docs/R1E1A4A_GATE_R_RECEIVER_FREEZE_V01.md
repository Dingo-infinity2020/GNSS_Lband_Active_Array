# R1E1A4A Gate R — Receiver/System Acceptance Freeze V0.1

Status: PRE-RESULT FREEZE FOR FUTURE R1E1A4B MECHANICAL/HUB CANDIDATES

Gate R supplements, and does not replace, Gate T.

Gate T asks whether a support can be treated as electromagnetically negligible.
Gate R asks whether the actual support/hub/source-impedance environment is acceptable to the first-stage receiver.

The current S1 result was viewed before Gate R existed, so it may be replayed for context but cannot be used to tune these limits.

## Budget authority

Existing project receiver requirements:
- reference receiver NF target <= 0.5 dB under relevant source impedances;
- stretch NF target <= 0.4 dB;
- pre-LNA passive loss must be minimized;
- stability must include source-impedance variation and common-mode behavior.

Gate-R numerical budgets are allocated before any new R1E1A4B candidate result:

### R-NF0 — source-conditioned device-noise shadow
For the G0 reference LNA model, nominal source-conditioned first-stage device NF must satisfy:
`NF_device_shadow <= 0.40 dB`
for every qualified core-scan state and every science-band sample in 1.15–1.65 GHz.

Rationale: use the existing project stretch target as the device/source-condition design target rather than allowing mechanics/mismatch to consume the full 0.5-dB system target.

### R-LOSS — passive loss before first gain
The passive P0-to-P1 feed/hub network must contribute no more than:
`IL_preLNA <= 0.05 dB`
across 1.15–1.65 GHz under nominal geometry.

Rationale: preserve a low-noise architecture and reserve the remaining 0.05 dB between 0.45 and the 0.5-dB system target for model error, device spread, temperature and manufacturing variation.

### R-NF1 — nominal integrated first-stage estimate
After combining source-conditioned device noise with modeled passive pre-LNA loss:
`NF_receiver_nominal <= 0.45 dB`
through the required band/core scan.

This is the primary nominal receiver gate.

### R-DNF — structure-induced noise penalty
For a candidate mechanical/hub structure relative to the same radiator/scan state at the same P1 definition:
`Delta NF_receiver <= +0.05 dB`
at every science-band sample.

Negative Delta-NF is allowed and is not interpreted as proof that the structure is globally superior.

### R-SCAN — scan robustness
The candidate must still satisfy R-NF1 independently at B0, C60P45 and C60P135; no averaging across scan states is allowed.

A later R1E2 atlas will extend this check to intermediate scan states.

## Stability gate

### R-STAB0 — intrinsic G0 two-port check
Traceable QPL9547 5-V/65-mA S-parameter data must satisfy in the modeled device reference:
- Rollet K > 1;
- mu > 1;
- mu-prime > 1;
- |Delta| < 1.

For the currently acquired de-embedded data these conditions are true throughout 1.15–1.65 GHz and also across the checked 0.1–6 GHz span. This is necessary but not sufficient for the assembled active antenna.

### R-STAB1 — assembled feedback stability
Before hardware release, the circuit + passive-EM hub/shield/output-routing model must show no unstable pole / right-half-plane pole over the modeled out-of-band range, with source/load variations covering the actual antenna and output interfaces.

A standalone LNA K/mu PASS cannot waive R-STAB1 because shield/ground/output-to-input coupling is outside the simple two-port device model.

## Mixed-mode integrity gate

These limits apply to the nominal symmetric passive P1A/P1B model before transistor insertion:
- `|Sdc| <= -30 dB` across 1.15–1.65 GHz;
- `|Scd| <= -30 dB` across 1.15–1.65 GHz;
- branch magnitude imbalance <= 0.20 dB;
- odd-mode branch phase imbalance from ideal 180 degrees <= 2 degrees.

These are nominal symmetry-integrity limits. A separate fabrication-tolerance study will later define relaxed as-built limits if needed.

## What Gate R does not authorize

Gate R does not select QPL9547 as final.
Gate R does not authorize a matching network.
Gate R does not authorize CST build/solve.
Gate R does not override Gate T.
Gate R does not permit post-result threshold relaxation.

## Entry to R1E1A4B

R1E1A4B may begin only after:
- H0/P1 geometry contract is frozen;
- QPL9547 reference S/noise data are audit-clean;
- mixed-mode build-only audit predicates are frozen;
- separate BUILD authorization is received.
