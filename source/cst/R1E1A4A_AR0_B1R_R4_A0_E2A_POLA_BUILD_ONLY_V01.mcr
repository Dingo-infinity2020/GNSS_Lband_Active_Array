Option Explicit
' GNSS_Lband_Active_Array
' R4-A0-E2A Pol-A integrated antenna + twin E1 landing zones BUILD ONLY V01
'
' Parent authority:
'   R1E1A4A_AR0_B1R_T1R1_GROUND_PLACEMENT_CORRECTED_BUILD_ONLY_V01.cst
'   SHA256 fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e
'
' HARD STOP:
'   persistent History List build only;
'   no solver; no optimizer; no circuit-domain components;
'   exactly 12 raw 50-ohm single-ended ports after fresh reopen.
'
' Coordinate system:
'   Pol-A local u=(+1,+1)/sqrt(2), n=(-1,+1)/sqrt(2)
'   downstream v increases as global z decreases from Z0=57.1428571428 mm.
'   Pol-A branch centers u=+3 and -3 mm.
'
' Via construction:
'   true CST cylinders are created along global x and rotated +135 deg about global z,
'   producing the exact Pol-A local n axis.
'   FR4 drill tool: OD 0.35 mm; plated barrel: OD 0.35 mm / ID 0.25 mm.
'
' E1 donor is dimension-identical to V03 except:
'   no separate FR4 coupon is copied;
'   parent stalk FR4 is the only substrate;
'   existing B0_COPPER is used (same frozen conductivity/thickness baseline).

Sub Main()

' Remove superseded full-length B0/T1R1 active-feed objects.

Solid.Delete "B0_MSL:A_P_MSL"

Solid.Delete "B0_MSL:A_N_MSL"

Solid.Delete "B0_MSL:B_P_MSL"

Solid.Delete "B0_MSL:B_N_MSL"

Solid.Delete "B0_LNAEnvelope:A_P_QPL9547_ENV"

Solid.Delete "B0_LNAEnvelope:A_N_QPL9547_ENV"

Solid.Delete "B0_LNAEnvelope:B_P_QPL9547_ENV"

Solid.Delete "B0_LNAEnvelope:B_N_QPL9547_ENV"

Solid.Delete "B1RT1R1_BackGround:A_P_GROUND_TAPER"

Solid.Delete "B1RT1R1_BackGround:A_N_GROUND_TAPER"

Solid.Delete "B1RT1R1_BackGround:B_P_GROUND_TAPER"

Solid.Delete "B1RT1R1_BackGround:B_N_GROUND_TAPER"

' Rebuild four signal-only upstream stubs through the frozen v=3 mm handoff.

With Extrude
 .Reset
 .Name "A_P_V0_V3_STUB"
 .Component "E2A_ActivePolAStub"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.05", "0"
 .LineTo "3.95", "0"
 .LineTo "3.95", "3"
 .LineTo "2.05", "3"
 .LineTo "2.05", "0"
 .Create
End With

With Extrude
 .Reset
 .Name "A_N_V0_V3_STUB"
 .Component "E2A_ActivePolAStub"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.95", "0"
 .LineTo "-2.05", "0"
 .LineTo "-2.05", "3"
 .LineTo "-3.95", "3"
 .LineTo "-3.95", "0"
 .Create
End With

With Extrude
 .Reset
 .Name "B_P_V0_V3_STUB"
 .Component "E2A_InactivePolBStub"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.05", "0"
 .LineTo "3.95", "0"
 .LineTo "3.95", "3"
 .LineTo "2.05", "3"
 .LineTo "2.05", "0"
 .Create
End With

With Extrude
 .Reset
 .Name "B_N_V0_V3_STUB"
 .Component "E2A_InactivePolBStub"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.95", "0"
 .LineTo "-2.05", "0"
 .LineTo "-2.05", "3"
 .LineTo "-3.95", "3"
 .LineTo "-3.95", "0"
 .Create
End With

