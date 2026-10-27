# M7A Diagnostic SOLVE Freeze V0.1

M7A is solved with the exact full-E2C S0 12-port coexistence network: 12 retained ports, sources 1/2/4/5/7/8/10/11, passive 50-ohm loads 3/6/9/12, 1.0-1.8 GHz, second-order tetrahedral adaptive mesh, MaxDeltaS 0.02 for two consecutive checks, max 16 passes.

No H-field monitor is added. This intentionally preserves the full-E2C adaptive path and avoids the monitor-driven adaptation expansion seen in M6.

Corrective gates are frozen before solve:
- Primary: BOTH polarizations must show >=30% reduction versus full E2C in E_diff->common degradation at each full-E2C polarization's own severe mode peak frequency, AND >=30% reduction in branch-return imbalance at 1.2984 GHz.
- Secondary: worst own-pol source-side complex deviation over 1.15-1.65 GHz decreases >=20%.
- Guard: no off-diagonal solved response gains >6 dB local excursion relative to full E2C in any <=50 MHz window.

Exactly one formal solver invocation. No retry. M7B remains unauthorized.
