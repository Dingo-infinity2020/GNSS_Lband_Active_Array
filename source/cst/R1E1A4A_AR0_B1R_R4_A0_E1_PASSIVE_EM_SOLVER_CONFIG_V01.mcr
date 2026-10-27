Option Explicit

' GNSS_Lband_Active_Array
' R4-A0-E1 passive 6-port EM network qualification solver configuration V01
'
' HARD BOUNDARY:
'   solver/boundary/mesh/postprocess configuration only;
'   no geometry edits;
'   no port edits;
'   no active QPL9547 object;
'   no circuit-domain C_IN/C_OUT/L1/R4 insertion.
'
' The source artifact is the protected V03 landing-zone build.
' All six existing single-ended discrete ports remain unchanged.

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
        .XminSpace "30"
        .XmaxSpace "30"
        .YminSpace "30"
        .YmaxSpace "30"
        .ZminSpace "30"
        .ZmaxSpace "30"
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
        .MaxPasses "16"
        .MaxDeltaS "0.02"
        .NumberOfDeltaSChecks "2"
        .SetLinearGrowthLimitation "40"
    End With

    FDSolver.MeshAdaptionTet "True"
    PostProcess1D.ActivateOperation "yz-matrices", "TRUE"

End Sub
