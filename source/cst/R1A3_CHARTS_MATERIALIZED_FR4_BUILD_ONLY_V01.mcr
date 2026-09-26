Option Explicit

' GNSS_Lband_Active_Array
' R1A3 CHARTS-inspired materialized FR4 aperture - BUILD ONLY V01
' SimulationOps protocol 0.2.4
'
' PURPOSE
'   Materialize the accepted R1A1/R1A2 topology as a PCB-style structure:
'   one mechanically connected FR4 board, 35 um top conductor, 12 through-slots,
'   project-owned exact-rotation center cross copper isolation, and a continuous
'   square-ring copper isolation gap.
'
' HARD STOP
'   BUILD ONLY. NO ports. NO solver. NO monitors. NO optimizer. NO LNA.
'   No CST251 staging. Terminal reference coordinates remain design metadata only.
'
' SCIENTIFIC NOTE
'   This is a project-owned CHARTS-inspired GNSS derivative, not an exact CHARTS replica.
'   FR4 is a cost/materialization baseline only, not a selected final laminate.

Sub Main()

    Dim i As Integer
    Dim p As Integer
    Dim target As String
    Dim toolComponent As String
    Dim toolName As String
    Dim z1 As String
    Dim z2 As String
    Dim slotName(11) As String
    Dim sx1(11) As String
    Dim sx2(11) As String
    Dim sy1(11) As String
    Dim sy2(11) As String

    ' -------- provenance / frozen scale --------
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

    ' -------- scaled visible geometry --------
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

    ' -------- R1A3 materialization baseline --------
    StoreParameter "unit_cell_pitch_nominal", 94.0
    StoreParameter "ground_reference_span", "unit_cell_pitch_nominal"
    StoreParameter "ground_t", 0.50
    StoreParameter "substrate_t", 1.00
    StoreParameter "copper_t", 0.035
    StoreParameter "fr4_er", 4.2
    StoreParameter "fr4_tand", 0.018
    StoreParameter "eps", 0.01
    StoreParameter "substrate_bottom_z", "height_ground"
    StoreParameter "substrate_top_z", "height_ground+substrate_t"
    StoreParameter "copper_bottom_z", "substrate_top_z"
    StoreParameter "copper_top_z", "substrate_top_z+copper_t"
    StoreParameter "copper_mid_z", "(copper_bottom_z+copper_top_z)/2"

    ' -------- project-owned RF copper isolation --------
    StoreParameter "feed_gap_center_width", 1.20
    StoreParameter "feed_gap_outer_width", "inner_slot_width"
    StoreParameter "feed_gap_join_radius", "inner_slot_start_radius"
    StoreParameter "ring_gap_center_halfspan", "outer_slot_axis_offset"
    StoreParameter "ring_gap_width", "outer_slot_width"
    StoreParameter "ring_inner_edge", "ring_gap_center_halfspan-ring_gap_width/2"
    StoreParameter "ring_outer_edge", "ring_gap_center_halfspan+ring_gap_width/2"

    ' -------- terminal metadata retained, no terminal solids in R1A3 --------
    StoreParameter "terminal_r", 3.00
    StoreParameter "terminal_len", 2.00
    StoreParameter "terminal_w", 1.60

    ' -------- compact coordinate aliases --------
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

    ' -------- material: project-owned low-cost FR4 baseline --------
    With Material
        .Reset
        .Name "FR4_COST_BASELINE"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "fr4_er"
        .Mue "1.0"
        .TanD "fr4_tand"
        .TanDFreq "0.0"
        .TanDGiven "False"
        .TanDModel "ConstTanD"
        .Colour "0.75", "0.85", "0.65"
        .Create
    End With

    ' -------- ground reference --------
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

    ' -------- mechanically continuous substrate --------
    With Brick
        .Reset
        .Name "FR4_BOARD"
        .Component "Substrate"
        .Material "FR4_COST_BASELINE"
        .Xrange "-b", "b"
        .Yrange "-b", "b"
        .Zrange "substrate_bottom_z", "substrate_top_z"
        .Create
    End With

    ' -------- physical top conductor geometry; PEC only at build-only gate --------
    With Brick
        .Reset
        .Name "TOP_COPPER"
        .Component "TopCopper"
        .Material "PEC"
        .Xrange "-b", "b"
        .Yrange "-b", "b"
        .Zrange "copper_bottom_z", "copper_top_z"
        .Create
    End With

    ' -------- 12 accepted disconnected through-slot coordinates --------
    slotName(0)="OUTER_N_L": sx1(0)="outer_left_x1": sx2(0)="outer_left_x2": sy1(0)="ofs-ows/2": sy2(0)="ofs+ows/2"
    slotName(1)="OUTER_N_R": sx1(1)="outer_right_x1": sx2(1)="outer_right_x2": sy1(1)="ofs-ows/2": sy2(1)="ofs+ows/2"
    slotName(2)="OUTER_S_L": sx1(2)="outer_left_x1": sx2(2)="outer_left_x2": sy1(2)="-ofs-ows/2": sy2(2)="-ofs+ows/2"
    slotName(3)="OUTER_S_R": sx1(3)="outer_right_x1": sx2(3)="outer_right_x2": sy1(3)="-ofs-ows/2": sy2(3)="-ofs+ows/2"
    slotName(4)="OUTER_W_D": sx1(4)="-ofs-ows/2": sx2(4)="-ofs+ows/2": sy1(4)="outer_left_x1": sy2(4)="outer_left_x2"
    slotName(5)="OUTER_W_U": sx1(5)="-ofs-ows/2": sx2(5)="-ofs+ows/2": sy1(5)="outer_right_x1": sy2(5)="outer_right_x2"
    slotName(6)="OUTER_E_D": sx1(6)="ofs-ows/2": sx2(6)="ofs+ows/2": sy1(6)="outer_left_x1": sy2(6)="outer_left_x2"
    slotName(7)="OUTER_E_U": sx1(7)="ofs-ows/2": sx2(7)="ofs+ows/2": sy1(7)="outer_right_x1": sy2(7)="outer_right_x2"
    slotName(8)="INNER_N": sx1(8)="-iws/2": sx2(8)="iws/2": sy1(8)="isr": sy2(8)="ier"
    slotName(9)="INNER_S": sx1(9)="-iws/2": sx2(9)="iws/2": sy1(9)="-ier": sy2(9)="-isr"
    slotName(10)="INNER_E": sx1(10)="isr": sx2(10)="ier": sy1(10)="-iws/2": sy2(10)="iws/2"
    slotName(11)="INNER_W": sx1(11)="-ier": sx2(11)="-isr": sy1(11)="-iws/2": sy2(11)="iws/2"

    ' Apply identical 12 through-slots to substrate and top copper.
    For p=0 To 1
        If p=0 Then
            target="Substrate:FR4_BOARD"
            toolComponent="SubstrateSlotTools"
            z1="substrate_bottom_z-eps"
            z2="substrate_top_z+eps"
        Else
            target="TopCopper:TOP_COPPER"
            toolComponent="CopperSlotTools"
            z1="copper_bottom_z-eps"
            z2="copper_top_z+eps"
        End If

        For i=0 To 11
            toolName=IIf(p=0,"SUB_","CU_") & slotName(i)
            With Brick
                .Reset
                .Name toolName
                .Component toolComponent
                .Material "Vacuum"
                .Xrange sx1(i), sx2(i)
                .Yrange sy1(i), sy2(i)
                .Zrange z1, z2
                .Create
            End With
            Solid.Subtract target, toolComponent & ":" & toolName
        Next i
    Next p

    ' ============================================================
    ' PROJECT-OWNED COPPER-ONLY CENTER CROSS ISOLATION
    ' One north master, three exact 90-degree rotation copies.
    ' Subtracted BEFORE the square ring so TOP_COPPER remains a stable target.
    ' ============================================================
    With Extrude
        .Reset
        .Name "CENTER_CROSS_MASTER_N"
        .Component "CopperGapTools"
        .Material "Vacuum"
        .Mode "Pointlist"
        .Height "copper_t+2*eps"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "copper_bottom_z-eps"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-feed_gap_center_width/2", "0.0"
        .LineTo "feed_gap_center_width/2", "0.0"
        .LineTo "feed_gap_outer_width/2", "feed_gap_join_radius"
        .LineTo "feed_gap_outer_width/2", "ring_inner_edge"
        .LineTo "-feed_gap_outer_width/2", "ring_inner_edge"
        .LineTo "-feed_gap_outer_width/2", "feed_gap_join_radius"
        .LineTo "-feed_gap_center_width/2", "0.0"
        .Create
    End With

    With Transform
        .Reset
        .Name "CopperGapTools:CENTER_CROSS_MASTER_N"
        .Origin "Free"
        .Center "0.0", "0.0", "copper_mid_z"
        .Angle "0.0", "0.0", "90.0"
        .MultipleObjects "True"
        .GroupObjects "False"
        .Repetitions "3"
        .MultipleSelection "False"
        .AutoDestination "True"
        .Transform "Shape", "Rotate"
    End With

    For i=0 To 3
        If i=0 Then
            toolName="CopperGapTools:CENTER_CROSS_MASTER_N"
        Else
            toolName="CopperGapTools:CENTER_CROSS_MASTER_N_" & CStr(i)
        End If
        Solid.Subtract "TopCopper:TOP_COPPER", toolName
    Next i

    ' ============================================================
    ' PROJECT-OWNED CONTINUOUS SQUARE-RING COPPER ISOLATION
    ' One north master, three exact 90-degree rotation copies.
    ' This is the final copper operation; it may split copper into RF islands.
    ' ============================================================
    With Brick
        .Reset
        .Name "RING_GAP_MASTER_N"
        .Component "CopperGapTools"
        .Material "Vacuum"
        .Xrange "-ring_outer_edge", "ring_outer_edge"
        .Yrange "ofs-ows/2", "ofs+ows/2"
        .Zrange "copper_bottom_z-eps", "copper_top_z+eps"
        .Create
    End With

    With Transform
        .Reset
        .Name "CopperGapTools:RING_GAP_MASTER_N"
        .Origin "Free"
        .Center "0.0", "0.0", "copper_mid_z"
        .Angle "0.0", "0.0", "90.0"
        .MultipleObjects "True"
        .GroupObjects "False"
        .Repetitions "3"
        .MultipleSelection "False"
        .AutoDestination "True"
        .Transform "Shape", "Rotate"
    End With

    For i=0 To 3
        If i=0 Then
            toolName="CopperGapTools:RING_GAP_MASTER_N"
        Else
            toolName="CopperGapTools:RING_GAP_MASTER_N_" & CStr(i)
        End If
        Solid.Subtract "TopCopper:TOP_COPPER", toolName
    Next i

End Sub
