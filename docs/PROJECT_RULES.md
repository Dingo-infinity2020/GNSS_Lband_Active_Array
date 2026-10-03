# Project Rules — Anti-Divergence Charter

Status: **ACTIVE**
Applies to: humans, Codex/agents, scripts, simulation workflows, and design reviews.

The purpose of these rules is to keep the project convergent. New papers, new components, and new ideas are welcome, but they must not silently redefine the project.

---

## 1. Mission is frozen above architecture

The project mission is:

> Develop a low-cost, low-noise, dual-polarized, wide-field active antenna element for 1.15–1.65 GHz full-L-band GNSS, scalable to a digitally beamformed array.

The following are mission-level requirements and may not be changed by a normal design iteration:

- continuous 1.15–1.65 GHz coverage,
- two independent linear-polarization outputs,
- digital RHCP/LHCP formation in generation 1,
- array-aware impedance / scan design,
- first-stage gain located as close to the radiator feed as practical,
- low-cost, repeatable fabrication as a first-class objective,
- design must remain scalable beyond a single isolated antenna.

Changing a mission-level requirement requires a dedicated architecture-review issue and explicit human approval.

---

## 2. Architecture is allowed to evolve, but only one mainline exists

At any time the repository shall have:

- exactly one **MAINLINE** architecture,
- at most one **FIRST_BACKUP** architecture,
- any number of **REFERENCE_ONLY** architectures.

Current intent:

- MAINLINE: CHARTS-inspired planar balanced radiator + feed-point differential active frontend.
- FIRST_BACKUP: PUMA / unbalanced tightly-coupled element with LNA behind the ground plane.
- REFERENCE_ONLY: C-ORA, ASKAP chequerboard, Vivaldi/EMBRACE/ASTRON, Cui loop-loaded dipole, other literature structures.

A new paper does not become MAINLINE because it looks better.

Promotion to MAINLINE requires evidence against the current mainline using the same evaluation matrix.

---

## 3. No architecture switching inside a gate

A gate begins with a declared architecture and ends with PASS / HOLD / FAIL.

During a gate:

- do not switch radiator family,
- do not switch LNA family,
- do not add a new matching philosophy,
- do not change the stated optimization objective.

If a new idea appears, record it under `docs/IDEA_BACKLOG.md` or open an issue.

It may be evaluated only after the current gate closes.

---

## 4. One question per gate

Every gate must answer one primary question.

Examples:

- R0: Can we reconstruct the CHARTS passive topology honestly enough to reproduce its published behavior?
- R1: Does Maxwell scaling provide a useful L-band starting point?
- R2: Can a true dual-polarized version meet polarization and isolation requirements?
- R3: Does the geometry remain viable under periodic / finite-array active impedance?
- R4: Can the differential LNA meet noise and stability targets over the required source-impedance region?

A gate must not become a container for unrelated improvements.

---

## 5. Reproduction before optimization

For any literature-derived design:

1. reproduce or reconstruct,
2. quantify mismatch,
3. understand sensitivity,
4. only then optimize.

Never optimize a model before establishing whether the reference itself was modeled correctly.

No hidden fitting is allowed.

---

## 6. Provenance is mandatory

Every nontrivial design parameter must carry exactly one provenance class:

- `PAPER_EXPLICIT`
- `FIGURE_DERIVED_UNVERIFIED`
- `ASSUMPTION`
- `MEASURED`
- `OPTIMIZED`

A parameter may change provenance only through a documented commit / review.

Never relabel a guessed value as literature-derived merely because it produces a better plot.

---

## 7. No silent parameter drift

Any simulation commit that changes electromagnetic geometry must include:

- changed parameter names,
- old values,
- new values,
- reason,
- expected physical effect.

Bulk geometry edits without a parameter-level change report are not accepted.

---

## 8. Build and solve are separate permissions

A workflow must distinguish:

- BUILD_ONLY
- SOLVER
- OPTIMIZATION
- HARDWARE_RELEASE

Passing one does not authorize the next.

No agent may infer permission to run a solver from permission to build geometry.

No optimization may begin until the baseline solver gate is reviewed.

---

## 9. No solver result without a manifest

Every solver result must be traceable to:

- git commit,
- parameter manifest,
- model/script version,
- solver version,
- boundary / port definition,
- mesh settings or mesh policy,
- run type.

Plots without provenance are exploratory only and cannot support a design decision.

---

## 10. The project optimizes system performance, not pretty S11

The project does not use isolated-element return loss as the final objective.

Primary system quantities progressively become:

- active differential impedance,
- receiver noise temperature,
- realized gain / G/T,
- scan performance,
- X/Y phase and amplitude symmetry,
- RHCP/LHCP quality after digital combination,
- stability,
- manufacturability and cost.

An S11 improvement is not considered progress if it worsens noise, scan, stability, or manufacturability.

---

## 11. Complexity must earn its place

Every added structure must answer:

> What quantified problem does this part solve?

Examples:
- passive ring,
- extra dielectric layer,
- FSS / WAIM,
- balun,
- matching section,
- shielding cavity,
- extra LNA,
- special substrate.

If an added feature does not produce a measurable improvement against a frozen requirement, it should be removed.

