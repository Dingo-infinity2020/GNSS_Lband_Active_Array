Option Explicit
Sub Main()
    StoreParameter "h3b_o1_port_z0", 50.0
    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "h3b_o1_port_z0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "0.0", "12.0", "-0.035"
        .SetP2 "False", "0.0", "12.0", "1.035"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With
    With DiscretePort
        .Reset
        .PortNumber "2"
        .Type "SParameter"
        .Impedance "h3b_o1_port_z0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "0.0", "-12.0", "-0.035"
        .SetP2 "False", "0.0", "-12.0", "1.035"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With
End Sub
