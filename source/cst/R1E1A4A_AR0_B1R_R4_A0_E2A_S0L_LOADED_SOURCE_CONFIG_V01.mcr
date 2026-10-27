Option Explicit
' GNSS_Lband_Active_Array
' R4-A0-E2A-S0L loaded source-side solve-copy configuration V01
'
' SOURCE:
'   protected E2A V02 build artifact
'   SHA256 78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804
'
' PURPOSE:
'   solve-copy configuration only;
'   no geometry/material edits;
'   reduce 12 audit ports -> 6 solver ports;
'   source excitations only at new ports 1,2,4,5;
'   new ports 3,6 remain passive 50-ohm matched loads;
'   no solver start in this macro.
'
' RAW -> SOLVE PORT MAP:
'   raw1  A_E_UP   -> new1 source
'   raw2  A_P_IN   -> new2 source
'   raw3  A_P_OUT  -> new3 50-ohm load only
'   raw7  B_E_UP   -> new4 source
'   raw8  B_P_IN   -> new5 source
'   raw9  B_P_OUT  -> new6 50-ohm load only
'
' DELETED AUDIT PORTS:
'   raw4 A_E_DN
'   raw5 A_B_VDD
'   raw6 A_B_VBIAS
'   raw10 B_E_DN
'   raw11 B_B_VDD
'   raw12 B_B_VBIAS
'
' Their physical copper pads remain unchanged/open.
'
' HARD STOP:
'   no solver-start command
'   no geometry mutation
'   no circuit component insertion

Sub Main()

    ' Delete auxiliary audit ports in descending order.
    Port.Delete 12
    Port.Delete 11
    Port.Delete 10
    Port.Delete 6
    Port.Delete 5
    Port.Delete 4

    ' Compact remaining B-branch port numbers into the frozen six-port semantic map.
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

End Sub
