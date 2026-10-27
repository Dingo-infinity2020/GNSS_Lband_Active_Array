Option Explicit

' R1E0A periodic/unit-cell configuration BUILD-ONLY.
' No geometry, material, or port changes.
' No Floquet port.
' No solver start.

Sub Main()

    StoreParameter "R1E0_pitch_nominal_mm", 94.0
    StoreParameter "R1E0_scan_theta_deg", 0.0
    StoreParameter "R1E0_scan_phi_deg", 45.0

    ChangeSolverType "HF Frequency Domain"

    With Boundary
        .Xmin "unit cell"
        .Xmax "unit cell"
        .Ymin "unit cell"
        .Ymax "unit cell"
        .Zmin "expanded open"
        .Zmax "expanded open"
        .Xsymmetry "none"
        .Ysymmetry "none"
        .Zsymmetry "none"
        .ApplyInAllDirections "False"
        .OpenAddSpaceFactor "0.5"
        .XPeriodicShift "0.0"
        .YPeriodicShift "0.0"
        .ZPeriodicShift "0.0"
        .PeriodicUseConstantAngles "False"
        .SetPeriodicBoundaryAngles "R1E0_scan_theta_deg", "R1E0_scan_phi_deg"
        .SetPeriodicBoundaryAnglesDirection "outward"
        .UnitCellFitToBoundingBox "True"
        .UnitCellDs1 "0.0"
        .UnitCellDs2 "0.0"
        .UnitCellAngle "90.0"
    End With

End Sub