' Insert two branch-local E1 landing-zone geometries on Pol-A only.

With Extrude
 .Reset
 .Name "LOCAL_BACK_GROUND"
 .Component "E2A_P_BackGround"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "-0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "1", "3"
 .LineTo "5", "3"
 .LineTo "5", "13"
 .LineTo "1", "13"
 .LineTo "1", "3"
 .Create
End With

With Extrude
 .Reset
 .Name "UPSTREAM_MSL"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.05", "3"
 .LineTo "3.95", "3"
 .LineTo "3.95", "3.4"
 .LineTo "2.05", "3.4"
 .LineTo "2.05", "3"
 .Create
End With

With Extrude
 .Reset
 .Name "UPSTREAM_TAPER"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.05", "3.4"
 .LineTo "3.95", "3.4"
 .LineTo "3.3", "4.4"
 .LineTo "2.7", "4.4"
 .LineTo "2.05", "3.4"
 .Create
End With

With Extrude
 .Reset
 .Name "CIN_UP_PAD"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.7", "4.4"
 .LineTo "3.3", "4.4"
 .LineTo "3.3", "4.9"
 .LineTo "2.7", "4.9"
 .LineTo "2.7", "4.4"
 .Create
End With

With Extrude
 .Reset
 .Name "CIN_DN_PAD"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.7", "5.3"
 .LineTo "3.3", "5.3"
 .LineTo "3.3", "5.8"
 .LineTo "2.7", "5.8"
 .LineTo "2.7", "5.3"
 .Create
End With

With Extrude
 .Reset
 .Name "CIN_TO_RFIN_TAPER"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.7", "5.8"
 .LineTo "3.3", "5.8"
 .LineTo "3.125", "5.87"
 .LineTo "2.875", "5.87"
 .LineTo "2.7", "5.8"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN1_VBIAS"
 .Component "E2A_P_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.375", "5.87"
 .LineTo "2.625", "5.87"
 .LineTo "2.625", "6.3"
 .LineTo "2.375", "6.3"
 .LineTo "2.375", "5.87"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN2_RFIN"
 .Component "E2A_P_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.875", "5.87"
 .LineTo "3.125", "5.87"
 .LineTo "3.125", "6.3"
 .LineTo "2.875", "6.3"
 .LineTo "2.875", "5.87"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN3_GND"
 .Component "E2A_P_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "3.375", "5.87"
 .LineTo "3.625", "5.87"
 .LineTo "3.625", "6.3"
 .LineTo "3.375", "6.3"
 .LineTo "3.375", "5.87"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN4_GND"
 .Component "E2A_P_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "3.875", "5.87"
 .LineTo "4.125", "5.87"
 .LineTo "4.125", "6.3"
 .LineTo "3.875", "6.3"
 .LineTo "3.875", "5.87"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN8_GND"
 .Component "E2A_P_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.375", "7.7"
 .LineTo "2.625", "7.7"
 .LineTo "2.625", "8.13"
 .LineTo "2.375", "8.13"
 .LineTo "2.375", "7.7"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN7_RFOUT_VDD"
 .Component "E2A_P_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.875", "7.7"
 .LineTo "3.125", "7.7"
 .LineTo "3.125", "8.13"
 .LineTo "2.875", "8.13"
 .LineTo "2.875", "7.7"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN6_GND_FDD"
 .Component "E2A_P_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "3.375", "7.7"
 .LineTo "3.625", "7.7"
 .LineTo "3.625", "8.13"
 .LineTo "3.375", "8.13"
 .LineTo "3.375", "7.7"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN5_GND"
 .Component "E2A_P_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "3.875", "7.7"
 .LineTo "4.125", "7.7"
 .LineTo "4.125", "8.13"
 .LineTo "3.875", "8.13"
 .LineTo "3.875", "7.7"
 .Create
End With

