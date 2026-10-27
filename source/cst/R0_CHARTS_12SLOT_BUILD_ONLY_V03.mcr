Option Explicit

' GNSS_Lband_Active_Array
' R0-CHARTS-RECON-PASSIVE - TOPOLOGY BUILD-ONLY V0.3
' CST Studio Suite 2022
'
' PURPOSE
'   Build the Fig.2-refined CHARTS topology:
'   one continuous square PEC proxy plate with twelve disconnected slots
'   plus a reference ground plane.
'
' SCIENTIFIC STATUS
'   * RECONSTRUCTION HYPOTHESIS, NOT AN EXACT CHARTS REPLICA.
'   * 247.5 mm board span and 227.5 mm outer-slot frame span are
'     figure-derived interpretations.
'   * Outer/inner slot widths and lengths are photo-derived estimates.
'   * The Fig.1 40 mm label remains SEMANTICS_UNRESOLVED and is not used
'     to cut a center hole or force the inner-slot center spacing.
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
'   * 8 outer slot segments remain mutually disconnected.
'   * 4 inner radial slots remain mutually disconnected.
'   * no inner slot touches an outer slot.
'   * no central through-hole.
'
' REPLAY-SAFE STYLE
'   Flat Sub Main, native CST commands only.

Sub Main()

    ' ----------------------------
    ' Paper / figure-derived values
    ' ----------------------------
    StoreParameter "fig227", 227.5
    StoreParameter "fig247", 247.5
    StoreParameter "fig40_unresolved", 40.0
    StoreParameter "height_ground", 200.0

    ' -------------------------------------
    ' V0.3 photo-constrained reconstruction
    ' -------------------------------------
    StoreParameter "board_span", "fig247"
    StoreParameter "outer_slot_frame_span", "fig227"
    StoreParameter "outer_slot_axis_offset", "outer_slot_frame_span/2"

    StoreParameter "outer_slot_width", 5.0
    StoreParameter "outer_mid_bridge", 18.0
    StoreParameter "outer_slot_segment_length", 94.125

    StoreParameter "inner_slot_width", 9.0
    StoreParameter "inner_center_clear_span", 60.0
    StoreParameter "inner_slot_length", 73.0
    StoreParameter "inner_slot_start_radius", "inner_center_clear_span/2"
    StoreParameter "inner_slot_end_radius", "inner_slot_start_radius+inner_slot_length"

    ' --------------------------
    ' Topology-only placeholders
    ' --------------------------
    StoreParameter "topology_t", 0.1
    StoreParameter "ground_span", 1000.0
    StoreParameter "ground_t", 1.0

    ' -------------------
    ' Derived coordinates
    ' -------------------
    StoreParameter "b", "board_span/2"
    StoreParameter "ofs", "outer_slot_axis_offset"
    StoreParameter "ows", "outer_slot_width"
    StoreParameter "omb", "outer_mid_bridge"
    StoreParameter "osl", "outer_slot_segment_length"
    StoreParameter "iws", "inner_slot_width"
    StoreParameter "isr", "inner_slot_start_radius"
    StoreParameter "ier", "inner_slot_end_radius"

    StoreParameter "outer_left_x1", "-omb/2-osl"
    StoreParameter "outer_left_x2", "-omb/2"
    StoreParameter "outer_right_x1", "omb/2"
    StoreParameter "outer_right_x2", "omb/2+osl"

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

    ' -------------------------
    ' Continuous antenna plate
    ' -------------------------
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

    ' -------------------------------------------------
    ' OUTER SLOT FAMILY: 8 disconnected segments total
    ' Two segments per board side with a mid-side bridge
    ' -------------------------------------------------

    ' North-left
    With Brick
        .Reset
        .Name "CUT_OUTER_N_L"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "outer_left_x1", "outer_left_x2"
        .Yrange "ofs-ows/2", "ofs+ows/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_N_L"

    ' North-right
    With Brick
        .Reset
        .Name "CUT_OUTER_N_R"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "outer_right_x1", "outer_right_x2"
        .Yrange "ofs-ows/2", "ofs+ows/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_N_R"

    ' South-left
    With Brick
        .Reset
        .Name "CUT_OUTER_S_L"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "outer_left_x1", "outer_left_x2"
        .Yrange "-ofs-ows/2", "-ofs+ows/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_S_L"

    ' South-right
    With Brick
        .Reset
        .Name "CUT_OUTER_S_R"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "outer_right_x1", "outer_right_x2"
        .Yrange "-ofs-ows/2", "-ofs+ows/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_S_R"

    ' West-lower
    With Brick
        .Reset
        .Name "CUT_OUTER_W_D"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-ofs-ows/2", "-ofs+ows/2"
        .Yrange "outer_left_x1", "outer_left_x2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_W_D"

    ' West-upper
    With Brick
        .Reset
        .Name "CUT_OUTER_W_U"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-ofs-ows/2", "-ofs+ows/2"
        .Yrange "outer_right_x1", "outer_right_x2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_W_U"

    ' East-lower
    With Brick
        .Reset
        .Name "CUT_OUTER_E_D"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "ofs-ows/2", "ofs+ows/2"
        .Yrange "outer_left_x1", "outer_left_x2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_E_D"

    ' East-upper
    With Brick
        .Reset
        .Name "CUT_OUTER_E_U"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "ofs-ows/2", "ofs+ows/2"
        .Yrange "outer_right_x1", "outer_right_x2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_E_U"

    ' -----------------------------------------
    ' INNER SLOT FAMILY: 4 radial slots total
    ' -----------------------------------------

    ' North
    With Brick
        .Reset
        .Name "CUT_INNER_N"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-iws/2", "iws/2"
        .Yrange "isr", "ier"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_N"

    ' South
    With Brick
        .Reset
        .Name "CUT_INNER_S"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-iws/2", "iws/2"
        .Yrange "-ier", "-isr"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_S"

    ' East
    With Brick
        .Reset
        .Name "CUT_INNER_E"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "isr", "ier"
        .Yrange "-iws/2", "iws/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_E"

    ' West
    With Brick
        .Reset
        .Name "CUT_INNER_W"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-ier", "-isr"
        .Yrange "-iws/2", "iws/2"
        .Zrange "height_ground-0.01", "height_ground+topology_t+0.01"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_W"

End Sub
