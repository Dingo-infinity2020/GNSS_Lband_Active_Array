Option Explicit

' H3B-T01 Orthogonal PCB Post-LNA Transition Coupon V0.1 — BUILD ONLY
' Standalone coupon. No antenna, no active device, no solver, no RF ports.

Sub Main()

    StoreParameter "h3b_t01_board_t", 1
    StoreParameter "h3b_t01_cu_t", 0.035
    StoreParameter "h3b_t01_wsig", 1.6
    StoreParameter "h3b_t01_gap", 0.35
    StoreParameter "h3b_t01_wgnd", 2.2
    StoreParameter "h3b_t01_pad_sig", 2
    StoreParameter "h3b_t01_pad_gap", 0.3
    StoreParameter "h3b_t01_pad_gnd", 2.4
    StoreParameter "h3b_t01_rp1_y", 12
    StoreParameter "h3b_t01_rp2_z", -12
    StoreParameter "h3b_t01_via_outer_r", 0.2
    StoreParameter "h3b_t01_via_inner_r", 0.15
    StoreParameter "h3b_t01_viahole_r", 0.2
    StoreParameter "h3b_t01_freq_lo", 1
    StoreParameter "h3b_t01_freq_hi", 2
    StoreParameter "h3b_t01_decision_lo", 1.15
    StoreParameter "h3b_t01_decision_hi", 1.65

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

    With Material
        .Reset
        .Name "O3_COPPER"
        .Folder ""
        .FrqType "all"
        .Type "Lossy metal"
        .SetMaterialUnit "GHz", "mm"
        .Mue "1.0"
        .Sigma "58000000"
        .Create
    End With

    With Material
        .Reset
        .Name "O3_SOLDER_PROXY"
        .Folder ""
        .FrqType "all"
        .Type "Lossy metal"
        .SetMaterialUnit "GHz", "mm"
        .Mue "1.0"
        .Sigma "7000000"
        .Create
    End With

    With Brick
        .Reset
        .Name "HORIZONTAL_FR4"
        .Component "H3B_Board"
        .Material "FR4_COST_BASELINE"
        .Xrange "-5", "5"
        .Yrange "-4", "16"
        .Zrange "0", "1"
        .Create
    End With

    With Brick
        .Reset
        .Name "VERTICAL_FR4"
        .Component "H3B_Board"
        .Material "FR4_COST_BASELINE"
        .Xrange "-5", "5"
        .Yrange "-0.5", "0.5"
        .Zrange "-18", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "H_SIG"
        .Component "H3B_Line"
        .Material "O3_COPPER"
        .Xrange "-0.8", "0.8"
        .Yrange "1.8", "14.5"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "H_GND_L"
        .Component "H3B_Line"
        .Material "O3_COPPER"
        .Xrange "-3.35", "-1.15"
        .Yrange "1.8", "14.5"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "H_GND_R"
        .Component "H3B_Line"
        .Material "O3_COPPER"
        .Xrange "1.15", "3.35"
        .Yrange "1.8", "14.5"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "H_BACK_GND"
        .Component "H3B_BackGround"
        .Material "O3_COPPER"
        .Xrange "-4", "4"
        .Yrange "1.8", "14.5"
        .Zrange "1", "1.035"
        .Create
    End With

    With Brick
        .Reset
        .Name "V_SIG"
        .Component "H3B_Line"
        .Material "O3_COPPER"
        .Xrange "-0.8", "0.8"
        .Yrange "0.5", "0.535"
        .Zrange "-14.5", "-1.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "V_GND_L"
        .Component "H3B_Line"
        .Material "O3_COPPER"
        .Xrange "-3.35", "-1.15"
        .Yrange "0.5", "0.535"
        .Zrange "-14.5", "-1.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "V_GND_R"
        .Component "H3B_Line"
        .Material "O3_COPPER"
        .Xrange "1.15", "3.35"
        .Yrange "0.5", "0.535"
        .Zrange "-14.5", "-1.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "V_BACK_GND"
        .Component "H3B_BackGround"
        .Material "O3_COPPER"
        .Xrange "-4", "4"
        .Yrange "-0.535", "-0.5"
        .Zrange "-14.5", "-1.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "H_PAD_SIG"
        .Component "H3B_Transition"
        .Material "O3_COPPER"
        .Xrange "-1", "1"
        .Yrange "0.5", "1.8"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "H_PAD_GND_L"
        .Component "H3B_Transition"
        .Material "O3_COPPER"
        .Xrange "-3.7", "-1.3"
        .Yrange "0.5", "1.8"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "H_PAD_GND_R"
        .Component "H3B_Transition"
        .Material "O3_COPPER"
        .Xrange "1.3", "3.7"
        .Yrange "0.5", "1.8"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "V_PAD_SIG"
        .Component "H3B_Transition"
        .Material "O3_COPPER"
        .Xrange "-1", "1"
        .Yrange "0.5", "0.535"
        .Zrange "-1.5", "-0.035"
        .Create
    End With

    With Brick
        .Reset
        .Name "V_PAD_GND_L"
        .Component "H3B_Transition"
        .Material "O3_COPPER"
        .Xrange "-3.7", "-1.3"
        .Yrange "0.5", "0.535"
        .Zrange "-1.5", "-0.035"
        .Create
    End With

    With Brick
        .Reset
        .Name "V_PAD_GND_R"
        .Component "H3B_Transition"
        .Material "O3_COPPER"
        .Xrange "1.3", "3.7"
        .Yrange "0.5", "0.535"
        .Zrange "-1.5", "-0.035"
        .Create
    End With

    With Brick
        .Reset
        .Name "EDGE_CAP_SIG"
        .Component "H3B_EdgeCap"
        .Material "O3_COPPER"
        .Xrange "-1", "1"
        .Yrange "-0.5", "0.5"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "EDGE_CAP_GND_L"
        .Component "H3B_EdgeCap"
        .Material "O3_COPPER"
        .Xrange "-3.7", "-1.3"
        .Yrange "-0.5", "0.5"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "EDGE_CAP_GND_R"
        .Component "H3B_EdgeCap"
        .Material "O3_COPPER"
        .Xrange "1.3", "3.7"
        .Yrange "-0.5", "0.5"
        .Zrange "-0.035", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "SOLDER_SIG"
        .Component "H3B_Solder"
        .Material "O3_SOLDER_PROXY"
        .Xrange "-1", "1"
        .Yrange "0.535", "1"
        .Zrange "-0.45", "-0.035"
        .Create
    End With

    With Brick
        .Reset
        .Name "SOLDER_GND_L"
        .Component "H3B_Solder"
        .Material "O3_SOLDER_PROXY"
        .Xrange "-3.7", "-1.3"
        .Yrange "0.535", "1"
        .Zrange "-0.45", "-0.035"
        .Create
    End With

    With Brick
        .Reset
        .Name "SOLDER_GND_R"
        .Component "H3B_Solder"
        .Material "O3_SOLDER_PROXY"
        .Xrange "1.3", "3.7"
        .Yrange "0.535", "1"
        .Zrange "-0.45", "-0.035"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "H_VIAHOLE_L_1"
        .Component "H3B_Tools"
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

    Solid.Subtract "H3B_Board:HORIZONTAL_FR4", "H3B_Tools:H_VIAHOLE_L_1"

    With Cylinder
        .Reset
        .Name "H_VIA_L_1"
        .Component "H3B_Via"
        .Material "O3_COPPER"
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
        .Name "H_VIAHOLE_L_2"
        .Component "H3B_Tools"
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

    Solid.Subtract "H3B_Board:HORIZONTAL_FR4", "H3B_Tools:H_VIAHOLE_L_2"

    With Cylinder
        .Reset
        .Name "H_VIA_L_2"
        .Component "H3B_Via"
        .Material "O3_COPPER"
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
        .Name "H_VIAHOLE_L_3"
        .Component "H3B_Tools"
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

    Solid.Subtract "H3B_Board:HORIZONTAL_FR4", "H3B_Tools:H_VIAHOLE_L_3"

    With Cylinder
        .Reset
        .Name "H_VIA_L_3"
        .Component "H3B_Via"
        .Material "O3_COPPER"
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
        .Name "H_VIAHOLE_L_4"
        .Component "H3B_Tools"
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

    Solid.Subtract "H3B_Board:HORIZONTAL_FR4", "H3B_Tools:H_VIAHOLE_L_4"

    With Cylinder
        .Reset
        .Name "H_VIA_L_4"
        .Component "H3B_Via"
        .Material "O3_COPPER"
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
        .Name "V_VIAHOLE_L_1"
        .Component "H3B_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "y"
        .Yrange "-0.52", "0.52"
        .Xcenter "-2.3"
        .Zcenter "-3"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_Board:VERTICAL_FR4", "H3B_Tools:V_VIAHOLE_L_1"

    With Cylinder
        .Reset
        .Name "V_VIA_L_1"
        .Component "H3B_Via"
        .Material "O3_COPPER"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "y"
        .Yrange "-0.5", "0.5"
        .Xcenter "-2.3"
        .Zcenter "-3"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "V_VIAHOLE_L_2"
        .Component "H3B_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "y"
        .Yrange "-0.52", "0.52"
        .Xcenter "-2.3"
        .Zcenter "-6"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_Board:VERTICAL_FR4", "H3B_Tools:V_VIAHOLE_L_2"

    With Cylinder
        .Reset
        .Name "V_VIA_L_2"
        .Component "H3B_Via"
        .Material "O3_COPPER"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "y"
        .Yrange "-0.5", "0.5"
        .Xcenter "-2.3"
        .Zcenter "-6"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "V_VIAHOLE_L_3"
        .Component "H3B_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "y"
        .Yrange "-0.52", "0.52"
        .Xcenter "-2.3"
        .Zcenter "-9"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_Board:VERTICAL_FR4", "H3B_Tools:V_VIAHOLE_L_3"

    With Cylinder
        .Reset
        .Name "V_VIA_L_3"
        .Component "H3B_Via"
        .Material "O3_COPPER"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "y"
        .Yrange "-0.5", "0.5"
        .Xcenter "-2.3"
        .Zcenter "-9"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "V_VIAHOLE_L_4"
        .Component "H3B_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "y"
        .Yrange "-0.52", "0.52"
        .Xcenter "-2.3"
        .Zcenter "-12"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_Board:VERTICAL_FR4", "H3B_Tools:V_VIAHOLE_L_4"

    With Cylinder
        .Reset
        .Name "V_VIA_L_4"
        .Component "H3B_Via"
        .Material "O3_COPPER"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "y"
        .Yrange "-0.5", "0.5"
        .Xcenter "-2.3"
        .Zcenter "-12"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "H_VIAHOLE_R_1"
        .Component "H3B_Tools"
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

    Solid.Subtract "H3B_Board:HORIZONTAL_FR4", "H3B_Tools:H_VIAHOLE_R_1"

    With Cylinder
        .Reset
        .Name "H_VIA_R_1"
        .Component "H3B_Via"
        .Material "O3_COPPER"
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
        .Name "H_VIAHOLE_R_2"
        .Component "H3B_Tools"
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

    Solid.Subtract "H3B_Board:HORIZONTAL_FR4", "H3B_Tools:H_VIAHOLE_R_2"

    With Cylinder
        .Reset
        .Name "H_VIA_R_2"
        .Component "H3B_Via"
        .Material "O3_COPPER"
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
        .Name "H_VIAHOLE_R_3"
        .Component "H3B_Tools"
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

    Solid.Subtract "H3B_Board:HORIZONTAL_FR4", "H3B_Tools:H_VIAHOLE_R_3"

    With Cylinder
        .Reset
        .Name "H_VIA_R_3"
        .Component "H3B_Via"
        .Material "O3_COPPER"
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
        .Name "H_VIAHOLE_R_4"
        .Component "H3B_Tools"
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

    Solid.Subtract "H3B_Board:HORIZONTAL_FR4", "H3B_Tools:H_VIAHOLE_R_4"

    With Cylinder
        .Reset
        .Name "H_VIA_R_4"
        .Component "H3B_Via"
        .Material "O3_COPPER"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "z"
        .Zrange "0", "1"
        .Xcenter "2.3"
        .Ycenter "12"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "V_VIAHOLE_R_1"
        .Component "H3B_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "y"
        .Yrange "-0.52", "0.52"
        .Xcenter "2.3"
        .Zcenter "-3"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_Board:VERTICAL_FR4", "H3B_Tools:V_VIAHOLE_R_1"

    With Cylinder
        .Reset
        .Name "V_VIA_R_1"
        .Component "H3B_Via"
        .Material "O3_COPPER"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "y"
        .Yrange "-0.5", "0.5"
        .Xcenter "2.3"
        .Zcenter "-3"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "V_VIAHOLE_R_2"
        .Component "H3B_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "y"
        .Yrange "-0.52", "0.52"
        .Xcenter "2.3"
        .Zcenter "-6"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_Board:VERTICAL_FR4", "H3B_Tools:V_VIAHOLE_R_2"

    With Cylinder
        .Reset
        .Name "V_VIA_R_2"
        .Component "H3B_Via"
        .Material "O3_COPPER"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "y"
        .Yrange "-0.5", "0.5"
        .Xcenter "2.3"
        .Zcenter "-6"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "V_VIAHOLE_R_3"
        .Component "H3B_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "y"
        .Yrange "-0.52", "0.52"
        .Xcenter "2.3"
        .Zcenter "-9"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_Board:VERTICAL_FR4", "H3B_Tools:V_VIAHOLE_R_3"

    With Cylinder
        .Reset
        .Name "V_VIA_R_3"
        .Component "H3B_Via"
        .Material "O3_COPPER"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "y"
        .Yrange "-0.5", "0.5"
        .Xcenter "2.3"
        .Zcenter "-9"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "V_VIAHOLE_R_4"
        .Component "H3B_Tools"
        .Material "Vacuum"
        .OuterRadius "0.2"
        .InnerRadius "0"
        .Axis "y"
        .Yrange "-0.52", "0.52"
        .Xcenter "2.3"
        .Zcenter "-12"
        .Segments "0"
        .Create
    End With

    Solid.Subtract "H3B_Board:VERTICAL_FR4", "H3B_Tools:V_VIAHOLE_R_4"

    With Cylinder
        .Reset
        .Name "V_VIA_R_4"
        .Component "H3B_Via"
        .Material "O3_COPPER"
        .OuterRadius "0.2"
        .InnerRadius "0.15"
        .Axis "y"
        .Yrange "-0.5", "0.5"
        .Xcenter "2.3"
        .Zcenter "-12"
        .Segments "0"
        .Create
    End With


    ' H3B-T01 V0.1 intentionally creates no RF port and calls no solver.
End Sub