With Extrude
 .Reset
 .Name "EXPOSED_PADDLE"
 .Component "E2A_P_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.45", "6.6"
 .LineTo "4.05", "6.6"
 .LineTo "4.05", "7.4"
 .LineTo "2.45", "7.4"
 .LineTo "2.45", "6.6"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN3_SPOKE"
 .Component "E2A_P_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "3.4", "6.3"
 .LineTo "3.6", "6.3"
 .LineTo "3.6", "6.6"
 .LineTo "3.4", "6.6"
 .LineTo "3.4", "6.3"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN4_SPOKE"
 .Component "E2A_P_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "3.9", "6.3"
 .LineTo "4.1", "6.3"
 .LineTo "4.1", "6.6"
 .LineTo "3.9", "6.6"
 .LineTo "3.9", "6.3"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN8_SPOKE"
 .Component "E2A_P_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.4", "7.4"
 .LineTo "2.6", "7.4"
 .LineTo "2.6", "7.7"
 .LineTo "2.4", "7.7"
 .LineTo "2.4", "7.4"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN6_SPOKE"
 .Component "E2A_P_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "3.4", "7.4"
 .LineTo "3.6", "7.4"
 .LineTo "3.6", "7.7"
 .LineTo "3.4", "7.7"
 .LineTo "3.4", "7.4"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN5_SPOKE"
 .Component "E2A_P_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "3.9", "7.4"
 .LineTo "4.1", "7.4"
 .LineTo "4.1", "7.7"
 .LineTo "3.9", "7.7"
 .LineTo "3.9", "7.4"
 .Create
End With

With Cylinder
 .Reset
 .Name "PADDLE_VIA_M_DRILL"
 .Component "E2A_P_ViaHoleTools"
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
 .Name "E2A_P_ViaHoleTools:PADDLE_VIA_M_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_P_PRONG", "E2A_P_ViaHoleTools:PADDLE_VIA_M_DRILL"
With Cylinder
 .Reset
 .Name "PADDLE_VIA_M"
 .Component "E2A_P_Vias"
 .Material "B0_COPPER"
 .OuterRadius "0.175"
 .InnerRadius "0.125"
 .Axis "x"
 .Xrange "-1.035", "0.035"
 .Ycenter "-2.75"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2A_P_Vias:PADDLE_VIA_M"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With

With Cylinder
 .Reset
 .Name "PADDLE_VIA_C_DRILL"
 .Component "E2A_P_ViaHoleTools"
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
 .Name "E2A_P_ViaHoleTools:PADDLE_VIA_C_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_P_PRONG", "E2A_P_ViaHoleTools:PADDLE_VIA_C_DRILL"
With Cylinder
 .Reset
 .Name "PADDLE_VIA_C"
 .Component "E2A_P_Vias"
 .Material "B0_COPPER"
 .OuterRadius "0.175"
 .InnerRadius "0.125"
 .Axis "x"
 .Xrange "-1.035", "0.035"
 .Ycenter "-3.25"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2A_P_Vias:PADDLE_VIA_C"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With

With Cylinder
 .Reset
 .Name "PADDLE_VIA_P_DRILL"
 .Component "E2A_P_ViaHoleTools"
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
 .Name "E2A_P_ViaHoleTools:PADDLE_VIA_P_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_P_PRONG", "E2A_P_ViaHoleTools:PADDLE_VIA_P_DRILL"
With Cylinder
 .Reset
 .Name "PADDLE_VIA_P"
 .Component "E2A_P_Vias"
 .Material "B0_COPPER"
 .OuterRadius "0.175"
 .InnerRadius "0.125"
 .Axis "x"
 .Xrange "-1.035", "0.035"
 .Ycenter "-3.75"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2A_P_Vias:PADDLE_VIA_P"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With

With Extrude
 .Reset
 .Name "RFOUT_TO_COUT_TAPER"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.875", "8.13"
 .LineTo "3.125", "8.13"
 .LineTo "3.3", "8.2"
 .LineTo "2.7", "8.2"
 .LineTo "2.875", "8.13"
 .Create
End With

