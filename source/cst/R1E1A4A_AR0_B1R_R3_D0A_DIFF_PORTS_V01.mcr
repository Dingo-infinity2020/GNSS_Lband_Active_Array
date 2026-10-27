Option Explicit
Sub Main()
    StoreParameter "r3d0a_s2", 0.7071067811865476
    StoreParameter "r3d0a_z0", 57.1428571428
    StoreParameter "r3d0a_out_v", 10.0
    StoreParameter "r3d0a_sig_n", 0.035
    StoreParameter "r3d0a_up", 3.0
    StoreParameter "r3d0a_un", -3.0

    StoreParameter "r3d0a_top_p_x", "r3d0a_s2*(r3d0a_up-r3d0a_sig_n)"
    StoreParameter "r3d0a_top_p_y", "r3d0a_s2*(r3d0a_up+r3d0a_sig_n)"
    StoreParameter "r3d0a_top_n_x", "r3d0a_s2*(r3d0a_un-r3d0a_sig_n)"
    StoreParameter "r3d0a_top_n_y", "r3d0a_s2*(r3d0a_un+r3d0a_sig_n)"
    StoreParameter "r3d0a_out_z", "r3d0a_z0-r3d0a_out_v"

    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "100.0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "r3d0a_top_p_x", "r3d0a_top_p_y", "r3d0a_z0"
        .SetP2 "False", "r3d0a_top_n_x", "r3d0a_top_n_y", "r3d0a_z0"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

    With DiscretePort
        .Reset
        .PortNumber "2"
        .Type "SParameter"
        .Impedance "100.0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "r3d0a_top_p_x", "r3d0a_top_p_y", "r3d0a_out_z"
        .SetP2 "False", "r3d0a_top_n_x", "r3d0a_top_n_y", "r3d0a_out_z"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With
End Sub
