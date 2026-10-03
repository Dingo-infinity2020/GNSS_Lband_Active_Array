Option Explicit

' R1E0C-A C60P45 scan-state BUILD-ONLY.
' Only scan metadata changes. No boundary-type, geometry, material, port, or solver changes.

Sub Main()

    StoreParameter "R1E0_scan_theta_deg", 60.0
    StoreParameter "R1E0_scan_phi_deg", 45.0

    With Boundary
        .SetPeriodicBoundaryAngles "R1E0_scan_theta_deg", "R1E0_scan_phi_deg"
        .SetPeriodicBoundaryAnglesDirection "outward"
    End With

End Sub
