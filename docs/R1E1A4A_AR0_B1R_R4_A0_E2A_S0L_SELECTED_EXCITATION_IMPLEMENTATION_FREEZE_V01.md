# R4-A0-E2A-S0L Selected-Excitation Implementation Freeze V0.1

Status: STATIC PASS — BLOCKED BY E2A HUMAN 3D REVIEW  
Date: 2026-09-29  
SimulationOps minimum: 0.2.12

## 1. Authority

Solve contract:

`docs/R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_SOLVE_FREEZE_V01.md`

Protected E2A build SHA256:

`78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804`

Current project stage remains human 3D review.

No solve is authorized.

## 2. CST 2022 API route

The implementation uses documented CST 2022 VBA methods:

- `Port.Delete(int portnumber)`
- `Port.Rename(int oldportnumber, int newportnumber)`
- `FDSolver.Stimulation "List", "List"`
- `FDSolver.ResetExcitationList`
- `FDSolver.AddToExcitationList port, mode`

This avoids:
- rebuilding E2 geometry;
- artificial high-impedance open surrogates;
- six-source fallback;
- full 6x6 or 12x12 first-solve requirements.

## 3. Port-role reduction

Starting build ports: 1..12.

Delete in descending order:

`12, 11, 10, 6, 5, 4`

Remaining raw ports:

`1,2,3,7,8,9`

Rename:

- raw 7 -> solve 4
- raw 8 -> solve 5
- raw 9 -> solve 6

Final semantic solve ports:

1. A_E_UP — source
2. A_P_IN — source / device-input plane
3. A_P_OUT_LOAD50 — passive 50-ohm output load
4. B_E_UP — source
5. B_P_IN — source / device-input plane
6. B_P_OUT_LOAD50 — passive 50-ohm output load

No geometry/material object is changed.

The deleted audit-port copper pads remain physically present and open.

## 4. Selected excitation

Frequency-domain source type:

`Stimulation "List", "List"`

Excitation list:

- port 1 mode 1
- port 2 mode 1
- port 4 mode 1
- port 5 mode 1

Ports 3 and 6 are deliberately absent from the excitation list and remain 50-ohm S-parameter terminations.

No fallback to:
- `Stimulation "All","All"`
- source port 3
- source port 6

is permitted.

## 5. Frozen implementation sources

Configuration macro:

`source/cst/R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_CONFIG_V01.mcr`

Git blob:

`a42d59e0aa6dae84c0d6ff4b5bf20193a71a9bf5`

Presolve configuration runner:

`scripts/configure_r1e1a4a_ar0_b1r_r4_a0_e2a_s0l_presolve.py`

Git blob:

`ca520ccbc48fb56baf725c0216c3b32cd718af0c`

Formal solve runner:

`scripts/run_r1e1a4a_ar0_b1r_r4_a0_e2a_s0l_loaded_source_solve.py`

Git blob:

`9b944002dc65b5b21cad00c230ba041833c4de5e`

Qualified build inventory reused unchanged:

`execution/R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_BUILD_INVENTORY_V01.json`

Git blob:

`e10886a4c01d9aafd55a16d8126418b7e22025fd`

## 6. Static audit

Configuration macro:
- Port.Delete count = 6;
- Port.Rename count = 3;
- AddToExcitationList count = 4;
- exact sources = 1/2/4/5;
- ports 3/6 absent from excitation list;
- Stimulation List/List exactly once;
- no Stimulation All/All;
- no solver-start command;
- no Brick/Extrude/Cylinder/Solid.Add/Solid.Subtract geometry source.

Presolve runner:
- `run_solver()` count = 0;
- source SHA locked;
- exact 107-solid geometry signature required before/after configuration;
- exact six-port coordinate/50-ohm audit required;
- exact persistent selected-excitation History required;
- empty result tree required;
- configured-copy hash stability required.

Formal solve runner:
- `run_solver()` count = exactly 1;
- automatic retry = 0;
- source set = 1/2/4/5;
- load-only set = 3/6;
- response contract = 24 complex traces;
- no full 6x6 requirement;
- no full 12x12 requirement;
- source-side reciprocity only;
- power closure sums all six response rows for each of four source columns;
- native solver log is convergence authority.

Static audit result: PASS.

## 7. Runtime proof still required

Static PASS does **not** prove CST 2022 runtime behavior on this exact E2 artifact.

Before any formal solve invocation, a presolve configuration execution must fresh-reopen and prove:
- 107 geometry solids unchanged;
- six exact ports after delete/rename;
- exact coordinates and 50-ohm impedance;
- selected-excitation History persists exactly;
- result tree is empty;
- configured artifact hash is stable.

If port delete/rename or selected excitation behaves differently at runtime, HOLD before solver invocation.

## 8. Response contract

Formal required result:

24 complex traces:

`S(i,j)`

for:
- response rows i = 1..6;
- source columns j in {1,2,4,5}.

Required hard gates:
- 24/24 present on one common run/native grid;
- native final two DeltaS <= 0.02;
- source-side reciprocity among {1,2,4,5} <= 0.02;
- loaded column power sum over rows 1..6 <= 1.02;
- no fatal solver error;
- no mesh corruption.

## 9. Activation boundary

Current human-review dependency is unchanged.

After explicit E2A human 3D review PASS:

next local/runtime node:

`R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_PRESOLVE_CONFIG_AWAIT_AUTH`

That node configures a disposable solve copy only and runs no solver.

A separate explicit SOLVE authorization is still required for the formal S0L solve.

Current:
- BUILD_AUTHORIZED = false
- SOLVE_AUTHORIZED = false
- LNA_INTEGRATION_AUTHORIZED = false
