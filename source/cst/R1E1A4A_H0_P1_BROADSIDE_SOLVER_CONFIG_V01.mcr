Option Explicit

' R1E1A4A H0/P1 broadside mixed-mode solver config.
' Numerically identical to the qualified R1E1A3-R1 MaxPasses=12 baseline.
' No geometry, material, boundary, port, monitor, or optimization changes.

Sub Main()

    Solver.FrequencyRange "1.0", "1.8"

    ChangeSolverType "HF Frequency Domain"

    With MeshSettings
        .SetMeshType "Tet"
        .Set "CurvatureOrder", "3"
    End With

    FDSolver.OrderTet "Second"
    FDSolver.SetMethod "Tetrahedral", "General purpose"

    With MeshAdaption3D
        .SetType "HighFrequencyTet"
        .SetAdaptionStrategy "ExpertSystem"
        .MinPasses "3"
        .MaxPasses "12"
        .MaxDeltaS "0.02"
        .NumberOfDeltaSChecks "2"
        .SetLinearGrowthLimitation "40"
    End With

    FDSolver.MeshAdaptionTet "True"

End Sub
