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

Current task: **R1E1-A0-R2-DESIGN-ENDPOINT-PROOF**

Current permissions:
- inspect the completed R1 canonical-source PASS evidence: YES
- design/audit the R2 88/100-mm endpoint-proof bundle: YES
- run R2 endpoint proof: NO
- run any R1E1 solver: NO
- material A/B solve: NO
- LNA integration/CST251: NO

R1E1A0-R1 is closed PASS.
R1E1A0-R2 is DESIGN ONLY until its separate build ticket is frozen.

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
