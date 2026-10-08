# R4-A0-E2C-S0 M6 Geometry Attribution Freeze V0.1

Status: FROZEN_M6_GEOMETRY_ATTRIBUTION

This node adopts the literature-style mechanism workflow used in high-isolation dual-polarized antennas: identify differential/common current paths and modal coupling first, then perturb only the structure associated with the suspected path.

Frozen diagnostic order:

1. M6-SIG — pre-CIN signal-copper attribution;
2. M6-GND — local-ground/backside/via attribution;
3. M6-INT — nearest signal-ground interaction attribution, only if needed.

Each future diagnostic build must preserve the E2C R7 radiator dimensions and must state a directional prediction for a frozen modal observable before execution.

A diagnostic result may reject a mechanism. It may not be used as an excuse for unconstrained geometry optimization.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
