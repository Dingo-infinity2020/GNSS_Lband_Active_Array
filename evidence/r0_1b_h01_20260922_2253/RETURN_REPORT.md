# R0.1B CENTER/FEED PROVENANCE — Host Return Report

**FINAL_STATUS = HOLD_R0_PRIMARY_SOURCE_UNAVAILABLE**

- Task ID: `R0.1B-CENTER-FEED-PROVENANCE-H01`
- Host: H01 (DESKTOP-GBTI6Q4)
- Date: 2026-09-22
- Host start commit: `e1bb1a3`
- Scope: source/figure provenance extraction only
- CST / solver / geometry change: **none** (prohibited by the task)

## 1. Why HOLD (primary source unavailable)

The task required a high-resolution inspection of Fig. 1(a) and Fig. 2(a) of the
CHARTS ISAP 2025 proceeding. Those figures were **not available to H01**:

- the repository stores no copyrighted figures/PDF (`refs/charts2025/` is `.md`
  only);
- a local-machine search found no source copy;
- the DOI resolves to **bibliographic metadata only**, with no open full text or
  figure link; Crossref and DataCite APIs returned 404.

Full details and exact commands are in `source_audit_log.txt`.

Because the required primary-figure audit could not be performed, a new
center/feed extraction is not possible on H01. Per the task's own decision set,
the correct outcome is `HOLD_R0_PRIMARY_SOURCE_UNAVAILABLE`.

## 2. What was delivered anyway

A consolidated, provenance-only extraction was produced from the repository's
existing source-traceable records:

- `refs/charts2025/CENTER_FEED_EXTRACTION.md` — required extraction table plus
  candidates for the Fig.1 `40 mm` label. Every figure-derived item keeps its
  prior class and is explicitly marked as **not re-measured by H01**.
- `docs/figures/R0_CENTER_FEED_INTERPRETATION.svg` — project-owned redraw of the
  candidate interpretations (no source imagery embedded).

## 3. Required decision fields

```text
FIG40_SEMANTICS=UNRESOLVED
DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED
CENTRAL_REMOVED_REGION=PARTIAL
SOLVER_READY=NO
```

- `FIG40_SEMANTICS=UNRESOLVED`: default retained; the annotation endpoints are
  not made unambiguous by any available record.
- `DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED`: only the existence of a balanced
  feed is source-supported.
- `CENTRAL_REMOVED_REGION=PARTIAL`: paper-explicit that a small central area may
  be removed for feed/electronics; no large through-hole recorded; exact shape
  and size unresolved.
- `SOLVER_READY=NO`: a balanced excitation cannot be defined without inventing
  hidden terminal/cutout geometry.

## 4. Text-supported center/feed statements (`PAPER_EXPLICIT`)

From `refs/charts2025/PROVENANCE.md` / `FIGURE_EXTRACTION.md`:

- small central low-field area may be removed for feed/electronics;
- balanced output directly feeds a pair of LNAs;
- small local ground plane beneath the feed points (active implementation);
- LNA circuits mounted at the feed region;
- center impedance design region `(100 +/- 40) + j(0 +/- 40) ohm`.

No numerical central-cutout or feed-terminal dimension is supplied by the text.

## 5. `40 mm` label — candidates (no winner)

- **A** — differential feed-terminal separation.
- **B** — small central removed square for feed/electronics.
- **C** — extent of the local feed ground plane.
- **D** — an inner-region spacing other than the ~60 mm visible clear span.

All remain possible; none is selected. See `CENTER_FEED_EXTRACTION.md` §3 and the
interpretation SVG.

## 6. Prohibitions honored

- no CST and no solver run;
- no port/monitor/material/LNA/shield/Bias-Tee added;
- V0.3 geometry untouched; no dimension tuned;
- no L-band scaling;
- the `40 mm` label was not silently reinterpreted;
- no figure-derived value promoted to `PAPER_EXPLICIT`;
- no copyrighted paper/figures downloaded, copied, or committed.

## 7. Source-audit artifacts and hashes

See `source_audit_log.txt`, `center_feed_measurement_table.md`, and `hashes.txt`.

## 8. Next action

None issued. Per the handoff stop rule, H01 stops here; the design side decides
the successor (for example: obtain a higher-resolution source, author input, or a
measured center geometry). No solver is authorized.