With Extrude
 .Reset
 .Name "COUT_DEV_PAD"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.7", "8.2"
 .LineTo "3.3", "8.2"
 .LineTo "3.3", "8.7"
 .LineTo "2.7", "8.7"
 .LineTo "2.7", "8.2"
 .Create
End With

With Extrude
 .Reset
 .Name "COUT_DN_PAD"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.7", "9.1"
 .LineTo "3.3", "9.1"
 .LineTo "3.3", "9.6"
 .LineTo "2.7", "9.6"
 .LineTo "2.7", "9.1"
 .Create
End With

With Extrude
 .Reset
 .Name "L1_RF_PAD"
 .Component "E2A_P_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "4.15", "8.2"
 .LineTo "4.75", "8.2"
 .LineTo "4.75", "8.7"
 .LineTo "4.15", "8.7"
 .LineTo "4.15", "8.2"
 .Create
End With

With Extrude
 .Reset
 .Name "L1_VDD_PAD"
 .Component "E2A_P_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "4.15", "9.1"
 .LineTo "4.75", "9.1"
 .LineTo "4.75", "9.6"
 .LineTo "4.15", "9.6"
 .LineTo "4.15", "9.1"
 .Create
End With

With Extrude
 .Reset
 .Name "POUT_TO_L1_FAN"
 .Component "E2A_P_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "3.3", "8.3"
 .LineTo "4.15", "8.3"
 .LineTo "4.15", "8.6"
 .LineTo "3.3", "8.6"
 .LineTo "3.3", "8.3"
 .Create
End With

With Extrude
 .Reset
 .Name "VDD_TRACE"
 .Component "E2A_P_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "4.15", "9.6"
 .LineTo "4.75", "9.6"
 .LineTo "4.75", "10"
 .LineTo "4.15", "10"
 .LineTo "4.15", "9.6"
 .Create
End With

With Extrude
 .Reset
 .Name "CRF_VDD_PAD"
 .Component "E2A_P_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "4.15", "10"
 .LineTo "4.75", "10"
 .LineTo "4.75", "10.5"
 .LineTo "4.15", "10.5"
 .LineTo "4.15", "10"
 .Create
End With

With Extrude
 .Reset
 .Name "CRF_GND_PAD"
 .Component "E2A_P_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "4.15", "10.9"
 .LineTo "4.75", "10.9"
 .LineTo "4.75", "11.4"
 .LineTo "4.15", "11.4"
 .LineTo "4.15", "10.9"
 .Create
End With

With Cylinder
 .Reset
 .Name "CRF_GROUND_VIA_DRILL"
 .Component "E2A_P_ViaHoleTools"
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
 .Name "E2A_P_ViaHoleTools:CRF_GROUND_VIA_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_P_PRONG", "E2A_P_ViaHoleTools:CRF_GROUND_VIA_DRILL"
With Cylinder
 .Reset
 .Name "CRF_GROUND_VIA"
 .Component "E2A_P_Vias"
 .Material "B0_COPPER"
 .OuterRadius "0.175"
 .InnerRadius "0.125"
 .Axis "x"
 .Xrange "-1.035", "0.035"
 .Ycenter "-4.45"
 .Zcenter "45.9928571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2A_P_Vias:CRF_GROUND_VIA"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With

With Extrude
 .Reset
 .Name "DOWNSTREAM_TAPER"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.7", "9.6"
 .LineTo "3.3", "9.6"
 .LineTo "3.95", "10.6"
 .LineTo "2.05", "10.6"
 .LineTo "2.7", "9.6"
 .Create
End With

With Extrude
 .Reset
 .Name "DOWNSTREAM_MSL"
 .Component "E2A_P_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "2.05", "10.6"
 .LineTo "3.95", "10.6"
 .LineTo "3.95", "13"
 .LineTo "2.05", "13"
 .LineTo "2.05", "10.6"
 .Create
End With

