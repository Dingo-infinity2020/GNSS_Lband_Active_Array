# R1E1A4A Receiver Shadow + Interface Freeze Plan

Status: DESIGN / CIRCUIT ANALYSIS ONLY — NO CST BUILD OR SOLVER AUTHORIZATION

## Purpose

Before spending more full-wave solves on support geometry, define the electrical interface that matters to the final active receiver.

The project must stop asking only:
"How little does the support move the bare antenna impedance?"

and additionally ask:
"Given the complete scan-dependent source impedance, what noise / gain / stability environment does each first-stage LNA actually see?"

R1E1A4A does not select the final LNA and does not integrate a transistor into CST.

Reference-plane / co-simulation authority:
`docs/R1E1A4A_REFERENCE_PLANE_AND_COSIM_SPEC.md`.

## Reference planes to freeze

P0:
antenna differential terminal plane used by the current periodic CST source.

P1A / P1B:
the two single-ended first-stage LNA input reference planes for one polarization.

The mainline architecture is:
balanced radiator -> LNA-A and LNA-B -> post-gain combining / differential handling.

Do NOT assume blindly that each LNA sees Z_diff/2.

That relation is valid only under an explicitly qualified symmetric / virtual-ground condition with negligible common-mode excitation at the chosen reference planes.

R1E1A4A must document:
- local-ground definition;
- common-mode reference;
- terminal polarity;
- any series feed geometry between P0 and P1A/P1B;
- whether the ideal differential CST port can be mapped analytically or whether a later mixed-mode multiport EM model is required.

## QPL9547 G0 receiver shadow

Use QPL9547 as the first reference device because traceable in-band noise parameters are available.

Reference data:
`circuit/qpl9547/QPL9547_NOISE_REFERENCE_1P1_1P7.csv`

Required calculations:
- GammaOpt(f);
- Zopt(f);
- NFmin(f);
- Rn(f);
- source-reflection coefficient seen at each LNA;
- noise factor using the standard four-noise-parameter relation;
- mismatch / available-gain or transducer-gain proxy using the available S-parameter model;
- source/load stability checks over the actual impedance locus.

The current `illustrative_2xzopt` column is context only. It is not a frozen differential target.

## Existing data to replay before any new support result exists

At minimum evaluate:
- bare P094 B0;
- bare P094 C60P45;
- bare P094 C60P135;
- S1 bonded B0 qualified recovery result;
- S1 bonded C60P45 qualified result;
- S1 bonded C60P135 qualified numerical result despite Gate-T failure.

Purpose:
determine whether the 15.09-ohm C60P135 support shift is:
- harmful to receiver noise;
- nearly neutral at receiver level;
- or accidentally beneficial to the reference LNA match.

This analysis must not retroactively change Gate T.

## Gate R freeze

Before any R1E1A4B candidate result is viewed, freeze system-level acceptance limits for:
- maximum added receiver noise / NF penalty relative to the chosen G0 reference;
- scan-to-scan noise spread;
- mismatch / gain degradation;
- source-conditioned stability;
- allowable passive loss before first gain;
- polarization / branch-balance requirement where supported by the model.

Numeric Gate-R limits must come from the project receiver/noise budget, not from fitting the current S1 result.

## Mechanical architecture freeze performed in the same stage

Prepare dimensioned, manufacturable concept envelopes for:
- M0 bonded low-density foam reference;
- M1 serviceable PTFE-class / characterized dielectric standoff;
- M2 structural active-hub / vertical-PCB support;
- M3 optional grounded-metal intentional-RF architecture.

For M2, define a passive geometry envelope now for:
- PCB thickness / orientation;
- attachment points;
- local ground;
- eventual RF shield envelope;
- LNA keepout / package region.

Do not add active transistor behavior to CST in R1E1A4A.

## Exit condition

R1E1A4A closes only when:
- P0/P1A/P1B are unambiguous;
- QPL9547 reference shadow is reproducible;
- existing S0/S1 states have receiver-shadow metrics;
- Gate R is frozen;
- M0/M1/M2 geometry envelopes are ready for later build-only.

Only then request authorization for R1E1A4B C60P135 builds/solves.

## Preliminary ideal-odd-mode diagnostic already completed

A deliberately non-authoritative diagnostic assumed `Z_branch = Z_diff/2` and no P0-to-P1 feed transformation/loss, then applied the QPL9547 noise-parameter model to existing bare and S1 states.

Under this assumption:
- B0 support-induced max |Delta NF| ~0.0145 dB (~1.03 K);
- C60P45 ~0.00205 dB (~0.146 K);
- C60P135 ~0.00787 dB (~0.564 K), with the largest signed change slightly improving NF.

This does not freeze Gate R. It demonstrates only that the 15.09-ohm differential-impedance Gate-T failure does not automatically imply a comparable receiver-noise penalty.

Evidence/analysis:
`circuit/qpl9547/analysis/R1E1A4A_IDEAL_ODDMODE_DIAGNOSTIC.md`.
