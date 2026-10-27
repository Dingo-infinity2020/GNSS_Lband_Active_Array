Option Explicit
' GNSS_Lband_Active_Array
' R4-A0-E2C 16-via CST/ACIS drill-kernel reference V01
' Disposable complete-project-copy tooling only. No production geometry; no solver.

Sub Main()

' Exact frozen Pol-A eight drill operations.
' CST/ACIS native drill-kernel reference for E2A Pol-A. No production geometry is retained.

With Cylinder
 .Reset
 .Name "PADDLE_M_DRILL"
 .Component "E2C_REF_A_P_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "-2.75"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_A_P_Tools:PADDLE_M_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_P_PRONG", "E2C_REF_A_P_Tools:PADDLE_M_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_C_DRILL"
 .Component "E2C_REF_A_P_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "-3.25"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_A_P_Tools:PADDLE_C_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_P_PRONG", "E2C_REF_A_P_Tools:PADDLE_C_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_P_DRILL"
 .Component "E2C_REF_A_P_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "-3.75"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_A_P_Tools:PADDLE_P_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_P_PRONG", "E2C_REF_A_P_Tools:PADDLE_P_DRILL"

With Cylinder
 .Reset
 .Name "CRF_DRILL"
 .Component "E2C_REF_A_P_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "-4.45"
 .Zcenter "45.9928571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_A_P_Tools:CRF_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_P_PRONG", "E2C_REF_A_P_Tools:CRF_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_M_DRILL"
 .Component "E2C_REF_A_N_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "3.25"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_A_N_Tools:PADDLE_M_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_N_PRONG", "E2C_REF_A_N_Tools:PADDLE_M_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_C_DRILL"
 .Component "E2C_REF_A_N_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "2.75"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_A_N_Tools:PADDLE_C_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_N_PRONG", "E2C_REF_A_N_Tools:PADDLE_C_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_P_DRILL"
 .Component "E2C_REF_A_N_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "2.25"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_A_N_Tools:PADDLE_P_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_N_PRONG", "E2C_REF_A_N_Tools:PADDLE_P_DRILL"

With Cylinder
 .Reset
 .Name "CRF_DRILL"
 .Component "E2C_REF_A_N_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "1.55"
 .Zcenter "45.9928571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_A_N_Tools:CRF_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_N_PRONG", "E2C_REF_A_N_Tools:CRF_DRILL"

' Exact frozen Pol-B eight drill operations.
' CST/ACIS native drill-kernel reference for E2B Pol-B. No production geometry is retained.

With Cylinder
 .Reset
 .Name "PADDLE_M_DRILL"
 .Component "E2C_REF_B_P_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "-2.75"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_B_P_Tools:PADDLE_M_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_P_PRONG", "E2C_REF_B_P_Tools:PADDLE_M_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_C_DRILL"
 .Component "E2C_REF_B_P_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "-3.25"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_B_P_Tools:PADDLE_C_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_P_PRONG", "E2C_REF_B_P_Tools:PADDLE_C_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_P_DRILL"
 .Component "E2C_REF_B_P_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "-3.75"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_B_P_Tools:PADDLE_P_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_P_PRONG", "E2C_REF_B_P_Tools:PADDLE_P_DRILL"

With Cylinder
 .Reset
 .Name "CRF_DRILL"
 .Component "E2C_REF_B_P_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "-4.45"
 .Zcenter "45.9928571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_B_P_Tools:CRF_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_P_PRONG", "E2C_REF_B_P_Tools:CRF_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_M_DRILL"
 .Component "E2C_REF_B_N_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "3.25"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_B_N_Tools:PADDLE_M_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_N_PRONG", "E2C_REF_B_N_Tools:PADDLE_M_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_C_DRILL"
 .Component "E2C_REF_B_N_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "2.75"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_B_N_Tools:PADDLE_C_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_N_PRONG", "E2C_REF_B_N_Tools:PADDLE_C_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_P_DRILL"
 .Component "E2C_REF_B_N_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "2.25"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_B_N_Tools:PADDLE_P_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_N_PRONG", "E2C_REF_B_N_Tools:PADDLE_P_DRILL"

With Cylinder
 .Reset
 .Name "CRF_DRILL"
 .Component "E2C_REF_B_N_Tools"
 .Material "Vacuum"
 .OuterRadius "0.175"
 .InnerRadius "0.0"
 .Axis "x"
 .Xrange "-1.01", "0.01"
 .Ycenter "1.55"
 .Zcenter "45.9928571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2C_REF_B_N_Tools:CRF_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_N_PRONG", "E2C_REF_B_N_Tools:CRF_DRILL"

End Sub
