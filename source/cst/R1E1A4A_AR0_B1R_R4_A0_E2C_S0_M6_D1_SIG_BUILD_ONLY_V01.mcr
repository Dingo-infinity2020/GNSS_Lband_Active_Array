Option Explicit
' GNSS_Lband_Active_Array
' R4-A0-E2C-S0-M6-D1 attribution BUILD ONLY V01
'
' Parent: canonical E2A Pol-A BUILD_ONLY baseline
' Parent SHA256: 78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804
' Diagnostic only; no ports, monitors, solver configuration, or solver invocation added.

Sub Main()

  With Extrude
   .Reset
   .Name "UPSTREAM_MSL"
   .Component "E2C_B_P_Signal"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_Signal"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_P_Signal"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Name "UPSTREAM_MSL"
   .Component "E2C_B_N_Signal"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_Signal"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
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
   .Component "E2C_B_N_Signal"
   .Material "B0_COPPER"
   .Mode "Pointlist"
   .Height "0.035"
   .Twist "0.0"
   .Taper "0.0"
   .Origin "0", "0", "57.1428571428"
   .Uvector "-0.707106781186547", "0.707106781186547", "0.0"
   .Vvector "0.0", "0.0", "-1.0"
   .Point "-3.3", "4.4"
   .LineTo "-2.7", "4.4"
   .LineTo "-2.7", "4.9"
   .LineTo "-3.3", "4.9"
   .LineTo "-3.3", "4.4"
   .Create
  End With

End Sub
