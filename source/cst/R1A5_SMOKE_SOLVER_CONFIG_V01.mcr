Option Explicit

' R1A5 solver/boundary configuration only.
' Applied to a hash-verified COPY of R1A4.
' No geometry changes. No port changes. No optimization.

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
    FDSolver.OrderTet "First"
    FDSolver.MeshAdaptionTet "False"
    PostProcess1D.ActivateOperation "yz-matrices", "TRUE"

End Sub
