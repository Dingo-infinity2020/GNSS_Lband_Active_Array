# R4-A0-E1 One-LNA Passive EM Port Contract V0.2

Status: SIX-NODE TOPOLOGY + LOCAL ENDPOINT RULE FROZEN

Supersedes V0.1 five-node topology.

## Six exported single-ended nodes

All normalized to 50 ohm and referenced to the finite branch-local backside ground.

1. E_UP
   upstream side of C_IN

2. P_IN
   QPL9547 pin-2 RF-IN device-lead node

3. P_OUT
   QPL9547 pin-7 RF-OUT/VDD device-lead node

4. E_DN
   downstream side of C_OUT

5. B_VDD
   VDD side of L1 / decoupling node

6. B_VBIAS
   QPL9547 pin-1 bias node

## Circuit connections

C_IN:
E_UP <-> P_IN

QPL9547 S2P:
P_IN <-> P_OUT

C_OUT:
P_OUT <-> E_DN

L1:
P_OUT <-> B_VDD

C_RF:
B_VDD <-> ground

C_BULK:
B_VDD <-> ground

R4:
B_VDD <-> B_VBIAS

The 5-V / 65-mA active operating point remains embedded in the QPL9547 measured S2P/noise model.

## Local endpoint rule

For every node port at local (q,v):

signal endpoint:
(q,v,n=0.0)

ground endpoint:
(q,v,n=-1.0)

The port segment lies only through FR4.

This is the corrected conductor-interface rule established after the earlier output-port mesh-corruption incident.

## Frozen nominal node locations

E_UP:
q=0
v=4.650 mm
node ownership = C_IN upstream pad

P_IN:
q=0
v=6.085 mm
node ownership = QPL9547 pin-2 land / downstream input trace

P_OUT:
q=0
v=7.915 mm
node ownership = QPL9547 pin-7 land / RF-output fan

E_DN:
q=0
v=9.350 mm
node ownership = C_OUT downstream pad

B_VDD:
q=+1.45 mm
v=9.80 mm
node ownership = L1/C_RF VDD interconnect

B_VBIAS:
q=-0.50 mm
v=6.085 mm
node ownership = pin-1 bias land

Exact coordinates may move only through a new placement-contract revision before build.

## No differential port

No 100-ohm differential port exists in A0-E1.

Differential/common-mode quantities belong to the later twin-LNA integrated EM/circuit model.

## Port-count acceptance

Build-only:
exactly 6 ports after fresh reopen.
Result tree empty.
Solver count 0.
