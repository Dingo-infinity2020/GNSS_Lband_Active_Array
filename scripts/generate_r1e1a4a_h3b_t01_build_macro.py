#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DST=ROOT/"source/cst/R1E1A4A_H3B_T01_ORTHOGONAL_TRANSITION_BUILD_ONLY_V01.mcr"

def q(v):
    return f"{v:.12g}" if isinstance(v,(int,float)) else str(v)

def brick(name,comp,mat,x1,x2,y1,y2,z1,z2):
    return [
        "    With Brick","        .Reset",f'        .Name "{name}"',
        f'        .Component "{comp}"',f'        .Material "{mat}"',
        f'        .Xrange "{q(x1)}", "{q(x2)}"',
        f'        .Yrange "{q(y1)}", "{q(y2)}"',
        f'        .Zrange "{q(z1)}", "{q(z2)}"',
        "        .Create","    End With",""
    ]

def cyl(name,comp,mat,axis,r,c1,c2,xc,yc,zc,inner=0.0):
    lines=["    With Cylinder","        .Reset",f'        .Name "{name}"',
           f'        .Component "{comp}"',f'        .Material "{mat}"',
           f'        .OuterRadius "{q(r)}"',f'        .InnerRadius "{q(inner)}"',
           f'        .Axis "{axis}"']
    if axis=="z":
        lines += [f'        .Zrange "{q(c1)}", "{q(c2)}"',
                  f'        .Xcenter "{q(xc)}"',f'        .Ycenter "{q(yc)}"']
    elif axis=="y":
        lines += [f'        .Yrange "{q(c1)}", "{q(c2)}"',
                  f'        .Xcenter "{q(xc)}"',f'        .Zcenter "{q(zc)}"']
    else:
        raise ValueError(axis)
    lines += ['        .Segments "0"','        .Create',"    End With",""]
    return lines

W=1.8
G=0.30
WG=2.20
TP=0.035
PAD_SIG=2.20
PAD_G=2.40
PAD_GAP=0.25
BOARD_X=5.0
H_Y0,H_Y1=-4.0,16.0
V_Z0,V_Z1=-18.0,0.0
V_YH=0.5
H_LINE_Y0,H_LINE_Y1=1.5,14.5
V_LINE_Z0,V_LINE_Z1=-14.5,-1.2
RP1=12.0
RP2=-12.0

sig_h=(-W/2,W/2)
g1_h=(-(W/2+G+WG),-(W/2+G))
g2_h=((W/2+G),(W/2+G+WG))

pad_sig=(-PAD_SIG/2,PAD_SIG/2)
pad_g1=(-(PAD_SIG/2+PAD_GAP+PAD_G),-(PAD_SIG/2+PAD_GAP))
pad_g2=((PAD_SIG/2+PAD_GAP),(PAD_SIG/2+PAD_GAP+PAD_G))

lines=["Option Explicit","","' H3B-T01 Orthogonal PCB Post-LNA Transition Coupon V0.1 — BUILD ONLY",
"' Standalone coupon. No antenna, no active device, no solver, no RF ports.","","Sub Main()",""]
for k,v in {
    "h3b_t01_board_t":1.0,
    "h3b_t01_cu_t":TP,
    "h3b_t01_wsig":W,
    "h3b_t01_gap":G,
    "h3b_t01_wgnd":WG,
    "h3b_t01_pad_sig":PAD_SIG,
    "h3b_t01_pad_gap":PAD_GAP,
    "h3b_t01_pad_gnd":PAD_G,
    "h3b_t01_rp1_y":RP1,
    "h3b_t01_rp2_z":RP2,
    "h3b_t01_via_outer_r":0.20,
    "h3b_t01_via_inner_r":0.15,
    "h3b_t01_viahole_r":0.20,
    "h3b_t01_freq_lo":1.0,
    "h3b_t01_freq_hi":2.0,
    "h3b_t01_decision_lo":1.15,
    "h3b_t01_decision_hi":1.65,
}.items():
    lines.append(f'    StoreParameter "{k}", {q(v)}')
lines += ["","    With Solid",'        .SetAutoIntersectionCheckElMag "True"',
          '        .SetAutoIntersectionCheckThermal "False"',
          '        .SetAutoIntersectionCheckMechanics "False"',"    End With",""]

# FR4 material baseline.
lines += [
"    With Material","        .Reset",'        .Name "FR4_COST_BASELINE"',
'        .Folder ""','        .FrqType "all"','        .Type "Normal"',
'        .SetMaterialUnit "GHz", "mm"','        .Epsilon "4.3"',
'        .Mue "1.0"','        .TanD "0.02"','        .TanDFreq "1.5"',
'        .TanDGiven "True"','        .TanDModel "ConstTanD"','        .Create',"    End With",""
]

