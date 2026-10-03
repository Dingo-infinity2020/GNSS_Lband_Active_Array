Option Explicit
' GNSS_Lband_Active_Array
' R4-A0-E1 one-LNA landing-zone BUILD ONLY V01
' SimulationOps 0.2.8
'
' HARD STOP:
'   build-only; exactly six single-ended discrete ports;
'   no solver, no monitor, no optimizer, no active QPL9547 object.
'
' Coordinate map:
'   CST x = q (transverse)
'   CST y = v (downstream)
'   CST z = n (board normal)
'
' Circuit-only elements after EM export:
'   C_IN E_UP<->P_IN
'   QPL9547 S2P P_IN<->P_OUT
'   C_OUT P_OUT<->E_DN
'   L1 P_OUT<->B_VDD
'   C_RF B_VDD<->ground
'   R4 B_VDD<->B_VBIAS

Sub Main()

    With Units
        .Geometry "mm"
        .Frequency "GHz"
        .Time "ns"
        .Voltage "V"
    End With

    ' ---------- frozen parameters ----------
    StoreParameter "e1_qmin", -2.0
    StoreParameter "e1_qmax", 2.0
    StoreParameter "e1_vmin", 3.0
    StoreParameter "e1_vmax", 13.0
    StoreParameter "e1_board_t", 1.0
    StoreParameter "e1_cu_t", 0.035
    StoreParameter "e1_fr4_er", 4.2
    StoreParameter "e1_fr4_tand", 0.018
    StoreParameter "e1_via_ro", 0.175
    StoreParameter "e1_via_ri", 0.125

    ' ---------- materials ----------
    With Material
        .Reset
        .Name "FR4_COST_BASELINE"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "e1_fr4_er"
        .Mue "1.0"
        .TanD "e1_fr4_tand"
        .TanDFreq "1.4"
        .TanDGiven "True"
        .TanDModel "ConstTanD"
        .Create
    End With

    With Material
        .Reset
        .Name "E1_COPPER"
        .Folder ""
        .FrqType "all"
        .Type "Lossy metal"
        .SetMaterialUnit "GHz", "mm"
        .Mue "1.0"
        .Sigma "58000000"
        .Create
    End With

    ' ---------- substrate ----------
    With Brick
        .Reset
        .Name "FR4_COUPON"
        .Component "E1_Substrate"
        .Material "FR4_COST_BASELINE"
        .Xrange "-2.0", "2.0"
        .Yrange "3.0", "13.0"
        .Zrange "-1.0", "0.0"
        .Create
    End With

    ' ---------- full local backside ground ----------
    With Brick
        .Reset
        .Name "LOCAL_BACK_GROUND"
        .Component "E1_BackGround"
        .Material "E1_COPPER"
        .Xrange "-2.0", "2.0"
        .Yrange "3.0", "13.0"
        .Zrange "-1.035", "-1.0"
        .Create
    End With

    ' ---------- upstream branch line ----------
    With Brick
        .Reset
        .Name "UPSTREAM_MSL"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Xrange "-0.95", "0.95"
        .Yrange "3.0", "3.4"
        .Zrange "0.0", "0.035"
        .Create
    End With

    With Extrude
        .Reset
        .Name "UPSTREAM_TAPER"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Mode "Pointlist"
        .Height "0.035"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "0.0"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-0.95", "3.4"
        .LineTo "0.95", "3.4"
        .LineTo "0.30", "4.4"
        .LineTo "-0.30", "4.4"
        .LineTo "-0.95", "3.4"
        .Create
    End With

    ' ---------- C_IN pads ----------
    With Brick
        .Reset
        .Name "CIN_UP_PAD"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Xrange "-0.30", "0.30"
        .Yrange "4.40", "4.90"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "CIN_DN_PAD"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Xrange "-0.30", "0.30"
        .Yrange "5.30", "5.80"
        .Zrange "0.0", "0.035"
        .Create
    End With

    With Extrude
        .Reset
        .Name "CIN_TO_RFIN_TAPER"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Mode "Pointlist"
        .Height "0.035"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "0.0"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-0.30", "5.80"
        .LineTo "0.30", "5.80"
        .LineTo "0.125", "5.87"
        .LineTo "-0.125", "5.87"
        .LineTo "-0.30", "5.80"
        .Create
    End With

    ' ---------- QPL9547 eight side lands ----------
    ' upstream x_pkg=-0.915 -> v=6.085
    Call MakeLand("PIN1_VBIAS","E1_PackageLands",-0.50,5.870,6.300)
    Call MakeLand("PIN2_RFIN","E1_PackageLands",0.00,5.870,6.300)
    Call MakeLand("PIN3_GND","E1_PackageLands",0.50,5.870,6.300)
    Call MakeLand("PIN4_GND","E1_PackageLands",1.00,5.870,6.300)
    ' downstream x_pkg=+0.915 -> v=7.915
    Call MakeLand("PIN8_GND","E1_PackageLands",-0.50,7.700,8.130)
    Call MakeLand("PIN7_RFOUT_VDD","E1_PackageLands",0.00,7.700,8.130)
    Call MakeLand("PIN6_GND_FDD","E1_PackageLands",0.50,7.700,8.130)
    Call MakeLand("PIN5_GND","E1_PackageLands",1.00,7.700,8.130)

    ' ---------- exposed paddle ----------
    With Brick
        .Reset
        .Name "EXPOSED_PADDLE"
        .Component "E1_LocalGroundTop"
        .Material "E1_COPPER"
        .Xrange "-0.55", "1.05"
        .Yrange "6.60", "7.40"
        .Zrange "0.0", "0.035"
        .Create
    End With

    ' five grounded-pin spokes
    Call MakeSpoke("PIN3_SPOKE",0.50,6.30,6.60)
    Call MakeSpoke("PIN4_SPOKE",1.00,6.30,6.60)
    Call MakeSpoke("PIN8_SPOKE",-0.50,7.40,7.70)
    Call MakeSpoke("PIN6_SPOKE",0.50,7.40,7.70)
    Call MakeSpoke("PIN5_SPOKE",1.00,7.40,7.70)

    ' ---------- paddle vias ----------
    Call MakeVia("PADDLE_VIA_M",-0.25,7.00)
    Call MakeVia("PADDLE_VIA_C",0.25,7.00)
    Call MakeVia("PADDLE_VIA_P",0.75,7.00)

    ' ---------- RF output short taper ----------
    With Extrude
        .Reset
        .Name "RFOUT_TO_COUT_TAPER"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Mode "Pointlist"
        .Height "0.035"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "0.0"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-0.125", "8.13"
        .LineTo "0.125", "8.13"
        .LineTo "0.30", "8.20"
        .LineTo "-0.30", "8.20"
        .LineTo "-0.125", "8.13"
        .Create
    End With

    ' ---------- C_OUT pads ----------
    Call MakeRect("COUT_DEV_PAD","E1_Signal",-0.30,0.30,8.20,8.70)
    Call MakeRect("COUT_DN_PAD","E1_Signal",-0.30,0.30,9.10,9.60)

    ' ---------- L1 pads and P_OUT fan ----------
    Call MakeRect("L1_RF_PAD","E1_Bias",1.15,1.75,8.20,8.70)
    Call MakeRect("L1_VDD_PAD","E1_Bias",1.15,1.75,9.10,9.60)
    Call MakeRect("POUT_TO_L1_FAN","E1_Bias",0.30,1.15,8.30,8.60)

    ' ---------- VDD interconnect / C_RF ----------
    Call MakeRect("VDD_TRACE","E1_Bias",1.15,1.75,9.60,10.00)
    Call MakeRect("CRF_VDD_PAD","E1_Bias",1.15,1.75,10.00,10.50)
    Call MakeRect("CRF_GND_PAD","E1_LocalGroundTop",1.15,1.75,10.90,11.40)
    Call MakeVia("CRF_GROUND_VIA",1.45,11.15)

    ' ---------- downstream RF taper / line ----------
    With Extrude
        .Reset
        .Name "DOWNSTREAM_TAPER"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Mode "Pointlist"
        .Height "0.035"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "0.0"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-0.30", "9.60"
        .LineTo "0.30", "9.60"
        .LineTo "0.95", "10.60"
        .LineTo "-0.95", "10.60"
        .LineTo "-0.30", "9.60"
        .Create
    End With
    Call MakeRect("DOWNSTREAM_MSL","E1_Signal",-0.95,0.95,10.60,13.00)

    ' ---------- six single-ended ports ----------
    Call MakePort(1,0.00,4.650,50.0)
    Call MakePort(2,0.00,6.085,50.0)
    Call MakePort(3,0.00,7.915,50.0)
    Call MakePort(4,0.00,9.350,50.0)
    Call MakePort(5,1.45,9.800,50.0)
    Call MakePort(6,-0.50,6.085,50.0)

