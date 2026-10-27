Option Explicit

' GNSS_Lband_Active_Array
' R1A1 CHARTS-inspired scaled visible aperture - BUILD ONLY V01
' SimulationOps stage: BUILD_ONLY_R1A1
'
' PURPOSE
'   Scale only the accepted R0 V0.3 visible 12-slot topology from the
'   ~400 MHz CHARTS reference scale to a 1.40 GHz nominal-center baseline.
'
' HARD STOP
'   BUILD ONLY. NO ports. NO solver. NO monitors. NO optimizer.
'   NO substrate/material claim. NO feed. NO LNA. NO tuning.
'
' EXPECTED FINAL INVENTORY
'   2 solids:
'     UnitCellGround:UNITCELL_GROUND_REFERENCE
'     Radiator:ANTENNA_PLATE
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

End Sub
