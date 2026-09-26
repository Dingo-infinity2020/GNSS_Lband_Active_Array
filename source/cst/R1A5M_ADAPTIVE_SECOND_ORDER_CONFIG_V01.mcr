Option Explicit

' R1A5M adaptive mesh convergence configuration.
' No geometry, port, material, or science-design changes.

Sub Main()

    Solver.FrequencyRange "1.0", "1.8"

    With Boundary
        .Xmin "open"
        .Xmax "open"
        .Ymin "open"
        .Ymax "open"
        .Zmin "open"
        .Zmax "open"
        .Xsymmetry "none"
        .Ysymmetry "none"
        .Zsymmetry "none"
        .ApplyInAllDirections "False"
    End With

    With Background
        .ResetBackground
        .XminSpace "50"
        .XmaxSpace "50"
        .YminSpace "50"
        .YmaxSpace "50"
        .ZminSpace "50"
        .ZmaxSpace "50"
        .ApplyInAllDirections "False"
    End With

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
        .MaxPasses "6"
        .MaxDeltaS "0.02"
        .NumberOfDeltaSChecks "2"
        .SetLinearGrowthLimitation "40"
    End With

    FDSolver.MeshAdaptionTet "True"
    PostProcess1D.ActivateOperation "yz-matrices", "TRUE"

End Sub
