# SIM_EXECUTION

## Authority

- Mainline: PROJECT_MAINLINE.md
- SimulationOps: 0.2.4

## Current stage

R1A5F_SPLIT_SINGLE_PORT_BUILD_ONLY

BUILD_AUTHORIZED: true
SOLVE_AUTHORIZED: false
PRODUCTION_SOLVE_AUTHORIZED: false

## Host/toolchain

Host: NW
CST: 2022.5
Runtime: CST bundled Python 3.6 / cst.interface
Mode: BUILD_ONLY

## Immutable source

D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst

SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

## Models

A:
- Pol-A
- NE -> SW
- one 100 ohm differential port

B:
- Pol-B
- NW -> SE
- exact +90 deg rotation of A
- one 100 ohm differential port

Both are generated from one canonical endpoint definition.

## Paths

Work:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work

Evidence:
evidence/r1a5f_dc_nw_20260924_build01/

## Hard stop

- no solver
- no frequency configuration
- no far-field monitors
- no material changes
- no geometry changes
- no optimization
- no periodic boundary work

Fresh reopen + one-port persistence + geometry identity + runtime rotational symmetry is the stop boundary.
