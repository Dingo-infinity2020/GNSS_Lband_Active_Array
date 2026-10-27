Option Explicit
' GNSS_Lband_Active_Array
' R4-A0-E2C-S0-M6-D2 attribution BUILD ONLY V01
'
' Parent: canonical E2A Pol-A BUILD_ONLY baseline
' Parent SHA256: 78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804
' Diagnostic only; no ports, monitors, solver configuration, or solver invocation added.

Sub Main()

  With Extrude
   .Reset
   .Name "LOCAL_BACK_GROUND"
   .Component "E2C_B_P_BackGround"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "-0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Name "PIN3_GND"
   .Component "E2C_B_P_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Name "PIN6_GND_FDD"
   .Component "E2C_B_P_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_ViaHoleTools"
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
   .Name "E2C_B_P_ViaHoleTools:PADDLE_VIA_M_DRILL"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  Solid.Subtract "B0_Stalk:B_P_PRONG", "E2C_B_P_ViaHoleTools:PADDLE_VIA_M_DRILL"

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_M"
   .Component "E2C_B_P_Vias"
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
   .Name "E2C_B_P_Vias:PADDLE_VIA_M"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_C_DRILL"
   .Component "E2C_B_P_ViaHoleTools"
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
   .Name "E2C_B_P_ViaHoleTools:PADDLE_VIA_C_DRILL"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  Solid.Subtract "B0_Stalk:B_P_PRONG", "E2C_B_P_ViaHoleTools:PADDLE_VIA_C_DRILL"

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_C"
   .Component "E2C_B_P_Vias"
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
   .Name "E2C_B_P_Vias:PADDLE_VIA_C"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_P_DRILL"
   .Component "E2C_B_P_ViaHoleTools"
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
   .Name "E2C_B_P_ViaHoleTools:PADDLE_VIA_P_DRILL"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  Solid.Subtract "B0_Stalk:B_P_PRONG", "E2C_B_P_ViaHoleTools:PADDLE_VIA_P_DRILL"

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_P"
   .Component "E2C_B_P_Vias"
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
   .Name "E2C_B_P_Vias:PADDLE_VIA_P"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  With Extrude
   .Reset
   .Name "CRF_GND_PAD"
   .Component "E2C_B_P_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_ViaHoleTools"
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
   .Name "E2C_B_P_ViaHoleTools:CRF_GROUND_VIA_DRILL"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  Solid.Subtract "B0_Stalk:B_P_PRONG", "E2C_B_P_ViaHoleTools:CRF_GROUND_VIA_DRILL"

  With Cylinder
   .Reset
   .Name "CRF_GROUND_VIA"
   .Component "E2C_B_P_Vias"
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
   .Name "E2C_B_P_Vias:CRF_GROUND_VIA"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  With Extrude
   .Reset
   .Name "LOCAL_BACK_GROUND"
   .Component "E2C_B_N_BackGround"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "-0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0.707106781186547", "0.707106781186547", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
   .Vvector "0.0", "0.0", "-1.0"
   .Point "-5", "3"
   .LineTo "-1", "3"
   .LineTo "-1", "12"
   .LineTo "-1.125", "12"
   .LineTo "-1.125", "13"
   .LineTo "-5", "13"
   .LineTo "-5", "3"
   .Create
  End With

  With Extrude
   .Reset
   .Name "PIN3_GND"
   .Component "E2C_B_N_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Name "PIN6_GND_FDD"
   .Component "E2C_B_N_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_PackageLands"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_ViaHoleTools"
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
   .Name "E2C_B_N_ViaHoleTools:PADDLE_VIA_M_DRILL"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  Solid.Subtract "B0_Stalk:B_N_PRONG", "E2C_B_N_ViaHoleTools:PADDLE_VIA_M_DRILL"

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_M"
   .Component "E2C_B_N_Vias"
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
   .Name "E2C_B_N_Vias:PADDLE_VIA_M"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_C_DRILL"
   .Component "E2C_B_N_ViaHoleTools"
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
   .Name "E2C_B_N_ViaHoleTools:PADDLE_VIA_C_DRILL"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  Solid.Subtract "B0_Stalk:B_N_PRONG", "E2C_B_N_ViaHoleTools:PADDLE_VIA_C_DRILL"

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_C"
   .Component "E2C_B_N_Vias"
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
   .Name "E2C_B_N_Vias:PADDLE_VIA_C"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_P_DRILL"
   .Component "E2C_B_N_ViaHoleTools"
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
   .Name "E2C_B_N_ViaHoleTools:PADDLE_VIA_P_DRILL"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  Solid.Subtract "B0_Stalk:B_N_PRONG", "E2C_B_N_ViaHoleTools:PADDLE_VIA_P_DRILL"

  With Cylinder
   .Reset
   .Name "PADDLE_VIA_P"
   .Component "E2C_B_N_Vias"
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
   .Name "E2C_B_N_Vias:PADDLE_VIA_P"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  With Extrude
   .Reset
   .Name "CRF_GND_PAD"
   .Component "E2C_B_N_LocalGroundTop"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_ViaHoleTools"
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
   .Name "E2C_B_N_ViaHoleTools:CRF_GROUND_VIA_DRILL"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

  Solid.Subtract "B0_Stalk:B_N_PRONG", "E2C_B_N_ViaHoleTools:CRF_GROUND_VIA_DRILL"

  With Cylinder
   .Reset
   .Name "CRF_GROUND_VIA"
   .Component "E2C_B_N_Vias"
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
   .Name "E2C_B_N_Vias:CRF_GROUND_VIA"
   .Origin "Free"
   .Center "0", "0", "0"
   .Angle "0", "0", "-135"
   .MultipleObjects "False"
   .GroupObjects "False"
   .Repetitions "1"
   .MultipleSelection "False"
   .Transform "Shape", "Rotate"
  End With

End Sub
