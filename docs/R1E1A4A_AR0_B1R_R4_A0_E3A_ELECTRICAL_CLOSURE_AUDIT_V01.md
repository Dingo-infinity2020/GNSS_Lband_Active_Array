# R4-A0-E3A Electrical Closure Audit V0.1

Status: PASS FOR E2C COEXISTENCE SENTINEL ELIGIBILITY / NOT PRODUCT-ACTIVE AUTHORITY
Date: 2026-10-01
Execution: OFFLINE ONLY; no CST launch; no BUILD; no SOLVE.

## Scope

Audit the accepted E2C R7 dual-polarization geometry after automated BUILD_ONLY PASS and human 3D geometry review PASS.

Canonical E2C R7 SHA256:
cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c

Human geometry review:
PASS_E2C_R7_HUMAN_GEOMETRY_REVIEW

R7 contains 177 solids, 24 raw single-ended ports, 16 plated ground vias, and four active branches: A_P, A_N, B_P, B_N.

## Physical RF path closure

The pre-E2 parent preserves, for all four branches:
radiator terminal -> RF tenon -> RF tongue copper -> solder bridge.

E2A/E2B freeze the continuation:
solder/tongue region -> upstream MSL -> upstream taper -> C_IN upstream pad (E_UP plane).

E2B changes only the frozen N-branch backside-ground half-lap clearance notch and does not alter signal/top-ground geometry. E2C combines the proven A/B donor geometries without RF retuning.

Decision: PASS. No corrective signal-path BUILD_ONLY is required before the E2C coexistence sentinel.## Local RF ground closure

For every branch the frozen geometry contains finite branch-local LOCAL_BACK_GROUND, top local-ground copper around the exposed paddle, five grounded package-side spokes, three plated paddle vias, and one dedicated C_RF ground via.

Each plated via passes through the real branch-prong FR4 and connects the top local-ground system to the branch-local backside-ground representation.

Frozen prohibitions remain: no ground-to-radiator galvanic contact, no D2 remote common-ground merge, and no silent A/B or +/- branch local-ground bridge.

Decision: PASS for the branch-local reference ground required by the passive EM model. This does not assert that final hardware grounds must remain branch-isolated forever.

## Raw port/reference-plane closure

R7 exports 24 single-ended 50-ohm raw ports:
A_P 1..6; A_N 7..12; B_P 13..18; B_N 19..24.

Per branch the six nodes are:
1 E_UP; 2 P_IN; 3 P_OUT; 4 E_DN; 5 B_VDD; 6 B_VBIAS.

Each port follows the frozen conductor-interface rule: signal endpoint at local n=0, local-ground endpoint at local n=-1 mm, through FR4 only.

The QPL9547 device-lead planes are P_IN and P_OUT. These are the correct planes for later insertion of the measured QPL9547 S/noise model. No physical 100-ohm differential LNA port is required.

Decision: PASS. The existing 24-port interface is deliberate co-simulation infrastructure and should not be replaced by a two-port simplification.## Intentional circuit-domain discontinuities

The passive EM geometry intentionally does not close these components inside CST:
- C_IN: E_UP <-> P_IN
- QPL9547: P_IN <-> P_OUT
- C_OUT: P_OUT <-> E_DN
- L1: P_OUT <-> B_VDD
- C_RF / bulk decoupling: B_VDD <-> local ground
- R4 / bias network: B_VDD <-> B_VBIAS

Therefore the raw CST block is not a literal continuous active receiver chain. This is by design.

Consequences: bare-CST return loss is not product input-match authority; QPL9547 source impedance is not product authority until qualified circuit-domain components are inserted; no additional BUILD_ONLY is justified merely to close these intentional gaps.

## E2C coexistence sentinel eligibility

The frozen combined-sentinel contract reduces the raw 24-port build network to 12 solve ports. Per branch it retains E_UP and P_IN as sources and P_OUT as a 50-ohm matched load. E_DN, B_VDD, and B_VBIAS are removed from the solve copy while their physical pads remain open.

With E2C R7 BUILD_ONLY PASS, human geometry review PASS, and this offline electrical-closure audit PASS, the geometry/reference-plane prerequisites for that sentinel are satisfied.

This document does not authorize SOLVE.

## Decision

PASS_E3A_E2C_R7_ELECTRICAL_CLOSURE_FOR_SENTINEL

No corrective BUILD_ONLY is required by E3A. R7 remains the geometry baseline.

Next offline node: E3B_REFERENCE_PLANE_AND_PORT_AUTHORITY_REVIEW

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false