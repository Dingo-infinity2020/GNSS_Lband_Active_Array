Option Explicit
Sub Main()
    StoreParameter "r3d0b_s2", 0.7071067811865476
    StoreParameter "r3d0b_z0", 57.1428571428
    StoreParameter "r3d0b_output_v", 10.0
    StoreParameter "r3d0b_p1_sig_n", 0.035
    StoreParameter "r3d0b_out_sig_n", 0.0
    StoreParameter "r3d0b_out_gnd_n", -1.0
    StoreParameter "r3d0b_up", 3.0
    StoreParameter "r3d0b_un", -3.0

    StoreParameter "r3d0b_p1_x", "r3d0b_s2*(r3d0b_up-r3d0b_p1_sig_n)"
    StoreParameter "r3d0b_p1_y", "r3d0b_s2*(r3d0b_up+r3d0b_p1_sig_n)"
    StoreParameter "r3d0b_p2_x", "r3d0b_s2*(r3d0b_un-r3d0b_p1_sig_n)"
    StoreParameter "r3d0b_p2_y", "r3d0b_s2*(r3d0b_un+r3d0b_p1_sig_n)"

    StoreParameter "r3d0b_outp_sig_x", "r3d0b_s2*(r3d0b_up-r3d0b_out_sig_n)"
    StoreParameter "r3d0b_outp_sig_y", "r3d0b_s2*(r3d0b_up+r3d0b_out_sig_n)"
    StoreParameter "r3d0b_outp_gnd_x", "r3d0b_s2*(r3d0b_up-r3d0b_out_gnd_n)"
    StoreParameter "r3d0b_outp_gnd_y", "r3d0b_s2*(r3d0b_up+r3d0b_out_gnd_n)"

    StoreParameter "r3d0b_outn_sig_x", "r3d0b_s2*(r3d0b_un-r3d0b_out_sig_n)"
    StoreParameter "r3d0b_outn_sig_y", "r3d0b_s2*(r3d0b_un+r3d0b_out_sig_n)"
    StoreParameter "r3d0b_outn_gnd_x", "r3d0b_s2*(r3d0b_un-r3d0b_out_gnd_n)"
    StoreParameter "r3d0b_outn_gnd_y", "r3d0b_s2*(r3d0b_un+r3d0b_out_gnd_n)"
    StoreParameter "r3d0b_output_z", "r3d0b_z0-r3d0b_output_v"

    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "100.0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "r3d0b_p1_x", "r3d0b_p1_y", "r3d0b_z0"
        .SetP2 "False", "r3d0b_p2_x", "r3d0b_p2_y", "r3d0b_z0"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

    With DiscretePort
        .Reset
        .PortNumber "2"
        .Type "SParameter"
        .Impedance "50.0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "r3d0b_outp_sig_x", "r3d0b_outp_sig_y", "r3d0b_output_z"
        .SetP2 "False", "r3d0b_outp_gnd_x", "r3d0b_outp_gnd_y", "r3d0b_output_z"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

    With DiscretePort
        .Reset
        .PortNumber "3"
        .Type "SParameter"
        .Impedance "50.0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "r3d0b_outn_sig_x", "r3d0b_outn_sig_y", "r3d0b_output_z"
        .SetP2 "False", "r3d0b_outn_gnd_x", "r3d0b_outn_gnd_y", "r3d0b_output_z"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With
End Sub
