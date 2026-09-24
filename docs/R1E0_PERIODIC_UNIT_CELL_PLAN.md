# R1E0 94-mm Periodic Unit-Cell Baseline Plan

Status: R1E0A PASS; R1E0B PASS; R1E0C-A PASS; R1E0C-B PASS; R1E0 CLOSED

## Mainline role

R1E0 is the first primary array-physics gate after isolated passive qualification.

The objective is not isolated return-loss optimization.

The objective is to establish a trustworthy infinite-array unit-cell workflow and measure scan-dependent active differential impedance.

## Canonical clean source

Clean periodic source:

D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

This source contains:
- one clean Pol-A differential port
- X/Y unit-cell boundaries
- Z expanded-open boundaries
- 94 x 94 mm fitted unit cell
- broadside scan metadata
- no solver result

Pol-B is deferred from the first workflow proof because prior clean-feed qualification established the rotational relationship. It returns in later symmetry/atlas gates.

## Lattice baseline

Square lattice.

Initial pitch:
94 mm.

Implementation:
`Boundary.UnitCellFitToBoundingBox = True`

The structure x/y span is 94 mm, so the repeated unit cell is 94 x 94 mm.

No pitch optimization is allowed inside R1E0.

## Verified CST 2022.5 API basis

Installed CST macro:

D:\Program Files (x86)\CST Studio Suite 2022\Library\Macros\Solver\F-Solver\Change settings from Full Array to Unitcell^+MWS.mcr

Verified relevant commands:
- Xmin/Xmax = unit cell
- Ymin/Ymax = unit cell
- Zmin/Zmax = expanded open
- OpenAddSpaceFactor = 0.5
- X/Y/Z periodic shifts = 0
- PeriodicUseConstantAngles = False
- SetPeriodicBoundaryAngles theta, phi
- SetPeriodicBoundaryAnglesDirection outward
- UnitCellFitToBoundingBox = True
- UnitCellDs1/Ds2 = 0 when fit-to-box is used by the macro
- UnitCellAngle = 90 deg

R1E0 does not copy the installed macro's Floquet-port excitation section because this array is driven by the retained antenna differential discrete port.

## Excitation interpretation

The retained differential port represents one identically driven feed in every periodic cell.

With periodic scan phase, the driven-port self-reflection is the active reflection coefficient for that scan state.

Using differential reference impedance Z0=100 ohm:

`Z_active = Z0 * (1 + S11) / (1 - S11)`

Periodic result path observed in CST 2022.5:

`1D Results\S-Parameters\S1(1),1(1)`

## R1E0A - periodic configuration BUILD-ONLY

Status:
PASS

Qualified:
- X/Y = unit cell
- Z = expanded open
- 94 x 94 mm
- theta=0
- phi=45
- direction=outward
- geometry unchanged
- one discrete port
- no solver output

Artifact SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

## R1E0B - broadside periodic smoke

Status:
PASS

Canonical solved artifact:

D:\GNSS_Lband_Active_Array\_r1e0b_broadside_smoke_work\R1E0B_POLA_PERIODIC_BROADSIDE_SMOKE_V01.cst

SHA256:
339021e580efa6aae6dfcfa229e4194b4dcf0bbef854398d44a0efed65aac7ad

Numerical result:
- adaptive convergence PASS
- final two Delta-S values below 0.02
- desired-accuracy termination
- broadband sweep PASS
- 1001-point finite S11 and Z_active

Science-band broadside range:
- Re(Z_active): 85.05 to 264.39 ohm
- Im(Z_active): -84.19 to +141.95 ohm
- |Z_active|: 105.33 to 266.79 ohm
- S11: about -5.24 to -9.70 dB

The large difference from the isolated element is accepted as physical mutual-coupling evidence.

## R1E0C - first scan qualification

Current status:
DESIGN READY

Primary Pol-A scan plane:
phi=45 deg.

Prepared core states:
- theta=30, phi=45
- theta=45, phi=45
- theta=60, phi=45

Orthogonal-plane sentinel:
- theta=60, phi=135

Broadside reference:
R1E0B theta=0, phi=45.

R1E0C-A will first create/fresh-reopen hash-locked scan-state CSTs with only scan metadata changed.

R1E0C-B will later solve each scan state under separate solver authorization.

Primary questions:
- how far Z_active moves with scan
- whether severe active mismatch or scan blindness appears
- whether 94-mm pitch remains viable through the 0-60 deg core region
- whether principal and orthogonal scan planes differ materially

## R1E0 stop boundary

R1E0 does not:
- vary pitch
- compare materials
- integrate the LNA
- optimize radiator geometry

Those belong to R1E1/R1E2 and later active-frontend stages.
