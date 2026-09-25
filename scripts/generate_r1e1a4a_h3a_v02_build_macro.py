#!/usr/bin/env python3
from pathlib import Path
import math, json

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"execution/h3a_architecture_manifest_v01.json"
DST=ROOT/"source/cst/R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY_V02.mcr"
m=json.loads(MANIFEST.read_text(encoding="utf-8"))

def q(v):
    if isinstance(v,(int,float)): return f"{v:.12g}"
    return str(v)

def brick(name,comp,mat,x1,x2,y1,y2,z1,z2):
    return [
      "    With Brick","        .Reset",f'        .Name "{name}"',
      f'        .Component "{comp}"',f'        .Material "{mat}"',
      f'        .Xrange "{q(x1)}", "{q(x2)}"',
      f'        .Yrange "{q(y1)}", "{q(y2)}"',
      f'        .Zrange "{q(z1)}", "{q(z2)}"',
      "        .Create","    End With",""
    ]

def extrude_poly(name,comp,mat,pts,z0,h):
    out=["    With Extrude","        .Reset",f'        .Name "{name}"',
         f'        .Component "{comp}"',f'        .Material "{mat}"',
         '        .Mode "Pointlist"',f'        .Height "{q(h)}"',
         '        .Twist "0.0"','        .Taper "0.0"',
         f'        .Origin "0.0", "0.0", "{q(z0)}"',
         '        .Uvector "1.0", "0.0", "0.0"',
         '        .Vvector "0.0", "1.0", "0.0"']
    x0,y0=pts[0]; out.append(f'        .Point "{q(x0)}", "{q(y0)}"')
    for x,y in pts[1:]:
        out.append(f'        .LineTo "{q(x)}", "{q(y)}"')
    out += ["        .Create","    End With",""]
    return out

def route_rect(p0,p1,width):
    x0,y0=p0; x1,y1=p1
    dx=x1-x0; dy=y1-y0; L=math.hypot(dx,dy)
    nx=-dy/L*width/2; ny=dx/L*width/2
    return [(x0+nx,y0+ny),(x1+nx,y1+ny),(x1-nx,y1-ny),(x0-nx,y0-ny),(x0+nx,y0+ny)]

lines=["Option Explicit","","' H3A Orthogonal PCB Feed-Stalk / Support Assembly V0.2 — FR4 BRIDGED MORTISE — BUILD ONLY",
"' Parent: immutable R1E1A1 P094 bare radiator.",
"' SimulationOps >=0.2.5. NO solver, NO RF port, NO active transistor.","","Sub Main()",""]
# Frozen coordinates / dimensions.
z_bp0,z_bp1=-0.5,0.0
z_rad0,z_rad1=57.1428571428,58.1428571428
z_cu0,z_cu1=58.1428571428,58.1778571428
stalk_t=1.0; stalk_h=57.1428571428; stalk_half=15.0
notch_half=8.5; notch_bottom=50.1428571428
slot_w=1.25; half_slot=slot_w/2
mid=25.0714285714
tenon_centers=(-12.0,12.0); tenon_len=3.0
mortise_len=3.30; mortise_w=1.25
rf_centers=(-9.4,9.4)
eps=0.02
cu=0.035

# Key build parameters retained inside CST.
params={
"h3a_stalk_t":stalk_t,"h3a_stalk_halfwidth":stalk_half,
"h3a_notch_half":notch_half,"h3a_notch_bottom_z":notch_bottom,
"h3a_interlock_slot_w":slot_w,"h3a_interlock_mid_z":mid,
"h3a_tenon_abs":12.0,"h3a_tenon_len":tenon_len,
"h3a_mortise_len":mortise_len,"h3a_mortise_w":mortise_w,
"h3a_rf_transition_abs":9.4,"h3a_cavity_span":17.0,
"h3a_shield_outer_half":8.0,"h3a_shield_depth":5.5,
"h3a_route_env_w":0.7,"h3a_service_zone_w":6.0,"h3a_service_zone_h":8.0,
"h3a_v02_bridge_len":5.50,"h3a_v02_bridge_width":2.571428571426,
}
for k,v in params.items():
    lines.append(f'    StoreParameter "{k}", {q(v)}')
