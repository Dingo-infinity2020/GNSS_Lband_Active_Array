Option Explicit
' GNSS_Lband_Active_Array
' M6 diagnostic solve-copy configuration V01
' VARIANT: D2
' SOURCE BUILD SHA256: c2a935e8d3a9e2d1f8b1ee7d58320e8ffd6d8f0513a859a01869f4f757855f2a
'
' E2A observer semantics are preserved exactly.
' Raw 12 audit ports -> 6 solve ports.
' Sources: 1,2,4,5. Passive 50-ohm loads only: 3,6.
' H-field monitors are used because CST's HF workflow derives surface-current
' evidence on conducting surfaces from the H-field monitor result.
' No solver start in this macro.

Sub Main()

    Port.Delete 12
    Port.Delete 11
    Port.Delete 10
    Port.Delete 6
    Port.Delete 5
    Port.Delete 4

    Port.Rename 7, 4
    Port.Rename 8, 5
    Port.Rename 9, 6

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

    With Monitor
        .Reset
        .Name "M6_HFIELD_SURFCURRENT_L2_1p2276"
        .Dimension "Volume"
        .Domain "Frequency"
        .FieldType "Hfield"
        .Frequency "1.2276"
        .UseSubvolume "False"
        .Create
    End With

    With Monitor
        .Reset
        .Name "M6_HFIELD_SURFCURRENT_MIXED_WORST_1p3384"
        .Dimension "Volume"
        .Domain "Frequency"
        .FieldType "Hfield"
        .Frequency "1.3384"
        .UseSubvolume "False"
        .Create
    End With

    With Monitor
        .Reset
        .Name "M6_HFIELD_SURFCURRENT_L1_1p57542"
        .Dimension "Volume"
        .Domain "Frequency"
        .FieldType "Hfield"
        .Frequency "1.57542"
        .UseSubvolume "False"
        .Create
    End With


End Sub
