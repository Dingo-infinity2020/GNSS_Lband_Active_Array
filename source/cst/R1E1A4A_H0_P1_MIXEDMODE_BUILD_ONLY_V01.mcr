Option Explicit

' R1E1A4A H0/P1 mixed-mode reference-plane BUILD ONLY
' Parent: qualified bare P094 source.
' No solver, monitor, support, package, shield, bias, output, or optimization.

Sub Main()

    StoreParameter "r1e1a4a_h0_ground_half", 5.0
    StoreParameter "r1e1a4a_p1_ref_ohm", 50.0
    StoreParameter "r1e1a4a_port_s2", 0.7071067811865476
    StoreParameter "r1e1a4a_port_xy", "terminal_r*r1e1a4a_port_s2"
    StoreParameter "r1e1a4a_port_top_z", "copper_top_z"
    StoreParameter "r1e1a4a_ground_top_z", "height_ground"
    StoreParameter "r1e1a4a_ground_bottom_z", "height_ground-copper_t"

    ' Remove the existing 100-ohm Pol-A differential discrete port.
    Port.Delete (1)

    ' H0 local-ground island on the underside of the radiator substrate.
    With Brick
        .Reset
        .Name "H0_LOCAL_GROUND"
        .Component "ActiveHub"
        .Material "PEC"
        .Xrange "-r1e1a4a_h0_ground_half", "r1e1a4a_h0_ground_half"
        .Yrange "-r1e1a4a_h0_ground_half", "r1e1a4a_h0_ground_half"
        .Zrange "r1e1a4a_ground_bottom_z", "r1e1a4a_ground_top_z"
        .Create
    End With

    ' P1A: NE terminal to H0 local ground.
    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "r1e1a4a_p1_ref_ohm"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "r1e1a4a_port_xy", "r1e1a4a_port_xy", "r1e1a4a_port_top_z"
        .SetP2 "False", "r1e1a4a_port_xy", "r1e1a4a_port_xy", "r1e1a4a_ground_top_z"
        .InvertDirection "False"
        .LocalCoordinates "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

    ' P1B: exact 180-degree partner at the SW terminal.
    With DiscretePort
        .Reset
        .PortNumber "2"
        .Type "SParameter"
        .Impedance "r1e1a4a_p1_ref_ohm"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "-r1e1a4a_port_xy", "-r1e1a4a_port_xy", "r1e1a4a_port_top_z"
        .SetP2 "False", "-r1e1a4a_port_xy", "-r1e1a4a_port_xy", "r1e1a4a_ground_top_z"
        .InvertDirection "False"
        .LocalCoordinates "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

End Sub