With Extrude
 .Reset
 .Name "LOCAL_BACK_GROUND"
 .Component "E2A_N_BackGround"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "-0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0.707106781186547", "-0.707106781186547", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-5", "3"
 .LineTo "-1", "3"
 .LineTo "-1", "13"
 .LineTo "-5", "13"
 .LineTo "-5", "3"
 .Create
End With

With Extrude
 .Reset
 .Name "UPSTREAM_MSL"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.95", "3"
 .LineTo "-2.05", "3"
 .LineTo "-2.05", "3.4"
 .LineTo "-3.95", "3.4"
 .LineTo "-3.95", "3"
 .Create
End With

With Extrude
 .Reset
 .Name "UPSTREAM_TAPER"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.95", "3.4"
 .LineTo "-2.05", "3.4"
 .LineTo "-2.7", "4.4"
 .LineTo "-3.3", "4.4"
 .LineTo "-3.95", "3.4"
 .Create
End With

With Extrude
 .Reset
 .Name "CIN_UP_PAD"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.3", "4.4"
 .LineTo "-2.7", "4.4"
 .LineTo "-2.7", "4.9"
 .LineTo "-3.3", "4.9"
 .LineTo "-3.3", "4.4"
 .Create
End With

With Extrude
 .Reset
 .Name "CIN_DN_PAD"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.3", "5.3"
 .LineTo "-2.7", "5.3"
 .LineTo "-2.7", "5.8"
 .LineTo "-3.3", "5.8"
 .LineTo "-3.3", "5.3"
 .Create
End With

With Extrude
 .Reset
 .Name "CIN_TO_RFIN_TAPER"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.3", "5.8"
 .LineTo "-2.7", "5.8"
 .LineTo "-2.875", "5.87"
 .LineTo "-3.125", "5.87"
 .LineTo "-3.3", "5.8"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN1_VBIAS"
 .Component "E2A_N_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.625", "5.87"
 .LineTo "-3.375", "5.87"
 .LineTo "-3.375", "6.3"
 .LineTo "-3.625", "6.3"
 .LineTo "-3.625", "5.87"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN2_RFIN"
 .Component "E2A_N_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.125", "5.87"
 .LineTo "-2.875", "5.87"
 .LineTo "-2.875", "6.3"
 .LineTo "-3.125", "6.3"
 .LineTo "-3.125", "5.87"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN3_GND"
 .Component "E2A_N_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-2.625", "5.87"
 .LineTo "-2.375", "5.87"
 .LineTo "-2.375", "6.3"
 .LineTo "-2.625", "6.3"
 .LineTo "-2.625", "5.87"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN4_GND"
 .Component "E2A_N_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-2.125", "5.87"
 .LineTo "-1.875", "5.87"
 .LineTo "-1.875", "6.3"
 .LineTo "-2.125", "6.3"
 .LineTo "-2.125", "5.87"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN8_GND"
 .Component "E2A_N_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.625", "7.7"
 .LineTo "-3.375", "7.7"
 .LineTo "-3.375", "8.13"
 .LineTo "-3.625", "8.13"
 .LineTo "-3.625", "7.7"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN7_RFOUT_VDD"
 .Component "E2A_N_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.125", "7.7"
 .LineTo "-2.875", "7.7"
 .LineTo "-2.875", "8.13"
 .LineTo "-3.125", "8.13"
 .LineTo "-3.125", "7.7"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN6_GND_FDD"
 .Component "E2A_N_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-2.625", "7.7"
 .LineTo "-2.375", "7.7"
 .LineTo "-2.375", "8.13"
 .LineTo "-2.625", "8.13"
 .LineTo "-2.625", "7.7"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN5_GND"
 .Component "E2A_N_PackageLands"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-2.125", "7.7"
 .LineTo "-1.875", "7.7"
 .LineTo "-1.875", "8.13"
 .LineTo "-2.125", "8.13"
 .LineTo "-2.125", "7.7"
 .Create
End With

