# SIM_EXECUTION

## Global protocol

- SimulationOps version: 0.2.4
- Build host: NW
- Simulator: CST Studio Suite 2022.5
- Runtime: CST bundled Python 3.6 / cst.interface
- Solver host: not authorized for current stage

## Current model

Model identity:
CHARTS_GNSS_R1A4_DIFFERENTIAL_PORT_V01

Stage:
BUILD_ONLY_R1A4

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: false

## Immutable geometry source

R1A3 reviewed CST:
D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst

SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

R1A4 harness must copy this file and verify its hash before adding ports.

## Port freeze

- Port 1 / Pol-A: NE -> SW
- Port 2 / Pol-B: NW -> SE
- exact +90 degree rotational relation
- terminal_r = 3.00 mm
- terminal z = copper_top_z
- reference impedance = 100 ohm per differential port
- port type = SParameter
- ground reference = none

## Build artifact

D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

Evidence:
evidence/r1a4_dc_nw_20260924_build01/

PASS:
PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY

## Hard stop

- no geometry changes
- no solver
- no frequency sweep
- no monitors
- no optimization
- no CST251 staging

Fresh reopen + port count + geometry identity is the stop boundary.
