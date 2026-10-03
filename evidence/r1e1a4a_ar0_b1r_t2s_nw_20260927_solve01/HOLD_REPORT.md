# AR0-B1R-T2S NW HOLD Report

Final status: **HOLD_R1E1A4A_AR0_B1R_T2S_NW_OUTPUT_PORT_MESH_CORRUPTION**

## Formal execution

- NW formal solver invocations: 1
- automatic retries: 0
- HF Frequency Domain solver started: yes
- adaptive mesh pass reached: 1
- S-parameters produced: no
- post-attempt CST SHA256: d50ce586e7e1bdfd21877aa6434b41189961ba600107679fdfd3e1f8f4acd2bd

## Root cause

NW HF Frequency Domain solver started and entered adaptive mesh refinement pass 1, but CST reported that Ports 2 and 3 had at least one endpoint not connected to a good conductor. The solver then failed with The mesh near lumped element "2" seems to be corrupted. The current P2/P3 discrete-port segment runs from the outer/front signal-copper surface n=+0.035 to the outer/back ground-copper surface n=-1.035, so the lumped-element line traverses the finite-thickness lossy copper sheets. CST explicitly warns that the element must not pass through PEC or lossy metal.

Native CST evidence:
- warning: Ports 2 and 3 have endpoint(s) not connected to a good conductor;
- error: mesh near lumped element 2 is corrupted;
- solver advice: the element must not pass through PEC or lossy metal.

## Recovery geometry

Do not change T1 copper or stalk geometry.

Keep Port 1 unchanged.

For Ports 2 and 3:
- move signal endpoint from n=+0.035 mm to n=0.0 mm;
- move local-ground endpoint from n=-1.035 mm to n=-1.0 mm;
- keep u, z, impedance and v=10-mm reference plane unchanged.

Then the discrete-port segment spans only the 1.0-mm FR4 thickness and terminates exactly on the signal/FR4 and ground/FR4 conductor interfaces.

This is a fixture-port build correction and requires a new BUILD-ONLY authorization before another solve.
