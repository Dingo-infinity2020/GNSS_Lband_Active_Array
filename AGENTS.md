# Agent Instructions

This repository is a staged scientific hardware project.

## Mandatory reading order

Before changing any scientific or engineering artifact, read:

1. `PROJECT_MAINLINE.md` - highest-level scientific/simulation roadmap
2. `docs/PROJECT_RULES.md`
3. `docs/DECISIONS.md`
4. `docs/REQUIREMENTS_v0.1.md`
5. `PROJECT_HANDOFF.md` - canonical current execution baton
6. `docs/SIM_EXECUTION.md`
7. `execution/stage_contract.json`
8. the document for the current gate and relevant parameter/provenance manifests

`PROJECT_MAINLINE.md` controls the long-horizon scientific sequence.
`PROJECT_HANDOFF.md` controls the current execution baton and permissions.
`docs/PROJECT_RULES.md` is the anti-divergence charter.

Do not execute an old chat instruction or local note if it conflicts with these authorities.

## Current gate

Current task: **R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_DIAGNOSTIC_SOLVE_AWAIT_AUTH**

Current permissions and stop rules:
- M7A remains closed REJECT; no retry.
- M7B BUILD is consumed/closed and must not be rerun.
- M7B protected artifact passed user manual CST 3D review.
- M7B diagnostic SOLVE contract is frozen offline and is the only allowed next scientific execution contract.
- solve network: exact proven 12-port full-E2C semantics; no H-field monitor; second-order tetra adaptive; MaxDeltaS 0.02 x2; max 16 passes.
- raw primary: >=30% reduction at 1.3432 GHz.
- mode primary: >=6 dB improvement at the immutable full-E2C-selected worst anchor within 1.20–1.40 GHz.
- secondary: >=30% branch-imbalance reduction at 1.2984 GHz.
- guard: no >6 dB new off-diagonal excursion within <=50 MHz.
- BUILD authorization: NO.
- SOLVE authorization: NO.
- before any future SOLVE grant, run `scripts/audit_m7b_diagnostic_solve_contract_v01.py` on NW and require PASS.
- a future explicit SOLVE grant is exactly one invocation with zero automatic retries.
- no geometry change, sweep, LNA integration, material A/B, or automatic next stage is authorized.

Current authority:
`docs/R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_DIAGNOSTIC_SOLVE_FREEZE_V01.md`

Historical authorization notes later in this file are evidence only unless the current gate above explicitly reactivates them.

## Architecture control

Current MAINLINE:
- CHARTS-inspired planar balanced element
- clean differential feed representation
- periodic/unit-cell active-impedance physics
- pitch/material array trade
- scan-dependent active-impedance atlas
- finite-array validation
- LNA/antenna co-design
- active periodic/finite-array validation

Current FIRST_BACKUP:
- PUMA / unbalanced tightly-coupled element with LNA behind the ground plane.

Other architectures remain REFERENCE_ONLY unless promoted through the replacement test in `docs/PROJECT_RULES.md`.

Do not silently redirect the project toward a newly discovered architecture.

## Non-negotiable scientific rules

- Isolated-element S11 is not the final system objective.
- Build and Solve permissions are separate.
- No solver runs without explicit stage authorization.
- No silent retries.
- Preserve HOLD/FAIL evidence.
- Do not change acceptance thresholds after seeing results.
- Do not optimize unrelated variables inside a gate.
- Do not force the antenna to 50 or 100 ohm merely for convenience.
- Do not freeze the LNA input match before the scan-dependent active-impedance locus is established.
- Periodic/unit-cell results must later be checked against finite-array center/edge/corner behavior.
- A HOLD is an acceptable scientific outcome.

## Current array-physics interpretation

R1E0C closed PASS for the 94-mm periodic baseline through the required 0-60 deg scan gate under the frozen severe-mismatch criteria.

The scan-locus evidence also shows large scan-angle and scan-plane dependence, including about 209 ohm maximum active-impedance separation between the two 60-deg planes.

Therefore:
- do not reopen isolated-element matching optimization;
- move to R1E1 pitch/material trade;
- do not freeze the LNA input match yet;
- use the later R1E2 array impedance cloud as the authoritative frontend source environment.

## SimulationOps discipline

Follow the global SimulationOps protocol.

Normal CST flow:
Scientific Freeze -> Source Bundle -> Build-Only -> Hash Lock -> Fresh Solve -> Read-Only Qualification -> Scientific Gate.

For every formal execution:
- record exact source commit/hash
- use fresh work/evidence paths
- record invocation
- do not overwrite historical results
- do not automatically retry
- checkpoint/protect artifacts at task nodes

NW is the default control/build/lightweight-smoke host.
CST251 is reserved for explicitly authorized heavier production solves.

## Change discipline

Any electromagnetic geometry change must report:
- parameter
- old value
- new value
- provenance
- reason
- expected physical effect

Any design-decision reversal must update `docs/DECISIONS.md`.

Any new candidate architecture/component should enter `docs/IDEA_BACKLOG.md` before mainline promotion.

## Expected engineering style

