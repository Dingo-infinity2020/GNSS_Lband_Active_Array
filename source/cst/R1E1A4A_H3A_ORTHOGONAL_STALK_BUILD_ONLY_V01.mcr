Option Explicit

' H3A Orthogonal PCB Feed-Stalk / Support Assembly V0.1 — BUILD ONLY
' Parent: immutable R1E1A1 P094 bare radiator.
' SimulationOps >=0.2.5. NO solver, NO RF port, NO active transistor.

Sub Main()

    StoreParameter "h3a_stalk_t", 1
    StoreParameter "h3a_stalk_halfwidth", 15
    StoreParameter "h3a_notch_half", 8.5
    StoreParameter "h3a_notch_bottom_z", 50.1428571428
    StoreParameter "h3a_interlock_slot_w", 1.25
    StoreParameter "h3a_interlock_mid_z", 25.0714285714
    StoreParameter "h3a_tenon_abs", 12
    StoreParameter "h3a_tenon_len", 3
    StoreParameter "h3a_mortise_len", 3.3
    StoreParameter "h3a_mortise_w", 1.25
    StoreParameter "h3a_rf_transition_abs", 9.4
    StoreParameter "h3a_cavity_span", 17
    StoreParameter "h3a_shield_outer_half", 8
    StoreParameter "h3a_shield_depth", 5.5
    StoreParameter "h3a_route_env_w", 0.7
    StoreParameter "h3a_service_zone_w", 6
    StoreParameter "h3a_service_zone_h", 8

    With Solid
        .SetAutoIntersectionCheckElMag "True"
        .SetAutoIntersectionCheckThermal "False"
        .SetAutoIntersectionCheckMechanics "False"
    End With

    On Error Resume Next
    Port.Delete (1)
    On Error GoTo 0

    With Material
        .Reset
        .Name "H3A_LNA_VISUAL_SURROGATE"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "4"
        .Mue "1.0"
        .TanD "0.02"
        .TanDFreq "0.0"
        .TanDGiven "False"
        .TanDModel "ConstTanD"
        .Colour "0.85", "0.45", "0.25"
        .Create
    End With

    With Material
        .Reset
        .Name "H3A_ROUTE_VISUAL_SURROGATE"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "1.05"
        .Mue "1.0"
        .TanD "0.001"
        .TanDFreq "0.0"
        .TanDGiven "False"
        .TanDModel "ConstTanD"
        .Colour "0.25", "0.75", "0.95"
        .Create
    End With

    With Material
        .Reset
        .Name "H3A_SERVICE_VISUAL_SURROGATE"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "2.5"
        .Mue "1.0"
        .TanD "0.01"
        .TanDFreq "0.0"
        .TanDGiven "False"
        .TanDModel "ConstTanD"
        .Colour "0.7", "0.7", "0.85"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_RAD_X_N"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-13.65", "-10.35"
        .Yrange "-0.625", "0.625"
        .Zrange "57.1228571428", "58.1628571428"
        .Create
    End With

    Solid.Subtract "Substrate:FR4_BOARD", "H3A_Tools:CUT_RAD_X_N"

    With Brick
        .Reset
        .Name "CUT_BP_X_N"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-13.65", "-10.35"
        .Yrange "-0.625", "0.625"
        .Zrange "-0.52", "0.02"
        .Create
    End With

    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H3A_Tools:CUT_BP_X_N"

    With Brick
        .Reset
        .Name "CUT_RAD_X_P"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "10.35", "13.65"
        .Yrange "-0.625", "0.625"
        .Zrange "57.1228571428", "58.1628571428"
        .Create
    End With

    Solid.Subtract "Substrate:FR4_BOARD", "H3A_Tools:CUT_RAD_X_P"

    With Brick
        .Reset
        .Name "CUT_BP_X_P"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "10.35", "13.65"
        .Yrange "-0.625", "0.625"
        .Zrange "-0.52", "0.02"
        .Create
    End With

    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H3A_Tools:CUT_BP_X_P"

    With Brick
        .Reset
        .Name "CUT_RAD_Y_N"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-0.625", "0.625"
        .Yrange "-13.65", "-10.35"
        .Zrange "57.1228571428", "58.1628571428"
        .Create
    End With

    Solid.Subtract "Substrate:FR4_BOARD", "H3A_Tools:CUT_RAD_Y_N"

    With Brick
        .Reset
        .Name "CUT_BP_Y_N"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-0.625", "0.625"
        .Yrange "-13.65", "-10.35"
        .Zrange "-0.52", "0.02"
        .Create
    End With

    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H3A_Tools:CUT_BP_Y_N"

    With Brick
        .Reset
        .Name "CUT_RAD_Y_P"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-0.625", "0.625"
        .Yrange "10.35", "13.65"
        .Zrange "57.1228571428", "58.1628571428"
        .Create
    End With

    Solid.Subtract "Substrate:FR4_BOARD", "H3A_Tools:CUT_RAD_Y_P"

    With Brick
        .Reset
        .Name "CUT_BP_Y_P"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-0.625", "0.625"
        .Yrange "10.35", "13.65"
        .Zrange "-0.52", "0.02"
        .Create
    End With

    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H3A_Tools:CUT_BP_Y_P"

    With Brick
        .Reset
        .Name "X_STALK_BODY"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "-15", "15"
        .Yrange "-0.5", "0.5"
        .Zrange "0", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_X_TOP_NOTCH"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-8.5", "8.5"
        .Yrange "-1", "1"
        .Zrange "50.1428571428", "57.1628571428"
        .Create
    End With

    Solid.Subtract "H3A_Stalk:X_STALK_BODY", "H3A_Tools:CUT_X_TOP_NOTCH"

    With Brick
        .Reset
        .Name "CUT_X_INTERLOCK"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-0.625", "0.625"
        .Yrange "-1", "1"
        .Zrange "-0.02", "25.0714285714"
        .Create
    End With

    Solid.Subtract "H3A_Stalk:X_STALK_BODY", "H3A_Tools:CUT_X_INTERLOCK"

    With Brick
        .Reset
        .Name "Y_STALK_BODY"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "-0.5", "0.5"
        .Yrange "-15", "15"
        .Zrange "0", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_Y_TOP_NOTCH"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-1", "1"
        .Yrange "-8.5", "8.5"
        .Zrange "50.1428571428", "57.1628571428"
        .Create
    End With

    Solid.Subtract "H3A_Stalk:Y_STALK_BODY", "H3A_Tools:CUT_Y_TOP_NOTCH"

    With Brick
        .Reset
        .Name "CUT_Y_INTERLOCK"
        .Component "H3A_Tools"
        .Material "Vacuum"
        .Xrange "-1", "1"
        .Yrange "-0.625", "0.625"
        .Zrange "25.0714285714", "50.1628571428"
        .Create
    End With

    Solid.Subtract "H3A_Stalk:Y_STALK_BODY", "H3A_Tools:CUT_Y_INTERLOCK"

    With Brick
        .Reset
        .Name "X_TOP_TENON_N"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "-13.5", "-10.5"
        .Yrange "-0.5", "0.5"
        .Zrange "57.1428571428", "58.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOTTOM_TENON_N"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "-13.5", "-10.5"
        .Yrange "-0.5", "0.5"
        .Zrange "-0.5", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_TENON_P"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "10.5", "13.5"
        .Yrange "-0.5", "0.5"
        .Zrange "57.1428571428", "58.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOTTOM_TENON_P"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "10.5", "13.5"
        .Yrange "-0.5", "0.5"
        .Zrange "-0.5", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_TENON_N"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "-0.5", "0.5"
        .Yrange "-13.5", "-10.5"
        .Zrange "57.1428571428", "58.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOTTOM_TENON_N"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "-0.5", "0.5"
        .Yrange "-13.5", "-10.5"
        .Zrange "-0.5", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_TENON_P"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "-0.5", "0.5"
        .Yrange "10.5", "13.5"
        .Zrange "57.1428571428", "58.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOTTOM_TENON_P"
        .Component "H3A_Stalk"
        .Material "FR4_COST_BASELINE"
        .Xrange "-0.5", "0.5"
        .Yrange "10.5", "13.5"
        .Zrange "-0.5", "0"
        .Create
    End With

    With Brick
        .Reset
        .Name "GROUND_NE"
        .Component "H3A_HubGround"
        .Material "PEC"
        .Xrange "4", "10"
        .Yrange "4", "10"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "GROUND_NW"
        .Component "H3A_HubGround"
        .Material "PEC"
        .Xrange "-10", "-4"
        .Yrange "4", "10"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "GROUND_SW"
        .Component "H3A_HubGround"
        .Material "PEC"
        .Xrange "-10", "-4"
        .Yrange "-10", "-4"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "GROUND_SE"
        .Component "H3A_HubGround"
        .Material "PEC"
        .Xrange "4", "10"
        .Yrange "-10", "-4"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "LNA_ENV_NE"
        .Component "H3A_LNAEnvelope"
        .Material "H3A_LNA_VISUAL_SURROGATE"
        .Xrange "3.38406204336", "5.38406204336"
        .Yrange "3.38406204336", "5.38406204336"
        .Zrange "56.5078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "LNA_ENV_NW"
        .Component "H3A_LNAEnvelope"
        .Material "H3A_LNA_VISUAL_SURROGATE"
        .Xrange "-5.38406204336", "-3.38406204336"
        .Yrange "3.38406204336", "5.38406204336"
        .Zrange "56.5078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "LNA_ENV_SW"
        .Component "H3A_LNAEnvelope"
        .Material "H3A_LNA_VISUAL_SURROGATE"
        .Xrange "-5.38406204336", "-3.38406204336"
        .Yrange "-5.38406204336", "-3.38406204336"
        .Zrange "56.5078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "LNA_ENV_SE"
        .Component "H3A_LNAEnvelope"
        .Material "H3A_LNA_VISUAL_SURROGATE"
        .Xrange "3.38406204336", "5.38406204336"
        .Yrange "-5.38406204336", "-3.38406204336"
        .Zrange "56.5078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_N_L"
        .Component "H3A_Shield"
        .Material "PEC"
        .Xrange "-8", "-2"
        .Yrange "7.6", "8"
        .Zrange "51.6078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_N_R"
        .Component "H3A_Shield"
        .Material "PEC"
        .Xrange "2", "8"
        .Yrange "7.6", "8"
        .Zrange "51.6078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_S_L"
        .Component "H3A_Shield"
        .Material "PEC"
        .Xrange "-8", "-2"
        .Yrange "-8", "-7.6"
        .Zrange "51.6078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_S_R"
        .Component "H3A_Shield"
        .Material "PEC"
        .Xrange "2", "8"
        .Yrange "-8", "-7.6"
        .Zrange "51.6078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_E_B"
        .Component "H3A_Shield"
        .Material "PEC"
        .Xrange "7.6", "8"
        .Yrange "-8", "-2"
        .Zrange "51.6078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_E_T"
        .Component "H3A_Shield"
        .Material "PEC"
        .Xrange "7.6", "8"
        .Yrange "2", "8"
        .Zrange "51.6078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_W_B"
        .Component "H3A_Shield"
        .Material "PEC"
        .Xrange "-8", "-7.6"
        .Yrange "-8", "-2"
        .Zrange "51.6078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_W_T"
        .Component "H3A_Shield"
        .Material "PEC"
        .Xrange "-8", "-7.6"
        .Yrange "2", "8"
        .Zrange "51.6078571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_LID"
        .Component "H3A_Shield"
        .Material "PEC"
        .Xrange "-8", "8"
        .Yrange "-8", "8"
        .Zrange "51.3078571428", "51.6078571428"
        .Create
    End With

    With Extrude
        .Reset
        .Name "ROUTE_ENV_NE"
        .Component "H3A_RouteEnvelope"
        .Material "H3A_ROUTE_VISUAL_SURROGATE"
        .Mode "Pointlist"
        .Height "0.22"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "56.7528571428"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "5.85674410178", "3.56174364103"
        .LineTo "8.95268536713", "0.855809335785"
        .LineTo "8.49202285078", "0.328751420528"
        .LineTo "5.39608158543", "3.03468572577"
        .LineTo "5.85674410178", "3.56174364103"
        .Create
    End With

    With Extrude
        .Reset
        .Name "ROUTE_ENV_SW"
        .Component "H3A_RouteEnvelope"
        .Material "H3A_ROUTE_VISUAL_SURROGATE"
        .Mode "Pointlist"
        .Height "0.22"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "56.7528571428"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-5.85674410178", "-3.56174364103"
        .LineTo "-8.95268536713", "-0.855809335785"
        .LineTo "-8.49202285078", "-0.328751420528"
        .LineTo "-5.39608158543", "-3.03468572577"
        .LineTo "-5.85674410178", "-3.56174364103"
        .Create
    End With

    With Extrude
        .Reset
        .Name "ROUTE_ENV_NW"
        .Component "H3A_RouteEnvelope"
        .Material "H3A_ROUTE_VISUAL_SURROGATE"
        .Mode "Pointlist"
        .Height "0.22"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "56.7528571428"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-3.56174364103", "5.85674410178"
        .LineTo "-0.855809335785", "8.95268536713"
        .LineTo "-0.328751420528", "8.49202285078"
        .LineTo "-3.03468572577", "5.39608158543"
        .LineTo "-3.56174364103", "5.85674410178"
        .Create
    End With

    With Extrude
        .Reset
        .Name "ROUTE_ENV_SE"
        .Component "H3A_RouteEnvelope"
        .Material "H3A_ROUTE_VISUAL_SURROGATE"
        .Mode "Pointlist"
        .Height "0.22"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "56.7528571428"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "3.56174364103", "-5.85674410178"
        .LineTo "0.855809335785", "-8.95268536713"
        .LineTo "0.328751420528", "-8.49202285078"
        .LineTo "3.03468572577", "-5.39608158543"
        .LineTo "3.56174364103", "-5.85674410178"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_PAD_N_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-13", "-11"
        .Yrange "-0.535", "-0.5"
        .Zrange "56.4", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_LAND_N_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-13.4", "-10.6"
        .Yrange "-1.625", "-0.625"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_SOLDER_N_A"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "-13", "-11"
        .Yrange "-1", "-0.535"
        .Zrange "56.65", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_PAD_N_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-13", "-11"
        .Yrange "0.5", "0.535"
        .Zrange "56.4", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_LAND_N_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-13.4", "-10.6"
        .Yrange "0.625", "1.625"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_SOLDER_N_B"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "-13", "-11"
        .Yrange "0.535", "1"
        .Zrange "56.65", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_PAD_P_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "11", "13"
        .Yrange "-0.535", "-0.5"
        .Zrange "56.4", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_LAND_P_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "10.6", "13.4"
        .Yrange "-1.625", "-0.625"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_SOLDER_P_A"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "11", "13"
        .Yrange "-1", "-0.535"
        .Zrange "56.65", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_PAD_P_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "11", "13"
        .Yrange "0.5", "0.535"
        .Zrange "56.4", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_LAND_P_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "10.6", "13.4"
        .Yrange "0.625", "1.625"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_TOP_SOLDER_P_B"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "11", "13"
        .Yrange "0.535", "1"
        .Zrange "56.65", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_PAD_N_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "-13", "-11"
        .Zrange "56.4", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_LAND_N_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-1.625", "-0.625"
        .Yrange "-13.4", "-10.6"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_SOLDER_N_A"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "-1", "-0.535"
        .Yrange "-13", "-11"
        .Zrange "56.65", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_PAD_N_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "0.5", "0.535"
        .Yrange "-13", "-11"
        .Zrange "56.4", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_LAND_N_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "0.625", "1.625"
        .Yrange "-13.4", "-10.6"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_SOLDER_N_B"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "0.535", "1"
        .Yrange "-13", "-11"
        .Zrange "56.65", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_PAD_P_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "11", "13"
        .Zrange "56.4", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_LAND_P_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-1.625", "-0.625"
        .Yrange "10.6", "13.4"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_SOLDER_P_A"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "-1", "-0.535"
        .Yrange "11", "13"
        .Zrange "56.65", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_PAD_P_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "0.5", "0.535"
        .Yrange "11", "13"
        .Zrange "56.4", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_LAND_P_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "0.625", "1.625"
        .Yrange "10.6", "13.4"
        .Zrange "57.1078571428", "57.1428571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_TOP_SOLDER_P_B"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "0.535", "1"
        .Yrange "11", "13"
        .Zrange "56.65", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOT_PAD_N_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-13", "-11"
        .Yrange "-0.535", "-0.5"
        .Zrange "0", "0.7"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOT_SOLDER_N_A"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "-13", "-11"
        .Yrange "-0.9", "-0.535"
        .Zrange "0", "0.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOT_PAD_N_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-13", "-11"
        .Yrange "0.5", "0.535"
        .Zrange "0", "0.7"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOT_SOLDER_N_B"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "-13", "-11"
        .Yrange "0.535", "0.9"
        .Zrange "0", "0.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOT_PAD_P_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "11", "13"
        .Yrange "-0.535", "-0.5"
        .Zrange "0", "0.7"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOT_SOLDER_P_A"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "11", "13"
        .Yrange "-0.9", "-0.535"
        .Zrange "0", "0.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOT_PAD_P_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "11", "13"
        .Yrange "0.5", "0.535"
        .Zrange "0", "0.7"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_BOT_SOLDER_P_B"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "11", "13"
        .Yrange "0.535", "0.9"
        .Zrange "0", "0.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOT_PAD_N_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "-13", "-11"
        .Zrange "0", "0.7"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOT_SOLDER_N_A"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "-0.9", "-0.535"
        .Yrange "-13", "-11"
        .Zrange "0", "0.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOT_PAD_N_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "0.5", "0.535"
        .Yrange "-13", "-11"
        .Zrange "0", "0.7"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOT_SOLDER_N_B"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "0.535", "0.9"
        .Yrange "-13", "-11"
        .Zrange "0", "0.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOT_PAD_P_A"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "11", "13"
        .Zrange "0", "0.7"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOT_SOLDER_P_A"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "-0.9", "-0.535"
        .Yrange "11", "13"
        .Zrange "0", "0.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOT_PAD_P_B"
        .Component "H3A_MechLand"
        .Material "PEC"
        .Xrange "0.5", "0.535"
        .Yrange "11", "13"
        .Zrange "0", "0.7"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_BOT_SOLDER_P_B"
        .Component "H3A_MechSolder"
        .Material "PEC"
        .Xrange "0.535", "0.9"
        .Yrange "11", "13"
        .Zrange "0", "0.5"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_VPAD_N_G1"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-10.6", "-10.2"
        .Yrange "0.5", "0.535"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_HPAD_N_G1"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-10.6", "-10.2"
        .Yrange "0.535", "1.335"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_SOLDER_N_G1"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "-10.6", "-10.2"
        .Yrange "0.535", "0.95"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_ROUTE_N_G1"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "-10.6", "-10.2"
        .Yrange "0.5", "0.535"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_VPAD_N_SIG"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-9.7", "-9.1"
        .Yrange "0.5", "0.535"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_HPAD_N_SIG"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-9.7", "-9.1"
        .Yrange "0.535", "1.335"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_SOLDER_N_SIG"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "-9.7", "-9.1"
        .Yrange "0.535", "0.95"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_ROUTE_N_SIG"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "-9.7", "-9.1"
        .Yrange "0.5", "0.535"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_VPAD_N_G2"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-8.6", "-8.2"
        .Yrange "0.5", "0.535"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_HPAD_N_G2"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-8.6", "-8.2"
        .Yrange "0.535", "1.335"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_SOLDER_N_G2"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "-8.6", "-8.2"
        .Yrange "0.535", "0.95"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_ROUTE_N_G2"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "-8.6", "-8.2"
        .Yrange "0.5", "0.535"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_SERVICE_ENV_N"
        .Component "H3A_ServiceEnvelope"
        .Material "H3A_SERVICE_VISUAL_SURROGATE"
        .Xrange "-12.4", "-6.4"
        .Yrange "1", "2"
        .Zrange "9", "17"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_VPAD_P_G1"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "8.2", "8.6"
        .Yrange "0.5", "0.535"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_HPAD_P_G1"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "8.2", "8.6"
        .Yrange "0.535", "1.335"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_SOLDER_P_G1"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "8.2", "8.6"
        .Yrange "0.535", "0.95"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_ROUTE_P_G1"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "8.2", "8.6"
        .Yrange "0.5", "0.535"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_VPAD_P_SIG"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "9.1", "9.7"
        .Yrange "0.5", "0.535"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_HPAD_P_SIG"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "9.1", "9.7"
        .Yrange "0.535", "1.335"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_SOLDER_P_SIG"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "9.1", "9.7"
        .Yrange "0.535", "0.95"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_ROUTE_P_SIG"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "9.1", "9.7"
        .Yrange "0.5", "0.535"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_VPAD_P_G2"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "10.2", "10.6"
        .Yrange "0.5", "0.535"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_HPAD_P_G2"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "10.2", "10.6"
        .Yrange "0.535", "1.335"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_RF_SOLDER_P_G2"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "10.2", "10.6"
        .Yrange "0.535", "0.95"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_ROUTE_P_G2"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "10.2", "10.6"
        .Yrange "0.5", "0.535"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "X_SERVICE_ENV_P"
        .Component "H3A_ServiceEnvelope"
        .Material "H3A_SERVICE_VISUAL_SURROGATE"
        .Xrange "6.4", "12.4"
        .Yrange "1", "2"
        .Zrange "9", "17"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_VPAD_N_G1"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "-10.6", "-10.2"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_HPAD_N_G1"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-1.335", "-0.535"
        .Yrange "-10.6", "-10.2"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_SOLDER_N_G1"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "-0.95", "-0.535"
        .Yrange "-10.6", "-10.2"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_ROUTE_N_G1"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "-10.6", "-10.2"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_VPAD_N_SIG"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "-9.7", "-9.1"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_HPAD_N_SIG"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-1.335", "-0.535"
        .Yrange "-9.7", "-9.1"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_SOLDER_N_SIG"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "-0.95", "-0.535"
        .Yrange "-9.7", "-9.1"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_ROUTE_N_SIG"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "-9.7", "-9.1"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_VPAD_N_G2"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "-8.6", "-8.2"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_HPAD_N_G2"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-1.335", "-0.535"
        .Yrange "-8.6", "-8.2"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_SOLDER_N_G2"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "-0.95", "-0.535"
        .Yrange "-8.6", "-8.2"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_ROUTE_N_G2"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "-8.6", "-8.2"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_SERVICE_ENV_N"
        .Component "H3A_ServiceEnvelope"
        .Material "H3A_SERVICE_VISUAL_SURROGATE"
        .Xrange "-2", "-1"
        .Yrange "-12.4", "-6.4"
        .Zrange "9", "17"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_VPAD_P_G1"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "8.2", "8.6"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_HPAD_P_G1"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-1.335", "-0.535"
        .Yrange "8.2", "8.6"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_SOLDER_P_G1"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "-0.95", "-0.535"
        .Yrange "8.2", "8.6"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_ROUTE_P_G1"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "8.2", "8.6"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_VPAD_P_SIG"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "9.1", "9.7"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_HPAD_P_SIG"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-1.335", "-0.535"
        .Yrange "9.1", "9.7"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_SOLDER_P_SIG"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "-0.95", "-0.535"
        .Yrange "9.1", "9.7"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_ROUTE_P_SIG"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "9.1", "9.7"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_VPAD_P_G2"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "10.2", "10.6"
        .Zrange "56.4", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_HPAD_P_G2"
        .Component "H3A_RFTransition"
        .Material "PEC"
        .Xrange "-1.335", "-0.535"
        .Yrange "10.2", "10.6"
        .Zrange "57.0728571428", "57.1078571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_RF_SOLDER_P_G2"
        .Component "H3A_RFSolder"
        .Material "PEC"
        .Xrange "-0.95", "-0.535"
        .Yrange "10.2", "10.6"
        .Zrange "56.78", "57.0728571428"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_ROUTE_P_G2"
        .Component "H3A_StalkRF"
        .Material "PEC"
        .Xrange "-0.535", "-0.5"
        .Yrange "10.2", "10.6"
        .Zrange "5", "56.4"
        .Create
    End With

    With Brick
        .Reset
        .Name "Y_SERVICE_ENV_P"
        .Component "H3A_ServiceEnvelope"
        .Material "H3A_SERVICE_VISUAL_SURROGATE"
        .Xrange "-2", "-1"
        .Yrange "6.4", "12.4"
        .Zrange "9", "17"
        .Create
    End With


    ' H3A V0.1 intentionally creates no RF port and calls no solver.
End Sub
