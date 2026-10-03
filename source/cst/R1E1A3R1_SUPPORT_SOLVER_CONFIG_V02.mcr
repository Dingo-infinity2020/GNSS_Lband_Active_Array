Option Explicit

' R1E1A3-R1 numerical recovery solver configuration.
' Sole intended change from R1E0C_B_SCAN_SOLVER_CONFIG_V01:
' MaxPasses = 12 instead of 8.

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
