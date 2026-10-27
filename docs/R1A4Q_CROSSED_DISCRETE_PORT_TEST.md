# R1A4Q — Crossed Discrete-Port Topology Qualification

Status: FROZEN FOR ISOLATED TOY-MODEL SOLVE

## Motivation

R1A4 proved only that two crossed diagonal CST discrete ports can be created and survive fresh reopen.

CST 2022.5 local Help states that a discrete edge port consists of:
- a perfect conducting wire connecting its start and end points;
- a lumped element/source in the center of that wire.

The mesh representation is metallic wire except for the source element.

Therefore two diagonal discrete edge ports that geometrically intersect at the center may create an unintended conductive connection or other numerical artifact.

This must be qualified before any GNSS antenna solver is authorized.

## Scope

This is NOT an antenna solve.

No R1A3/R1A4 production CST file is opened for solver execution.

Two fresh toy models are created from source code:

A — CROSS
- four isolated PEC pads in a square;
- Port 1 connects NE to SW;
- Port 2 connects NW to SE;
- both discrete-port wires geometrically intersect at the center.

B — LIFTED_REFERENCE
- same four isolated PEC pads;
- Port 1 remains NE to SW at pad level;
- two short PEC vertical posts lift NW and SE terminals;
- Port 2 connects the lifted terminals above Port 1;
- port lines cross only in XY projection, not in 3D.

## Diagnostic logic

The models intentionally have no physical conductive path between the two port pairs other than any path introduced by the discrete-port representation itself.

Compare:
- S11/S22;
- S21/S12;
- solver warnings;
- result existence.

A large/direct coupling unique to CROSS is evidence that the crossed-port topology is unsafe.

Even if CROSS appears numerically benign, the official metallic-wire representation remains a modeling concern. R1A4 production ports will not be promoted to science use solely from this toy test.

## Authorization boundary

Authorized:
- NW only;
- two tiny fresh CST toy projects;
- HF frequency-domain solver;
- 0.5–2.0 GHz;
- no adaptive mesh;
- no optimization;
- no production geometry;
- no CST251.

Not authorized:
- any solver run on R1A4 GNSS CST;
- any geometry change to R1A4 GNSS CST;
- R1A5 antenna smoke solve.

Allowed return:
- PASS_R1A4Q_CROSSED_PORT_NOT_DIRECTLY_SHORTED
- HOLD_R1A4Q_CROSSED_PORT_UNSAFE
- HOLD_R1A4Q_TEST_INCONCLUSIVE
- FAIL_R1A4Q_RUNTIME
