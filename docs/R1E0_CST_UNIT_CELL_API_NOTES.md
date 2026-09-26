# R1E0 CST 2022.5 Unit-Cell API Notes

Purpose:
record locally verified CST behavior so future agents do not rediscover or guess the periodic-array API.

## Verified installed CST macro

D:\Program Files (x86)\CST Studio Suite 2022\Library\Macros\Solver\F-Solver\Change settings from Full Array to Unitcell^+MWS.mcr

Relevant commands include:

- ChangeSolverType "HF Frequency Domain"
- Boundary.Xmin "unit cell"
- Boundary.Xmax "unit cell"
- Boundary.Ymin "unit cell"
- Boundary.Ymax "unit cell"
- Boundary.Zmin "expanded open"
- Boundary.Zmax "expanded open"
- Boundary.OpenAddSpaceFactor "0.5"
- Boundary.XPeriodicShift "0.0"
- Boundary.YPeriodicShift "0.0"
- Boundary.ZPeriodicShift "0.0"
- Boundary.PeriodicUseConstantAngles "False"
- Boundary.SetPeriodicBoundaryAngles theta, phi
- Boundary.SetPeriodicBoundaryAnglesDirection "outward"
- Boundary.UnitCellFitToBoundingBox "True"
- Boundary.UnitCellAngle "90.0"

The same CST macro also creates Floquet ports, but that portion is not copied into R1E0 because our array is driven by the retained antenna differential discrete port rather than an incident plane wave.

## Verified installed help

Boundary Conditions - Unit Cell:
- unit cell repeats the structure periodically to infinity in the x-y plane;
- supported by general-purpose frequency-domain solvers;
- Fit to bounding box repeats at structure borders.

Boundary Conditions - Scan Angles:
- scan angles modify phase on periodic boundaries;
- theta is the angle from z;
- phi is spherical azimuth;
- frequency-domain only;
- direction can be outward or inward.

VBA Boundary Object:
- PeriodicUseConstantAngles True activates angle-driven frequency-dependent phase for ordinary periodic boundaries;
- SetPeriodicBoundaryAngles remains relevant whenever unit-cell boundaries are used;
- GetUnitCellScanAngle returns theta, phi and direction and indicates whether unit-cell scan metadata are valid;
- UnitCellFitToBoundingBox True ignores explicit Ds1/Ds2 and repeats at the structure bounding-box border;
- GetStructureBox returns the physical structure bounding box.

## R1E0 convention

Use actual "unit cell" boundaries in x/y.

Use:
PeriodicUseConstantAngles False

and:
SetPeriodicBoundaryAngles theta, phi

This matches the installed CST Full Array -> Unit Cell macro. Unit-cell boundaries themselves make the scan-angle definition active.

Direction:
outward.

No manually calculated fixed XPeriodicShift/YPeriodicShift is used for scan steering.

This avoids an incorrect frequency-independent phase shift over the 1.0–1.8 GHz broadband solve.
