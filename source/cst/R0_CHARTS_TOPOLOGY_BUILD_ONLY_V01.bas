Option Explicit

' DEPRECATED SCIENTIFIC TOPOLOGY - DO NOT USE FOR NEW BUILDS
' V0.1 executed/reopened successfully, but Fig.2 review showed the topology is wrong.
' Use R0_CHARTS_SLOTTED_PLATE_BUILD_ONLY_V02.mcr instead.

' GNSS_Lband_Active_Array
' R0-CHARTS-RECON-PASSIVE — TOPOLOGY BUILD-ONLY V0.1
' CST Studio Suite 2022
'
' PURPOSE
'   Build a schematic, parameterized CHARTS-like four-petal + square-ring
'   topology for human visual review.
'
' SCIENTIFIC STATUS
'   * RECONSTRUCTION HYPOTHESIS, NOT AN EXACT CHARTS REPLICA.
'   * 227.5 / 247.5 / 40 mm are figure-derived, unverified labels.
'   * Candidate A is selected by candidate_swap=0.
'   * candidate_swap=1 swaps the two large figure-derived dimensions.
'   * petal_slit, ring_trace_width, ground span and conductor thickness are
'     topology-only assumptions/placeholders.
'
' HARD STOP
'   * BUILD ONLY.
'   * NO ports.
'   * NO solver, sweep, optimizer, mesh adaptation, monitor, or solve command.
'   * NO dielectric/substrate material claim.
'   * Run only as a CST Structure Macro in a fresh already-open MWS project.
'
' REPLAY-SAFE STYLE
'   Flat Sub Main, native CST commands only, following the proven RA_Lband_LNA
'   Structure Macro discipline.

Sub Main()

    ' ------------------------------------------
    ' Figure-derived labels and candidate mapping
    ' ------------------------------------------
    StoreParameter "fig227", 227.5
    StoreParameter "fig247", 247.5
    StoreParameter "center_opening", 40.0

    ' 0 = Candidate A: petal=227.5, ring=247.5
    ' 1 = Candidate B: petal=247.5, ring=227.5
    StoreParameter "candidate_swap", 0

    StoreParameter "petal_span", "fig227 + candidate_swap*(fig247-fig227)"
    StoreParameter "ring_span", "fig247 - candidate_swap*(fig247-fig227)"

    ' --------------------------
    ' Topology-only placeholders
    ' --------------------------
    StoreParameter "petal_slit", 5.0
    StoreParameter "diag_off", "0.70710678*petal_slit"
    StoreParameter "ring_trace_width", 5.0
    StoreParameter "height_ground", 200.0
    StoreParameter "ground_span", 1000.0
    StoreParameter "ground_t", 1.0
    StoreParameter "topology_t", 0.1

    StoreParameter "p", "petal_span/2"
    StoreParameter "c", "center_opening/2"
    StoreParameter "d", "diag_off"
    StoreParameter "r", "ring_span/2"
    StoreParameter "rw", "ring_trace_width"

    ' -----
    ' Units
    ' -----
    With Units
        .Geometry "mm"
        .Frequency "GHz"
        .Time "ns"
        .Voltage "V"
    End With

    ' ---------------------------------
    ' Visualization/reference ground PEC
    ' ---------------------------------
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

    ' --------------------------------------------
    ' Four-petal schematic conductor family
    ' Diagonal gaps are controlled by d=slit/sqrt2
    ' --------------------------------------------

    ' North petal
    With Extrude
        .Reset
        .Name "PETAL_N"
        .Component "Radiator"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "topology_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "height_ground"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-p+d", "p"
        .LineTo "p-d", "p"
        .LineTo "c-d", "c"
        .LineTo "-c+d", "c"
        .LineTo "-p+d", "p"
        .Create
    End With

    ' East petal
    With Extrude
        .Reset
        .Name "PETAL_E"
        .Component "Radiator"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "topology_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "height_ground"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "p", "-p+d"
        .LineTo "p", "p-d"
        .LineTo "c", "c-d"
        .LineTo "c", "-c+d"
        .LineTo "p", "-p+d"
        .Create
    End With

    ' South petal
    With Extrude
        .Reset
        .Name "PETAL_S"
        .Component "Radiator"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "topology_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "height_ground"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-p+d", "-p"
        .LineTo "-c+d", "-c"
        .LineTo "c-d", "-c"
        .LineTo "p-d", "-p"
        .LineTo "-p+d", "-p"
        .Create
    End With

    ' West petal
    With Extrude
        .Reset
        .Name "PETAL_W"
        .Component "Radiator"
        .Material "PEC"
        .Mode "Pointlist"
        .Height "topology_t"
        .Twist "0.0"
        .Taper "0.0"
        .Origin "0.0", "0.0", "height_ground"
        .Uvector "1.0", "0.0", "0.0"
        .Vvector "0.0", "1.0", "0.0"
        .Point "-p", "-p+d"
        .LineTo "-c", "-c+d"
        .LineTo "-c", "c-d"
        .LineTo "-p", "p-d"
        .LineTo "-p", "-p+d"
        .Create
    End With

    ' -----------------------------------------
    ' Surrounding passive square ring — 4 bars
    ' Kept as separate solids for build auditing
    ' -----------------------------------------
    With Brick
        .Reset
        .Name "RING_N"
        .Component "PassiveRing"
        .Material "PEC"
        .Xrange "-r", "r"
        .Yrange "r-rw", "r"
        .Zrange "height_ground", "height_ground+topology_t"
        .Create
    End With

    With Brick
        .Reset
        .Name "RING_S"
        .Component "PassiveRing"
        .Material "PEC"
        .Xrange "-r", "r"
        .Yrange "-r", "-r+rw"
        .Zrange "height_ground", "height_ground+topology_t"
        .Create
    End With

    With Brick
        .Reset
        .Name "RING_E"
        .Component "PassiveRing"
        .Material "PEC"
        .Xrange "r-rw", "r"
        .Yrange "-r+rw", "r-rw"
        .Zrange "height_ground", "height_ground+topology_t"
        .Create
    End With

    With Brick
        .Reset
        .Name "RING_W"
        .Component "PassiveRing"
        .Material "PEC"
        .Xrange "-r", "-r+rw"
        .Yrange "-r+rw", "r-rw"
        .Zrange "height_ground", "height_ground+topology_t"
        .Create
    End With

End Sub
