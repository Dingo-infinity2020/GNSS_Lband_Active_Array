Option Explicit

' R1E1A4A-H1A OFFSET_GROUND_G2P0 BUILD ONLY
' Parent: qualified bare P094 source.
' Diagnostic only: same 10x10-mm ground footprint, 2.0-mm air offset.

Sub Main()

    StoreParameter "r1e1a4a_h1a_ground_half", 5.0
    StoreParameter "r1e1a4a_h1a_air_gap", 2.0
    StoreParameter "r1e1a4a_h1a_p1_ref_ohm", 50.0
    StoreParameter "r1e1a4a_h1a_port_s2", 0.7071067811865476
    StoreParameter "r1e1a4a_h1a_port_xy", "terminal_r*r1e1a4a_h1a_port_s2"
    StoreParameter "r1e1a4a_h1a_port_top_z", "copper_top_z"
    StoreParameter "r1e1a4a_h1a_ground_top_z", "height_ground-r1e1a4a_h1a_air_gap"
    StoreParameter "r1e1a4a_h1a_ground_bottom_z", "height_ground-r1e1a4a_h1a_air_gap-copper_t"

    Port.Delete (1)

    With Brick
        .Reset
        .Name "H1A_OFFSET_LOCAL_GROUND"
        .Component "ActiveHub"
        .Material "PEC"
        .Xrange "-r1e1a4a_h1a_ground_half", "r1e1a4a_h1a_ground_half"
        .Yrange "-r1e1a4a_h1a_ground_half", "r1e1a4a_h1a_ground_half"
        .Zrange "r1e1a4a_h1a_ground_bottom_z", "r1e1a4a_h1a_ground_top_z"
        .Create
    End With

    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "r1e1a4a_h1a_p1_ref_ohm"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "r1e1a4a_h1a_port_xy", "r1e1a4a_h1a_port_xy", "r1e1a4a_h1a_port_top_z"
        .SetP2 "False", "r1e1a4a_h1a_port_xy", "r1e1a4a_h1a_port_xy", "r1e1a4a_h1a_ground_top_z"
        .InvertDirection "False"
        .LocalCoordinates "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

    With DiscretePort
        .Reset
        .PortNumber "2"
        .Type "SParameter"
        .Impedance "r1e1a4a_h1a_p1_ref_ohm"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "-r1e1a4a_h1a_port_xy", "-r1e1a4a_h1a_port_xy", "r1e1a4a_h1a_port_top_z"
        .SetP2 "False", "-r1e1a4a_h1a_port_xy", "-r1e1a4a_h1a_port_xy", "r1e1a4a_h1a_ground_top_z"
        .InvertDirection "False"
        .LocalCoordinates "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

End Sub
