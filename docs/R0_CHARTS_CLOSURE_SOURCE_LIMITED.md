# R0 CHARTS Closure — Source-Limited Reconstruction

Status: **R0_CLOSED_SOURCE_LIMITED**

## What R0 successfully established

The project reconstructed and reviewed the large-scale visible CHARTS planar topology from the 2025 source:

- square planar aperture / PCB,
- 12 disconnected slot segments in the accepted V0.3 visible topology,
- preserved single-piece conductive topology,
- 200 mm height over the main ground plane,
- center region reserved for feed/electronics,
- balanced/differential active-feed concept,
- local feed electronics / local ground / EMI-shield concept.

The V0.3 visible topology is the accepted R0 geometric reference.

## What R0 cannot establish from the public source

The two-page CHARTS proceeding does not uniquely expose:

- exact center copper-removal geometry,
- differential terminal pad geometry,
- exact meaning/endpoints of the Fig.1 40 mm center-region label,
- local feed-ground dimensions,
- exact substrate material/stack,
- exact hidden active-feed mechanical integration.

Repeated source review does not remove this ambiguity.

## Scientific closure decision

R0 is not declared an exact-replica PASS.

Instead:

```text
VISIBLE_APERTURE_TOPOLOGY=PASS
CST_BUILD_REPLAY_WORKFLOW=PASS
EXACT_CENTER_FEED=SOURCE_UNDERSPECIFIED
EXACT_MATERIAL_STACK=SOURCE_UNDERSPECIFIED
EXACT_CHARTS_REPLICA=NO
R0_STATUS=R0_CLOSED_SOURCE_LIMITED
```

The project will not invent missing CHARTS details and call them literature facts.

## Transition to R1

R1 becomes a **project-owned CHARTS-inspired GNSS derivative**, with every new feed/material choice explicitly marked PROJECT_DESIGN rather than PAPER_EXPLICIT.

The goal is no longer to reproduce hidden CHARTS details.

The goal is:

> preserve the attractive CHARTS visible aperture / center-active integration philosophy while deliberately designing the missing feed, material, and L-band scaling for our own 1.15–1.65 GHz array element.

## R1 initial rules

Before any solver:

1. preserve the accepted V0.3 aperture topology as the starting family;
2. scale only source-visible geometry through an explicit scale parameter;
3. define a project-owned balanced feed in a separate design document;
4. use ideal differential terminals before adding any QPL9547 model;
5. keep material choice as an explicit design variable;
6. do not claim the resulting antenna is the original CHARTS antenna;
7. array periodic/finite behavior remains a later mandatory gate.

## REF-CUI status

REF-CUI is frozen as REFERENCE_ONLY evidence.

Its R0B build proved CST automation/replay discipline, but the scientific geometry is held before solver.

It does not gate R1.
