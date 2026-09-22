# Execution Host Registry

Status: **ACTIVE**

This file registers the hosts used to execute this project's tools and records
the verified toolchain on each host.

It is infrastructure bookkeeping only. It does not change the mainline
architecture, gate permissions, or any scientific artifact.

Registering a host does not grant any permission that is not already defined in
`docs/PROJECT_RULES.md` and `AGENTS.md`. In particular, the ability to run CST
does not authorize a solver, optimizer, L-band scaling, or hardware release.

## Registered hosts

### H01 — DESKTOP-GBTI6Q4

| Item | Value |
|---|---|
| Role | Primary CST + Python execution host |
| Operator | Dingo-infinity2020 (local user `Administrator`) |
| OS | Windows 10 Pro, version 10.0.19045 |
| Git | 2.55.0.windows.3 |
| CST | CST Studio Suite 2022 (build 2022.5.0.0) |
| CST path | `D:\Program Files (x86)\CST Studio Suite 2022\CST DESIGN ENVIRONMENT.exe` |
| Python | Miniconda3, CPython 3.13.9 (Anaconda), 64-bit |
| Python path | `D:\Users\Administrator.DESKTOP-GBTI6Q4\Miniconda3\python.exe` |
| Repository | `D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold` |
| Local branch | `project/r0-charts-scaffold` -> `origin/project/r0-charts-scaffold` |
| Core line-ending | `core.autocrlf=false`, `core.eol=lf` (LF working tree) |

## H01 verification record

Verified on 2026-09-22 against commit `4760465`.

CST executable present and versioned:

```text
ProductName    : CST DESIGN ENVIRONMENT
ProductVersion : 2022, 5, 0, 0
```

Python gate checks (run with the Miniconda interpreter above):

```text
$ python scripts/r0_manifest_gate.py --stage topology
PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY

$ python scripts/audit_r0_topology_macro.py
PASS_R0_TOPOLOGY_MACRO_STATIC_AUDIT
EXPECTED_SOLIDS=9
EXPECTED_PORTS=0
SOLVER_RUN=NO
```

## H01 notes and limitations

- The default `python` on `PATH` is a Microsoft Store stub
  (`...\WindowsApps\python.exe`) that produces no output. Always invoke the
  Miniconda interpreter by full path, or activate the conda base environment
  first.
- CST build-only execution is a human GUI action: open a fresh MWS project and
  run `source/cst/R0_CHARTS_TOPOLOGY_BUILD_ONLY_V01.mcr` as a Structure Macro
  per `em/cst/R0_CHARTS_300_500/RUNBOOK_TOPOLOGY_BUILD_ONLY.md`.
- No solver, optimizer, or port creation is authorized during R0.

## Registration protocol

When a new host is used to execute project tools:

1. add a row/entry under "Registered hosts" with OS, tool paths, versions;
2. record the exact verification commands and PASS/HOLD output;
3. commit as an infrastructure change, separate from scientific artifacts;
4. do not infer elevated permissions from registration.
