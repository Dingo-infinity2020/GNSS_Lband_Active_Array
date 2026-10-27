# R1A1 CHARTS-Inspired Scaled Aperture — NW/DC Return Report

**FINAL_STATUS = PASS_R1A1_SCALED_APERTURE_BUILD_ONLY**

- Task: R1A1-RECOVERY-CSTPY-BUILD-ONLY-DC-NW
- Host: NW / DESKTOP-GBTI6Q4
- Source HEAD: bc06173084cf9c62f99f52c4cfee33afdade9770
- SimulationOps protocol: 0.2.4
- CST: 2022.5
- Build interpreter: CST bundled Python 3.6.0
- Solver: NOT RUN
- Ports: NONE
- Feed/LNA/substrate: NOT PRESENT

## Preflight

Static audit:

PASS_R1A1_MACRO_STATIC_AUDIT

Expected contract:
- 2 final solids
- 8 outer slot segments
- 4 inner slot segments
- 12 slot subtractions
- 0 ports
- no solver

## Build / reopen

CST build-only completed in a fresh MWS and was saved to:

D:\GNSS_Lband_Active_Array\_r1a1_scaled_aperture_work_recovery\R1A1_CHARTS_SCALED_APERTURE_BUILD_ONLY_V01.cst

Fresh reopen succeeded.

Final and reopen inventories are identical:

- SHAPE_COUNT=2
- UnitCellGround:UNITCELL_GROUND_REFERENCE
- Radiator:ANTENNA_PLATE

## Geometry / parameter checks

- scale factor = 0.285714285714
- board span = 70.714285714 mm
- outer slot-frame span = 65.0 mm
- height above ground = 57.142857143 mm
- nominal unit-cell reference = 94 mm
- unresolved source 40 mm label is stored only as scaled_fig40_unused

CST antenna-plate volume:
447.863265305201 mm^3

Analytical frozen-geometry volume:
447.863265306122 mm^3

Agreement is at numerical construction precision.

## Artifact hashes

Macro SHA256:
7382b6baa62f86c2e6b49fd6f74eeff6fd1187bd7dec41824309e9d55d2084ad

CST project SHA256:
c039106312861674d13e92983688672e0fce05d77fbcec6712a075fc2343253

## Notes

DesignEnvironment.version() emitted two non-blocking "Access is denied." lines while reporting the CST installation/version. The build, save, evidence session, and fresh-reopen all completed successfully.

The previous Miniconda/Python-3.13 attempt remains preserved separately as HOLD_ENVIRONMENT in evidence/r1a1_dc_nw_20260924_1111/; this recovery invocation was explicitly authorized and was not a silent retry.

## Stop boundary

R1A1 stops here.

No solver, ports, feed, substrate, optimization, LNA, or CST251 staging is authorized by this PASS.
