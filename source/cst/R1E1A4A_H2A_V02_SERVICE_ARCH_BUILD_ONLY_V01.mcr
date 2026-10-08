Option Explicit

' H2A Universal Passive/Active Center Structure V0.2 SERVICE ARCHITECTURE — BUILD ONLY
' Parent: immutable R1E1A1 P094 bare radiator.
' Service-routing build-only model; NO solver, transistor or optimization.

Sub Main()

    StoreParameter "h2a_s2", 0.7071067811865476
    StoreParameter "h2a_ground_outer_half", 10.0
    StoreParameter "h2a_clear_half", 4.0
    StoreParameter "h2a_pad_half", 0.45
    StoreParameter "h2a_pin_half", 0.15
    StoreParameter "h2a_terminal_xy", "terminal_r*h2a_s2"
    StoreParameter "h2a_package_r", 6.2
    StoreParameter "h2a_package_xy", "h2a_package_r*h2a_s2"
    StoreParameter "h2a_package_half", 1.0
    StoreParameter "h2a_package_h", 0.60
    StoreParameter "h2a_backside_cu_top", "substrate_bottom_z"
    StoreParameter "h2a_backside_cu_bottom", "substrate_bottom_z-copper_t"
    StoreParameter "h2a_package_top_z", "h2a_backside_cu_bottom"
    StoreParameter "h2a_package_bottom_z", "h2a_package_top_z-h2a_package_h"

    ' Remove the old ideal 100-ohm differential port; H2A has no RF port.
    Port.Delete (1)

    StoreParameter "h2a_shield_outer_half", 9.0
    StoreParameter "h2a_shield_wall", 0.50
    StoreParameter "h2a_shield_inner_half", "h2a_shield_outer_half-h2a_shield_wall"
    StoreParameter "h2a_shield_depth", 6.0
    StoreParameter "h2a_shield_lid_t", 0.30
    StoreParameter "h2a_shield_top_z", "h2a_backside_cu_bottom"
    StoreParameter "h2a_shield_bottom_z", "h2a_shield_top_z-h2a_shield_depth"
    StoreParameter "h2a_shield_lid_bottom_z", "h2a_shield_bottom_z-h2a_shield_lid_t"

    StoreParameter "h2a_carrier_outer_half", 15.0
    StoreParameter "h2a_carrier_inner_half", 10.5
    StoreParameter "h2a_carrier_z_bottom", 0.0
    StoreParameter "h2a_carrier_z_top", "substrate_bottom_z"

    With Material
        .Reset
        .Name "PEEK_VISUAL_SURROGATE"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "3.2"
        .Mue "1.0"
        .TanD "0.004"
        .TanDFreq "0.0"
        .TanDGiven "False"
        .TanDModel "ConstTanD"
        .Create
    End With

    With Material
        .Reset
        .Name "H2A_PACKAGE_VISUAL_SURROGATE"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "4.0"
        .Mue "1.0"
        .TanD "0.02"
        .TanDFreq "0.0"
        .TanDGiven "False"
        .TanDModel "ConstTanD"
        .Create
    End With

    ' Patterned backside ground frame: 20x20 mm outer, 8x8 mm center clearance.
    With Brick
        .Reset
        .Name "GROUND_N"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "-h2a_ground_outer_half", "h2a_ground_outer_half"
        .Yrange "h2a_clear_half", "h2a_ground_outer_half"
        .Zrange "h2a_backside_cu_bottom", "h2a_backside_cu_top"
        .Create
    End With

    With Brick
        .Reset
        .Name "GROUND_S"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "-h2a_ground_outer_half", "h2a_ground_outer_half"
        .Yrange "-h2a_ground_outer_half", "-h2a_clear_half"
        .Zrange "h2a_backside_cu_bottom", "h2a_backside_cu_top"
        .Create
    End With
    With Brick
        .Reset
        .Name "GROUND_E"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "h2a_clear_half", "h2a_ground_outer_half"
        .Yrange "-h2a_clear_half", "h2a_clear_half"
        .Zrange "h2a_backside_cu_bottom", "h2a_backside_cu_top"
        .Create
    End With
    With Brick
        .Reset
        .Name "GROUND_W"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "-h2a_ground_outer_half", "-h2a_clear_half"
        .Yrange "-h2a_clear_half", "h2a_clear_half"
        .Zrange "h2a_backside_cu_bottom", "h2a_backside_cu_top"
        .Create
    End With

    ' Four signal landing pads and RF pin/via proxies.
    With Brick
        .Reset
        .Name "PAD_NE"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "h2a_terminal_xy-h2a_pad_half", "h2a_terminal_xy+h2a_pad_half"
        .Yrange "h2a_terminal_xy-h2a_pad_half", "h2a_terminal_xy+h2a_pad_half"
        .Zrange "h2a_backside_cu_bottom", "h2a_backside_cu_top"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN_NE"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "h2a_terminal_xy-h2a_pin_half", "h2a_terminal_xy+h2a_pin_half"
        .Yrange "h2a_terminal_xy-h2a_pin_half", "h2a_terminal_xy+h2a_pin_half"
        .Zrange "h2a_backside_cu_bottom", "copper_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "PAD_NW"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "-h2a_terminal_xy-h2a_pad_half", "-h2a_terminal_xy+h2a_pad_half"
        .Yrange "h2a_terminal_xy-h2a_pad_half", "h2a_terminal_xy+h2a_pad_half"
        .Zrange "h2a_backside_cu_bottom", "h2a_backside_cu_top"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN_NW"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "-h2a_terminal_xy-h2a_pin_half", "-h2a_terminal_xy+h2a_pin_half"
        .Yrange "h2a_terminal_xy-h2a_pin_half", "h2a_terminal_xy+h2a_pin_half"
        .Zrange "h2a_backside_cu_bottom", "copper_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "PAD_SW"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "-h2a_terminal_xy-h2a_pad_half", "-h2a_terminal_xy+h2a_pad_half"
        .Yrange "-h2a_terminal_xy-h2a_pad_half", "-h2a_terminal_xy+h2a_pad_half"
        .Zrange "h2a_backside_cu_bottom", "h2a_backside_cu_top"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN_SW"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "-h2a_terminal_xy-h2a_pin_half", "-h2a_terminal_xy+h2a_pin_half"
        .Yrange "-h2a_terminal_xy-h2a_pin_half", "-h2a_terminal_xy+h2a_pin_half"
        .Zrange "h2a_backside_cu_bottom", "copper_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "PAD_SE"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "h2a_terminal_xy-h2a_pad_half", "h2a_terminal_xy+h2a_pad_half"
        .Yrange "-h2a_terminal_xy-h2a_pad_half", "-h2a_terminal_xy+h2a_pad_half"
        .Zrange "h2a_backside_cu_bottom", "h2a_backside_cu_top"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN_SE"
        .Component "H2A_FeedModule"
        .Material "PEC"
        .Xrange "h2a_terminal_xy-h2a_pin_half", "h2a_terminal_xy+h2a_pin_half"
        .Yrange "-h2a_terminal_xy-h2a_pin_half", "-h2a_terminal_xy+h2a_pin_half"
        .Zrange "h2a_backside_cu_bottom", "copper_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "LNA_ENV_NE"
        .Component "H2A_PopulationEnvelope"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "h2a_package_xy-h2a_package_half", "h2a_package_xy+h2a_package_half"
        .Yrange "h2a_package_xy-h2a_package_half", "h2a_package_xy+h2a_package_half"
        .Zrange "h2a_package_bottom_z", "h2a_package_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "LNA_ENV_NW"
        .Component "H2A_PopulationEnvelope"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "-h2a_package_xy-h2a_package_half", "-h2a_package_xy+h2a_package_half"
        .Yrange "h2a_package_xy-h2a_package_half", "h2a_package_xy+h2a_package_half"
        .Zrange "h2a_package_bottom_z", "h2a_package_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "LNA_ENV_SW"
        .Component "H2A_PopulationEnvelope"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "-h2a_package_xy-h2a_package_half", "-h2a_package_xy+h2a_package_half"
        .Yrange "-h2a_package_xy-h2a_package_half", "-h2a_package_xy+h2a_package_half"
        .Zrange "h2a_package_bottom_z", "h2a_package_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "LNA_ENV_SE"
        .Component "H2A_PopulationEnvelope"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "h2a_package_xy-h2a_package_half", "h2a_package_xy+h2a_package_half"
        .Yrange "-h2a_package_xy-h2a_package_half", "-h2a_package_xy+h2a_package_half"
        .Zrange "h2a_package_bottom_z", "h2a_package_top_z"
        .Create
    End With

    ' H2A V0.2 service architecture parameters.
    StoreParameter "h2av02_mhf_r", 9.0
    StoreParameter "h2av02_mhf_xy", "h2av02_mhf_r*h2a_s2"
    StoreParameter "h2av02_mhf_half", 1.20
    StoreParameter "h2av02_mhf_h", 1.20
    StoreParameter "h2av02_mhf_top_z", "h2a_backside_cu_bottom"
    StoreParameter "h2av02_mhf_bottom_z", "h2av02_mhf_top_z-h2av02_mhf_h"
    StoreParameter "h2av02_route_z", "(h2av02_mhf_top_z+h2av02_mhf_bottom_z)/2"
    StoreParameter "h2av02_output_r0", 7.20
    StoreParameter "h2av02_output_r1", 8.70
    StoreParameter "h2av02_output_halfw", 0.30
    StoreParameter "h2av02_tube_r", 13.50
    StoreParameter "h2av02_tube_xy", "h2av02_tube_r*h2a_s2"
    StoreParameter "h2av02_tube_outer_half", 1.50
    StoreParameter "h2av02_tube_inner_half", 0.70
    StoreParameter "h2av02_spacer_half", 1.80
    StoreParameter "h2av02_spacer_t", 0.50
    StoreParameter "h2av02_feedthrough_half", 0.90
    StoreParameter "h2av02_tube_top_z", "h2a_backside_cu_bottom-h2av02_spacer_t"
    StoreParameter "h2av02_tube_bottom_z", "h2av02_spacer_t"
    StoreParameter "h2av02_cable_half", 0.405
    StoreParameter "h2av02_cable_r0", 9.0
    StoreParameter "h2av02_cable_r1", "h2av02_tube_r"
    StoreParameter "h2av02_shield_mid_half", 5.50
    StoreParameter "h2av02_mmcx_half", 2.50
    StoreParameter "h2av02_mmcx_bottom_z", -6.0
    StoreParameter "h2av02_mmcx_top_z", -0.5

    With Material
        .Reset
        .Name "H2A_MICROCOAX_ENVELOPE_SURROGATE"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "2.1"
        .Mue "1.0"
        .TanD "0.001"
        .TanDFreq "0.0"
        .TanDGiven "False"
        .TanDModel "ConstTanD"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_N"
        .Component "H2A_Shield"
        .Material "PEC"
        .Xrange "-h2av02_shield_mid_half", "h2av02_shield_mid_half"
        .Yrange "h2a_shield_inner_half", "h2a_shield_outer_half"
        .Zrange "h2a_shield_bottom_z", "h2a_shield_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_S"
        .Component "H2A_Shield"
        .Material "PEC"
        .Xrange "-h2av02_shield_mid_half", "h2av02_shield_mid_half"
        .Yrange "-h2a_shield_outer_half", "-h2a_shield_inner_half"
        .Zrange "h2a_shield_bottom_z", "h2a_shield_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_E"
        .Component "H2A_Shield"
        .Material "PEC"
        .Xrange "h2a_shield_inner_half", "h2a_shield_outer_half"
        .Yrange "-h2av02_shield_mid_half", "h2av02_shield_mid_half"
        .Zrange "h2a_shield_bottom_z", "h2a_shield_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_W"
        .Component "H2A_Shield"
        .Material "PEC"
        .Xrange "-h2a_shield_outer_half", "-h2a_shield_inner_half"
        .Yrange "-h2av02_shield_mid_half", "h2av02_shield_mid_half"
        .Zrange "h2a_shield_bottom_z", "h2a_shield_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "SHIELD_LID"
        .Component "H2A_Shield"
        .Material "PEC"
        .Xrange "-h2a_shield_outer_half", "h2a_shield_outer_half"
        .Yrange "-h2a_shield_outer_half", "h2a_shield_outer_half"
        .Zrange "h2a_shield_lid_bottom_z", "h2a_shield_bottom_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "MHF_ENV_NE"
        .Component "H2A_ServiceConnector"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "h2av02_mhf_xy-h2av02_mhf_half", "h2av02_mhf_xy+h2av02_mhf_half"
        .Yrange "h2av02_mhf_xy-h2av02_mhf_half", "h2av02_mhf_xy+h2av02_mhf_half"
        .Zrange "h2av02_mhf_bottom_z", "h2av02_mhf_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "MHF_ENV_NW"
        .Component "H2A_ServiceConnector"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "-h2av02_mhf_xy-h2av02_mhf_half", "-h2av02_mhf_xy+h2av02_mhf_half"
        .Yrange "h2av02_mhf_xy-h2av02_mhf_half", "h2av02_mhf_xy+h2av02_mhf_half"
        .Zrange "h2av02_mhf_bottom_z", "h2av02_mhf_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "MHF_ENV_SW"
        .Component "H2A_ServiceConnector"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "-h2av02_mhf_xy-h2av02_mhf_half", "-h2av02_mhf_xy+h2av02_mhf_half"
        .Yrange "-h2av02_mhf_xy-h2av02_mhf_half", "-h2av02_mhf_xy+h2av02_mhf_half"
        .Zrange "h2av02_mhf_bottom_z", "h2av02_mhf_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "MHF_ENV_SE"
        .Component "H2A_ServiceConnector"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "h2av02_mhf_xy-h2av02_mhf_half", "h2av02_mhf_xy+h2av02_mhf_half"
        .Yrange "-h2av02_mhf_xy-h2av02_mhf_half", "-h2av02_mhf_xy+h2av02_mhf_half"
        .Zrange "h2av02_mhf_bottom_z", "h2av02_mhf_top_z"
        .Create
    End With

    With Extrude
        .Reset
        .Name "OUTPUT_ROUTE_ENV_NE"
        .Component "H2A_ServiceRouting"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Mode "Pointlist"
        .Height "0.10"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "h2av02_route_z-0.05"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "(h2av02_output_r0-h2av02_output_halfw)*h2a_s2", "(h2av02_output_r0+h2av02_output_halfw)*h2a_s2"
        .LineTo "(h2av02_output_r1-h2av02_output_halfw)*h2a_s2", "(h2av02_output_r1+h2av02_output_halfw)*h2a_s2"
        .LineTo "(h2av02_output_r1+h2av02_output_halfw)*h2a_s2", "(h2av02_output_r1-h2av02_output_halfw)*h2a_s2"
        .LineTo "(h2av02_output_r0+h2av02_output_halfw)*h2a_s2", "(h2av02_output_r0-h2av02_output_halfw)*h2a_s2"
        .LineTo "(h2av02_output_r0-h2av02_output_halfw)*h2a_s2", "(h2av02_output_r0+h2av02_output_halfw)*h2a_s2"
        .Create
    End With

    With Transform
        .Reset
        .Name "H2A_ServiceRouting:OUTPUT_ROUTE_ENV_NE"
        .Origin "Free"
        .Center "0.0", "0.0", "h2av02_route_z-0.05"
        .Angle "0.0", "0.0", "90.0"
        .MultipleObjects "True"
        .GroupObjects "False"
        .Repetitions "3"
        .MultipleSelection "False"
        .AutoDestination "True"
        .Transform "Shape", "Rotate"
    End With

    With Extrude
        .Reset
        .Name "MICROCOAX_HORIZ_NE"
        .Component "H2A_ServiceRouting"
        .Material "H2A_MICROCOAX_ENVELOPE_SURROGATE"
        .Mode "Pointlist"
        .Height "2*h2av02_cable_half"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "h2av02_route_z-h2av02_cable_half"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "(h2av02_cable_r0-h2av02_cable_half)*h2a_s2", "(h2av02_cable_r0+h2av02_cable_half)*h2a_s2"
        .LineTo "(h2av02_cable_r1-h2av02_cable_half)*h2a_s2", "(h2av02_cable_r1+h2av02_cable_half)*h2a_s2"
        .LineTo "(h2av02_cable_r1+h2av02_cable_half)*h2a_s2", "(h2av02_cable_r1-h2av02_cable_half)*h2a_s2"
        .LineTo "(h2av02_cable_r0+h2av02_cable_half)*h2a_s2", "(h2av02_cable_r0-h2av02_cable_half)*h2a_s2"
        .LineTo "(h2av02_cable_r0-h2av02_cable_half)*h2a_s2", "(h2av02_cable_r0+h2av02_cable_half)*h2a_s2"
        .Create
    End With

    With Transform
        .Reset
        .Name "H2A_ServiceRouting:MICROCOAX_HORIZ_NE"
        .Origin "Free"
        .Center "0.0", "0.0", "h2av02_route_z-h2av02_cable_half"
        .Angle "0.0", "0.0", "90.0"
        .MultipleObjects "True"
        .GroupObjects "False"
        .Repetitions "3"
        .MultipleSelection "False"
        .AutoDestination "True"
        .Transform "Shape", "Rotate"
    End With

    With Brick
        .Reset
        .Name "CUT_BACKPLANE_NE"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "-0.55", "0.05"
        .Create
    End With

    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H2A_Tools:CUT_BACKPLANE_NE"

    With Brick
        .Reset
        .Name "COPPER_TUBE_NE"
        .Component "H2A_ServiceTube"
        .Material "PEC"
        .Xrange "h2av02_tube_xy-h2av02_tube_outer_half", "h2av02_tube_xy+h2av02_tube_outer_half"
        .Yrange "h2av02_tube_xy-h2av02_tube_outer_half", "h2av02_tube_xy+h2av02_tube_outer_half"
        .Zrange "h2av02_tube_bottom_z", "h2av02_tube_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_COPPER_TUBE_NE"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "h2av02_tube_xy-h2av02_tube_inner_half", "h2av02_tube_xy+h2av02_tube_inner_half"
        .Yrange "h2av02_tube_xy-h2av02_tube_inner_half", "h2av02_tube_xy+h2av02_tube_inner_half"
        .Zrange "(h2av02_tube_bottom_z)-0.05", "(h2av02_tube_top_z)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceTube:COPPER_TUBE_NE", "H2A_Tools:CUT_COPPER_TUBE_NE"

    With Brick
        .Reset
        .Name "TOP_SPACER_NE"
        .Component "H2A_ServiceInterface"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "h2av02_tube_xy-h2av02_spacer_half", "h2av02_tube_xy+h2av02_spacer_half"
        .Yrange "h2av02_tube_xy-h2av02_spacer_half", "h2av02_tube_xy+h2av02_spacer_half"
        .Zrange "h2av02_tube_top_z", "h2a_backside_cu_bottom"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_TOP_SPACER_NE"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "(h2av02_tube_top_z)-0.05", "(h2a_backside_cu_bottom)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceInterface:TOP_SPACER_NE", "H2A_Tools:CUT_TOP_SPACER_NE"

    With Brick
        .Reset
        .Name "BOTTOM_SPACER_NE"
        .Component "H2A_ServiceInterface"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "h2av02_tube_xy-h2av02_spacer_half", "h2av02_tube_xy+h2av02_spacer_half"
        .Yrange "h2av02_tube_xy-h2av02_spacer_half", "h2av02_tube_xy+h2av02_spacer_half"
        .Zrange "0.0", "h2av02_tube_bottom_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_BOTTOM_SPACER_NE"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "(0.0)-0.05", "(h2av02_tube_bottom_z)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceInterface:BOTTOM_SPACER_NE", "H2A_Tools:CUT_BOTTOM_SPACER_NE"

    With Brick
        .Reset
        .Name "MICROCOAX_VERT_NE"
        .Component "H2A_ServiceRouting"
        .Material "H2A_MICROCOAX_ENVELOPE_SURROGATE"
        .Xrange "h2av02_tube_xy-h2av02_cable_half", "h2av02_tube_xy+h2av02_cable_half"
        .Yrange "h2av02_tube_xy-h2av02_cable_half", "h2av02_tube_xy+h2av02_cable_half"
        .Zrange "h2av02_mmcx_bottom_z", "h2av02_route_z+h2av02_cable_half"
        .Create
    End With

    With Brick
        .Reset
        .Name "MMCX_ENV_NE"
        .Component "H2A_ServiceConnector"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "h2av02_tube_xy-h2av02_mmcx_half", "h2av02_tube_xy+h2av02_mmcx_half"
        .Yrange "h2av02_tube_xy-h2av02_mmcx_half", "h2av02_tube_xy+h2av02_mmcx_half"
        .Zrange "h2av02_mmcx_bottom_z", "h2av02_mmcx_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_BACKPLANE_NW"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "-0.55", "0.05"
        .Create
    End With

    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H2A_Tools:CUT_BACKPLANE_NW"

    With Brick
        .Reset
        .Name "COPPER_TUBE_NW"
        .Component "H2A_ServiceTube"
        .Material "PEC"
        .Xrange "-h2av02_tube_xy-h2av02_tube_outer_half", "-h2av02_tube_xy+h2av02_tube_outer_half"
        .Yrange "h2av02_tube_xy-h2av02_tube_outer_half", "h2av02_tube_xy+h2av02_tube_outer_half"
        .Zrange "h2av02_tube_bottom_z", "h2av02_tube_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_COPPER_TUBE_NW"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "-h2av02_tube_xy-h2av02_tube_inner_half", "-h2av02_tube_xy+h2av02_tube_inner_half"
        .Yrange "h2av02_tube_xy-h2av02_tube_inner_half", "h2av02_tube_xy+h2av02_tube_inner_half"
        .Zrange "(h2av02_tube_bottom_z)-0.05", "(h2av02_tube_top_z)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceTube:COPPER_TUBE_NW", "H2A_Tools:CUT_COPPER_TUBE_NW"

    With Brick
        .Reset
        .Name "TOP_SPACER_NW"
        .Component "H2A_ServiceInterface"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "-h2av02_tube_xy-h2av02_spacer_half", "-h2av02_tube_xy+h2av02_spacer_half"
        .Yrange "h2av02_tube_xy-h2av02_spacer_half", "h2av02_tube_xy+h2av02_spacer_half"
        .Zrange "h2av02_tube_top_z", "h2a_backside_cu_bottom"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_TOP_SPACER_NW"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "(h2av02_tube_top_z)-0.05", "(h2a_backside_cu_bottom)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceInterface:TOP_SPACER_NW", "H2A_Tools:CUT_TOP_SPACER_NW"

    With Brick
        .Reset
        .Name "BOTTOM_SPACER_NW"
        .Component "H2A_ServiceInterface"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "-h2av02_tube_xy-h2av02_spacer_half", "-h2av02_tube_xy+h2av02_spacer_half"
        .Yrange "h2av02_tube_xy-h2av02_spacer_half", "h2av02_tube_xy+h2av02_spacer_half"
        .Zrange "0.0", "h2av02_tube_bottom_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_BOTTOM_SPACER_NW"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "(0.0)-0.05", "(h2av02_tube_bottom_z)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceInterface:BOTTOM_SPACER_NW", "H2A_Tools:CUT_BOTTOM_SPACER_NW"

    With Brick
        .Reset
        .Name "MICROCOAX_VERT_NW"
        .Component "H2A_ServiceRouting"
        .Material "H2A_MICROCOAX_ENVELOPE_SURROGATE"
        .Xrange "-h2av02_tube_xy-h2av02_cable_half", "-h2av02_tube_xy+h2av02_cable_half"
        .Yrange "h2av02_tube_xy-h2av02_cable_half", "h2av02_tube_xy+h2av02_cable_half"
        .Zrange "h2av02_mmcx_bottom_z", "h2av02_route_z+h2av02_cable_half"
        .Create
    End With

    With Brick
        .Reset
        .Name "MMCX_ENV_NW"
        .Component "H2A_ServiceConnector"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "-h2av02_tube_xy-h2av02_mmcx_half", "-h2av02_tube_xy+h2av02_mmcx_half"
        .Yrange "h2av02_tube_xy-h2av02_mmcx_half", "h2av02_tube_xy+h2av02_mmcx_half"
        .Zrange "h2av02_mmcx_bottom_z", "h2av02_mmcx_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_BACKPLANE_SW"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "-0.55", "0.05"
        .Create
    End With

    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H2A_Tools:CUT_BACKPLANE_SW"

    With Brick
        .Reset
        .Name "COPPER_TUBE_SW"
        .Component "H2A_ServiceTube"
        .Material "PEC"
        .Xrange "-h2av02_tube_xy-h2av02_tube_outer_half", "-h2av02_tube_xy+h2av02_tube_outer_half"
        .Yrange "-h2av02_tube_xy-h2av02_tube_outer_half", "-h2av02_tube_xy+h2av02_tube_outer_half"
        .Zrange "h2av02_tube_bottom_z", "h2av02_tube_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_COPPER_TUBE_SW"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "-h2av02_tube_xy-h2av02_tube_inner_half", "-h2av02_tube_xy+h2av02_tube_inner_half"
        .Yrange "-h2av02_tube_xy-h2av02_tube_inner_half", "-h2av02_tube_xy+h2av02_tube_inner_half"
        .Zrange "(h2av02_tube_bottom_z)-0.05", "(h2av02_tube_top_z)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceTube:COPPER_TUBE_SW", "H2A_Tools:CUT_COPPER_TUBE_SW"

    With Brick
        .Reset
        .Name "TOP_SPACER_SW"
        .Component "H2A_ServiceInterface"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "-h2av02_tube_xy-h2av02_spacer_half", "-h2av02_tube_xy+h2av02_spacer_half"
        .Yrange "-h2av02_tube_xy-h2av02_spacer_half", "-h2av02_tube_xy+h2av02_spacer_half"
        .Zrange "h2av02_tube_top_z", "h2a_backside_cu_bottom"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_TOP_SPACER_SW"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "(h2av02_tube_top_z)-0.05", "(h2a_backside_cu_bottom)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceInterface:TOP_SPACER_SW", "H2A_Tools:CUT_TOP_SPACER_SW"

    With Brick
        .Reset
        .Name "BOTTOM_SPACER_SW"
        .Component "H2A_ServiceInterface"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "-h2av02_tube_xy-h2av02_spacer_half", "-h2av02_tube_xy+h2av02_spacer_half"
        .Yrange "-h2av02_tube_xy-h2av02_spacer_half", "-h2av02_tube_xy+h2av02_spacer_half"
        .Zrange "0.0", "h2av02_tube_bottom_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_BOTTOM_SPACER_SW"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "(0.0)-0.05", "(h2av02_tube_bottom_z)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceInterface:BOTTOM_SPACER_SW", "H2A_Tools:CUT_BOTTOM_SPACER_SW"

    With Brick
        .Reset
        .Name "MICROCOAX_VERT_SW"
        .Component "H2A_ServiceRouting"
        .Material "H2A_MICROCOAX_ENVELOPE_SURROGATE"
        .Xrange "-h2av02_tube_xy-h2av02_cable_half", "-h2av02_tube_xy+h2av02_cable_half"
        .Yrange "-h2av02_tube_xy-h2av02_cable_half", "-h2av02_tube_xy+h2av02_cable_half"
        .Zrange "h2av02_mmcx_bottom_z", "h2av02_route_z+h2av02_cable_half"
        .Create
    End With

    With Brick
        .Reset
        .Name "MMCX_ENV_SW"
        .Component "H2A_ServiceConnector"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "-h2av02_tube_xy-h2av02_mmcx_half", "-h2av02_tube_xy+h2av02_mmcx_half"
        .Yrange "-h2av02_tube_xy-h2av02_mmcx_half", "-h2av02_tube_xy+h2av02_mmcx_half"
        .Zrange "h2av02_mmcx_bottom_z", "h2av02_mmcx_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_BACKPLANE_SE"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "-0.55", "0.05"
        .Create
    End With

    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H2A_Tools:CUT_BACKPLANE_SE"

    With Brick
        .Reset
        .Name "COPPER_TUBE_SE"
        .Component "H2A_ServiceTube"
        .Material "PEC"
        .Xrange "h2av02_tube_xy-h2av02_tube_outer_half", "h2av02_tube_xy+h2av02_tube_outer_half"
        .Yrange "-h2av02_tube_xy-h2av02_tube_outer_half", "-h2av02_tube_xy+h2av02_tube_outer_half"
        .Zrange "h2av02_tube_bottom_z", "h2av02_tube_top_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_COPPER_TUBE_SE"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "h2av02_tube_xy-h2av02_tube_inner_half", "h2av02_tube_xy+h2av02_tube_inner_half"
        .Yrange "-h2av02_tube_xy-h2av02_tube_inner_half", "-h2av02_tube_xy+h2av02_tube_inner_half"
        .Zrange "(h2av02_tube_bottom_z)-0.05", "(h2av02_tube_top_z)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceTube:COPPER_TUBE_SE", "H2A_Tools:CUT_COPPER_TUBE_SE"

    With Brick
        .Reset
        .Name "TOP_SPACER_SE"
        .Component "H2A_ServiceInterface"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "h2av02_tube_xy-h2av02_spacer_half", "h2av02_tube_xy+h2av02_spacer_half"
        .Yrange "-h2av02_tube_xy-h2av02_spacer_half", "-h2av02_tube_xy+h2av02_spacer_half"
        .Zrange "h2av02_tube_top_z", "h2a_backside_cu_bottom"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_TOP_SPACER_SE"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "(h2av02_tube_top_z)-0.05", "(h2a_backside_cu_bottom)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceInterface:TOP_SPACER_SE", "H2A_Tools:CUT_TOP_SPACER_SE"

    With Brick
        .Reset
        .Name "BOTTOM_SPACER_SE"
        .Component "H2A_ServiceInterface"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "h2av02_tube_xy-h2av02_spacer_half", "h2av02_tube_xy+h2av02_spacer_half"
        .Yrange "-h2av02_tube_xy-h2av02_spacer_half", "-h2av02_tube_xy+h2av02_spacer_half"
        .Zrange "0.0", "h2av02_tube_bottom_z"
        .Create
    End With

    With Brick
        .Reset
        .Name "CUT_BOTTOM_SPACER_SE"
        .Component "H2A_Tools"
        .Material "Vacuum"
        .Xrange "h2av02_tube_xy-h2av02_feedthrough_half", "h2av02_tube_xy+h2av02_feedthrough_half"
        .Yrange "-h2av02_tube_xy-h2av02_feedthrough_half", "-h2av02_tube_xy+h2av02_feedthrough_half"
        .Zrange "(0.0)-0.05", "(h2av02_tube_bottom_z)+0.05"
        .Create
    End With

    Solid.Subtract "H2A_ServiceInterface:BOTTOM_SPACER_SE", "H2A_Tools:CUT_BOTTOM_SPACER_SE"

    With Brick
        .Reset
        .Name "MICROCOAX_VERT_SE"
        .Component "H2A_ServiceRouting"
        .Material "H2A_MICROCOAX_ENVELOPE_SURROGATE"
        .Xrange "h2av02_tube_xy-h2av02_cable_half", "h2av02_tube_xy+h2av02_cable_half"
        .Yrange "-h2av02_tube_xy-h2av02_cable_half", "-h2av02_tube_xy+h2av02_cable_half"
        .Zrange "h2av02_mmcx_bottom_z", "h2av02_route_z+h2av02_cable_half"
        .Create
    End With

    With Brick
        .Reset
        .Name "MMCX_ENV_SE"
        .Component "H2A_ServiceConnector"
        .Material "H2A_PACKAGE_VISUAL_SURROGATE"
        .Xrange "h2av02_tube_xy-h2av02_mmcx_half", "h2av02_tube_xy+h2av02_mmcx_half"
        .Yrange "-h2av02_tube_xy-h2av02_mmcx_half", "-h2av02_tube_xy+h2av02_mmcx_half"
        .Zrange "h2av02_mmcx_bottom_z", "h2av02_mmcx_top_z"
        .Create
    End With


    ' H2A V0.2 intentionally creates no RF port and calls no solver.
End Sub