# Boards.
lines += brick("HORIZONTAL_FR4","H3B_Board","FR4_COST_BASELINE",-BOARD_X,BOARD_X,H_Y0,H_Y1,0.0,1.0)
lines += brick("VERTICAL_FR4","H3B_Board","FR4_COST_BASELINE",-BOARD_X,BOARD_X,-V_YH,V_YH,V_Z0,V_Z1)

# Same-side horizontal GSG on underside.
lines += brick("H_SIG","H3B_Line","PEC",sig_h[0],sig_h[1],H_LINE_Y0,H_LINE_Y1,-TP,0.0)
lines += brick("H_GND_L","H3B_Line","PEC",g1_h[0],g1_h[1],H_LINE_Y0,H_LINE_Y1,-TP,0.0)
lines += brick("H_GND_R","H3B_Line","PEC",g2_h[0],g2_h[1],H_LINE_Y0,H_LINE_Y1,-TP,0.0)
# Horizontal local backing plane.
lines += brick("H_BACK_GND","H3B_BackGround","PEC",-4.0,4.0,H_LINE_Y0,H_LINE_Y1,1.0,1.0+TP)

# Same-side vertical GSG on +Y face.
lines += brick("V_SIG","H3B_Line","PEC",sig_h[0],sig_h[1],V_YH,V_YH+TP,V_LINE_Z0,V_LINE_Z1)
lines += brick("V_GND_L","H3B_Line","PEC",g1_h[0],g1_h[1],V_YH,V_YH+TP,V_LINE_Z0,V_LINE_Z1)
lines += brick("V_GND_R","H3B_Line","PEC",g2_h[0],g2_h[1],V_YH,V_YH+TP,V_LINE_Z0,V_LINE_Z1)
# Vertical local backing plane.
lines += brick("V_BACK_GND","H3B_BackGround","PEC",-4.0,4.0,-V_YH-TP,-V_YH,V_LINE_Z0,V_LINE_Z1)

# Transition pads on horizontal underside.
for nm,(x1,x2) in [("SIG",pad_sig),("GND_L",pad_g1),("GND_R",pad_g2)]:
    lines += brick("H_PAD_"+nm,"H3B_Transition","PEC",x1,x2,0.5,1.5,-TP,0.0)

# Transition pads on vertical +Y face.
for nm,(x1,x2) in [("SIG",pad_sig),("GND_L",pad_g1),("GND_R",pad_g2)]:
    lines += brick("V_PAD_"+nm,"H3B_Transition","PEC",x1,x2,V_YH,V_YH+TP,-1.2,-TP)

# Plated/castellated top-edge caps.
for nm,(x1,x2) in [("SIG",pad_sig),("GND_L",pad_g1),("GND_R",pad_g2)]:
    lines += brick("EDGE_CAP_"+nm,"H3B_EdgeCap","PEC",x1,x2,-V_YH,V_YH,-TP,0.0)

# Explicit solder fillet envelopes.
for nm,(x1,x2) in [("SIG",pad_sig),("GND_L",pad_g1),("GND_R",pad_g2)]:
    lines += brick("SOLDER_"+nm,"H3B_Solder","PEC",x1,x2,V_YH+TP,1.0,-0.45,-TP)

# Via fences: holes through substrates, then PEC barrels.
for side,x in [("L",-2.3),("R",2.3)]:
    for idx,y in enumerate((3.0,6.0,9.0,12.0),1):
        tool=f"H_VIAHOLE_{side}_{idx}"
        lines += cyl(tool,"H3B_Tools","Vacuum","z",0.20,-0.02,1.02,x,y,0)
        lines += [f'    Solid.Subtract "H3B_Board:HORIZONTAL_FR4", "H3B_Tools:{tool}"',""]
        lines += cyl(f"H_VIA_{side}_{idx}","H3B_Via","PEC","z",0.20,0.0,1.0,x,y,0,inner=0.15)
    for idx,z in enumerate((-3.0,-6.0,-9.0,-12.0),1):
        tool=f"V_VIAHOLE_{side}_{idx}"
        lines += cyl(tool,"H3B_Tools","Vacuum","y",0.20,-0.52,0.52,x,0,z)
        lines += [f'    Solid.Subtract "H3B_Board:VERTICAL_FR4", "H3B_Tools:{tool}"',""]
        lines += cyl(f"V_VIA_{side}_{idx}","H3B_Via","PEC","y",0.20,-V_YH,V_YH,x,0,z,inner=0.15)

lines += ["","    ' H3B-T01 V0.1 intentionally creates no RF port and calls no solver.","End Sub",""]
DST.parent.mkdir(parents=True,exist_ok=True)
DST.write_text("\n".join(lines),encoding="utf-8")
print("WROTE="+str(DST))
print("LINES="+str(len(lines)))