End Sub

Sub MakeRect(nm As String, comp As String, q1 As Double, q2 As Double, v1 As Double, v2 As Double)
    With Brick
        .Reset
        .Name nm
        .Component comp
        .Material "E1_COPPER"
        .Xrange CStr(q1), CStr(q2)
        .Yrange CStr(v1), CStr(v2)
        .Zrange "0.0", "0.035"
        .Create
    End With
End Sub

Sub MakeLand(nm As String, comp As String, qc As Double, v1 As Double, v2 As Double)
    Call MakeRect(nm,comp,qc-0.125,qc+0.125,v1,v2)
End Sub

Sub MakeSpoke(nm As String, qc As Double, v1 As Double, v2 As Double)
    Call MakeRect(nm,"E1_LocalGroundTop",qc-0.10,qc+0.10,v1,v2)
End Sub

Sub MakeVia(nm As String, qc As Double, vc As Double)
    With Cylinder
        .Reset
        .Name nm
        .Component "E1_Vias"
        .Material "E1_COPPER"
        .OuterRadius "0.175"
        .InnerRadius "0.125"
        .Axis "z"
        .Zrange "-1.035", "0.035"
        .Xcenter CStr(qc)
        .Ycenter CStr(vc)
        .Segments "0"
        .Create
    End With
End Sub

Sub MakePort(pn As Integer, qc As Double, vc As Double, zref As Double)
    With DiscretePort
        .Reset
        .PortNumber CStr(pn)
        .Type "SParameter"
        .Impedance CStr(zref)
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", CStr(qc), CStr(vc), "0.0"
        .SetP2 "False", CStr(qc), CStr(vc), "-1.0"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With
End Sub