lines.append("")

# Enable CST electromagnetic auto-intersection checking during build, then remove parent port.
lines += ['    With Solid','        .SetAutoIntersectionCheckElMag "True"','        .SetAutoIntersectionCheckThermal "False"','        .SetAutoIntersectionCheckMechanics "False"','    End With',""]
lines += ['    On Error Resume Next','    Port.Delete (1)','    On Error GoTo 0',""]

# Visual-surrogate materials used only for assembly review.
for name,er,tand,r,g,b in [
 ("H3A_LNA_VISUAL_SURROGATE",4.0,0.02,0.85,0.45,0.25),
 ("H3A_ROUTE_VISUAL_SURROGATE",1.05,0.001,0.25,0.75,0.95),
 ("H3A_SERVICE_VISUAL_SURROGATE",2.5,0.01,0.70,0.70,0.85),
]:
    lines += [
      "    With Material","        .Reset",f'        .Name "{name}"',
      '        .Folder ""','        .FrqType "all"','        .Type "Normal"',
      '        .SetMaterialUnit "GHz", "mm"',f'        .Epsilon "{q(er)}"',
      '        .Mue "1.0"',f'        .TanD "{q(tand)}"','        .TanDFreq "0.0"',
      '        .TanDGiven "False"','        .TanDModel "ConstTanD"',
      f'        .Colour "{q(r)}", "{q(g)}", "{q(b)}"',"        .Create","    End With",""
    ]
# V0.2: locally restore radiator FR4 inside the parent INNER_N/S/E/W slots.
# Top copper remains untouched. Each bridge is united into the parent substrate
# before the true tenon mortise is cut.
bridge_len=5.50
inner_slot_width=2.571428571426
for axis in ("X","Y"):
    for sgn,label in [(-1,"N"),(1,"P")]:
        c=sgn*12.0
        if axis=="X":
            x1,x2=c-bridge_len/2,c+bridge_len/2
            y1,y2=-inner_slot_width/2,inner_slot_width/2
        else:
            x1,x2=-inner_slot_width/2,inner_slot_width/2
            y1,y2=c-bridge_len/2,c+bridge_len/2
        nm=f"FR4_BRIDGE_{axis}_{label}"
        lines += brick(nm,"H3A_RadiatorBridge","FR4_COST_BASELINE",
                       x1,x2,y1,y2,z_rad0,z_rad1)
        lines += [f'    Solid.Add "Substrate:FR4_BOARD", "H3A_RadiatorBridge:{nm}"',""]

# Radiator FR4 mortises and backplane mortises.
for axis in ("X","Y"):
    for sgn,label in [(-1,"N"),(1,"P")]:
        c=sgn*12.0
        if axis=="X":
            x1,x2=c-mortise_len/2,c+mortise_len/2
            y1,y2=-mortise_w/2,mortise_w/2
        else:
            x1,x2=-mortise_w/2,mortise_w/2
            y1,y2=c-mortise_len/2,c+mortise_len/2
        tool=f"CUT_RAD_{axis}_{label}"
        lines += brick(tool,"H3A_Tools","Vacuum",x1,x2,y1,y2,z_rad0-eps,z_rad1+eps)
        lines += [f'    Solid.Subtract "Substrate:FR4_BOARD", "H3A_Tools:{tool}"',""]

        tool=f"CUT_BP_{axis}_{label}"
        lines += brick(tool,"H3A_Tools","Vacuum",x1,x2,y1,y2,z_bp0-eps,z_bp1+eps)
        lines += [f'    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H3A_Tools:{tool}"',""]

# X stalk body with top U-notch and lower half-depth center slot.
lines += brick("X_STALK_BODY","H3A_Stalk","FR4_COST_BASELINE",
               -stalk_half,stalk_half,-stalk_t/2,stalk_t/2,0.0,stalk_h)
lines += brick("CUT_X_TOP_NOTCH","H3A_Tools","Vacuum",
               -notch_half,notch_half,-stalk_t,stalk_t,notch_bottom,stalk_h+eps)
