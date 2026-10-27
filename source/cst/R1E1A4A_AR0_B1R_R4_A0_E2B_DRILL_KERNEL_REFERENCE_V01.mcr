Option Explicit
' R4-A0-E2B CST/ACIS drill-kernel reference V01
' Tooling/recovery source only.
' Parent must be the canonical T1R1 SHA256 fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e.
' Mutates only disposable complete-project copies.
' Creates/consumes exactly 8 Vacuum drill tools and no retained new solids.
' No solver.

Sub Main()

' CST/ACIS native drill-kernel reference for E2B Pol-B. No production geometry is retained.

With Cylinder
 .Reset
 .Name "PADDLE_M_DRILL"
 .Component "E2B_REF_P_Tools"
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
 .Name "E2B_REF_P_Tools:PADDLE_M_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_P_PRONG", "E2B_REF_P_Tools:PADDLE_M_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_C_DRILL"
 .Component "E2B_REF_P_Tools"
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
 .Name "E2B_REF_P_Tools:PADDLE_C_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_P_PRONG", "E2B_REF_P_Tools:PADDLE_C_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_P_DRILL"
 .Component "E2B_REF_P_Tools"
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
 .Name "E2B_REF_P_Tools:PADDLE_P_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_P_PRONG", "E2B_REF_P_Tools:PADDLE_P_DRILL"

With Cylinder
 .Reset
 .Name "CRF_DRILL"
 .Component "E2B_REF_P_Tools"
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
 .Name "E2B_REF_P_Tools:CRF_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_P_PRONG", "E2B_REF_P_Tools:CRF_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_M_DRILL"
 .Component "E2B_REF_N_Tools"
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
 .Name "E2B_REF_N_Tools:PADDLE_M_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_N_PRONG", "E2B_REF_N_Tools:PADDLE_M_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_C_DRILL"
 .Component "E2B_REF_N_Tools"
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
 .Name "E2B_REF_N_Tools:PADDLE_C_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_N_PRONG", "E2B_REF_N_Tools:PADDLE_C_DRILL"

With Cylinder
 .Reset
 .Name "PADDLE_P_DRILL"
 .Component "E2B_REF_N_Tools"
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
 .Name "E2B_REF_N_Tools:PADDLE_P_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_N_PRONG", "E2B_REF_N_Tools:PADDLE_P_DRILL"

With Cylinder
 .Reset
 .Name "CRF_DRILL"
 .Component "E2B_REF_N_Tools"
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
 .Name "E2B_REF_N_Tools:CRF_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "-135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:B_N_PRONG", "E2B_REF_N_Tools:CRF_DRILL"

End Sub
