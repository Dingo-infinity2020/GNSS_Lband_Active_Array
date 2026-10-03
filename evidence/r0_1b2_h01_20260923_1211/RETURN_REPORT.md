# R0.1B2 CENTER/FEED SOURCE-RECOVERY — Host Return Report

**FINAL_STATUS = HOLD_R0_PRIMARY_SOURCE_ACCESS_FAILED**

- Task ID: `R0.1B2-CENTER-FEED-SOURCE-RECOVERY-H01`
- Host: H01 (DESKTOP-GBTI6Q4)
- Date: 2026-09-23
- Host start commit: `cb7e650`
- Scope: official-source center/feed provenance audit only
- CST / solver / geometry change: **none** (prohibited)

## 1. Outcome

The recovered official IEICE PDF could **not** be downloaded by H01. Both the
landing page and the direct PDF endpoint are protected by an **AWS WAF
"Human Verification" CAPTCHA** (JavaScript + human puzzle):

- `Invoke-WebRequest` (plain and with browser headers): **HTTP 403**;
- `curl.exe` with browser UA + Referer: **HTTP 405**, returning a 2144-byte WAF
  challenge page;
- `webfetch` on both URLs: **non-2xx (405)**.

No PDF bytes were obtained, so the Fig.1(a) / Fig.2(a) center-feed audit could not
be performed. H01 did not attempt to bypass the CAPTCHA. Details, hashes and the
captured challenge page are in `source_access_log.txt` (challenge page kept in a
local temp dir only, not committed).

## 2. Required decision fields

```text
FIG40_SEMANTICS=UNRESOLVED
DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED
CENTRAL_REMOVED_REGION=PARTIAL
SOLVER_READY=NO
```

- `FIG40_SEMANTICS=UNRESOLVED`: no source figure was accessible to fix the
  annotation endpoints.
- `DIFFERENTIAL_TERMINALS_GEOMETRY=UNRESOLVED`: no terminal geometry observed.
- `CENTRAL_REMOVED_REGION=PARTIAL`: unchanged from repository provenance — the
  text allows a small central removal for feed/electronics; the shape/size remain
  unmeasured.
- `SOLVER_READY=NO`: a balanced excitation still cannot be defined without
  inventing hidden geometry.

## 3. Deliverables

- `refs/charts2025/CENTER_FEED_EXTRACTION.md` — updated with an R0.1B2 section
  documenting the access attempt; prior R0.1B history preserved; no figure-derived
  value upgraded.
- Evidence package:
  - `RETURN_REPORT.md` (this file)
  - `source_access_log.txt`
  - `figure_measurements.md` (all fields `NOT_OBSERVED`)
  - `hashes.txt`
- No `R0_CENTER_FEED_INTERPRETATION_V2.svg` was created, because no new
  measurements were possible; the prior `R0_CENTER_FEED_INTERPRETATION.svg`
  (R0.1B, project-owned) remains valid.

## 4. Prohibitions honored

- no CST, no solver, no geometry edit;
- no ports/materials/LNA/shield/Bias-Tee, no optimization, no L-band scaling;
- no copyrighted PDF, figure crop, or raw source image was downloaded into the
  repository or committed (the captured 2144-byte WAF challenge page is not
  publisher content and was left in a local temp dir);
- no hidden copper was silently interpreted.

## 5. Recommended unblocking path for the design side

Either:

- provide the PDF to H01 through a channel that does not require interactive
  CAPTCHA (e.g., a git-ignored local file path, with the host permitted to read
  it), or
- perform the figure audit on the design side (which reported it can access the
  PDF) and issue a host task limited to consolidation/verification.

Until then, the center/feed geometry and `FIRST_SOLVER` readiness remain blocked.

## 6. Next action

None issued. Per the stop rule, H01 stops here; the design side decides the
successor. No solver is authorized.
