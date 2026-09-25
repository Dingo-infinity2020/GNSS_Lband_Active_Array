# R1E1A4A Mixed-Mode Reference-Plane BUILD-ONLY Contract — Draft

Status: BUILD CONSUMED — CANONICAL PASS VIA READ-ONLY RECOVERY; SOLVE NOT AUTHORIZED

## Purpose

Create the smallest passive CST model that can test the new P1A/P1B receiver reference plane without conflating it with mechanical-support optimization or active-device physics.

This is a reference-plane qualification model, not a production active-hub model.

## Frozen parent

Use the qualified bare P094 periodic source lineage.

Parent source hash:
`fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e`

Do not use the S1 support-inclusive source for this reference-plane gate.

## H0-RP1 geometry

Keep unchanged:
- radiator / substrate / top copper;
- 94-mm periodic cell and main backplane;
- 57.142857-mm radiator-substrate bottom height;
- all slot geometry;
- all science-band / boundary settings.

Remove the existing one-port Pol-A differential excitation.

Add one centered underside local-ground island:
- square PEC/copper footprint: 10.0 x 10.0 mm;
- centered at x=y=0;
- located directly on the underside of the 1.00-mm radiator substrate;
- use the project copper thickness for the first geometry baseline.

Do not add package, bias, output trace, shield or support geometry in this model.

## P1 port abstraction

Create exactly two 50-ohm single-ended discrete ports for Pol-A:
- P1A at the NE terminal center (+2.12132,+2.12132), from top terminal copper vertically to the H0 local ground;
- P1B at the SW terminal center (-2.12132,-2.12132), from top terminal copper vertically to the same H0 local ground.

The two ports must be exact 180-degree geometric partners.

Mixed-mode interpretation:
- each single-ended reference impedance = 50 ohm;
- differential mixed-mode reference impedance = 100 ohm;
- common-mode reference impedance follows the standard two-port mixed-mode transform.

Do not add Pol-B ports during this first Pol-A mapping gate.

## BUILD-ONLY audit

Required:
- parent hash verified before copy;
- one local-ground object with exact 10.0 x 10.0 mm footprint;
- exactly two ports, each 50 ohm;
- exact port coordinates and opposite-pair symmetry;
- 94-mm unit-cell metadata unchanged;
- radiator/substrate/top-copper object inventory unchanged except removal of the original one-port excitation;
- no support geometry;
- no shield / package / bias / output geometry;
- no solver result tree;
- no solver markers;
- fresh reopen reproduces all predicates.

One formal build invocation only. No silent retry.

## Later solve qualification — NOT AUTHORIZED BY THIS CONTRACT

After a separate solver authorization, first solve broadside only.

Required read-only derived quantities:
- 2-port S/Z matrix at P1A/P1B;
- mixed-mode Sdd, Scc, Sdc, Scd;
- differential Zdd;
- per-branch impedance under odd-mode excitation;
- local-ground current / field diagnostics if available.

Comparison:
- compare Zdd/Sdd against the existing P0 broadside result, but do not demand equality because the newly introduced local-ground island is a real EM object;
- test whether `Z_branch = Zdd/2` is numerically valid in the nominal symmetric model;
- apply the frozen mixed-mode integrity portion of Gate R.

Stop after broadside mapping. Do not add support candidates until the reference-plane model is qualified.
