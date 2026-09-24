# SIM_EXECUTION

## Global protocol

- SimulationOps: Dingo-infinity2020/SimulationOps
- protocol version: 0.2.4
- host registry: infrastructure/HOSTS.md
- workspace lifecycle: WORKSPACE_LIFECYCLE.md
- adoption commit: 45fcb8c89445f05a696cde524d762641ea7ea961

## Project state

- Project: GNSS L-band Active Array
- Current model identity: CHARTS_GNSS_R1A4_DIFFERENTIAL_PORT_V01
- Source branch: project/r0-charts-scaffold
- Current stage: DESIGN_R1A4_DIFFERENTIAL_PORT
- BUILD_AUTHORIZED: false
- SOLVE_AUTHORIZED: false
- Last completed stage: HUMAN_REVIEW_R1A3
- Last status: PASS_R1A3_HUMAN_REVIEW

## Immutable geometry source

Reviewed R1A3 CST:
D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst

SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

R1A4 must copy this artifact into a fresh work directory. It must not rebuild or overwrite R1A3 geometry.

## Planned R1A4 build host

- Build host: NW
- Simulator: CST Studio Suite 2022.5
- Runtime: CST bundled Python 3.6 / cst.interface
- Solve host: none at this stage
- Solver: forbidden

## Planned gate

R1A4 build-only shall prove:
- exactly 2 discrete differential ports;
- 100 ohm reference per differential port;
- Pol-B is +90 degree rotation of Pol-A;
- fresh reopen preserves port count;
- shape inventory is unchanged from reviewed R1A3;
- no solver is started.

Until the source bundle and static audit are frozen, BUILD_AUTHORIZED remains false.