- parameterized scripts/macros over opaque manual edits
- deterministic builds
- small commits
- one scientific question per gate
- build reports before solver reports
- explicit PASS/HOLD status
- no silent auto-tuning
- preserve failed evidence rather than rewriting history
- stop optimization when the gate question is answered

## Primary tools

- CST: antenna/full-wave and periodic/finite-array EM
- ADS: later LNA/noise/stability and EM-circuit co-design
- HFSS: optional independent cross-check
- Python: post-processing and parameter bookkeeping

## Stop rules

Stop and document instead of guessing when:
- a source ambiguity materially changes geometry
- a new idea would change architecture mid-gate
- a solver result cannot be traced to a frozen source
- an optimization objective has not been frozen
- a proposed feature has no quantified problem it solves

## H3B optimization-route authority
- H3A V0.2 is accepted as the mechanical baseline.
- Optimization method is hierarchical modular co-design with system-level closure.
- Do not force the antenna/LNA interface to 50 ohms.
- Eventual authoritative LNA source condition is scan-dependent active array impedance.
- Final system objective is robust A_eff/T_sys or G/T over the core frequency/scan domain.
- Local proxy metrics such as S11/transition return loss cannot override system sensitivity.
- Immediate next node is H3B_T01_POST_LNA_ORTHOGONAL_TRANSITION_COUPON_FREEZE.
- No BUILD/SOLVE permission is currently open.

## H3B-T01 build authorization
- exactly one standalone H3B-T01 transition-coupon BUILD-ONLY invocation on NW is authorized;
- coupon contains only horizontal/vertical 1-mm FR4 boards, grounded-CPW-class lines, via fences, explicit edge pads/caps and solder envelopes;
- RP1/RP2 are stored reference-plane parameters only; no RF ports are created in build-only;
- no antenna radiator, real LNA, input match, balun, filter, final connector or array geometry is present;
- BUILD PASS requires SimulationOps 0.2.6 intersection gate;
- no solve or optimization sweep is authorized.

## H3B-T01 build closeout
- H3B-T01 standalone coupon BUILD-ONLY is closed PASS; formal invocation count = 1; do not rebuild.
- artifact SHA256 = f321b678d390470a2420df40fd6d0cf6553cc041f9219bfcd011c7e41fbadf3d.
- fresh reopen verified 38 solids, zero RF ports, no solver results and completed CST intersection gate.
- current task is human 3D/manufacturing review only.
- no passive solve, optimization sweep, H3B-I01 integration or active-device execution is authorized.

## H3B-T01A passive solve authorization
- T01-A geometry human review is accepted.
- exactly one passive baseline solve on NW is authorized.
- source is the protected T01 BUILD artifact with SHA256 f321b678d390470a2420df40fd6d0cf6553cc041f9219bfcd011c7e41fbadf3d.
- only two 50-ohm discrete ports at frozen RP1/RP2 and the frozen solver configuration may be added to the solve copy.
- no geometry changes, no optimization sweep, no T01-C, no H3B-I01 integration, no active device.
- solve range 1.0–2.0 GHz; decision band 1.15–1.65 GHz.
- silent retry is forbidden.

## H3B-T01A passive baseline solve closeout
- one formal T01-A passive solve was consumed; do not retry silently;
- solver returned a full 2-port result set, but native CST adaptive-mesh convergence FAILED the frozen criterion;
- pass count reached 8/8; final two All-S DeltaS values were 0.0320727160 and 0.0309454700, both above 0.02;
- canonical status: HOLD_R1E1A4A_H3B_T01A_ADAPTIVE_MAXPASS8_NOT_CONVERGED;
- solved artifact SHA256 = 846919954fc99f541d8d0cfa3b4246fb49bf520d51b6c14de675d6fed54b0734;
- current S-parameters are provisional diagnostics only, not science-qualified;
- next action is numerical convergence recovery under a fresh explicit solve authorization;
- no geometry optimization, T01-C, H3B-I01 or active-device work is authorized.

## H3B-T01A maxpass16 recovery authorization
- exactly one numerical-recovery solve on NW is authorized;
- source is the same protected T01 BUILD artifact;
- the ONLY solver delta versus T01-A baseline is adaptive MaxPasses 8 -> 16;
- ports, frequency range, mesh formulation, threshold and geometry remain frozen;
- convergence authority is the CST Adaptive Meshing All-S Delta result tree, not output.txt alone;
- no geometry/RF optimization or T01-C/H3B-I01/active-device work is authorized;
- silent retry remains forbidden.
## Integrated next-route authority
- master plan: docs/R1E1A4A_H3B_TO_ACTIVE_ARRAY_MASTERPLAN_V01.md
- SimulationOps minimum: 0.2.7
- next step is T01A-O0 straight-reference calibration, not an immediate geometry sweep
- T01-C remains deferred
- H3B-I01 is blocked until T01-A local RF freeze
- R1E1B/R1E2 return to the mainline after H3B-I01
- H3C-LNA0 may run in parallel only under separate authorization
- H3C-C01 is blocked until R1E2 authoritative active-impedance atlas exists
- no BUILD or SOLVE permission is currently open