Prefer the simplest architecture that passes.

---

## 12. Cost and fabrication are gate metrics, not post-processing

Every candidate architecture review must include:

- PCB count,
- layer count,
- special substrate requirement,
- manual assembly steps,
- RF connector count,
- shield / metalwork requirements,
- LNA count,
- estimated BOM class,
- tolerance sensitivity.

An electrically superior architecture may be rejected if it is materially harder or more expensive to manufacture without sufficient system benefit.

---

## 13. LNA choice remains open until R4

QPL9547 is the reference device because it has strong low-noise data and relevant differential-radio-astronomy precedent.

It is not the production winner.

No LNA is promoted to final choice before:
- matched noise comparison,
- stability comparison,
- gain / linearity comparison,
- cost comparison,
- power comparison,
- package / PCB integration comparison.

All candidates must be tested under the same source-impedance assumptions.

---

## 14. No pre-LNA passive network by default

A passive structure before the first gain stage must be justified by measurement or simulation.

Examples requiring explicit justification:
- balun,
- narrowband filter,
- long microstrip,
- cable,
- connector,
- hybrid,
- lossy matching network.

The default position is: minimize pre-LNA loss.

Exception: a preselector or stabilization network may be accepted if strong-RFI compression or instability evidence makes it necessary.

---

## 15. Array behavior cannot be deferred indefinitely

An isolated element may be used only for early reference reconstruction.

Before an architecture is considered viable for hardware:
- periodic-array active impedance must be evaluated,
- finite-array behavior must be checked,
- the effect of scan on noise/stability must be considered.

No architecture may be declared “finished” based only on isolated-element results.

---

## 16. New literature goes to backlog first

When a new paper/patent/product appears:

1. add a short record to `docs/IDEA_BACKLOG.md`,
2. state what problem it may solve,
3. state what current baseline it would replace,
4. state what evidence would justify promotion.

Do not immediately edit the mainline geometry.

---

## 17. Require a replacement test before changing mainline

A candidate may replace MAINLINE only if it is compared on the same frozen dimensions:

- band coverage,
- core scan region,
- active impedance,
- polarization behavior,
- expected receiver noise,
- pre-LNA loss,
- PCB/mechanical complexity,
- cost,
- power,
- integration risk.

The replacement must solve a demonstrated mainline limitation, not merely look more sophisticated.

---

## 18. Maintain a design decision log

Important decisions must be recorded in `docs/DECISIONS.md`.

Each decision contains:

- date,
- decision,
- evidence,
- rejected alternatives,
- reversal condition.

A later iteration may reverse a decision, but must explicitly satisfy the reversal condition or document new evidence.

---

## 19. FAIL is allowed; silent redesign is not

A gate may end in:

- PASS
- HOLD
- FAIL

FAIL is scientifically useful.

If a model fails:
- preserve evidence,
- explain why,
- create a successor gate if justified.

Do not rewrite history by silently modifying the model until it passes.

---

## 20. Hardware follows evidence

No PCB release because “the simulation looks promising.”

Before hardware:
- geometry gate PASS,
- array-awareness gate PASS,
- active-front-end stability check PASS,
- clear measurement plan,
- BOM and fabrication review.

The first hardware may intentionally test uncertainty, but its purpose must be written before fabrication.

---

## 21. Keep mainline and exploration physically separated

Recommended repository convention:

- `mainline/` or current staged directories: approved path
- `experiments/`: exploratory branches or alternative concepts
- `refs/`: literature provenance only
- `evidence/`: run outputs and gate reports

Exploration must not overwrite mainline artifacts.

---

## 22. Freeze before sweep

Before any parameter sweep or optimizer run:
- define the variables allowed to move,
- define fixed variables,
- define bounds,
- define objective functions,
- define stop criteria.

Optimization without a frozen search space is not accepted.

---

## 23. Every optimizer needs a physical interpretation

An optimized geometry is not accepted solely because the objective improved.

The report must explain:
- which resonances moved,
- what coupling changed,
- what current distribution changed,
- why scan/noise behavior improved.

Black-box success without physical explanation is provisional only.

---

## 24. Favor incremental commits

One scientific idea per commit when practical.

Preferred sequence:
- provenance,
- geometry,
- build check,
- solver setup,
- solver result,
- interpretation.

Do not mix literature changes, geometry changes, circuit changes, and conclusion changes into one opaque commit.

---

## 25. Stop when the current question is answered

Do not continue improving a passing gate simply because more optimization is possible.

When acceptance criteria are met:
- record PASS,
- freeze artifacts,
- move to the next gate.

This rule exists specifically to prevent endless local optimization.

---

# Current project control statement

Until explicitly changed:

- Current gate: **R0-CHARTS-RECON-PASSIVE**
- Mainline: **CHARTS-inspired planar balanced active element**
- First backup: **PUMA / unbalanced tightly-coupled element**
- LNA reference: **QPL9547**
- Solver permission: **NO**
- Optimization permission: **NO**
- Hardware permission: **NO**

Current allowed work:
- literature provenance,
- parameter extraction,
- reconstruction assumptions,
- parameter manifest review,
- build-only tooling after manifest PASS.
