# R1E0 94-mm Periodic Unit-Cell Baseline Plan

Status: DESIGN BASELINE

## Mainline role

R1E0 is the first primary array-physics gate after isolated passive qualification.

The objective is not isolated return-loss optimization.

The objective is to establish a trustworthy infinite-array unit-cell workflow and measure scan-dependent active differential impedance.

## Canonical source

Start from the clean Pol-A R1A5F source model:

D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst

SHA256:
74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce

Reason:
- one clean differential port;
- no crossed-port artifact;
- geometry already human-reviewed;
- R1A5FQ proved self-response equivalence to the converged passive baseline.

Pol-B is not required for the first workflow proof because R1A5FQ established exact rotational feed construction and close electromagnetic equivalence.

Pol-B returns in later periodic symmetry/atlas gates.

## Lattice baseline

Square lattice.

Initial pitch:
94 mm.

Implementation:
Boundary.UnitCellFitToBoundingBox = True.

The structure x/y bounding box is fixed by the 94-mm square ground/reference, so the repeated unit cell is 94 mm x 94 mm.

No pitch optimization is allowed in R1E0.

## CST 2022.5 verified API basis

Installed CST help confirms:

- Unit Cell boundaries virtually repeat the modeled structure to infinity in two directions.
- Unit Cell boundaries are supported by the general-purpose frequency-domain solver.
- Scan angles modify the periodic phase according to theta/phi.
- theta is measured from +z.
- phi is the global spherical azimuth.
- SetPeriodicBoundaryAngles creates the frequency-dependent phase relation.
- SetPeriodicBoundaryAnglesDirection "outward" uses the outward-traveling convention.
- UnitCellFitToBoundingBox True repeats at structure bounding-box borders.
- unit-cell boundaries use SetPeriodicBoundaryAngles directly; explicit Floquet ports are not required for a discrete-port-driven antenna model.

Installed references:
- Online Help / Boundary Conditions - Unit Cell
- Online Help / Boundary Conditions - Scan Angles
- VBA Boundary Object
- Library/Macros/Solver/F-Solver/Change settings from Full Array to Unitcell^+MWS.mcr

## Excitation interpretation

The retained discrete S-parameter port represents one identically driven differential feed in every periodic cell.

With unit-cell scan phase, the one-port S11 is interpreted as the active reflection coefficient for that scan state.

Using Z0 = 100 ohm:

Z_active = Z0 * (1 + S11) / (1 - S11).

This is the quantity that later constrains the LNA source-impedance environment.

## R1E0A — periodic configuration BUILD-ONLY

Purpose:
prove that the actual antenna CST can carry the intended periodic metadata without geometry or port changes.

Configuration:
- Pol-A only
- Xmin/Xmax = unit cell
- Ymin/Ymax = unit cell
- Zmin/Zmax = expanded open
- OpenAddSpaceFactor = 0.5
- X/Y/Z explicit periodic shifts = 0
- PeriodicUseConstantAngles = False
- scan theta = 0 deg
- scan phi = 45 deg
- scan direction = outward
- UnitCellFitToBoundingBox = True
- UnitCellAngle = 90 deg
- no explicit UnitCellOrigin override; FitToBoundingBox defines the repeated cell from the structure bounds
- no Floquet port
- HF Frequency Domain selected
- no solver run

Why phi=45 at broadside:
phi is physically irrelevant at theta=0, but 45 deg is the Pol-A axis and becomes the first principal scan plane in later R1E0 scan work.

PASS requires:
- geometry identical to R1A5F source;
- one discrete port remains;
- fresh reopen;
- x/y boundaries report unit cell;
- z boundaries report expanded open;
- GetUnitCellScanAngle returns valid theta=0, phi=45, outward;
- structure x span = 94 mm;
- structure y span = 94 mm;
- no solver.

## R1E0B — broadside periodic smoke

Separate later authorization.

Purpose:
establish that the periodic driven model solves and produces a finite, continuous active-impedance curve.

Use the converged second-order adaptive tetra formulation from R1A5M2/R1A5FQ.

Broadside:
theta=0 deg.

Important:
broadside periodic Z_active is NOT required to equal isolated Zin because mutual coupling is physically expected.

The isolated curve is only a contextual reference.

Required outputs:
- active S11
- Z_active
- native adaptive convergence
- comparison with clean isolated Pol-A
- scan/boundary provenance

No geometry optimization is allowed.

## R1E0C — first scan qualification

Only after R1E0B passes.

Primary Pol-A scan plane:
phi=45 deg.

Core theta:
0, 30, 45, 60 deg.

Cross-plane sentinel:
theta=60 deg, phi=135 deg.

First scientific questions:
- how far does Z_active move with scan;
- whether a severe mismatch/impedance singularity appears;
- whether 94-mm pitch remains viable through 60 deg;
- whether the principal and orthogonal scan planes differ materially.

The first scan gate may use full-band frequency-domain solves if resource checks remain lightweight.

## R1E0 stop boundary

R1E0 does not:
- vary pitch;
- compare materials;
- integrate the LNA;
- optimize the radiator.

Those belong to R1E1/R1E2 and later active-frontend stages.
