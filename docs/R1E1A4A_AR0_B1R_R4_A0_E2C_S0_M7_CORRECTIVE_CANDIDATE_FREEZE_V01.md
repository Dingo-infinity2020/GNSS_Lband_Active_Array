# R4-A0-E2C-S0 M7 Corrective Candidate Freeze V0.1

Status: **FROZEN — AWAIT BUILD AUTHORIZATION**

M6 established:
- pre-CIN signal-only perturbation is WEAK;
- ground/backside/via-only perturbation is INTERMEDIATE;
- ground-only frequency shape is not a scaled copy of the full severe coexistence state;
- the working physical picture is a composite return-path / signal-ground interaction.

M7 deliberately freezes only two corrective candidates. No parameter sweep is allowed.

## M7A — INNER_EDGE_UPSTREAM_SETBACK

Change only the four backside branch-local grounds.

For each positive branch, remove local u=1.0..1.5 mm over v=3.0..5.0 mm.
For each negative branch, remove local u=-1.5..-1.0 mm over v=3.0..5.0 mm.

The frozen upstream MSL inner edge is at |u|=2.05 mm. Therefore the modified backside ground still extends to |u|=1.50 mm and retains 0.55 mm of center-side ground overhang beneath the signal. Outer ground edge, signal copper, CIN pad, package ground, spokes and vias remain unchanged.

Physical question:
Does the center-facing backside-ground edge provide a necessary near-field coupling surface for the composite mode?

Prediction:
If yes, full-E2C common-mode degradation and branch imbalance in the 1.2–1.4 GHz severe region should fall without a large unrelated resonance.

Falsification:
If diff/common degradation and imbalance stay within 10% of the full-E2C severe values, this edge-overlap mechanism is not the useful corrective lever.

Pre-registered success:
- >=30% reduction in BOTH E_UP diff-to-common degradation and branch-return imbalance at frozen severe anchors;
- secondary: >=20% reduction in maximum source-side complex deviation;
- no new >6 dB narrow excursion within <=50 MHz.

## M7B — CIN_PAD_PROJECTION_CLEARANCE

Keep the backside-ground perimeter unchanged.

Under every frozen CIN_UP_PAD, open an exact projection window with 0.25 mm guard:
- positive branch: u=2.45..3.55 mm, v=4.15..5.15 mm;
- negative branch: u=-3.55..-2.45 mm, v=4.15..5.15 mm.

The window is 1.10 x 1.00 mm. It does not reach the paddle-via or CRF-via regions. Upstream MSL ground remains present.

This implements the earlier H1C shaped/perforated-ground principle in the smallest current geometry: remove ground under a terminal/contact projection rather than optimize an arbitrary ground shape.

Physical question:
Is local CIN signal-to-return shunt capacitance a necessary resonant element in the composite mode?

Prediction:
If yes, the full-E2C ~1.3432 GHz raw-deviation peak and 1.2–1.4 GHz diff/common degradation should fall.

Falsification:
If the raw peak and diff/common degradation remain within 10% of full E2C, CIN-local shunt capacitance is not the controlling corrective lever.

Pre-registered success:
- >=30% reduction of source-side complex deviation around the frozen raw-peak neighborhood;
- >=6 dB reduction of E_UP diff-to-common degradation in 1.2–1.4 GHz;
- secondary: >=30% reduction of branch imbalance at 1.2984 GHz;
- no new >6 dB narrow excursion within <=50 MHz.

## Common BUILD contract

Parent is the frozen full-E2C R7 canonical BUILD_ONLY artifact, SHA256:
cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c

Each candidate:
- starts from the same parent;
- modifies only the four LOCAL_BACK_GROUND solids;
- uses four disposable clearance tools;
- must consume all four tools;
- expected final solids remain 177;
- expected raw ports remain 24;
- no port, material, signal, package, via, bias, radiator or solver mutation;
- requires fresh reopen and human geometry review;
- stops before SOLVE.

Default future order: **M7A BUILD first**. M7B remains unbuilt until separately authorized.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
