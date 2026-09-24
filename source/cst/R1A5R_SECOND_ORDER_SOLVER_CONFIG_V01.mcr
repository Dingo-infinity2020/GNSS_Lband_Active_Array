Option Explicit

' R1A5R numerical refinement only.
' Same physical model, ports, boundary and frequency as R1A5.
' Only tetrahedral numerical order/method is refined.

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
    FDSolver.MeshAdaptionTet "False"
    PostProcess1D.ActivateOperation "yz-matrices", "TRUE"

End Sub
