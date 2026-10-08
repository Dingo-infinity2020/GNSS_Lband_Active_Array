Option Explicit
' M7C LOCAL_RETURN_ISLAND_MOAT corrective BUILD_ONLY V01
' Parent: frozen full E2C R7 canonical build.
' Preserve copper directly beneath the CIN/RFIN/local-paddle path.
' Isolate that branch-local return region from the surrounding backside sheet with a 0.25-mm moat.
' No ports, monitors, solver settings or solver start.

Sub Main()

' A_P: inner island u=[2.45,4.05], v=[4.15,7.40]; outer moat envelope u=[2.2,4.3], v=[3.90,7.65]
With Extrude
 .Reset
 .Name "M7C_A_P_MOAT_UP"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "2.2", "3.9"
 .LineTo "4.3", "3.9"
 .LineTo "4.3", "4.15"
 .LineTo "2.2", "4.15"
 .LineTo "2.2", "3.9"
 .Create
End With
Solid.Subtract "E2C_A_P_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_A_P_MOAT_UP"

With Extrude
 .Reset
 .Name "M7C_A_P_MOAT_DN"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "2.2", "7.4"
 .LineTo "4.3", "7.4"
 .LineTo "4.3", "7.65"
 .LineTo "2.2", "7.65"
 .LineTo "2.2", "7.4"
 .Create
End With
Solid.Subtract "E2C_A_P_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_A_P_MOAT_DN"

With Extrude
 .Reset
 .Name "M7C_A_P_MOAT_LOWU"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "2.2", "4.15"
 .LineTo "2.45", "4.15"
 .LineTo "2.45", "7.4"
 .LineTo "2.2", "7.4"
 .LineTo "2.2", "4.15"
 .Create
End With
Solid.Subtract "E2C_A_P_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_A_P_MOAT_LOWU"

With Extrude
 .Reset
 .Name "M7C_A_P_MOAT_HIGHU"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "4.05", "4.15"
 .LineTo "4.3", "4.15"
 .LineTo "4.3", "7.4"
 .LineTo "4.05", "7.4"
 .LineTo "4.05", "4.15"
 .Create
End With
Solid.Subtract "E2C_A_P_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_A_P_MOAT_HIGHU"

' A_N: inner island u=[-4.05,-2.45], v=[4.15,7.40]; outer moat envelope u=[-4.3,-2.2], v=[3.90,7.65]
With Extrude
 .Reset
 .Name "M7C_A_N_MOAT_UP"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-4.3", "3.9"
 .LineTo "-2.2", "3.9"
 .LineTo "-2.2", "4.15"
 .LineTo "-4.3", "4.15"
 .LineTo "-4.3", "3.9"
 .Create
End With
Solid.Subtract "E2C_A_N_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_A_N_MOAT_UP"

With Extrude
 .Reset
 .Name "M7C_A_N_MOAT_DN"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-4.3", "7.4"
 .LineTo "-2.2", "7.4"
 .LineTo "-2.2", "7.65"
 .LineTo "-4.3", "7.65"
 .LineTo "-4.3", "7.4"
 .Create
End With
Solid.Subtract "E2C_A_N_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_A_N_MOAT_DN"

With Extrude
 .Reset
 .Name "M7C_A_N_MOAT_LOWU"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-4.3", "4.15"
 .LineTo "-4.05", "4.15"
 .LineTo "-4.05", "7.4"
 .LineTo "-4.3", "7.4"
 .LineTo "-4.3", "4.15"
 .Create
End With
Solid.Subtract "E2C_A_N_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_A_N_MOAT_LOWU"

With Extrude
 .Reset
 .Name "M7C_A_N_MOAT_HIGHU"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-2.45", "4.15"
 .LineTo "-2.2", "4.15"
 .LineTo "-2.2", "7.4"
 .LineTo "-2.45", "7.4"
 .LineTo "-2.45", "4.15"
 .Create
