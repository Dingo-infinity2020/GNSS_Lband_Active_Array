Option Explicit
' GNSS_Lband_Active_Array
' R4-A0-E1 one-LNA landing-zone BUILD ONLY V03
' Recovery from V02 tooling HOLD.
'
' HARD STOP:
'   persistent History List build only;
'   exactly six single-ended discrete ports;
'   no solver, no monitor, no optimizer, no active QPL9547 object.
'
' V03 geometry/electrical dimensions are identical to V02.
' Only build persistence/execution semantics change:
'   V03 MUST be executed through Project.modeler.add_to_history()
'   using the body of Main(), never by direct schematic.execute_vba_code().
'
' Coordinate map:
'   CST x = q (transverse)
'   CST y = v (downstream)
'   CST z = n (board normal)

Sub Main()

    With Units
        .Geometry "mm"
        .Frequency "GHz"
        .Time "ns"
        .Voltage "V"
    End With

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

    With Brick
        .Reset
        .Name "PIN1_VBIAS"
        .Component "E1_PackageLands"
        .Material "E1_COPPER"
        .Xrange "-0.625", "-0.375"
        .Yrange "5.870", "6.300"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN2_RFIN"
        .Component "E1_PackageLands"
        .Material "E1_COPPER"
        .Xrange "-0.125", "0.125"
        .Yrange "5.870", "6.300"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN3_GND"
        .Component "E1_PackageLands"
        .Material "E1_COPPER"
        .Xrange "0.375", "0.625"
        .Yrange "5.870", "6.300"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN4_GND"
        .Component "E1_PackageLands"
        .Material "E1_COPPER"
        .Xrange "0.875", "1.125"
        .Yrange "5.870", "6.300"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN8_GND"
        .Component "E1_PackageLands"
        .Material "E1_COPPER"
        .Xrange "-0.625", "-0.375"
        .Yrange "7.700", "8.130"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN7_RFOUT_VDD"
        .Component "E1_PackageLands"
        .Material "E1_COPPER"
        .Xrange "-0.125", "0.125"
        .Yrange "7.700", "8.130"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN6_GND_FDD"
        .Component "E1_PackageLands"
        .Material "E1_COPPER"
        .Xrange "0.375", "0.625"
        .Yrange "7.700", "8.130"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN5_GND"
        .Component "E1_PackageLands"
        .Material "E1_COPPER"
        .Xrange "0.875", "1.125"
        .Yrange "7.700", "8.130"
        .Zrange "0.0", "0.035"
        .Create
    End With

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

    With Brick
        .Reset
        .Name "PIN3_SPOKE"
        .Component "E1_LocalGroundTop"
        .Material "E1_COPPER"
        .Xrange "0.400", "0.600"
        .Yrange "6.300", "6.600"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN4_SPOKE"
        .Component "E1_LocalGroundTop"
        .Material "E1_COPPER"
        .Xrange "0.900", "1.100"
        .Yrange "6.300", "6.600"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN8_SPOKE"
        .Component "E1_LocalGroundTop"
        .Material "E1_COPPER"
        .Xrange "-0.600", "-0.400"
        .Yrange "7.400", "7.700"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN6_SPOKE"
        .Component "E1_LocalGroundTop"
        .Material "E1_COPPER"
        .Xrange "0.400", "0.600"
        .Yrange "7.400", "7.700"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "PIN5_SPOKE"
        .Component "E1_LocalGroundTop"
        .Material "E1_COPPER"
        .Xrange "0.900", "1.100"
        .Yrange "7.400", "7.700"
        .Zrange "0.0", "0.035"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "PADDLE_VIA_M_DRILL"
        .Component "E1_ViaHoleTools"
        .Material "Vacuum"
        .OuterRadius "0.175"
        .InnerRadius "0.0"
        .Axis "z"
        .Zrange "-1.01", "0.01"
        .Xcenter "-0.250"
        .Ycenter "7.000"
        .Segments "0"
        .Create
    End With
    Solid.Subtract "E1_Substrate:FR4_COUPON", "E1_ViaHoleTools:PADDLE_VIA_M_DRILL"
    With Cylinder
        .Reset
        .Name "PADDLE_VIA_M"
        .Component "E1_Vias"
        .Material "E1_COPPER"
        .OuterRadius "0.175"
        .InnerRadius "0.125"
        .Axis "z"
        .Zrange "-1.035", "0.035"
        .Xcenter "-0.250"
        .Ycenter "7.000"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "PADDLE_VIA_C_DRILL"
        .Component "E1_ViaHoleTools"
        .Material "Vacuum"
        .OuterRadius "0.175"
        .InnerRadius "0.0"
        .Axis "z"
        .Zrange "-1.01", "0.01"
        .Xcenter "0.250"
        .Ycenter "7.000"
        .Segments "0"
        .Create
    End With
    Solid.Subtract "E1_Substrate:FR4_COUPON", "E1_ViaHoleTools:PADDLE_VIA_C_DRILL"
    With Cylinder
        .Reset
        .Name "PADDLE_VIA_C"
        .Component "E1_Vias"
        .Material "E1_COPPER"
        .OuterRadius "0.175"
        .InnerRadius "0.125"
        .Axis "z"
        .Zrange "-1.035", "0.035"
        .Xcenter "0.250"
        .Ycenter "7.000"
        .Segments "0"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "PADDLE_VIA_P_DRILL"
        .Component "E1_ViaHoleTools"
        .Material "Vacuum"
        .OuterRadius "0.175"
        .InnerRadius "0.0"
        .Axis "z"
        .Zrange "-1.01", "0.01"
        .Xcenter "0.750"
        .Ycenter "7.000"
        .Segments "0"
        .Create
    End With
    Solid.Subtract "E1_Substrate:FR4_COUPON", "E1_ViaHoleTools:PADDLE_VIA_P_DRILL"
    With Cylinder
        .Reset
        .Name "PADDLE_VIA_P"
        .Component "E1_Vias"
        .Material "E1_COPPER"
        .OuterRadius "0.175"
        .InnerRadius "0.125"
        .Axis "z"
        .Zrange "-1.035", "0.035"
        .Xcenter "0.750"
        .Ycenter "7.000"
        .Segments "0"
        .Create
    End With

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

    With Brick
        .Reset
        .Name "COUT_DEV_PAD"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Xrange "-0.30", "0.30"
        .Yrange "8.20", "8.70"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "COUT_DN_PAD"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Xrange "-0.30", "0.30"
        .Yrange "9.10", "9.60"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "L1_RF_PAD"
        .Component "E1_Bias"
        .Material "E1_COPPER"
        .Xrange "1.15", "1.75"
        .Yrange "8.20", "8.70"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "L1_VDD_PAD"
        .Component "E1_Bias"
        .Material "E1_COPPER"
        .Xrange "1.15", "1.75"
        .Yrange "9.10", "9.60"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "POUT_TO_L1_FAN"
        .Component "E1_Bias"
        .Material "E1_COPPER"
        .Xrange "0.30", "1.15"
        .Yrange "8.30", "8.60"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "VDD_TRACE"
        .Component "E1_Bias"
        .Material "E1_COPPER"
        .Xrange "1.15", "1.75"
        .Yrange "9.60", "10.00"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "CRF_VDD_PAD"
        .Component "E1_Bias"
        .Material "E1_COPPER"
        .Xrange "1.15", "1.75"
        .Yrange "10.00", "10.50"
        .Zrange "0.0", "0.035"
        .Create
    End With
    With Brick
        .Reset
        .Name "CRF_GND_PAD"
        .Component "E1_LocalGroundTop"
        .Material "E1_COPPER"
        .Xrange "1.15", "1.75"
        .Yrange "10.90", "11.40"
        .Zrange "0.0", "0.035"
        .Create
    End With

    With Cylinder
        .Reset
        .Name "CRF_GROUND_VIA_DRILL"
        .Component "E1_ViaHoleTools"
        .Material "Vacuum"
        .OuterRadius "0.175"
        .InnerRadius "0.0"
        .Axis "z"
        .Zrange "-1.01", "0.01"
        .Xcenter "1.450"
        .Ycenter "11.150"
        .Segments "0"
        .Create
    End With
    Solid.Subtract "E1_Substrate:FR4_COUPON", "E1_ViaHoleTools:CRF_GROUND_VIA_DRILL"
    With Cylinder
        .Reset
        .Name "CRF_GROUND_VIA"
        .Component "E1_Vias"
        .Material "E1_COPPER"
        .OuterRadius "0.175"
        .InnerRadius "0.125"
        .Axis "z"
        .Zrange "-1.035", "0.035"
        .Xcenter "1.450"
        .Ycenter "11.150"
        .Segments "0"
        .Create
    End With

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

    With Brick
        .Reset
        .Name "DOWNSTREAM_MSL"
        .Component "E1_Signal"
        .Material "E1_COPPER"
        .Xrange "-0.95", "0.95"
        .Yrange "10.60", "13.00"
        .Zrange "0.0", "0.035"
        .Create
    End With

    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "50.0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "0.000", "4.650", "0.0"
        .SetP2 "False", "0.000", "4.650", "-1.0"
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
        .SetP1 "False", "0.000", "6.085", "0.0"
        .SetP2 "False", "0.000", "6.085", "-1.0"
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
        .SetP1 "False", "0.000", "7.915", "0.0"
        .SetP2 "False", "0.000", "7.915", "-1.0"
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
        .SetP1 "False", "0.000", "9.350", "0.0"
        .SetP2 "False", "0.000", "9.350", "-1.0"
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
        .SetP1 "False", "1.450", "9.800", "0.0"
        .SetP2 "False", "1.450", "9.800", "-1.0"
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
        .SetP1 "False", "-0.500", "6.085", "0.0"
        .SetP2 "False", "-0.500", "6.085", "-1.0"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

End Sub
