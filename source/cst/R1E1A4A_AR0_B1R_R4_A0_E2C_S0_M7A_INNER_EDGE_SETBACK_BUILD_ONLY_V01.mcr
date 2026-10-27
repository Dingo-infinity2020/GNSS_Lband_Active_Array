Option Explicit
' M7 M7A corrective BUILD_ONLY V01
' Parent: frozen full E2C R7 canonical build
' No ports, monitors, solver settings or solver start.

Sub Main()

With Extrude
 .Reset
 .Name "M7A_A_P_CLEARANCE"
 .Component "M7A_ClearanceTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "1.0", "3.0"
 .LineTo "1.5", "3.0"
 .LineTo "1.5", "5.0"
 .LineTo "1.0", "5.0"
 .LineTo "1.0", "3.0"
 .Create
End With
Solid.Subtract "E2C_A_P_BackGround:LOCAL_BACK_GROUND", "M7A_ClearanceTools:M7A_A_P_CLEARANCE"

With Extrude
 .Reset
 .Name "M7A_A_N_CLEARANCE"
 .Component "M7A_ClearanceTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-1.5", "3.0"
 .LineTo "-1.0", "3.0"
 .LineTo "-1.0", "5.0"
 .LineTo "-1.5", "5.0"
 .LineTo "-1.5", "3.0"
 .Create
End With
Solid.Subtract "E2C_A_N_BackGround:LOCAL_BACK_GROUND", "M7A_ClearanceTools:M7A_A_N_CLEARANCE"

With Extrude
 .Reset
 .Name "M7A_B_P_CLEARANCE"
 .Component "M7A_ClearanceTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "1.0", "3.0"
 .LineTo "1.5", "3.0"
 .LineTo "1.5", "5.0"
 .LineTo "1.0", "5.0"
 .LineTo "1.0", "3.0"
 .Create
End With
Solid.Subtract "E2C_B_P_BackGround:LOCAL_BACK_GROUND", "M7A_ClearanceTools:M7A_B_P_CLEARANCE"

With Extrude
 .Reset
 .Name "M7A_B_N_CLEARANCE"
 .Component "M7A_ClearanceTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-1.5", "3.0"
 .LineTo "-1.0", "3.0"
 .LineTo "-1.0", "5.0"
 .LineTo "-1.5", "5.0"
 .LineTo "-1.5", "3.0"
 .Create
End With
Solid.Subtract "E2C_B_N_BackGround:LOCAL_BACK_GROUND", "M7A_ClearanceTools:M7A_B_N_CLEARANCE"

End Sub