With Extrude
 .Reset
 .Name "EXPOSED_PADDLE"
 .Component "E2A_N_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.55", "6.6"
 .LineTo "-1.95", "6.6"
 .LineTo "-1.95", "7.4"
 .LineTo "-3.55", "7.4"
 .LineTo "-3.55", "6.6"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN3_SPOKE"
 .Component "E2A_N_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-2.6", "6.3"
 .LineTo "-2.4", "6.3"
 .LineTo "-2.4", "6.6"
 .LineTo "-2.6", "6.6"
 .LineTo "-2.6", "6.3"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN4_SPOKE"
 .Component "E2A_N_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-2.1", "6.3"
 .LineTo "-1.9", "6.3"
 .LineTo "-1.9", "6.6"
 .LineTo "-2.1", "6.6"
 .LineTo "-2.1", "6.3"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN8_SPOKE"
 .Component "E2A_N_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.6", "7.4"
 .LineTo "-3.4", "7.4"
 .LineTo "-3.4", "7.7"
 .LineTo "-3.6", "7.7"
 .LineTo "-3.6", "7.4"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN6_SPOKE"
 .Component "E2A_N_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-2.6", "7.4"
 .LineTo "-2.4", "7.4"
 .LineTo "-2.4", "7.7"
 .LineTo "-2.6", "7.7"
 .LineTo "-2.6", "7.4"
 .Create
End With

With Extrude
 .Reset
 .Name "PIN5_SPOKE"
 .Component "E2A_N_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-2.1", "7.4"
 .LineTo "-1.9", "7.4"
 .LineTo "-1.9", "7.7"
 .LineTo "-2.1", "7.7"
 .LineTo "-2.1", "7.4"
 .Create
End With

With Cylinder
 .Reset
 .Name "PADDLE_VIA_M_DRILL"
 .Component "E2A_N_ViaHoleTools"
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
 .Name "E2A_N_ViaHoleTools:PADDLE_VIA_M_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_N_PRONG", "E2A_N_ViaHoleTools:PADDLE_VIA_M_DRILL"
With Cylinder
 .Reset
 .Name "PADDLE_VIA_M"
 .Component "E2A_N_Vias"
 .Material "B0_COPPER"
 .OuterRadius "0.175"
 .InnerRadius "0.125"
 .Axis "x"
 .Xrange "-1.035", "0.035"
 .Ycenter "3.25"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2A_N_Vias:PADDLE_VIA_M"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With

With Cylinder
 .Reset
 .Name "PADDLE_VIA_C_DRILL"
 .Component "E2A_N_ViaHoleTools"
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
 .Name "E2A_N_ViaHoleTools:PADDLE_VIA_C_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_N_PRONG", "E2A_N_ViaHoleTools:PADDLE_VIA_C_DRILL"
With Cylinder
 .Reset
 .Name "PADDLE_VIA_C"
 .Component "E2A_N_Vias"
 .Material "B0_COPPER"
 .OuterRadius "0.175"
 .InnerRadius "0.125"
 .Axis "x"
 .Xrange "-1.035", "0.035"
 .Ycenter "2.75"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2A_N_Vias:PADDLE_VIA_C"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With

With Cylinder
 .Reset
 .Name "PADDLE_VIA_P_DRILL"
 .Component "E2A_N_ViaHoleTools"
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
 .Name "E2A_N_ViaHoleTools:PADDLE_VIA_P_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_N_PRONG", "E2A_N_ViaHoleTools:PADDLE_VIA_P_DRILL"
With Cylinder
 .Reset
 .Name "PADDLE_VIA_P"
 .Component "E2A_N_Vias"
 .Material "B0_COPPER"
 .OuterRadius "0.175"
 .InnerRadius "0.125"
 .Axis "x"
 .Xrange "-1.035", "0.035"
 .Ycenter "2.25"
 .Zcenter "50.1428571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2A_N_Vias:PADDLE_VIA_P"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With

With Extrude
 .Reset
 .Name "RFOUT_TO_COUT_TAPER"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.125", "8.13"
 .LineTo "-2.875", "8.13"
 .LineTo "-2.7", "8.2"
 .LineTo "-3.3", "8.2"
 .LineTo "-3.125", "8.13"
 .Create