End With
Solid.Subtract "E2C_A_N_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_A_N_MOAT_HIGHU"

' B_P: inner island u=[2.45,4.05], v=[4.15,7.40]; outer moat envelope u=[2.2,4.3], v=[3.90,7.65]
With Extrude
 .Reset
 .Name "M7C_B_P_MOAT_UP"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "2.2", "3.9"
 .LineTo "4.3", "3.9"
 .LineTo "4.3", "4.15"
 .LineTo "2.2", "4.15"
 .LineTo "2.2", "3.9"
 .Create
End With
Solid.Subtract "E2C_B_P_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_B_P_MOAT_UP"

With Extrude
 .Reset
 .Name "M7C_B_P_MOAT_DN"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "2.2", "7.4"
 .LineTo "4.3", "7.4"
 .LineTo "4.3", "7.65"
 .LineTo "2.2", "7.65"
 .LineTo "2.2", "7.4"
 .Create
End With
Solid.Subtract "E2C_B_P_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_B_P_MOAT_DN"

With Extrude
 .Reset
 .Name "M7C_B_P_MOAT_LOWU"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "2.2", "4.15"
 .LineTo "2.45", "4.15"
 .LineTo "2.45", "7.4"
 .LineTo "2.2", "7.4"
 .LineTo "2.2", "4.15"
 .Create
End With
Solid.Subtract "E2C_B_P_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_B_P_MOAT_LOWU"

With Extrude
 .Reset
 .Name "M7C_B_P_MOAT_HIGHU"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "4.05", "4.15"
 .LineTo "4.3", "4.15"
 .LineTo "4.3", "7.4"
 .LineTo "4.05", "7.4"
 .LineTo "4.05", "4.15"
 .Create
End With
Solid.Subtract "E2C_B_P_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_B_P_MOAT_HIGHU"

' B_N: inner island u=[-4.05,-2.45], v=[4.15,7.40]; outer moat envelope u=[-4.3,-2.2], v=[3.90,7.65]
With Extrude
 .Reset
 .Name "M7C_B_N_MOAT_UP"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-4.3", "3.9"
 .LineTo "-2.2", "3.9"
 .LineTo "-2.2", "4.15"
 .LineTo "-4.3", "4.15"
 .LineTo "-4.3", "3.9"
 .Create
End With
Solid.Subtract "E2C_B_N_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_B_N_MOAT_UP"

With Extrude
 .Reset
 .Name "M7C_B_N_MOAT_DN"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-4.3", "7.4"
 .LineTo "-2.2", "7.4"
 .LineTo "-2.2", "7.65"
 .LineTo "-4.3", "7.65"
 .LineTo "-4.3", "7.4"
 .Create
End With
Solid.Subtract "E2C_B_N_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_B_N_MOAT_DN"

With Extrude
 .Reset
 .Name "M7C_B_N_MOAT_LOWU"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-4.3", "4.15"
 .LineTo "-4.05", "4.15"
 .LineTo "-4.05", "7.4"
 .LineTo "-4.3", "7.4"
 .LineTo "-4.3", "4.15"
 .Create
End With
Solid.Subtract "E2C_B_N_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_B_N_MOAT_LOWU"

With Extrude
 .Reset
 .Name "M7C_B_N_MOAT_HIGHU"
 .Component "M7C_MoatTools"
 .Material "Vacuum"
 .Mode "Pointlist"
 .Height "-0.07"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0", "0", "-1"
 .Point "-2.45", "4.15"
 .LineTo "-2.2", "4.15"
 .LineTo "-2.2", "7.4"
 .LineTo "-2.45", "7.4"
 .LineTo "-2.45", "4.15"
 .Create
End With
Solid.Subtract "E2C_B_N_BackGround:LOCAL_BACK_GROUND", "M7C_MoatTools:M7C_B_N_MOAT_HIGHU"

End Sub
