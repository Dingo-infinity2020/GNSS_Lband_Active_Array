Option Explicit
' GNSS_Lband_Active_Array
' R4-A0-E2C-S0 dual-pol coexistence solve-copy configuration V01
'
' SOURCE: accepted E2C R7 build, SHA256
' cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c
'
' PURPOSE:
'   solve-copy configuration only; no geometry/material edits;
'   reduce 24 audit/reference ports -> 12 sentinel ports;
'   excite only E_UP and P_IN on four branches;
'   P_OUT ports remain passive 50-ohm matched loads;
'   no solver start in this macro.

Sub Main()

    ' Delete auxiliary ports in descending order.
    Port.Delete 24
    Port.Delete 23
    Port.Delete 22
    Port.Delete 18
    Port.Delete 17
    Port.Delete 16
    Port.Delete 12
    Port.Delete 11
    Port.Delete 10
    Port.Delete 6
    Port.Delete 5
    Port.Delete 4

    ' Compact retained raw ports into the frozen 12-port semantic map.
    Port.Rename 7, 4
    Port.Rename 8, 5
    Port.Rename 9, 6
    Port.Rename 13, 7
    Port.Rename 14, 8
    Port.Rename 15, 9
    Port.Rename 19, 10
    Port.Rename 20, 11
    Port.Rename 21, 12

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

    With FDSolver
        .SetMethod "Tetrahedral", "General purpose"
        .OrderTet "Second"
        .Stimulation "List", "List"
        .ResetExcitationList
        .AddToExcitationList "1", "1"
        .AddToExcitationList "2", "1"
        .AddToExcitationList "4", "1"
        .AddToExcitationList "5", "1"
        .AddToExcitationList "7", "1"
        .AddToExcitationList "8", "1"
        .AddToExcitationList "10", "1"
        .AddToExcitationList "11", "1"
        .AutoNormImpedance "True"
        .NormingImpedance "50"
        .ModesOnly "False"
        .MeshAdaptionTet "True"
        .StoreAllResults "True"
        .StoreResultsInCache "False"
        .CalcPowerLoss "True"
        .CalcPowerLossPerComponent "False"
    End With

    With MeshAdaption3D
        .SetType "HighFrequencyTet"
        .SetAdaptionStrategy "ExpertSystem"
        .MinPasses "3"
        .MaxPasses "16"
        .MaxDeltaS "0.02"
        .NumberOfDeltaSChecks "2"
        .SetLinearGrowthLimitation "40"
    End With

    PostProcess1D.ActivateOperation "yz-matrices", "TRUE"

End Sub