lines += ['    Solid.Subtract "H3A_Stalk:X_STALK_BODY", "H3A_Tools:CUT_X_TOP_NOTCH"',""]

lines += brick("CUT_X_INTERLOCK","H3A_Tools","Vacuum",
               -half_slot,half_slot,-stalk_t,stalk_t,-eps,mid)
lines += ['    Solid.Subtract "H3A_Stalk:X_STALK_BODY", "H3A_Tools:CUT_X_INTERLOCK"',""]

# Y stalk body with top U-notch and upper half-depth center slot.
lines += brick("Y_STALK_BODY","H3A_Stalk","FR4_COST_BASELINE",
               -stalk_t/2,stalk_t/2,-stalk_half,stalk_half,0.0,stalk_h)
lines += brick("CUT_Y_TOP_NOTCH","H3A_Tools","Vacuum",
               -stalk_t,stalk_t,-notch_half,notch_half,notch_bottom,stalk_h+eps)
lines += ['    Solid.Subtract "H3A_Stalk:Y_STALK_BODY", "H3A_Tools:CUT_Y_TOP_NOTCH"',""]

lines += brick("CUT_Y_INTERLOCK","H3A_Tools","Vacuum",
               -stalk_t,stalk_t,-half_slot,half_slot,mid,notch_bottom+eps)
lines += ['    Solid.Subtract "H3A_Stalk:Y_STALK_BODY", "H3A_Tools:CUT_Y_INTERLOCK"',""]

# Top and bottom tenons.
for axis in ("X","Y"):
    for sgn,label in [(-1,"N"),(1,"P")]:
        c=sgn*12.0
        if axis=="X":
            x1,x2=c-tenon_len/2,c+tenon_len/2; y1,y2=-stalk_t/2,stalk_t/2
        else:
            x1,x2=-stalk_t/2,stalk_t/2; y1,y2=c-tenon_len/2,c+tenon_len/2
        lines += brick(f"{axis}_TOP_TENON_{label}","H3A_Stalk","FR4_COST_BASELINE",
                       x1,x2,y1,y2,z_rad0,z_rad1)
        lines += brick(f"{axis}_BOTTOM_TENON_{label}","H3A_Stalk","FR4_COST_BASELINE",
                       x1,x2,y1,y2,z_bp0,z_bp1)
# First-pass backside local-ground corner patches: 20x20 envelope, central 8x8 clear and axis egresses.
zg0=z_rad0-cu; zg1=z_rad0
for sx,sy,label in [(1,1,"NE"),(-1,1,"NW"),(-1,-1,"SW"),(1,-1,"SE")]:
    x1,x2=(4.0,10.0) if sx>0 else (-10.0,-4.0)
    y1,y2=(4.0,10.0) if sy>0 else (-10.0,-4.0)
    lines += brick("GROUND_"+label,"H3A_HubGround","PEC",x1,x2,y1,y2,zg0,zg1)

# Four dummy first-stage LNA package envelopes at radius 6.2 mm.
lna_xy=6.2/math.sqrt(2.0)
for sx,sy,label in [(1,1,"NE"),(-1,1,"NW"),(-1,-1,"SW"),(1,-1,"SE")]:
    cx=sx*lna_xy; cy=sy*lna_xy
    lines += brick("LNA_ENV_"+label,"H3A_LNAEnvelope","H3A_LNA_VISUAL_SURROGATE",
                   cx-1.0,cx+1.0,cy-1.0,cy+1.0,z_rad0-0.635,z_rad0-0.035)

# 16-mm shield envelope inside 17-mm stalk cavity; cardinal egress width = 4 mm.
sh=8.0; wt=0.40; gap=2.0
zsh_top=z_rad0-cu
zsh_bot=zsh_top-5.5
for side,idx,(x1,x2,y1,y2) in [
 ("N","L",(-sh,-gap,sh-wt,sh)),("N","R",(gap,sh,sh-wt,sh)),
 ("S","L",(-sh,-gap,-sh,-sh+wt)),("S","R",(gap,sh,-sh,-sh+wt)),
 ("E","B",(sh-wt,sh,-sh,-gap)),("E","T",(sh-wt,sh,gap,sh)),
 ("W","B",(-sh,-sh+wt,-sh,-gap)),("W","T",(-sh,-sh+wt,gap,sh)),
]:
    lines += brick(f"SHIELD_{side}_{idx}","H3A_Shield","PEC",x1,x2,y1,y2,zsh_bot,zsh_top)
