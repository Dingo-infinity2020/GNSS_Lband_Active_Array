# R1A1 NW/DC BUILD-ONLY Runbook

SimulationOps protocol: 0.2.4

## Preconditions

- Build host: `NW`
- Model: `CHARTS_GNSS_R1A1_SCALED_APERTURE_V01`
- `BUILD_AUTHORIZED=true`
- `SOLVE_AUTHORIZED=false`

Run:

```powershell
python scripts\audit_r1a1_scaled_aperture.py
```

Expected:
`PASS_R1A1_MACRO_STATIC_AUDIT`

## Build

Use `scripts/run_r1a1_build_only_dc.py` through a fresh CST MWS.

Expected final geometry:
- 2 solids,
- 12 consumed slot cutters,
- no ports,
- no solver result tree.

## Visual checks

- board span ~70.714 mm,
- 8 outer disconnected slot segments,
- 4 inner disconnected slots,
- plate remains one connected solid,
- no center through-hole,
- plate height ~57.143 mm above reference ground,
- 94 mm nominal unit-cell ground reference.

## Stop boundary

After fresh reopen and evidence capture, stop.

Do not:
- create ports,
- add substrate,
- add feed,
- run solver,
- optimize geometry.
