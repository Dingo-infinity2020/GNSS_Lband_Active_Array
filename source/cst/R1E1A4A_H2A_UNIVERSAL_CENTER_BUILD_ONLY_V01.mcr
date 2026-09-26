Option Explicit

' H2A Universal Passive/Active Center Structure V0.1 — BUILD ONLY
' Parent: immutable R1E1A1 P094 bare radiator.
' Mechanical/manufacturing review model; NO solver, transistor or optimization.

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

    ' Shield can: four walls plus lid, soldered to the backside ground frame.
    With Brick
        .Reset
        .Name "SHIELD_N"
        .Component "H2A_Shield"
        .Material "PEC"
        .Xrange "-h2a_shield_outer_half", "h2a_shield_outer_half"
        .Yrange "h2a_shield_inner_half", "h2a_shield_outer_half"
        .Zrange "h2a_shield_bottom_z", "h2a_shield_top_z"
        .Create
    End With
    With Brick
        .Reset
        .Name "SHIELD_S"
        .Component "H2A_Shield"
        .Material "PEC"
        .Xrange "-h2a_shield_outer_half", "h2a_shield_outer_half"
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
        .Yrange "-h2a_shield_inner_half", "h2a_shield_inner_half"
        .Zrange "h2a_shield_bottom_z", "h2a_shield_top_z"
        .Create
    End With
    With Brick
        .Reset
        .Name "SHIELD_W"
        .Component "H2A_Shield"
        .Material "PEC"
        .Xrange "-h2a_shield_outer_half", "-h2a_shield_inner_half"
        .Yrange "-h2a_shield_inner_half", "h2a_shield_inner_half"
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

    ' Hollow square PEEK carrier, outside the shield volume.
    With Brick
        .Reset
        .Name "CARRIER_N"
        .Component "H2A_Carrier"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "-h2a_carrier_outer_half", "h2a_carrier_outer_half"
        .Yrange "h2a_carrier_inner_half", "h2a_carrier_outer_half"
        .Zrange "h2a_carrier_z_bottom", "h2a_carrier_z_top"
        .Create
    End With

    With Brick
        .Reset
        .Name "CARRIER_S"
        .Component "H2A_Carrier"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "-h2a_carrier_outer_half", "h2a_carrier_outer_half"
        .Yrange "-h2a_carrier_outer_half", "-h2a_carrier_inner_half"
        .Zrange "h2a_carrier_z_bottom", "h2a_carrier_z_top"
        .Create
    End With
    With Brick
        .Reset
        .Name "CARRIER_E"
        .Component "H2A_Carrier"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "h2a_carrier_inner_half", "h2a_carrier_outer_half"
        .Yrange "-h2a_carrier_inner_half", "h2a_carrier_inner_half"
        .Zrange "h2a_carrier_z_bottom", "h2a_carrier_z_top"
        .Create
    End With

    With Brick
        .Reset
        .Name "CARRIER_W"
        .Component "H2A_Carrier"
        .Material "PEEK_VISUAL_SURROGATE"
        .Xrange "-h2a_carrier_outer_half", "-h2a_carrier_inner_half"
        .Yrange "-h2a_carrier_inner_half", "h2a_carrier_inner_half"
        .Zrange "h2a_carrier_z_bottom", "h2a_carrier_z_top"
        .Create
    End With

End Sub
