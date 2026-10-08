# R4-A0-E3C Ground-Return Topology Freeze V0.1

Status: CURRENT PASSIVE TOPOLOGY FROZEN / ASSEMBLED GROUND MERGE STILL OPEN
Date: 2026-10-01
Execution: OFFLINE ONLY.

## Purpose

Translate the accepted E2C R7 ground geometry into an explicit electrical topology.

The current passive EM block contains four first-stage branch-local RF ground nodes:
G_AP
G_AN
G_BP
G_BN

These correspond to A_P, A_N, B_P, and B_N branches.

They are intentionally not one common ideal ground.## Per-branch local ground node

Each G_branch contains:
- top exposed-paddle land
- five grounded side-pin lands connected by positive-area copper spokes
- C_RF ground pad
- three exposed-paddle plated vias
- one dedicated C_RF plated ground via
- finite backside LOCAL_BACK_GROUND

Grounded QPL9547 side pins represented on this node:
3, 4, 5, 6, 8.

Pins that remain separate:
1 Vbias
2 RF IN
7 RF OUT/VDD.

The exposed-paddle and side-ground copper therefore have a direct top-copper path to the four local via barrels, and the vias connect through the full 1.00-mm FR4 thickness to the branch-local backside ground.

Decision: each branch has a physically represented local RF return node suitable for the frozen single-ended port references.## Connections intentionally absent in E2C

The following galvanic merges are NOT present and must not be silently assumed:
- G_AP <-> G_AN
- G_BP <-> G_BN
- any Pol-A local ground <-> any Pol-B local ground
- local ground <-> radiator copper
- local ground <-> historical D2 remote lower-stalk common-ground network
- local ground <-> an unspecified shield/chassis/connector ground

The UnitCellGround/reference structure is not authority for the first-stage LNA return unless a later physical connection is explicitly modeled.

The old remote lower-stalk M0/M1 merge remains historical/sentinel evidence only.

## Circuit-domain shunt return

When the circuit layer is inserted, C_RF and other local decoupling connect B_VDD to the corresponding G_branch.

Each RF decoupler is intended to have its own short ground via/return. The 1-uF bulk element must not force the RF 100-pF return through a long shared path.## Scope boundary

For E2C coexistence-sentinel work, four finite independent branch-local ground nodes are intentional and adequate.

For full assembled active stability / hardware release, this is not the end of the ground problem.

Still open:
1. whether the +/- branch grounds within one polarization merge locally;
2. the physical G-L1 merge structure if used;
3. whether/where Pol-A and Pol-B ground systems merge;
4. connector/cable shield reference;
5. supply return and downstream-combiner ground path;
6. grounded shield/mechanical metal topology;
7. output-to-input feedback through those structures.

Any future merge that materially changes the EM return geometry requires an explicit physical model. It may not be replaced by an abstract ideal common-ground assumption for hardware-release stability authority.

## Decision

PASS_E3C_CURRENT_BRANCH_LOCAL_GROUND_TOPOLOGY

No corrective BUILD_ONLY is required for the E2C sentinel.

Future assembled-ground topology remains an explicit design variable and later EM/stability gate.

Next offline node:
E3D_NEXT_SIMULATION_QUESTION_AND_MINIMUM_NETWORK_FREEZE

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false