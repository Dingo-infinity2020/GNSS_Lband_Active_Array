# R1A5F Split Single-Port BUILD-ONLY — Return Report

**FINAL_STATUS = PASS_R1A5F_SPLIT_SINGLE_PORT_BUILD_ONLY**

Mainline:
PROJECT_MAINLINE.md / M1 clean non-crossing feed.

Source HEAD:
b914822134ca6d3e2cc4cdca9de801e38d13863a

Host:
NW / DESKTOP-GBTI6Q4

CST:
2022.5

Formal invocation count:
1

Exit code:
0

Runtime:
113.17 s

Solver:
NOT RUN

## Immutable geometry provenance

R1A3 source:
D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst

SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

Both A and B pre-port copies were byte-identical to this source.

## Model A

Pol-A:
NE -> SW

Port count:
- build = 1
- fresh reopen = 1

CST:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst

SHA256:
74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce

Bytes:
48140

## Model B

Pol-B:
NW -> SE

Port count:
- build = 1
- fresh reopen = 1

CST:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLB_SINGLE_PORT_V01.cst

SHA256:
11ca4ae06baa1d3f18376789c90717f28aee2b02480d7eba88d2f5155d51a1bf

Bytes:
48171

## Geometry / symmetry

PASS:
- A geometry exactly equals R1A3 shape inventory.
- B geometry exactly equals R1A3 shape inventory.
- A/B geometry inventories are identical.
- B runtime endpoint tuple is exact Rz(+90 deg) rotation of A.
- both reference impedances = 100 ohm.
- each CST contains only one differential port.
- no port-port crossing remains.

## Engineering conclusion

The project now has two clean, deterministic, non-crossing passive-feed CST variants suitable for the short isolated-equivalence gate and later periodic/unit-cell development.

These artifacts do not directly provide simultaneous two-port S21 isolation. That metric remains deferred to a future physically meaningful multi-conductor/active feed model.

## Stop boundary

R1A5F build authorization is consumed.

Next stage:
R1A5FQ isolated-equivalence DESIGN ONLY.

No solver is authorized by this PASS.
No isolated optimization is authorized.
No periodic solve is authorized yet.
