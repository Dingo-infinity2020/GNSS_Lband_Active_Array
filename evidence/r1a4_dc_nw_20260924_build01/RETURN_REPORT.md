# R1A4 Differential Port BUILD-ONLY — NW/DC Return Report

**FINAL_STATUS = PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY**

- Task: R1A4-DIFFERENTIAL-PORT-BUILD-ONLY-DC-NW
- Host: NW / DESKTOP-GBTI6Q4
- Source HEAD: 80648b960d7d3ce91e6af99f52b9913637b1e820
- SimulationOps: 0.2.4
- CST: 2022.5
- Formal invocation count: 1
- Exit code: 0
- Runtime: 54.42 s
- Solver: NOT RUN
- CST251 staging: NOT PERFORMED

## Immutable geometry provenance

Reviewed R1A3 source SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

Fresh R1A4 copy before adding ports:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

Therefore the port build started from an exact byte-identical copy of the human-reviewed R1A3 CST.

## Port contract

Port 1 / Pol-A:
NE -> SW

Port 2 / Pol-B:
NW -> SE

Port 2 is the exact +90 degree rotational counterpart of Port 1.

Both:
- type SParameter;
- 100 ohm differential reference;
- terminal_r = 3.00 mm;
- terminal z = copper_top_z;
- no ground reference.

## Runtime audit

Build port count: 2
Fresh-reopen port count: 2

Geometry identity:
PASS — shape inventory is exactly unchanged versus R1A3.

Fresh-reopen geometry:
PASS.

## R1A4 CST artifact

Path:
D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

Bytes:
47220

Port macro SHA256:
19dd27589f980b5a7622c7ae6a7b3a422a08a4bb41353070eabd58408732bfec

## Stop boundary

R1A4 build authorization is consumed.

Next stage is R1A5 smoke-solve contract design.
No solve is authorized by this PASS.
