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

Current task: **R1E1-A4A-H3B-T01A-NUMERICAL-RECOVERY-AWAIT-AUTH**

Current permissions:
- inspect the closed R1E1A1 bare-array and R1E1A2/A3 support evidence: YES
- R1E1A2 canonical build status is PASS via read-only recovery
- R1E1A3-R1 broadside and C60P45 passed; C60P135 passed numerically but failed the frozen Gate-T Delta-Z criterion
- preserve Gate T unchanged; do not reinterpret the current S1 support as transparent
- perform receiver-shadow / LNA noise-S-parameter analysis using traceable data: YES
- freeze P0/P1A/P1B reference planes, local-ground/common-mode assumptions and Gate R: YES
- design the mandatory H0 active-hub interface plus C0 foam, C1 dielectric-tube/standoff and C2 PCB-frame carrier envelopes: YES
- R1E1A4A H0/P1 BUILD-ONLY authorization is consumed; canonical build PASS via read-only recovery; do not rerun build
- H0/P1 broadside solve authorization is consumed; no retry and no follow-on scan solve
- canonical H0 V0.1 status is HOLD_GATE_R_RNF0 despite numerical/mixed-mode PASS
- H1A OFFSET_GROUND_G2P0 build authorization is consumed; canonical build PASS via fresh-reopen recovery; do not rerun build
- H1A broadside production solve authorization is consumed; canonical status is numerical HOLD at MaxPasses=12; do not rerun
- H1R numerical recovery is DEFERRED; no H1R solve is authorized
- user promoted H2A Universal Passive/Active Center Structure to the product-architecture mainline
- H2A V0.1 BUILD-ONLY is closed PASS; formal build invocation count = 1; do not rebuild
- qualified H2A artifact is protected in place with SHA256 b8f9161d7530b194fec1f35cc69f3cb5c770fb9daaba8eaeb519fbf064da644b
- H2A V0.1 human review accepted the overall concept but identified missing RF cable egress/service architecture
- H2A V0.2 SERVICE-ARCHITECTURE BUILD-ONLY is closed PASS; formal build invocation count = 1; do not rebuild
- qualified V0.2 artifact is protected in place with SHA256 4756a525c407bac9f6de1c42c9274b74825a45a6b3cae81e60f1e67e64494064
- human review of H2A V0.2 found unintended geometry interference; the artifact is retained but is NOT an eligible solve source
- SimulationOps >=0.2.5 requires CST Geometry Intersection Check after fresh reopen before BUILD PASS
- H3A V0.1 remains immutable historical evidence but is not solve-eligible because its top tenons sat inside the parent FR4 through-slots without true mortise walls
- H3A V0.2 FR4-bridged mortise BUILD-ONLY is closed PASS; formal V0.2 invocation count = 1; do not rebuild
- V0.2 artifact SHA256 = 9e810560fc8fc759a88d4ac5fc39067863a1e078b6f01e6e343b004891201db5
- fresh reopen proved substrate volume 4518.70408162357 mm^3, bridge helpers consumed, top copper unbridged, zero RF ports, no solver results, CST intersection gate executed
- current task is H3A V0.2 human 3D/mechanical review only
- no H3A solve, H3B continuation, active transistor/device integration, H1R solve, follow-on scan, S4 sentinel or R1E1B pitch-screen solver is authorized
- material A/B solve: NO
- physical LNA integration/CST251: NO
- do not assume each LNA sees Zdiff/2 unless the virtual-ground/reference-plane condition is explicitly qualified
- silent retry: NO

R1E1A1 is closed `PASS_R1E1A1_SIX_PITCH_FR4_SOURCE_SET_BUILD_ONLY`.
R1E1A2/A3 scope is frozen in `docs/R1E1A2A3_SUPPORT_SENSITIVITY_CONTRACT.md`.

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