End With

With Extrude
 .Reset
 .Name "COUT_DEV_PAD"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.3", "8.2"
 .LineTo "-2.7", "8.2"
 .LineTo "-2.7", "8.7"
 .LineTo "-3.3", "8.7"
 .LineTo "-3.3", "8.2"
 .Create
End With

With Extrude
 .Reset
 .Name "COUT_DN_PAD"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.3", "9.1"
 .LineTo "-2.7", "9.1"
 .LineTo "-2.7", "9.6"
 .LineTo "-3.3", "9.6"
 .LineTo "-3.3", "9.1"
 .Create
End With

With Extrude
 .Reset
 .Name "L1_RF_PAD"
 .Component "E2A_N_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-1.85", "8.2"
 .LineTo "-1.25", "8.2"
 .LineTo "-1.25", "8.7"
 .LineTo "-1.85", "8.7"
 .LineTo "-1.85", "8.2"
 .Create
End With

With Extrude
 .Reset
 .Name "L1_VDD_PAD"
 .Component "E2A_N_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-1.85", "9.1"
 .LineTo "-1.25", "9.1"
 .LineTo "-1.25", "9.6"
 .LineTo "-1.85", "9.6"
 .LineTo "-1.85", "9.1"
 .Create
End With

With Extrude
 .Reset
 .Name "POUT_TO_L1_FAN"
 .Component "E2A_N_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-2.7", "8.3"
 .LineTo "-1.85", "8.3"
 .LineTo "-1.85", "8.6"
 .LineTo "-2.7", "8.6"
 .LineTo "-2.7", "8.3"
 .Create
End With

With Extrude
 .Reset
 .Name "VDD_TRACE"
 .Component "E2A_N_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-1.85", "9.6"
 .LineTo "-1.25", "9.6"
 .LineTo "-1.25", "10"
 .LineTo "-1.85", "10"
 .LineTo "-1.85", "9.6"
 .Create
End With

With Extrude
 .Reset
 .Name "CRF_VDD_PAD"
 .Component "E2A_N_Bias"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-1.85", "10"
 .LineTo "-1.25", "10"
 .LineTo "-1.25", "10.5"
 .LineTo "-1.85", "10.5"
 .LineTo "-1.85", "10"
 .Create
End With

With Extrude
 .Reset
 .Name "CRF_GND_PAD"
 .Component "E2A_N_LocalGroundTop"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-1.85", "10.9"
 .LineTo "-1.25", "10.9"
 .LineTo "-1.25", "11.4"
 .LineTo "-1.85", "11.4"
 .LineTo "-1.85", "10.9"
 .Create
End With

With Cylinder
 .Reset
 .Name "CRF_GROUND_VIA_DRILL"
 .Component "E2A_N_ViaHoleTools"
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
 .Name "E2A_N_ViaHoleTools:CRF_GROUND_VIA_DRILL"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With
Solid.Subtract "B0_Stalk:A_N_PRONG", "E2A_N_ViaHoleTools:CRF_GROUND_VIA_DRILL"
With Cylinder
 .Reset
 .Name "CRF_GROUND_VIA"
 .Component "E2A_N_Vias"
 .Material "B0_COPPER"
 .OuterRadius "0.175"
 .InnerRadius "0.125"
 .Axis "x"
 .Xrange "-1.035", "0.035"
 .Ycenter "1.55"
 .Zcenter "45.9928571428"
 .Segments "0"
 .Create
End With
With Transform
 .Reset
 .Name "E2A_N_Vias:CRF_GROUND_VIA"
 .Origin "Free"
 .Center "0", "0", "0"
 .Angle "0", "0", "135"
 .MultipleObjects "False"
 .GroupObjects "False"
 .Repetitions "1"
 .MultipleSelection "False"
 .Transform "Shape", "Rotate"
End With

