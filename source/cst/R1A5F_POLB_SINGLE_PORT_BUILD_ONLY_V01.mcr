Option Explicit

' R1A5F Pol-B_NW_TO_SE single differential port - PORT ONLY
' Generated from scripts/generate_r1a5f_single_port_macros.py
' No geometry, material, solver, monitor, or optimization commands.

Sub Main()

    StoreParameter "port_ref_impedance", 100.0
    StoreParameter "port_s2", 0.7071067811865476
    StoreParameter "port_terminal_xy", "terminal_r*port_s2"
    StoreParameter "port_terminal_z", "copper_top_z"
    StoreParameter "r1a5f_rotation_deg", 90
    StoreParameter "r1a5f_p1_x", "-port_terminal_xy"
    StoreParameter "r1a5f_p1_y", "port_terminal_xy"
    StoreParameter "r1a5f_p2_x", "port_terminal_xy"
    StoreParameter "r1a5f_p2_y", "-port_terminal_xy"

    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "port_ref_impedance"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "r1a5f_p1_x", "r1a5f_p1_y", "port_terminal_z"
        .SetP2 "False", "r1a5f_p2_x", "r1a5f_p2_y", "port_terminal_z"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

End Sub
