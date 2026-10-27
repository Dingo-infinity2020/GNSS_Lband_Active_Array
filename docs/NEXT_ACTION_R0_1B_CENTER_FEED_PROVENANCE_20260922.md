# Next action — R0.1B center/feed provenance extraction

Date: 2026-09-22
Task ID: `R0.1B-CENTER-FEED-PROVENANCE-H01`
Owner: H01
Gate: `R0-CHARTS-RECON-PASSIVE`

## Objective

Resolve as much as the published evidence permits about the **central feed/electronics region** of the CHARTS planar antenna before any passive solver model is authorized.

This task answers only:

> What central metal removal, feed-terminal topology, and Fig.1 `40 mm` semantics can be supported by the source figures/text, and what remains genuinely unresolved?

This is a provenance/extraction task. It is **not** a CST build task and is **not** a solver task.

## Authoritative sources

Use the repository provenance first:

- `refs/charts2025/PROVENANCE.md`
- `refs/charts2025/FIGURE_EXTRACTION.md`
- `refs/charts2025/PHOTO_GEOMETRY_ESTIMATE.md`
- `docs/R0_RECONSTRUCTION_ASSUMPTIONS.md`
- DOI recorded in `refs/charts2025/PROVENANCE.md`

The primary paper is the two-page ISAP 2025 proceeding by Lau et al., *Active Planar Antenna Design for CHARTS Array*.

Do not commit the copyrighted paper PDF or raw source photographs.

## Absolute prohibitions

Do not:

- run CST;
- edit V0.3 geometry;
- run any solver;
- add ports, monitors, materials, LNA, shield or Bias-Tee;
- optimize/tune dimensions;
- scale to L band;
- silently decide that the `40 mm` label is a centre hole/gap;
- convert any figure-derived value to `PAPER_EXPLICIT`;
- copy the source paper/figures into the repository.

## Required source audit

### 1. Fig.1(a) centre-region audit

At the highest source resolution available locally, inspect the simulation-model figure and record:

- the endpoints/orientation of the `40 mm` dimension annotation;
- whether the annotation clearly spans:
  - a central removed square/diamond,
  - a feed-terminal separation,
  - an inner-slot spacing,
  - another feature,
  - or remains ambiguous;
- visible conductor boundaries entering/leaving the centre;
- whether the figure clearly shows electrically separate petals at the feed region;
- whether there is a central through-hole/cutout, and if so whether its shape is identifiable.

Use normalized board coordinates where practical. Keep measurement uncertainty explicit.

### 2. Fig.2(a) fabricated-centre audit

Inspect the fabricated active-antenna image and record:

- which central features are directly visible;
- which are hidden by the electronics/local ground/shield region;
- whether any copper-gap or petal separation can be traced continuously into the centre;
- whether the photograph supports or contradicts any Fig.1 interpretation.

Do not infer hidden copper under the electronics.

### 3. Text audit

Record only source-explicit central/feed statements, including:

- small centre area may be removed for feed/electronics;
- balanced differential output;
- small ground plane beneath feed points in the active implementation;
- LNA circuits located at the feed region.

Do not turn those statements into dimensions unless the source supplies them.

## Required project-owned outputs

Create:

`refs/charts2025/CENTER_FEED_EXTRACTION.md`

It must contain a table with:

| Feature | Observation | Value/range | Provenance | Confidence | Solver consequence |
|---|---|---|---|---|---|

Use only:
- `PAPER_EXPLICIT`
- `FIGURE_DERIVED_UNVERIFIED`
- `SEMANTICS_UNRESOLVED`

Also create a project-owned schematic if useful:

`docs/figures/R0_CENTER_FEED_INTERPRETATION.svg`

The schematic must be redrawn from project measurements/interpretation and must not embed/copy the source photograph.

If more than one interpretation remains plausible, show them as **Candidate A / Candidate B / ...** without selecting a winner.

## 40 mm rule

The default state remains:

`FIG40_SEMANTICS=UNRESOLVED`

It may be changed only if the source geometry makes the annotation endpoints unambiguous.

A visually plausible guess is not enough.

## Final decision fields

Return exactly one:

- `PASS_R0_CENTER_FEED_EXTRACTION_COMPLETE`
- `HOLD_R0_CENTER_FEED_SOURCE_AMBIGUOUS`
- `HOLD_R0_PRIMARY_SOURCE_UNAVAILABLE`

`PASS_R0_CENTER_FEED_EXTRACTION_COMPLETE` means the extraction work is complete, **not** that the central geometry is necessarily resolved.

The report must separately state:

- `FIG40_SEMANTICS=...`
- `DIFFERENTIAL_TERMINALS_GEOMETRY=RESOLVED|PARTIAL|UNRESOLVED`
- `CENTRAL_REMOVED_REGION=RESOLVED|PARTIAL|UNRESOLVED`
- `SOLVER_READY=YES|NO`

`SOLVER_READY=YES` is allowed only when a balanced excitation can be defined without inventing hidden conductor topology. It does not itself authorize solver execution.

## Evidence package

Create:

`evidence/r0_1b_h01_<YYYYMMDD_HHMM>/`

Include at minimum:

- `RETURN_REPORT.md`
- a source-audit/measurement log;
- any project-owned measurement table;
- hashes of generated project-owned schematics/scripts;
- no raw copyrighted source images.

## Stop rule

After push:

- update `PROJECT_HANDOFF.md` HOST RETURN;
- set `TASK_STATUS=HOST_COMPLETE` or `HOST_HOLD`;
- push to `project/r0-charts-scaffold`;
- stop.

No successor task is pre-authorized.
