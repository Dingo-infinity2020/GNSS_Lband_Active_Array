# R1A5F Split Single-Port BUILD-ONLY Runbook

## Scope

Host: NW
CST: 2022.5
Mode: BUILD_ONLY

Create two separate single-port models from the same human-reviewed R1A3 geometry.

No solver is authorized.

## Immutable geometry source

D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst

Required SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

## Generated port sources

Model A:
source/cst/R1A5F_POLA_SINGLE_PORT_BUILD_ONLY_V01.mcr

Model B:
source/cst/R1A5F_POLB_SINGLE_PORT_BUILD_ONLY_V01.mcr

Both macros must exactly match the canonical generator:
scripts/generate_r1a5f_single_port_macros.py

Static audit:
scripts/audit_r1a5f_single_ports.py

## Formal execution

Fresh work:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work

Fresh evidence:
evidence/r1a5f_dc_nw_20260924_build01/

Expected CST artifacts:

A:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst

B:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLB_SINGLE_PORT_V01.cst

## Acceptance

For both A and B:
- pre-port copy hash equals R1A3 source hash;
- exactly one DiscretePort after build;
- exactly one port after fresh reopen;
- shape inventory exactly equals R1A3;
- no solver;
- fresh-reopen endpoint parameters persist.

Cross-model:
- A and B shape inventories identical;
- B endpoint tuple is exact Rz(+90 deg) rotation of A;
- same 100 ohm normalization;
- no simultaneous crossed ports exist in either model.

PASS:
PASS_R1A5F_SPLIT_SINGLE_PORT_BUILD_ONLY

## Stop boundary

Stop after build/fresh-reopen qualification.

Do not run the isolated equivalence solver in this gate.
Do not begin periodic/unit-cell work automatically.
