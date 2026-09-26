Option Explicit

' DEPRECATED SCIENTIFIC TOPOLOGY - DO NOT USE FOR NEW BUILDS
' V0.2 runtime/replay passed, but direct Fig.2 review shows 8 outer slot segments,
' not 4. Use R0_CHARTS_12SLOT_BUILD_ONLY_V03.mcr instead.

' GNSS_Lband_Active_Array
' R0-CHARTS-RECON-PASSIVE - TOPOLOGY BUILD-ONLY V0.2
' CST Studio Suite 2022
'
' PURPOSE
'   Build the corrected Fig.2-consistent CHARTS topology:
'   one continuous square PEC proxy plate with eight disconnected slots
'   plus a reference ground plane.
'
' SCIENTIFIC STATUS
'   * RECONSTRUCTION HYPOTHESIS, NOT AN EXACT CHARTS REPLICA.
'   * Candidate C interprets 247.5 mm as board span, 227.5 mm as the
'     characteristic outer-slot frame span, and 40 mm as the retained
'     central solid/electronics region.
'   * Slot width and bridge dimensions are topology-only assumptions.
'
' HARD STOP
'   * BUILD ONLY.
'   * NO ports.
'   * NO solver, sweep, optimizer, mesh adaptation, monitor, or solve command.
'   * NO dielectric/substrate material claim.
'   * NO LNA, shield, Bias-Tee, or L-band scaling.
'
' EXPECTED FINAL INVENTORY
'   2 solids total:
'     ReferenceGround:GROUND_REFERENCE
'     Radiator:ANTENNA_PLATE
'
' TOPOLOGY INVARIANTS
'   * ANTENNA_PLATE remains one connected solid.
'   * 4 outer slots do not reach corners/edges.
'   * 4 inner slots do not reach center or outer slots.
'   * no central through-hole.
'
' REPLAY-SAFE STYLE
'   Flat Sub Main, native CST commands only.

Sub Main()

    ' ----------------------------
    ' Figure-derived / paper values
    ' ----------------------------
    StoreParameter "fig227", 227.5
    StoreParameter "fig247", 247.5
    StoreParameter "fig40", 40.0
    StoreParameter "height_ground", 200.0

    ' -------------------------------------
    ' Candidate C topology interpretation
    ' -------------------------------------
    StoreParameter "board_span", "fig247"
    StoreParameter "outer_slot_frame_span", "fig227"
    StoreParameter "center_solid_span", "fig40"

    ' --------------------------
    ' Topology-only placeholders
    ' --------------------------
    StoreParameter "slot_width", 8.0
    StoreParameter "outer_slot_corner_bridge", 30.0
    StoreParameter "inner_outer_bridge", 18.0
    StoreParameter "topology_t", 0.1
    StoreParameter "ground_span", 1000.0
    StoreParameter "ground_t", 1.0

    ' -------------------
    ' Derived coordinates
    ' -------------------
    StoreParameter "b", "board_span/2"
    StoreParameter "ofs", "outer_slot_frame_span/2"
    StoreParameter "cs", "center_solid_span/2"
    StoreParameter "sw", "slot_width"
    StoreParameter "ocb", "outer_slot_corner_bridge"
    StoreParameter "iob", "inner_outer_bridge"

    ' Outer perimeter slots sit on the square frame x/y = +/-ofs.
    StoreParameter "outer_slot_half_len", "ofs-ocb"

    ' Inner slots begin outside retained center and stop before outer slot family.
    StoreParameter "inner_start", "cs"
    StoreParameter "inner_stop", "ofs-iob"

    ' -----
    ' Units
    ' -----
    With Units
        .Geometry "mm"
        .Frequency "GHz"
        .Time "ns"
        .Voltage "V"
    End With

    ' ----------------
    ' Reference ground
    ' ----------------
    With Brick
        .Reset
        .Name "GROUND_REFERENCE"
        .Component "ReferenceGround"
        .Material "PEC"
        .Xrange "-ground_span/2", "ground_span/2"
        .Yrange "-ground_span/2", "ground_span/2"
        .Zrange "-ground_t", "0"
        .Create
    End With

    ' ---------------------------------------------
    ' One continuous antenna/PCB silhouette proxy
    ' ---------------------------------------------
    With Brick
        .Reset
        .Name "ANTENNA_PLATE"
        .Component "Radiator"
        .Material "PEC"
        .Xrange "-b", "b"
        .Yrange "-b", "b"
        .Zrange "height_ground", "height_ground+topology_t"
        .Create
    End With

    ' --------------------------------
    ' Four outer disconnected slot cuts
    ' --------------------------------

    With Brick
        .Reset
        .Name "CUT_OUTER_N"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-outer_slot_half_len", "outer_slot_half_len"
        .Yrange "ofs-sw/2", "ofs+sw/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_N"

    With Brick
        .Reset
        .Name "CUT_OUTER_S"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-outer_slot_half_len", "outer_slot_half_len"
        .Yrange "-ofs-sw/2", "-ofs+sw/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_S"

    With Brick
        .Reset
        .Name "CUT_OUTER_E"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "ofs-sw/2", "ofs+sw/2"
        .Yrange "-outer_slot_half_len", "outer_slot_half_len"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_E"

    With Brick
        .Reset
        .Name "CUT_OUTER_W"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-ofs-sw/2", "-ofs+sw/2"
        .Yrange "-outer_slot_half_len", "outer_slot_half_len"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_W"

    ' --------------------------------
    ' Four inner disconnected slot cuts
    ' --------------------------------

    With Brick
        .Reset
        .Name "CUT_INNER_N"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-sw/2", "sw/2"
        .Yrange "inner_start", "inner_stop"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_N"

    With Brick
        .Reset
        .Name "CUT_INNER_S"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-sw/2", "sw/2"
        .Yrange "-inner_stop", "-inner_start"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_S"

    With Brick
        .Reset
        .Name "CUT_INNER_E"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "inner_start", "inner_stop"
        .Yrange "-sw/2", "sw/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_E"

    With Brick
        .Reset
        .Name "CUT_INNER_W"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-inner_stop", "-inner_start"
        .Yrange "-sw/2", "sw/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_W"

End Sub
