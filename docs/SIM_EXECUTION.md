# SIM_EXECUTION

## 1. Global Protocol

- Repository: `Dingo-infinity2020/SimulationOps`
- Protocol: `GLOBAL_DC_SIMULATION_PROTOCOL.md`
- Protocol version used: `0.2.8`
- Minimum compatible version: `>=0.2.8`
- Host registry: `infrastructure/HOSTS.md`
- Workspace lifecycle: `WORKSPACE_LIFECYCLE.md`
- DC call policy: `DC_CALL_EFFICIENCY.md`

## 2. Project Identity

- Project: GNSS_Lband_Active_Array
- Model identity: H3B-T01A post-O2B physical-fidelity closure
- Repository: `Dingo-infinity2020/GNSS_Lband_Active_Array`
- Source branch: `project/r0-charts-scaffold`

## 3. Current stage

`R1E1A4A_H3B_T01A_O3_PHYSICAL_FIDELITY_QUALIFICATION_AUTHORIZED`

- BUILD_AUTHORIZED: true
- SOLVE_AUTHORIZED: true
- O2C: DEFERRED_CONTINGENCY_ONLY
- T01-C: DEFERRED
- O3 status: AUTHORIZED_NOT_YET_EXECUTED
- O4 status: AUTHORIZED_NOT_YET_EXECUTED

## 4. Proven state

O2B = `PASS_R1E1A4A_H3B_T01A_O2B_ACCEPTABLE`

Winner: `P20_G30_E30`
- Wsig = 1.50 mm
- Gcpw = 0.40 mm
- signal pad width = 2.00 mm
- pad gap = 0.30 mm
- transition extension = 0.30 mm
- worst core return = -14.3819 dB
- max junction excess = 0.0639 dB
- solved SHA256 = `c80b704a257d9ead11c3465d43b907f1575708621d6f1a17a564c752f2b93bc7`

Authoritative route: `docs/R1E1A4A_POST_O2B_ROUTE_FREEZE_V02.md`

## 5. Toolchain / routing

- Build control host: NW
- CST build tool: CST Studio Suite 2022 bundled Python/API
- Solve routing: use project runner; NW is control plane and may orchestrate CST251/CST251-C through the verified Git OpenSSH route when a formal production solve is launched.
- XW: not required for O3/O4.
- GUI: not required unless deterministic API fails.

## 6. Workspace lifecycle

- Current state: CHECKPOINTED before O3 execution
- O2B task node: closed in Git; solver artifacts remain recoverable/protected as recorded evidence.
- O3/O4 workspaces must be closed out at PASS/HOLD.
- Dirty/untracked/unpushed work must not be deleted.
- Large solver results stay protected in place; Git stores only compact evidence/provenance.

## 7. DC call budget

- Preferred O3 task packet: `execution/task_packets/R1E1A4A_H3B_T01A_O3_task.json`
- Preferred O4 task packet: `execution/task_packets/R1E1A4A_H3B_T01A_O4_task.json`
- O3 result packet: `execution/result_packets/R1E1A4A_H3B_T01A_O3_result.json`
- O4 result packet: `execution/result_packets/R1E1A4A_H3B_T01A_O4_result.json`
- Target DC calls per routine stage: 2
- Long-run polling policy: launch once; inspect only at task node or explicit user status request
- GitHub/SimulationOps evidence must be checked before DC.
- Do not use command-by-command DC exploration when a stage runner can batch the work.

## 8. Stop boundary

O3:
- PASS -> O4 may execute under the already granted authorization.
- HOLD -> stop; preserve evidence; do not start O4.

O4:
- PASS -> create T01-A FREEZE package and stop before H3B-I01 unless separately authorized.
- HOLD -> stop; preserve evidence.

No O2C nominal optimization is authorized.
