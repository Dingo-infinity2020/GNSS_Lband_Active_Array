Option Explicit

' GNSS_Lband_Active_Array
' R1A2 CHARTS-inspired symmetric feed-reference overlay - BUILD ONLY V01
' SimulationOps stage: BUILD_ONLY_R1A1
'
' PURPOSE
'   Preserve the R1A1 scaled visible aperture and add a project-owned,
'   exact-rotation symmetric center-feed REFERENCE overlay.
'
' HARD STOP
'   BUILD ONLY. NO ports. NO solver. NO monitors. NO optimizer.
'   NO substrate/material claim. NO physical port. NO LNA. NO tuning.
'   Feed-reference solids are non-physical overlays and are not subtracted.
'
' EXPECTED FINAL INVENTORY
'   10 solids:
'     2 R1A1 base solids
'     4 exact-rotation FeedGapReference solids
'     4 exact-rotation TerminalReference solids
'
' SCIENTIFIC NOTE
'   This is a project-owned CHARTS-inspired derivative.
'   It is not claimed to be an exact CHARTS antenna.

Sub Main()

    ' -------- provenance / source-scale values --------
    StoreParameter "scale_factor", 0.285714285714
    StoreParameter "src_board_span", 247.5
    StoreParameter "src_outer_slot_frame_span", 227.5
    StoreParameter "src_outer_slot_width", 5.0
    StoreParameter "src_outer_mid_bridge", 18.0
    StoreParameter "src_outer_slot_segment_length", 94.125
    StoreParameter "src_inner_slot_width", 9.0
    StoreParameter "src_inner_slot_length", 73.0
    StoreParameter "src_inner_center_clear_span", 60.0
    StoreParameter "src_height_ground", 200.0
    StoreParameter "src_fig40_unresolved", 40.0

    ' -------- scaled R1A1 geometry --------
    StoreParameter "board_span", "src_board_span*scale_factor"
    StoreParameter "outer_slot_frame_span", "src_outer_slot_frame_span*scale_factor"
    StoreParameter "outer_slot_axis_offset", "outer_slot_frame_span/2"
    StoreParameter "outer_slot_width", "src_outer_slot_width*scale_factor"
    StoreParameter "outer_mid_bridge", "src_outer_mid_bridge*scale_factor"
    StoreParameter "outer_slot_segment_length", "src_outer_slot_segment_length*scale_factor"
    StoreParameter "inner_slot_width", "src_inner_slot_width*scale_factor"
    StoreParameter "inner_slot_length", "src_inner_slot_length*scale_factor"
    StoreParameter "inner_center_clear_span", "src_inner_center_clear_span*scale_factor"
    StoreParameter "inner_slot_start_radius", "inner_center_clear_span/2"
    StoreParameter "inner_slot_end_radius", "inner_slot_start_radius+inner_slot_length"
    StoreParameter "height_ground", "src_height_ground*scale_factor"
    StoreParameter "scaled_fig40_unused", "src_fig40_unresolved*scale_factor"

    ' -------- project build-only baseline --------
    StoreParameter "unit_cell_pitch_nominal", 94.0
    StoreParameter "ground_reference_span", "unit_cell_pitch_nominal"
    StoreParameter "topology_proxy_t", 0.10
    StoreParameter "ground_t", 0.50
    StoreParameter "eps", 0.01

    ' -------- R1A2 project-owned feed-reference geometry --------
    StoreParameter "feed_gap_center_width", 1.20
    StoreParameter "feed_gap_outer_width", "inner_slot_width"
    StoreParameter "feed_gap_join_radius", "inner_slot_start_radius"
    StoreParameter "terminal_r", 3.00
    StoreParameter "terminal_len", 2.00
    StoreParameter "terminal_w", 1.60
    StoreParameter "reference_t", 0.05
    StoreParameter "gap_reference_z", "height_ground+topology_proxy_t+0.50"
    StoreParameter "terminal_reference_z", "height_ground+topology_proxy_t+1.00"
    StoreParameter "s2", 0.7071067811865476
    StoreParameter "terminal_rmin", "terminal_r-terminal_len/2"
    StoreParameter "terminal_rmax", "terminal_r+terminal_len/2"
    StoreParameter "terminal_hw", "terminal_w/2"

    ' -------- derived coordinates --------
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

    With Units
        .Geometry "mm"
        .Frequency "GHz"
        .Time "ns"
        .Voltage "V"
    End With

    ' -------- nominal unit-cell ground reference --------
    With Brick
        .Reset
        .Name "UNITCELL_GROUND_REFERENCE"
        .Component "UnitCellGround"
        .Material "PEC"
        .Xrange "-ground_reference_span/2", "ground_reference_span/2"
        .Yrange "-ground_reference_span/2", "ground_reference_span/2"
        .Zrange "-ground_t", "0"
        .Create
    End With

    ' -------- one continuous antenna plate proxy --------
    With Brick
        .Reset
        .Name "ANTENNA_PLATE"
        .Component "Radiator"
        .Material "PEC"
        .Xrange "-b", "b"
        .Yrange "-b", "b"
        .Zrange "height_ground", "height_ground+topology_proxy_t"
        .Create
    End With

    ' -------- 8 outer disconnected slot segments --------
    With Brick
        .Reset
        .Name "CUT_OUTER_N_L"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "outer_left_x1", "outer_left_x2"
        .Yrange "ofs-ows/2", "ofs+ows/2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_N_L"

    With Brick
        .Reset
        .Name "CUT_OUTER_N_R"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "outer_right_x1", "outer_right_x2"
        .Yrange "ofs-ows/2", "ofs+ows/2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_N_R"

    With Brick
        .Reset
        .Name "CUT_OUTER_S_L"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "outer_left_x1", "outer_left_x2"
        .Yrange "-ofs-ows/2", "-ofs+ows/2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_S_L"

    With Brick
        .Reset
        .Name "CUT_OUTER_S_R"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "outer_right_x1", "outer_right_x2"
        .Yrange "-ofs-ows/2", "-ofs+ows/2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_S_R"

    With Brick
        .Reset
        .Name "CUT_OUTER_W_D"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-ofs-ows/2", "-ofs+ows/2"
        .Yrange "outer_left_x1", "outer_left_x2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_W_D"

    With Brick
        .Reset
        .Name "CUT_OUTER_W_U"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-ofs-ows/2", "-ofs+ows/2"
        .Yrange "outer_right_x1", "outer_right_x2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_W_U"

    With Brick
        .Reset
        .Name "CUT_OUTER_E_D"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "ofs-ows/2", "ofs+ows/2"
        .Yrange "outer_left_x1", "outer_left_x2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_E_D"

    With Brick
        .Reset
        .Name "CUT_OUTER_E_U"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "ofs-ows/2", "ofs+ows/2"
        .Yrange "outer_right_x1", "outer_right_x2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_OUTER_E_U"

    ' -------- 4 inner disconnected radial slots --------
    With Brick
        .Reset
        .Name "CUT_INNER_N"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-iws/2", "iws/2"
        .Yrange "isr", "ier"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_N"

    With Brick
        .Reset
        .Name "CUT_INNER_S"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-iws/2", "iws/2"
        .Yrange "-ier", "-isr"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_S"

    With Brick
        .Reset
        .Name "CUT_INNER_E"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "isr", "ier"
        .Yrange "-iws/2", "iws/2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_E"

    With Brick
        .Reset
        .Name "CUT_INNER_W"
        .Component "SlotTools"
        .Material "Vacuum"
        .Xrange "-ier", "-isr"
        .Yrange "-iws/2", "iws/2"
        .Zrange "height_ground-eps", "height_ground+topology_proxy_t+eps"
        .Create
    End With
    Solid.Subtract "Radiator:ANTENNA_PLATE", "SlotTools:CUT_INNER_W"


    ' ============================================================
    ' R1A2 FEED REFERENCE OVERLAY
    ' These solids are visual/reference geometry only.
    ' They are NOT ports and are NOT subtracted from ANTENNA_PLATE.
    ' One master geometry is authored; other quadrants are generated
    ' ONLY by exact 90-degree CST Transform rotations.
    ' ============================================================

    ' -------- canonical north center-gap reference --------
    With Extrude
        .Reset
        .Name "CENTER_GAP_MASTER_N"
        .Component "FeedGapReference"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "reference_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "gap_reference_z"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-feed_gap_center_width/2", "0.0"
        .LineTo "feed_gap_center_width/2", "0.0"
        .LineTo "feed_gap_outer_width/2", "feed_gap_join_radius"
        .LineTo "-feed_gap_outer_width/2", "feed_gap_join_radius"
        .LineTo "-feed_gap_center_width/2", "0.0"
        .Create
    End With

    ' Generate E/S/W gap references only by exact 90-degree rotation copies.
    With Transform
        .Reset
        .Name "FeedGapReference:CENTER_GAP_MASTER_N"
        .Origin "Free"
        .Center "0.0", "0.0", "gap_reference_z"
        .Angle "0.0", "0.0", "90.0"
        .MultipleObjects "True"
        .GroupObjects "False"
        .Repetitions "3"
        .MultipleSelection "False"
        .AutoDestination "True"
        .Transform "Shape", "Rotate"
    End With

    ' -------- canonical NE terminal contact-reference region --------
    ' Local radial axis is +45 deg. Tangential axis is +135 deg.
    With Extrude
        .Reset
        .Name "TERMINAL_MASTER_NE"
        .Component "TerminalReference"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "reference_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "terminal_reference_z"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "(terminal_rmin+terminal_hw)*s2", "(terminal_rmin-terminal_hw)*s2"
        .LineTo "(terminal_rmin-terminal_hw)*s2", "(terminal_rmin+terminal_hw)*s2"
        .LineTo "(terminal_rmax-terminal_hw)*s2", "(terminal_rmax+terminal_hw)*s2"
        .LineTo "(terminal_rmax+terminal_hw)*s2", "(terminal_rmax-terminal_hw)*s2"
        .LineTo "(terminal_rmin+terminal_hw)*s2", "(terminal_rmin-terminal_hw)*s2"
        .Create
    End With

    ' Generate NW/SW/SE terminal references only by exact 90-degree rotation copies.
    With Transform
        .Reset
        .Name "TerminalReference:TERMINAL_MASTER_NE"
        .Origin "Free"
        .Center "0.0", "0.0", "terminal_reference_z"
        .Angle "0.0", "0.0", "90.0"
        .MultipleObjects "True"
        .GroupObjects "False"
        .Repetitions "3"
        .MultipleSelection "False"
        .AutoDestination "True"
        .Transform "Shape", "Rotate"
    End With

End Sub
