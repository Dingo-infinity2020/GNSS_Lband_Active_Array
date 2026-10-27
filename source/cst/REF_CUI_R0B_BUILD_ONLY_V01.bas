Option Explicit

' GNSS_Lband_Active_Array
' REF-CUI-R0B - DETERMINISTIC BUILD-ONLY V01
' CST Studio Suite 2022
'
' PURPOSE
'   Deterministic CST reference build of Cui et al. 2023 from the frozen
'   project geometry map (refs/cui2023/GEOMETRY_MAP.md, parameters.csv).
'
' HARD STOP
'   * BUILD ONLY. NO ports. NO solver/sweep/optimizer/mesh/monitor.
'   * NO LNA, shield, Bias-Tee, GNSS scaling, or CHARTS geometry.
'
' SOURCE LOCK
'   * All 26 Table-1 values are PAPER_EXPLICIT and parameterized below.
'   * Rogers 4350B, er=3.48, substrate thickness=0.76 mm.
'
' CAD CONSTRUCTION ASSUMPTIONS (see RUNBOOK_BUILD_ONLY.md):
'   copper_t, ground_t, rad_margin, balun_w, balun_off, eps,
'   L-bend open-slot proxy, diagonal-taper triangle placement,
'   schematic balun metal strip proxy.

Sub Main()

    ' ---------------- Source-locked Table 1 ----------------
    StoreParameter "Lg", 260.0
    StoreParameter "H", 80.0
    StoreParameter "Lr", 115.0
    StoreParameter "Wr", 5.9
    StoreParameter "Ld", 97.0
    StoreParameter "Ws", 2.2
    StoreParameter "Ls", 26.6
    StoreParameter "Wg1", 1.7
    StoreParameter "Wg2", 3.9
    StoreParameter "Wp", 8.4
    StoreParameter "Lp1", 36.3
    StoreParameter "Lp2", 8.2
    StoreParameter "Lp3", 36.8
    StoreParameter "Lb1", 21.0
    StoreParameter "Lb2", 10.0
    StoreParameter "Lb3", 20.5
    StoreParameter "Lb4", 24.5
    StoreParameter "Lb5", 73.0
    StoreParameter "Wb1", 1.5
    StoreParameter "Wb2", 0.65
    StoreParameter "Wb3", 0.95
    StoreParameter "Wb4", 13.0
    StoreParameter "Wb5", 28.5
    StoreParameter "Wb6", 3.6
    StoreParameter "Wb7", 4.8
    StoreParameter "Wb8", 3.6

    ' ---------------- Source-locked material ----------------
    StoreParameter "er", 3.48
    StoreParameter "sub_t", 0.76

    ' ---------------- CAD construction assumptions ----------------
    StoreParameter "copper_t", 0.035
    StoreParameter "ground_t", 0.5
    StoreParameter "rad_margin", 5.0
    StoreParameter "rad_sub_side", "Lr+2*rad_margin"
    StoreParameter "balun_w", 30.0
    StoreParameter "balun_off", 1.0
    StoreParameter "s2", 0.70710678
    StoreParameter "eps", 0.01

    ' ---------------- Derived ----------------
    StoreParameter "a", "Ld/2"
    StoreParameter "g1", "Wg1/2"
    StoreParameter "g2", "Wg2/2"
    StoreParameter "hLr", "Lr/2"
    StoreParameter "hLri", "Lr/2-Wr"
    StoreParameter "xs", "a-Wp-Ls"
    StoreParameter "ys", "Lp1"
    StoreParameter "u0", "-balun_w/2+Wb5"
    StoreParameter "z1", "Lb1"
    StoreParameter "z2", "Lb1+Lb2"
    StoreParameter "z3", "Lb1+Lb2+Lb3"

    With Units
        .Geometry "mm"
        .Frequency "GHz"
        .Time "ns"
        .Voltage "V"
    End With

    ' ---------------- Material: Rogers 4350B ----------------
    With Material
        .Reset
        .Name "Rogers_4350B"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "er"
        .Mue "1.0"
        .TanD "0.0037"
        .TanDFreq "0.0"
        .TanDGiven "False"
        .TanDModel "ConstTanD"
        .Colour "0.85", "0.9", "0.75"
        .Create
    End With

    ' ---------------- Main ground ----------------
    With Brick
        .Reset
        .Name "GROUND"
        .Component "MainGround"
        .Material "PEC"
        .Xrange "-Lg/2", "Lg/2"
        .Yrange "-Lg/2", "Lg/2"
        .Zrange "-ground_t", "0"
        .Create
    End With

    ' ---------------- Radiator dielectric ----------------
    With Brick
        .Reset
        .Name "RADIATOR_SUB"
        .Component "RadiatorBoard"
        .Material "Rogers_4350B"
        .Xrange "-rad_sub_side/2", "rad_sub_side/2"
        .Yrange "-rad_sub_side/2", "rad_sub_side/2"
        .Zrange "H-sub_t", "H"
        .Create
    End With

    ' ---------------- Square loop (outer Lr, width Wr) ----------------
    With Brick
        .Reset
        .Name "LOOP"
        .Component "Radiator"
        .Material "PEC"
        .Xrange "-hLr", "hLr"
        .Yrange "-hLr", "hLr"
        .Zrange "H", "H+copper_t"
        .Create
    End With
    With Brick
        .Reset
        .Name "LOOP_CUT"
        .Component "Tools"
        .Material "Vacuum"
        .Xrange "-hLri", "hLri"
        .Yrange "-hLri", "hLri"
        .Zrange "H-eps", "H+copper_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:LOOP", "Tools:LOOP_CUT"

    ' ---------------- Crossed-dipole arm plate (envelope Ld) ----------------
    With Brick
        .Reset
        .Name "ARMS"
        .Component "Radiator"
        .Material "PEC"
        .Xrange "-a", "a"
        .Yrange "-a", "a"
        .Zrange "H", "H+copper_t"
        .Create
    End With

    ' ---------------- Tapered central cross gap (Wg1 -> Wg2) ----------------
    With Extrude
        .Reset
        .Name "GAP_N"
        .Component "Tools"
        .Material "Vacuum"
        .Mode "Pointlist"
        .Height "copper_t+2*eps"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "H-eps"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-g1", "0.0"
        .LineTo "g1", "0.0"
        .LineTo "g2", "a"
        .LineTo "-g2", "a"
        .LineTo "-g1", "0.0"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:GAP_N"
    With Extrude
        .Reset
        .Name "GAP_S"
        .Component "Tools"
        .Material "Vacuum"
        .Mode "Pointlist"
        .Height "copper_t+2*eps"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "H-eps"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-g1", "0.0"
        .LineTo "-g2", "-a"
        .LineTo "g2", "-a"
        .LineTo "g1", "0.0"
        .LineTo "-g1", "0.0"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:GAP_S"
    With Extrude
        .Reset
        .Name "GAP_E"
        .Component "Tools"
        .Material "Vacuum"
        .Mode "Pointlist"
        .Height "copper_t+2*eps"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "H-eps"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "0.0", "-g1"
        .LineTo "a", "-g2"
        .LineTo "a", "g2"
        .LineTo "0.0", "g1"
        .LineTo "0.0", "-g1"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:GAP_E"
    With Extrude
        .Reset
        .Name "GAP_W"
        .Component "Tools"
        .Material "Vacuum"
        .Mode "Pointlist"
        .Height "copper_t+2*eps"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "H-eps"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "0.0", "-g1"
        .LineTo "0.0", "g1"
        .LineTo "-a", "g2"
        .LineTo "-a", "-g2"
        .LineTo "0.0", "-g1"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:GAP_W"

    ' ---------------- Four open slots (L-bend proxy) ----------------
    With Brick
        .Reset
        .Name "SLOT1_A"
        .Component "Tools"
        .Material "Vacuum"
        .Xrange "xs", "xs+Ls"
        .Yrange "ys", "ys+Ws"
        .Zrange "H-eps", "H+copper_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:SLOT1_A"
    With Brick
        .Reset
        .Name "SLOT1_B"
        .Component "Tools"
        .Material "Vacuum"
        .Xrange "xs", "xs+Ws"
        .Yrange "ys", "ys+Ls"
        .Zrange "H-eps", "H+copper_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:SLOT1_B"

    With Brick
        .Reset
        .Name "SLOT2_A"
        .Component "Tools"
        .Material "Vacuum"
        .Xrange "-xs-Ls", "-xs"
        .Yrange "ys", "ys+Ws"
        .Zrange "H-eps", "H+copper_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:SLOT2_A"
    With Brick
        .Reset
        .Name "SLOT2_B"
        .Component "Tools"
        .Material "Vacuum"
        .Xrange "-xs-Ws", "-xs"
        .Yrange "ys", "ys+Ls"
        .Zrange "H-eps", "H+copper_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:SLOT2_B"

    With Brick
        .Reset
        .Name "SLOT3_A"
        .Component "Tools"
        .Material "Vacuum"
        .Xrange "-xs-Ls", "-xs"
        .Yrange "-ys-Ws", "-ys"
        .Zrange "H-eps", "H+copper_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:SLOT3_A"
    With Brick
        .Reset
        .Name "SLOT3_B"
        .Component "Tools"
        .Material "Vacuum"
        .Xrange "-xs-Ws", "-xs"
        .Yrange "-ys-Ls", "-ys"
        .Zrange "H-eps", "H+copper_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:SLOT3_B"

    With Brick
        .Reset
        .Name "SLOT4_A"
        .Component "Tools"
        .Material "Vacuum"
        .Xrange "xs", "xs+Ls"
        .Yrange "-ys-Ws", "-ys"
        .Zrange "H-eps", "H+copper_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:SLOT4_A"
    With Brick
        .Reset
        .Name "SLOT4_B"
        .Component "Tools"
        .Material "Vacuum"
        .Xrange "xs", "xs+Ws"
        .Yrange "-ys-Ls", "-ys"
        .Zrange "H-eps", "H+copper_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:SLOT4_B"

    ' ---------------- Diagonal inner taper triangles ----------------
    With Extrude
        .Reset
        .Name "TAPER1"
        .Component "Tools"
        .Material "Vacuum"
        .Mode "Pointlist"
        .Height "copper_t+2*eps"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "H-eps"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "xs", "ys"
        .LineTo "xs-Lp3", "ys"
        .LineTo "xs", "ys-Lp2"
        .LineTo "xs", "ys"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:TAPER1"
    With Extrude
        .Reset
        .Name "TAPER2"
        .Component "Tools"
        .Material "Vacuum"
        .Mode "Pointlist"
        .Height "copper_t+2*eps"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "H-eps"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-xs", "ys"
        .LineTo "-xs+Lp3", "ys"
        .LineTo "-xs", "ys-Lp2"
        .LineTo "-xs", "ys"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:TAPER2"
    With Extrude
        .Reset
        .Name "TAPER3"
        .Component "Tools"
        .Material "Vacuum"
        .Mode "Pointlist"
        .Height "copper_t+2*eps"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "H-eps"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-xs", "-ys"
        .LineTo "-xs+Lp3", "-ys"
        .LineTo "-xs", "-ys+Lp2"
        .LineTo "-xs", "-ys"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:TAPER3"
    With Extrude
        .Reset
        .Name "TAPER4"
        .Component "Tools"
        .Material "Vacuum"
        .Mode "Pointlist"
        .Height "copper_t+2*eps"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "H-eps"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "xs", "-ys"
        .LineTo "xs-Lp3", "-ys"
        .LineTo "xs", "-ys+Lp2"
        .LineTo "xs", "-ys"
        .Create
    End With
    Solid.Subtract "Radiator:ARMS", "Tools:TAPER4"

    ' ---------------- Balun 1 substrate (diagonal vertical plane) ----------------
    With Extrude
        .Reset
        .Name "BALUN1_SUB"
        .Component "Balun1"
        .Material "Rogers_4350B"
        .Mode "Pointlist"
        .Height "sub_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "balun_off*s2", "balun_off*s2", "0.0"
        .Uvector "s2", "s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "-balun_w/2", "0.0"
        .LineTo "balun_w/2", "0.0"
        .LineTo "balun_w/2", "Lb5"
        .LineTo "-balun_w/2", "Lb5"
        .LineTo "-balun_w/2", "0.0"
        .Create
    End With

    ' ---------------- Balun 2 substrate (orthogonal diagonal plane) ----------------
    With Extrude
        .Reset
        .Name "BALUN2_SUB"
        .Component "Balun2"
        .Material "Rogers_4350B"
        .Mode "Pointlist"
        .Height "sub_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "-balun_off*s2", "balun_off*s2", "0.0"
        .Uvector "s2", "-s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "-balun_w/2", "0.0"
        .LineTo "balun_w/2", "0.0"
        .LineTo "balun_w/2", "Lb5"
        .LineTo "-balun_w/2", "Lb5"
        .LineTo "-balun_w/2", "0.0"
        .Create
    End With

    ' ---------------- Balun 1 metal pattern (schematic proxy) ----------------
    With Extrude
        .Reset
        .Name "B1_F1"
        .Component "Balun1"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0", "0.0"
        .LineTo "u0+Wb1", "0.0"
        .LineTo "u0+Wb1", "z1"
        .LineTo "u0", "z1"
        .LineTo "u0", "0.0"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B1_F2"
        .Component "Balun1"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0", "z1"
        .LineTo "u0+Wb2", "z1"
        .LineTo "u0+Wb2", "z2"
        .LineTo "u0", "z2"
        .LineTo "u0", "z1"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B1_F3"
        .Component "Balun1"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0", "z2"
        .LineTo "u0+Wb3", "z2"
        .LineTo "u0+Wb3", "z3"
        .LineTo "u0", "z3"
        .LineTo "u0", "z2"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B1_STUB"
        .Component "Balun1"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0-Wb1", "z3-Lb4"
        .LineTo "u0", "z3-Lb4"
        .LineTo "u0", "z3"
        .LineTo "u0-Wb1", "z3"
        .LineTo "u0-Wb1", "z3-Lb4"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B1_UL"
        .Component "Balun1"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0", "z3"
        .LineTo "u0+Wb3", "z3"
        .LineTo "u0+Wb3", "z3+Wb4"
        .LineTo "u0", "z3+Wb4"
        .LineTo "u0", "z3"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B1_UR"
        .Component "Balun1"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0+Wb4-Wb3", "z3"
        .LineTo "u0+Wb4", "z3"
        .LineTo "u0+Wb4", "z3+Wb3"
        .LineTo "u0+Wb4-Wb3", "z3+Wb3"
        .LineTo "u0+Wb4-Wb3", "z3"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B1_TABR"
        .Component "Balun1"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0+Wb4", "z3+Wb4-Wb7"
        .LineTo "u0+Wb4+Wb7", "z3+Wb4-Wb7"
        .LineTo "u0+Wb4+Wb7", "z3+Wb4"
        .LineTo "u0+Wb4", "z3+Wb4"
        .LineTo "u0+Wb4", "z3+Wb4-Wb7"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B1_TABL"
        .Component "Balun1"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0-Wb8", "z3+Wb4-Wb8"
        .LineTo "u0", "z3+Wb4-Wb8"
        .LineTo "u0", "z3+Wb4"
        .LineTo "u0-Wb8", "z3+Wb4"
        .LineTo "u0-Wb8", "z3+Wb4-Wb8"
        .Create
    End With

    ' ---------------- Balun 2 metal pattern (schematic proxy) ----------------
    With Extrude
        .Reset
        .Name "B2_F1"
        .Component "Balun2"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "-balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "-s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0", "0.0"
        .LineTo "u0+Wb1", "0.0"
        .LineTo "u0+Wb1", "z1"
        .LineTo "u0", "z1"
        .LineTo "u0", "0.0"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B2_F2"
        .Component "Balun2"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "-balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "-s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0", "z1"
        .LineTo "u0+Wb2", "z1"
        .LineTo "u0+Wb2", "z2"
        .LineTo "u0", "z2"
        .LineTo "u0", "z1"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B2_F3"
        .Component "Balun2"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "-balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "-s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0", "z2"
        .LineTo "u0+Wb3", "z2"
        .LineTo "u0+Wb3", "z3"
        .LineTo "u0", "z3"
        .LineTo "u0", "z2"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B2_STUB"
        .Component "Balun2"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "-balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "-s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0-Wb1", "z3-Lb4"
        .LineTo "u0", "z3-Lb4"
        .LineTo "u0", "z3"
        .LineTo "u0-Wb1", "z3"
        .LineTo "u0-Wb1", "z3-Lb4"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B2_UL"
        .Component "Balun2"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "-balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "-s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0", "z3"
        .LineTo "u0+Wb3", "z3"
        .LineTo "u0+Wb3", "z3+Wb4"
        .LineTo "u0", "z3+Wb4"
        .LineTo "u0", "z3"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B2_UR"
        .Component "Balun2"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "-balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "-s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0+Wb4-Wb3", "z3"
        .LineTo "u0+Wb4", "z3"
        .LineTo "u0+Wb4", "z3+Wb3"
        .LineTo "u0+Wb4-Wb3", "z3+Wb3"
        .LineTo "u0+Wb4-Wb3", "z3"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B2_TABR"
        .Component "Balun2"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "-balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "-s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0+Wb4", "z3+Wb4-Wb7"
        .LineTo "u0+Wb4+Wb7", "z3+Wb4-Wb7"
        .LineTo "u0+Wb4+Wb7", "z3+Wb4"
        .LineTo "u0+Wb4", "z3+Wb4"
        .LineTo "u0+Wb4", "z3+Wb4-Wb7"
        .Create
    End With
    With Extrude
        .Reset
        .Name "B2_TABL"
        .Component "Balun2"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "copper_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "-balun_off*s2", "balun_off*s2", "sub_t"
        .Uvector "s2", "-s2", "0.0"
        .Vvector "0.0", "0.0", "1.0"
        .Point "u0-Wb8", "z3+Wb4-Wb8"
        .LineTo "u0", "z3+Wb4-Wb8"
        .LineTo "u0", "z3+Wb4"
        .LineTo "u0-Wb8", "z3+Wb4"
        .LineTo "u0-Wb8", "z3+Wb4-Wb8"
        .Create
    End With

End Sub
