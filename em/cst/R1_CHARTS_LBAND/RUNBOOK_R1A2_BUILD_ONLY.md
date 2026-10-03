# R1A2 Symmetric Center-Feed Reference BUILD-ONLY

Status: **READY FOR NW BUILD-ONLY AFTER STAGE CONTRACT AUTHORIZATION**

Purpose:
- preserve the accepted R1A1 12-slot scaled aperture,
- add project-owned center-gap and terminal **reference overlays**,
- prove exact 90-degree rotational construction,
- avoid making a premature material/port claim.

The reference shapes are intentionally placed slightly above the aperture and are **not subtracted** from the PEC topology proxy.

Expected final solids:
- 2 R1A1 base solids,
- 4 FeedGapReference solids,
- 4 TerminalReference solids,
- total = 10.

Acceptance:
- static audit PASS,
- 4 gap references produced from one master by 90-degree transform copies,
- 4 terminal references produced from one master by 90-degree transform copies,
- equal reference volumes within numerical tolerance,
- fresh reopen identical,
- 0 ports,
- no solver.

Stop after build-only. R1A3 will decide materialization / actual copper subtraction.
