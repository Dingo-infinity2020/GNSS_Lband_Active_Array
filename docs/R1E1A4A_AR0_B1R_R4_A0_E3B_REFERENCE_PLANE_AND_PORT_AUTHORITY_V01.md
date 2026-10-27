# R4-A0-E3B Reference-Plane and Port Authority Review V0.1

Status: PASS — EXISTING E2C R7 PORT AUTHORITY RETAINED
Date: 2026-10-01
Execution: OFFLINE ONLY; no CST launch; no BUILD; no SOLVE.

## Purpose

Determine whether the accepted E2C R7 24-port raw EM interface requires redesign before coexistence-sentinel or active-co-simulation work.

## Frozen semantic map

R7 has four active branches:
A_P ports 1..6
A_N ports 7..12
B_P ports 13..18
B_N ports 19..24

Each branch exports:
1 E_UP
2 P_IN
3 P_OUT
4 E_DN
5 B_VDD
6 B_VBIAS

Device-lead planes are P_IN and P_OUT. The raw interface is single-ended and referenced to finite branch-local backside ground.## Source-level geometry audit

All 24 DiscretePort definitions were parsed directly from the frozen E2C macro.

Hard checks:
- port count = 24
- all port segment lengths = 1.000000 mm
- all port endpoints have identical z within each segment
- E_UP geometry is identical in radial/z coordinates across all four branches
- P_IN geometry is identical in radial/z coordinates across all four branches
- P_OUT geometry is identical in radial/z coordinates across all four branches
- E_DN geometry is identical in radial/z coordinates across all four branches

B_VDD and B_VBIAS use the frozen signed local-q locations, so + and - branches intentionally occupy different radial positions. Pol-A and corresponding Pol-B branch values are identical; no cross-polarization port drift was introduced by E2C coexistence assembly.

The 1 mm port segment and constant-z geometry are consistent with the stalk-PCB local-normal rule: the port crosses the 1 mm FR4 thickness from top signal node to local backside ground.

## Device-plane authority

The QPL9547 measured S/noise model is referenced at device leads. Therefore P_IN/P_OUT remain the correct EM/circuit partition.

No 100-ohm differential physical LNA port should be introduced. Differential/common-mode quantities are mathematical transforms of the single-ended network.## Sentinel reduction

The E2C coexistence sentinel may derive a 12-port solve copy from R7:
- retain E_UP and P_IN as sources
- retain P_OUT as 50-ohm matched load only
- remove E_DN, B_VDD, B_VBIAS ports
- leave the physical pads unchanged/open

This is a solver-network reduction, not a geometry/reference-plane redesign.

## Decision

PASS_E3B_R7_REFERENCE_PLANE_AND_PORT_AUTHORITY

No port redesign is required.
No corrective BUILD_ONLY is required.
R7 raw 24-port geometry remains the passive EM master interface.

For product-active authority, the next missing layer is not geometry but component/device-model authority and circuit reconnection.

Next offline node:
D0_QPL9547_DEVICE_AND_PASSIVE_COMPONENT_MODEL_AUTHORITY

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false