lines += brick("SHIELD_LID","H3A_Shield","PEC",-sh,sh,-sh,sh,zsh_bot-0.30,zsh_bot)

# Post-LNA visual route envelopes. Start outside package and end before RF transition pad.
routes=[
 ("NE",( lna_xy, lna_xy),( 9.4,0.0)),
 ("SW",(-lna_xy,-lna_xy),(-9.4,0.0)),
 ("NW",(-lna_xy, lna_xy),(0.0, 9.4)),
 ("SE",( lna_xy,-lna_xy),(0.0,-9.4)),
]
for label,p0,p1 in routes:
    dx=p1[0]-p0[0]; dy=p1[1]-p0[1]; L=math.hypot(dx,dy)
    u=(dx/L,dy/L)
    a=(p0[0]+u[0]*1.65,p0[1]+u[1]*1.65)
    b=(p1[0]-u[0]*0.90,p1[1]-u[1]*0.90)
    lines += extrude_poly("ROUTE_ENV_"+label,"H3A_RouteEnvelope",
                          "H3A_ROUTE_VISUAL_SURROGATE",route_rect(a,b,0.70),
                          z_rad0-0.39,0.22)
# Dedicated top mechanical copper lands and solder-fillet envelopes.
for axis in ("X","Y"):
    for sgn,label in [(-1,"N"),(1,"P")]:
        c=sgn*12.0
        for side,ss in [("A",-1),("B",1)]:
            if axis=="X":
                # vertical stalk-face copper
                y1,y2=(-0.535,-0.5) if ss<0 else (0.5,0.535)
                lines += brick(f"{axis}_TOP_PAD_{label}_{side}","H3A_MechLand","PEC",
                               c-1.0,c+1.0,y1,y2,56.40,57.1078571428)
                # underside horizontal land outside mortise
                y1h,y2h=(-1.625,-0.625) if ss<0 else (0.625,1.625)
                lines += brick(f"{axis}_TOP_LAND_{label}_{side}","H3A_MechLand","PEC",
                               c-1.40,c+1.40,y1h,y2h,57.1078571428,z_rad0)
                # solder envelope touches both vertical pad and horizontal land
                y1s,y2s=(-1.0,-0.535) if ss<0 else (0.535,1.0)
                lines += brick(f"{axis}_TOP_SOLDER_{label}_{side}","H3A_MechSolder","PEC",
                               c-1.0,c+1.0,y1s,y2s,56.65,57.1078571428)
            else:
                x1,x2=(-0.535,-0.5) if ss<0 else (0.5,0.535)
                lines += brick(f"{axis}_TOP_PAD_{label}_{side}","H3A_MechLand","PEC",
                               x1,x2,c-1.0,c+1.0,56.40,57.1078571428)
                x1h,x2h=(-1.625,-0.625) if ss<0 else (0.625,1.625)
                lines += brick(f"{axis}_TOP_LAND_{label}_{side}","H3A_MechLand","PEC",
                               x1h,x2h,c-1.40,c+1.40,57.1078571428,z_rad0)
                x1s,x2s=(-1.0,-0.535) if ss<0 else (0.535,1.0)
                lines += brick(f"{axis}_TOP_SOLDER_{label}_{side}","H3A_MechSolder","PEC",
                               x1s,x2s,c-1.0,c+1.0,56.65,57.1078571428)