With Extrude
 .Reset
 .Name "DOWNSTREAM_TAPER"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.3", "9.6"
 .LineTo "-2.7", "9.6"
 .LineTo "-2.05", "10.6"
 .LineTo "-3.95", "10.6"
 .LineTo "-3.3", "9.6"
 .Create
End With

With Extrude
 .Reset
 .Name "DOWNSTREAM_MSL"
 .Component "E2A_N_Signal"
 .Material "B0_COPPER"
 .Mode "Pointlist"
 .Height "0.035"
 .Twist "0.0"
 .Taper "0.0"
 .Origin "0", "0", "57.1428571428"
 .Uvector "0.707106781186547", "0.707106781186547", "0.0"
 .Vvector "0.0", "0.0", "-1.0"
 .Point "-3.95", "10.6"
 .LineTo "-2.05", "10.6"
 .LineTo "-2.05", "13"
 .LineTo "-3.95", "13"
 .LineTo "-3.95", "10.6"
 .Create
End With

' Twelve raw single-ended ports; four QPL9547 device planes are ports 2/3/8/9.

With DiscretePort
 .Reset
 .PortNumber "1"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "2.12132034355964", "2.12132034355964", "52.4928571428"
 .SetP2 "False", "2.82842712474619", "1.41421356237309", "52.4928571428"
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
 .SetP1 "False", "2.12132034355964", "2.12132034355964", "51.0578571428"
 .SetP2 "False", "2.82842712474619", "1.41421356237309", "51.0578571428"
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
 .SetP1 "False", "2.12132034355964", "2.12132034355964", "49.2278571428"
 .SetP2 "False", "2.82842712474619", "1.41421356237309", "49.2278571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

With DiscretePort
 .Reset
 .PortNumber "4"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "2.12132034355964", "2.12132034355964", "47.7928571428"
 .SetP2 "False", "2.82842712474619", "1.41421356237309", "47.7928571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

With DiscretePort
 .Reset
 .PortNumber "5"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "3.14662517628014", "3.14662517628014", "47.3428571428"
 .SetP2 "False", "3.85373195746668", "2.43951839509359", "47.3428571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

With DiscretePort
 .Reset
 .PortNumber "6"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "1.76776695296637", "1.76776695296637", "51.0578571428"
 .SetP2 "False", "2.47487373415292", "1.06066017177982", "51.0578571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

With DiscretePort
 .Reset
 .PortNumber "7"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "-2.12132034355964", "-2.12132034355964", "52.4928571428"
 .SetP2 "False", "-1.41421356237309", "-2.82842712474619", "52.4928571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

With DiscretePort
 .Reset
 .PortNumber "8"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "-2.12132034355964", "-2.12132034355964", "51.0578571428"
 .SetP2 "False", "-1.41421356237309", "-2.82842712474619", "51.0578571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

With DiscretePort
 .Reset
 .PortNumber "9"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "-2.12132034355964", "-2.12132034355964", "49.2278571428"
 .SetP2 "False", "-1.41421356237309", "-2.82842712474619", "49.2278571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

With DiscretePort
 .Reset
 .PortNumber "10"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "-2.12132034355964", "-2.12132034355964", "47.7928571428"
 .SetP2 "False", "-1.41421356237309", "-2.82842712474619", "47.7928571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

With DiscretePort
 .Reset
 .PortNumber "11"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "-1.09601551083915", "-1.09601551083915", "47.3428571428"
 .SetP2 "False", "-0.388908729652601", "-1.8031222920257", "47.3428571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

With DiscretePort
 .Reset
 .PortNumber "12"
 .Type "SParameter"
 .Impedance "50.0"
 .Voltage "1.0"
 .Current "1.0"
 .SetP1 "False", "-2.47487373415292", "-2.47487373415292", "51.0578571428"
 .SetP2 "False", "-1.76776695296637", "-3.18198051533946", "51.0578571428"
 .InvertDirection "False"
 .Monitor "False"
 .Radius "0.0"
 .Create
End With

End Sub
