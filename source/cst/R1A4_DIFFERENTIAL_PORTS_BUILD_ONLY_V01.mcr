Option Explicit

' R1A4 differential port qualification - PORT ONLY
' HARD STOP: no geometry creation, no Boolean, no solver, no monitor.
' This macro is applied only to a hash-verified COPY of the human-reviewed R1A3 CST.

Sub Main()

    StoreParameter "port_ref_impedance", 100.0
    StoreParameter "port_s2", 0.7071067811865476
    StoreParameter "port_terminal_xy", "terminal_r*port_s2"
    StoreParameter "port_terminal_z", "copper_top_z"

    ' Port 1 / Pol-A: NE -> SW
    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "port_ref_impedance"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "port_terminal_xy", "port_terminal_xy", "port_terminal_z"
        .SetP2 "False", "-port_terminal_xy", "-port_terminal_xy", "port_terminal_z"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

    ' Port 2 / Pol-B: exact +90 deg rotation of Port 1, NW -> SE
    With DiscretePort
        .Reset
        .PortNumber "2"
        .Type "SParameter"
        .Impedance "port_ref_impedance"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "-port_terminal_xy", "port_terminal_xy", "port_terminal_z"
        .SetP2 "False", "port_terminal_xy", "-port_terminal_xy", "port_terminal_z"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

End Sub
