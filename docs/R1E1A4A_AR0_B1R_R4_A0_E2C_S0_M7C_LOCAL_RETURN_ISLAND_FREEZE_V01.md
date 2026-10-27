# M7C Local Return Island + Moat Freeze V0.1

Status: **PASS_M7C_OFFLINE_BUILD_CONTRACT_FROZEN_AWAIT_AUTH**

## First-principles purpose

M7B proved that removing the CIN-local backside reference almost eliminates branch asymmetry / differential-to-common conversion, but the same action creates a large symmetric differential-mode loading error. M7C therefore tests one and only one proposition:

> keep a branch-local RF return reference beneath the CIN/RFIN path, but stop that return node from being a broad low-impedance part of the surrounding/shared backside sheet.

This is a topology test, not a moat-width optimization.

## Parent

Canonical full E2C R7 build, not M7B. Starting from full E2C restores the copper that M7B removed and avoids any additive repair operation.

Parent SHA256:
`cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c`

## Frozen local geometry

For positive branches:
- retained island: u = 2.45..4.05 mm, v = 4.15..7.40 mm;
- moat outer envelope: u = 2.20..4.30 mm, v = 3.90..7.65 mm.

For negative branches the u coordinates are mirrored:
- retained island: u = -4.05..-2.45 mm;
- moat outer envelope: u = -4.30..-2.20 mm.

Moat width = 0.25 mm.

The retained island is the smallest simple local-u/v rectangle that contains both:
1. the tested M7B under-CIN region; and
2. the full projected EXPOSED_PADDLE / three-paddle-via return region.

Three paddle-via centers are at local u = 2.75, 3.25, 3.75 mm and v = 7.0 mm, with outer radius 0.175 mm. The minimum copper margin from a via annulus to the island edge is 0.125 mm.

The orthogonal backside-ground centerline contact occurs near |u| = 1.0, while the moat begins at |u| = 2.20. Therefore the retained M7C island cannot be directly shorted by the orthogonal-polarization backside sheet.

## Boolean implementation

Each branch uses four overlapping rectangular copper-clearance tools: upstream cap, downstream cap, low-u side and high-u side.

Per branch:
- outer rectangle area = 2.10 x 3.75 = 7.875 mm^2;
- retained island area = 1.60 x 3.25 = 5.200 mm^2;
- removed moat union area = 2.675 mm^2;
- parent copper thickness = 0.035 mm;
- expected copper volume removed = 0.093625 mm^3.

The cutter over-depth is 0.07 mm and is **not** used as the expected removed-material thickness.

## Invariants

Only the four `LOCAL_BACK_GROUND` solids may change. Final solid count remains 177 and raw-port count remains 24. Radiator, stalk dielectric, all signal copper, package lands, top local ground, all vias, bias/output copper and ports are unchanged.

No solver, monitor or port operation exists in the macro.

## Future solve hypothesis, frozen before BUILD

M7C should preserve the M7B suppression of Sdc / branch asymmetry while reducing the M7B Sdd penalty.

Primary symmetry gate:
`|Delta Sdc| <= 0.25 x full-E2C` at 1.2056, 1.2984, 1.3432, 1.5752 and 1.6496 GHz, both polarizations.

Primary differential-restoration gate:
`|Delta Sdd| <= 0.70 x M7B` at 1.3432, 1.5752 and 1.6496 GHz, both polarizations.

Secondary raw gate:
worst own-pol complex deviation over 1.15-1.65 GHz <= 0.6567025281.

Guard:
no new >6 dB off-diagonal excursion within <=50 MHz.

These gates are for a future separately authorized SOLVE. A successful BUILD does not authorize SOLVE.

## Current boundary

BUILD_AUTHORIZED = false.
SOLVE_AUTHORIZED = false.

Next legal action after host static qualification is one M7C BUILD-only transaction, but only after explicit user BUILD authorization.