# Bottom mechanical copper/solder envelopes; route ground remains separated above z=5 mm.
for axis in ("X","Y"):
    for sgn,label in [(-1,"N"),(1,"P")]:
        c=sgn*12.0
        for side,ss in [("A",-1),("B",1)]:
            if axis=="X":
                y1,y2=(-0.535,-0.5) if ss<0 else (0.5,0.535)
                lines += brick(f"{axis}_BOT_PAD_{label}_{side}","H3A_MechLand","PEC",
                               c-1.0,c+1.0,y1,y2,0.0,0.70)
                y1s,y2s=(-0.90,-0.535) if ss<0 else (0.535,0.90)
                lines += brick(f"{axis}_BOT_SOLDER_{label}_{side}","H3A_MechSolder","PEC",
                               c-1.0,c+1.0,y1s,y2s,0.0,0.50)
            else:
                x1,x2=(-0.535,-0.5) if ss<0 else (0.5,0.535)
                lines += brick(f"{axis}_BOT_PAD_{label}_{side}","H3A_MechLand","PEC",
                               x1,x2,c-1.0,c+1.0,0.0,0.70)
                x1s,x2s=(-0.90,-0.535) if ss<0 else (0.535,0.90)
                lines += brick(f"{axis}_BOT_SOLDER_{label}_{side}","H3A_MechSolder","PEC",
                               x1s,x2s,c-1.0,c+1.0,0.0,0.50)
# Post-LNA RF transition copper proxies and vertical stalk GCPW-class route representatives.
for c,label in [(-9.4,"N"),(9.4,"P")]:
    # X-stalk on +Y face: signal and two ground rails.
    centers=[("G1",c-1.0,0.40),("SIG",c,0.60),("G2",c+1.0,0.40)]
    for kind,xc,wid in centers:
        lines += brick(f"X_RF_VPAD_{label}_{kind}","H3A_RFTransition","PEC",
                       xc-wid/2,xc+wid/2,0.5,0.535,56.40,57.0728571428)
        lines += brick(f"X_RF_HPAD_{label}_{kind}","H3A_RFTransition","PEC",
                       xc-wid/2,xc+wid/2,0.535,1.335,57.0728571428,57.1078571428)
        lines += brick(f"X_RF_SOLDER_{label}_{kind}","H3A_RFSolder","PEC",
                       xc-wid/2,xc+wid/2,0.535,0.95,56.78,57.0728571428)
        # representative vertical route copper, stops 5 mm above backplane
        lines += brick(f"X_ROUTE_{label}_{kind}","H3A_StalkRF","PEC",
                       xc-wid/2,xc+wid/2,0.5,0.535,5.0,56.40)

    # lower service volume, outside stalk face
    lines += brick(f"X_SERVICE_ENV_{label}","H3A_ServiceEnvelope","H3A_SERVICE_VISUAL_SURROGATE",
                   c-3.0,c+3.0,1.0,2.0,9.0,17.0)

for c,label in [(-9.4,"N"),(9.4,"P")]:
    # Y-stalk on -X face.
    centers=[("G1",c-1.0,0.40),("SIG",c,0.60),("G2",c+1.0,0.40)]
    for kind,yc,wid in centers:
        lines += brick(f"Y_RF_VPAD_{label}_{kind}","H3A_RFTransition","PEC",
                       -0.535,-0.5,yc-wid/2,yc+wid/2,56.40,57.0728571428)
        lines += brick(f"Y_RF_HPAD_{label}_{kind}","H3A_RFTransition","PEC",
                       -1.335,-0.535,yc-wid/2,yc+wid/2,57.0728571428,57.1078571428)
        lines += brick(f"Y_RF_SOLDER_{label}_{kind}","H3A_RFSolder","PEC",
                       -0.95,-0.535,yc-wid/2,yc+wid/2,56.78,57.0728571428)
        lines += brick(f"Y_ROUTE_{label}_{kind}","H3A_StalkRF","PEC",
                       -0.535,-0.5,yc-wid/2,yc+wid/2,5.0,56.40)

    lines += brick(f"Y_SERVICE_ENV_{label}","H3A_ServiceEnvelope","H3A_SERVICE_VISUAL_SURROGATE",
                   -2.0,-1.0,c-3.0,c+3.0,9.0,17.0)

lines += [
"",
"    ' H3A V0.2 intentionally creates no RF port and calls no solver.",
"End Sub",""
]
DST.parent.mkdir(parents=True,exist_ok=True)
DST.write_text("\n".join(lines),encoding="utf-8")
print("WROTE="+str(DST))
print("LINES="+str(len(lines)))
