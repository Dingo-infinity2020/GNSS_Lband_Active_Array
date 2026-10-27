Option Explicit
Sub Main()
    StoreParameter "t2f_s2", 0.7071067811865476
    StoreParameter "t2f_z0", 57.1428571428
    StoreParameter "t2f_output_v", 10.0
    StoreParameter "t2f_sig_n", 0.035
    StoreParameter "t2f_gnd_n", -1.035
    StoreParameter "t2f_up", 3.0
    StoreParameter "t2f_un", -3.0

    StoreParameter "t2f_p1_x", "t2f_s2*(t2f_up-t2f_sig_n)"
    StoreParameter "t2f_p1_y", "t2f_s2*(t2f_up+t2f_sig_n)"
    StoreParameter "t2f_p2_x", "t2f_s2*(t2f_un-t2f_sig_n)"
    StoreParameter "t2f_p2_y", "t2f_s2*(t2f_un+t2f_sig_n)"

    StoreParameter "t2f_outp_sig_x", "t2f_s2*(t2f_up-t2f_sig_n)"
    StoreParameter "t2f_outp_sig_y", "t2f_s2*(t2f_up+t2f_sig_n)"
    StoreParameter "t2f_outp_gnd_x", "t2f_s2*(t2f_up-t2f_gnd_n)"
    StoreParameter "t2f_outp_gnd_y", "t2f_s2*(t2f_up+t2f_gnd_n)"

    StoreParameter "t2f_outn_sig_x", "t2f_s2*(t2f_un-t2f_sig_n)"
    StoreParameter "t2f_outn_sig_y", "t2f_s2*(t2f_un+t2f_sig_n)"
    StoreParameter "t2f_outn_gnd_x", "t2f_s2*(t2f_un-t2f_gnd_n)"
    StoreParameter "t2f_outn_gnd_y", "t2f_s2*(t2f_un+t2f_gnd_n)"

    StoreParameter "t2f_output_z", "t2f_z0-t2f_output_v"

    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "100.0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "t2f_p1_x", "t2f_p1_y", "t2f_z0"
        .SetP2 "False", "t2f_p2_x", "t2f_p2_y", "t2f_z0"
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
        .SetP1 "False", "t2f_outp_sig_x", "t2f_outp_sig_y", "t2f_output_z"
        .SetP2 "False", "t2f_outp_gnd_x", "t2f_outp_gnd_y", "t2f_output_z"
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
        .SetP1 "False", "t2f_outn_sig_x", "t2f_outn_sig_y", "t2f_output_z"
        .SetP2 "False", "t2f_outn_gnd_x", "t2f_outn_gnd_y", "t2f_output_z"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With
End Sub
