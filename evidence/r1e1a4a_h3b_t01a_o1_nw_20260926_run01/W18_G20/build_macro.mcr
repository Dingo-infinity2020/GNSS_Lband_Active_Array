Option Explicit

' H3B-T01A-O1 straight GCPW candidate - BUILD ONLY
Sub Main()

    StoreParameter "h3b_o1_board_t", 1.0
    StoreParameter "h3b_o1_cu_t", 0.035
    StoreParameter "h3b_o1_wsig", 1.8
    StoreParameter "h3b_o1_gap", 0.2
    StoreParameter "h3b_o1_wgnd", 2.2
    StoreParameter "h3b_o1_rp1_y", 12.0
    StoreParameter "h3b_o1_rp2_y", -12.0
    StoreParameter "h3b_o1_rp_spacing", 24.0
    StoreParameter "h3b_o1_freq_lo", 1.0
    StoreParameter "h3b_o1_freq_hi", 2.0
    StoreParameter "h3b_o1_decision_lo", 1.15
    StoreParameter "h3b_o1_decision_hi", 1.65

    With Solid
        .SetAutoIntersectionCheckElMag "True"
        .SetAutoIntersectionCheckThermal "False"
        .SetAutoIntersectionCheckMechanics "False"
    End With

    With Material
        .Reset
        .Name "FR4_COST_BASELINE"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "4.3"
        .Mue "1.0"
        .TanD "0.02"
        .TanDFreq "1.5"
        .TanDGiven "True"
        .TanDModel "ConstTanD"
        .Create
    End With

    With Brick
        .Reset
        .Name "REFERENCE_FR4"
        .Component "H3B_O1_Board"
        .Material "FR4_COST_BASELINE"
        .Xrange "-5", "5"
        .Yrange "-16", "16"
        .Zrange "0", "1"
        .Create
    End With

    With Brick
        .Reset
        .Name "REF_SIG"
        .Component "H3B_O1_Line"
        .Material "PEC"
        .Xrange "-0.9", "0.9"
        .Yrange "-14.5", "14.5"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "REF_GND_L"
        .Component "H3B_O1_Line"
        .Material "PEC"
        .Xrange "-3.3000000000000003", "-1.1"
        .Yrange "-14.5", "14.5"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "REF_GND_R"
        .Component "H3B_O1_Line"
        .Material "PEC"
        .Xrange "1.1", "3.3000000000000003"
        .Yrange "-14.5", "14.5"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "REF_BACK_GND"
        .Component "H3B_O1_BackGround"
        .Material "PEC"
        .Xrange "-4", "4"
        .Yrange "-14.5", "14.5"
        .Zrange "1", "1.035"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_L_1"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "-2.3"
        .Ycenter "-12"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_L_1"

    With Cylinder
        .Reset
        .Name "REF_VIA_L_1"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "-2.3"
        .Ycenter "-12"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_L_2"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "-2.3"
        .Ycenter "-9"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_L_2"

    With Cylinder
        .Reset
        .Name "REF_VIA_L_2"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "-2.3"
        .Ycenter "-9"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_L_3"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "-2.3"
        .Ycenter "-6"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_L_3"

    With Cylinder
        .Reset
        .Name "REF_VIA_L_3"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "-2.3"
        .Ycenter "-6"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_L_4"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "-2.3"
        .Ycenter "-3"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_L_4"

    With Cylinder
        .Reset
        .Name "REF_VIA_L_4"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "-2.3"
        .Ycenter "-3"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_L_5"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "-2.3"
        .Ycenter "3"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_L_5"

    With Cylinder
        .Reset
        .Name "REF_VIA_L_5"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "-2.3"
        .Ycenter "3"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_L_6"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "-2.3"
        .Ycenter "6"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_L_6"

    With Cylinder
        .Reset
        .Name "REF_VIA_L_6"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "-2.3"
        .Ycenter "6"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_L_7"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "-2.3"
        .Ycenter "9"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_L_7"

    With Cylinder
        .Reset
        .Name "REF_VIA_L_7"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "-2.3"
        .Ycenter "9"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_L_8"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "-2.3"
        .Ycenter "12"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_L_8"

    With Cylinder
        .Reset
        .Name "REF_VIA_L_8"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "-2.3"
        .Ycenter "12"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_R_1"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "2.3"
        .Ycenter "-12"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_R_1"

    With Cylinder
        .Reset
        .Name "REF_VIA_R_1"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "2.3"
        .Ycenter "-12"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_R_2"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "2.3"
        .Ycenter "-9"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_R_2"

    With Cylinder
        .Reset
        .Name "REF_VIA_R_2"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "2.3"
        .Ycenter "-9"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_R_3"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "2.3"
        .Ycenter "-6"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_R_3"

    With Cylinder
        .Reset
        .Name "REF_VIA_R_3"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "2.3"
        .Ycenter "-6"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_R_4"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "2.3"
        .Ycenter "-3"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_R_4"

    With Cylinder
        .Reset
        .Name "REF_VIA_R_4"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "2.3"
        .Ycenter "-3"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_R_5"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "2.3"
        .Ycenter "3"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_R_5"

    With Cylinder
        .Reset
        .Name "REF_VIA_R_5"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "2.3"
        .Ycenter "3"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_R_6"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "2.3"
        .Ycenter "6"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_R_6"

    With Cylinder
        .Reset
        .Name "REF_VIA_R_6"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "2.3"
        .Ycenter "6"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_R_7"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "2.3"
        .Ycenter "9"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_R_7"

    With Cylinder
        .Reset
        .Name "REF_VIA_R_7"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "2.3"
        .Ycenter "9"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "REF_VIAHOLE_R_8"
        .Component "H3B_O1_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "z"
        .Zrange "-0.02", "1.02"
        .Xcenter "2.3"
        .Ycenter "12"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:REF_VIAHOLE_R_8"

    With Cylinder
        .Reset
        .Name "REF_VIA_R_8"
        .Component "H3B_O1_Via"
        .Material "PEC"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "2.3"
        .Ycenter "12"
        .Segments "0"
        .Create
    End With


    ' BUILD ONLY: no RF ports and no solver.
End Sub
