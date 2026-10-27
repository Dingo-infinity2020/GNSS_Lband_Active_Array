# Next action — R0.1B2 center/feed provenance with recovered primary source

Date: 2026-09-22
Task ID: `R0.1B2-CENTER-FEED-SOURCE-RECOVERY-H01`
Owner: H01
Gate: `R0-CHARTS-RECON-PASSIVE`

## Context

The prior R0.1B task ended correctly in:

`HOLD_R0_PRIMARY_SOURCE_UNAVAILABLE`

because H01's DOI/metadata route did not expose the paper.

Design-side review has now recovered the official IEICE publisher PDF. Read:

`docs/R0_1B_SOURCE_RECOVERY_20260922.md`

before starting.

## Official source

Landing page:

https://www.ieice.org/publications/proceedings/summary.php?expandable=13&iconf=ISAP&number=1571143655&session_num=Pos1&year=2025

Direct PDF:

https://www.ieice.org/publications/proceedings/bin/pdf_link.php?fname=1571143655.pdf&iconf=ISAP&lang=E&number=1571143655&vol=98&year=2025

The PDF may be downloaded only to a local temporary/git-ignored location for inspection. Do not commit it or raw figure crops.

## Objective

Perform the previously blocked high-resolution Fig. 1(a) / Fig. 2(a) centre-feed audit.

Answer only:

1. What exactly does the Fig. 1(a) `40 mm` dimension appear to span?
2. What conductor boundaries and centre removal are actually visible in Fig. 1(a)?
3. Can the balanced terminal pair/gap/orientation be defined from the source without inventing hidden copper?
4. What centre geometry is visible or hidden in Fig. 2(a)?
5. Does Fig. 2(a) support, contradict, or fail to resolve the Fig. 1(a) interpretation?

## Required method

### Source integrity

Record:

- download URL;
- HTTP/download result;
- local temporary path;
- PDF file size and SHA-256;
- page count.

Do not commit the PDF itself.

### Fig. 1(a)

Use the highest practical local render/zoom.

Record in project-owned coordinates/notes:

- endpoints of the `40 mm` dimension arrows/extension lines;
- orientation of the dimension;
- which visible edges/features those endpoints correspond to;
- centre cutout/opening shape if visible;
- visible petal/feed conductor separation;
- whether two differential terminals can be localized;
- uncertainty caused by figure resolution.

Do not infer hidden geometry.

### Fig. 2(a)

Record:

- directly visible centre/feed copper;
- electronics/local-ground occlusion;
- whether the centre cutout can be traced;
- whether terminal/gap geometry is visible;
- whether the photo independently supports any Fig. 1(a) interpretation.

## Required outputs

Update/replace the provisional extraction with a new source-backed section in:

`refs/charts2025/CENTER_FEED_EXTRACTION.md`

Clearly preserve the history that the first H01 pass lacked the source.

Create:

`evidence/r0_1b2_h01_<YYYYMMDD_HHMM>/`

with at minimum:

- `RETURN_REPORT.md`
- `source_access_log.txt`
- `figure_measurements.md`
- hashes of any project-owned scripts/redraws

Raw publisher figures/crops are forbidden from git.

A project-owned redraw is allowed:

`docs/figures/R0_CENTER_FEED_INTERPRETATION_V2.svg`

## Decision fields

Return all:

- `FIG40_SEMANTICS=RESOLVED:<meaning>|PARTIAL|UNRESOLVED`
- `DIFFERENTIAL_TERMINALS_GEOMETRY=RESOLVED|PARTIAL|UNRESOLVED`
- `CENTRAL_REMOVED_REGION=RESOLVED|PARTIAL|UNRESOLVED`
- `SOLVER_READY=YES|NO`

Final status exactly one of:

- `PASS_R0_CENTER_FEED_PRIMARY_SOURCE_AUDIT_COMPLETE`
- `HOLD_R0_CENTER_FEED_SOURCE_AMBIGUOUS`
- `HOLD_R0_PRIMARY_SOURCE_ACCESS_FAILED`

A PASS means the official source audit was completed, not that every feature must be resolved.

## Absolute prohibitions

- NO CST.
- NO solver.
- NO geometry edit.
- NO ports/materials/LNA/shield/Bias-Tee.
- NO optimization.
- NO L-band scaling.
- NO raw copyrighted PDF/figure commit.
- NO silent interpretation of hidden copper.

## Stop rule

After pushing evidence and updating HOST RETURN, stop. No successor task is pre-authorized.
