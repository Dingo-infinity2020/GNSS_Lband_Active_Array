Option Explicit

' R1E0B periodic broadside solver configuration.
' IMPORTANT: no Boundary block is allowed here.
' The qualified R1E0A unit-cell metadata must remain untouched.

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
        .MaxPasses "8"
        .MaxDeltaS "0.02"
        .NumberOfDeltaSChecks "2"
        .SetLinearGrowthLimitation "40"
    End With

    FDSolver.MeshAdaptionTet "True"
    PostProcess1D.ActivateOperation "yz-matrices", "TRUE"

End Sub
