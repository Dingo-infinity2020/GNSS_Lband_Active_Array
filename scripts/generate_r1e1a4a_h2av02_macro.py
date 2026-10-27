#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"source/cst/R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY_V01.mcr"
DST=ROOT/"source/cst/R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY_V01.mcr"

def brick(name,comp,mat,x1,x2,y1,y2,z1,z2):
    return [
      "    With Brick","        .Reset",f'        .Name "{name}"',
      f'        .Component "{comp}"',f'        .Material "{mat}"',
      f'        .Xrange "{x1}", "{x2}"',f'        .Yrange "{y1}", "{y2}"',
      f'        .Zrange "{z1}", "{z2}"',"        .Create","    End With",""
    ]

def center(sign,param):
    return param if sign>0 else "-"+param

def rng(c,half):
    return f"{c}-{half}",f"{c}+{half}"
src=SRC.read_text(encoding="utf-8")
marker="    ' Shield can: four walls plus lid, soldered to the backside ground frame."
if marker not in src:
    raise SystemExit("HOLD_H2AV02_V01_MARKER_MISSING")
prefix=src.split(marker,1)[0]
prefix=prefix.replace("H2A Universal Passive/Active Center Structure V0.1",
                      "H2A Universal Passive/Active Center Structure V0.2 SERVICE ARCHITECTURE")
prefix=prefix.replace("Mechanical/manufacturing review model; NO solver, transistor or optimization.",
                      "Service-routing build-only model; NO solver, transistor or optimization.")

lines=[prefix.rstrip(),"",
"    ' H2A V0.2 service architecture parameters.",
'    StoreParameter "h2av02_mhf_r", 9.0',
'    StoreParameter "h2av02_mhf_xy", "h2av02_mhf_r*h2a_s2"',
'    StoreParameter "h2av02_mhf_half", 1.20',
'    StoreParameter "h2av02_mhf_h", 1.20',
'    StoreParameter "h2av02_mhf_top_z", "h2a_backside_cu_bottom"',
'    StoreParameter "h2av02_mhf_bottom_z", "h2av02_mhf_top_z-h2av02_mhf_h"',
'    StoreParameter "h2av02_route_z", "(h2av02_mhf_top_z+h2av02_mhf_bottom_z)/2"',
'    StoreParameter "h2av02_output_r0", 7.20',
'    StoreParameter "h2av02_output_r1", 8.70',
'    StoreParameter "h2av02_output_halfw", 0.30',
]
lines += [
'    StoreParameter "h2av02_tube_r", 13.50',
'    StoreParameter "h2av02_tube_xy", "h2av02_tube_r*h2a_s2"',
'    StoreParameter "h2av02_tube_outer_half", 1.50',
'    StoreParameter "h2av02_tube_inner_half", 0.70',
'    StoreParameter "h2av02_spacer_half", 1.80',
'    StoreParameter "h2av02_spacer_t", 0.50',
'    StoreParameter "h2av02_feedthrough_half", 0.90',
'    StoreParameter "h2av02_tube_top_z", "h2a_backside_cu_bottom-h2av02_spacer_t"',
'    StoreParameter "h2av02_tube_bottom_z", "h2av02_spacer_t"',
'    StoreParameter "h2av02_cable_half", 0.405',
'    StoreParameter "h2av02_cable_r0", 9.0',
'    StoreParameter "h2av02_cable_r1", "h2av02_tube_r"',
'    StoreParameter "h2av02_shield_mid_half", 5.50',
'    StoreParameter "h2av02_mmcx_half", 2.50',
'    StoreParameter "h2av02_mmcx_bottom_z", -6.0',
'    StoreParameter "h2av02_mmcx_top_z", -0.5',
"",
"    With Material",
"        .Reset",
'        .Name "H2A_MICROCOAX_ENVELOPE_SURROGATE"',
'        .Folder ""',
'        .FrqType "all"',
'        .Type "Normal"',
'        .SetMaterialUnit "GHz", "mm"',
'        .Epsilon "2.1"',
'        .Mue "1.0"',
'        .TanD "0.001"',
'        .TanDFreq "0.0"',
'        .TanDGiven "False"',
'        .TanDModel "ConstTanD"',
"        .Create",
"    End With",""
]
# Corner-open shield walls; lid retained.
lines += brick("SHIELD_N","H2A_Shield","PEC",
               "-h2av02_shield_mid_half","h2av02_shield_mid_half",
               "h2a_shield_inner_half","h2a_shield_outer_half",
               "h2a_shield_bottom_z","h2a_shield_top_z")
lines += brick("SHIELD_S","H2A_Shield","PEC",
               "-h2av02_shield_mid_half","h2av02_shield_mid_half",
               "-h2a_shield_outer_half","-h2a_shield_inner_half",
               "h2a_shield_bottom_z","h2a_shield_top_z")
lines += brick("SHIELD_E","H2A_Shield","PEC",
               "h2a_shield_inner_half","h2a_shield_outer_half",
               "-h2av02_shield_mid_half","h2av02_shield_mid_half",
               "h2a_shield_bottom_z","h2a_shield_top_z")
lines += brick("SHIELD_W","H2A_Shield","PEC",
               "-h2a_shield_outer_half","-h2a_shield_inner_half",
               "-h2av02_shield_mid_half","h2av02_shield_mid_half",
               "h2a_shield_bottom_z","h2a_shield_top_z")
lines += brick("SHIELD_LID","H2A_Shield","PEC",
               "-h2a_shield_outer_half","h2a_shield_outer_half",
               "-h2a_shield_outer_half","h2a_shield_outer_half",
               "h2a_shield_lid_bottom_z","h2a_shield_bottom_z")
def radial_master(name,comp,mat,r0,r1,halfw,z0,height):
    a0=f"({r0}-{halfw})*h2a_s2"; b0=f"({r0}+{halfw})*h2a_s2"
    a1=f"({r1}-{halfw})*h2a_s2"; b1=f"({r1}+{halfw})*h2a_s2"
    lines.extend([
      "    With Extrude","        .Reset",f'        .Name "{name}"',
      f'        .Component "{comp}"',f'        .Material "{mat}"',
      '        .Mode "Pointlist"',f'        .Height "{height}"',
      '        .Twist "0.0"','        .Taper "0.0"',
      f'        .Origin "0.0", "0.0", "{z0}"',
      '        .Uvector "1.0", "0.0", "0.0"',
      '        .Vvector "0.0", "1.0", "0.0"',
      f'        .Point "{a0}", "{b0}"',
      f'        .LineTo "{a1}", "{b1}"',
      f'        .LineTo "{b1}", "{a1}"',
      f'        .LineTo "{b0}", "{a0}"',
      f'        .LineTo "{a0}", "{b0}"',"        .Create","    End With","",
      "    With Transform","        .Reset",
      f'        .Name "{comp}:{name}"','        .Origin "Free"',
      f'        .Center "0.0", "0.0", "{z0}"',
      '        .Angle "0.0", "0.0", "90.0"',
      '        .MultipleObjects "True"','        .GroupObjects "False"',
      '        .Repetitions "3"','        .MultipleSelection "False"',
      '        .AutoDestination "True"','        .Transform "Shape", "Rotate"',
      "    End With",""
    ])

# MHF4/U.FL-class board connector envelopes.
for label,sx,sy in (("NE",1,1),("NW",-1,1),("SW",-1,-1),("SE",1,-1)):
    xc=center(sx,"h2av02_mhf_xy"); yc=center(sy,"h2av02_mhf_xy")
    x1,x2=rng(xc,"h2av02_mhf_half"); y1,y2=rng(yc,"h2av02_mhf_half")
    lines += brick("MHF_ENV_"+label,"H2A_ServiceConnector",
                   "H2A_PACKAGE_VISUAL_SURROGATE",x1,x2,y1,y2,
                   "h2av02_mhf_bottom_z","h2av02_mhf_top_z")

radial_master("OUTPUT_ROUTE_ENV_NE","H2A_ServiceRouting",
              "H2A_PACKAGE_VISUAL_SURROGATE",
              "h2av02_output_r0","h2av02_output_r1",
              "h2av02_output_halfw","h2av02_route_z-0.05","0.10")
radial_master("MICROCOAX_HORIZ_NE","H2A_ServiceRouting",
              "H2A_MICROCOAX_ENVELOPE_SURROGATE",
              "h2av02_cable_r0","h2av02_cable_r1",
              "h2av02_cable_half","h2av02_route_z-h2av02_cable_half",
              "2*h2av02_cable_half")
def hollow_brick(name,comp,mat,xc,yc,outer_half,inner_half,z1,z2):
    x1,x2=rng(xc,outer_half); y1,y2=rng(yc,outer_half)
    lines.extend(brick(name,comp,mat,x1,x2,y1,y2,z1,z2))
    ix1,ix2=rng(xc,inner_half); iy1,iy2=rng(yc,inner_half)
    tool="CUT_"+name
    lines.extend(brick(tool,"H2A_Tools","Vacuum",
                       ix1,ix2,iy1,iy2,f"({z1})-0.05",f"({z2})+0.05"))
    lines.append(f'    Solid.Subtract "{comp}:{name}", "H2A_Tools:{tool}"')
    lines.append("")

# Backplane cable feedthroughs, hollow copper tubes, spacers and vertical cable envelopes.
for label,sx,sy in (("NE",1,1),("NW",-1,1),("SW",-1,-1),("SE",1,-1)):
    xc=center(sx,"h2av02_tube_xy"); yc=center(sy,"h2av02_tube_xy")

    # Permanent service hole through the parent main backplane.
    x1,x2=rng(xc,"h2av02_feedthrough_half")
    y1,y2=rng(yc,"h2av02_feedthrough_half")
    tool="CUT_BACKPLANE_"+label
    lines += brick(tool,"H2A_Tools","Vacuum",x1,x2,y1,y2,"-0.55","0.05")
    lines.append(f'    Solid.Subtract "UnitCellGround:UNITCELL_GROUND_REFERENCE", "H2A_Tools:{tool}"')
    lines.append("")

    hollow_brick("COPPER_TUBE_"+label,"H2A_ServiceTube","PEC",
                 xc,yc,"h2av02_tube_outer_half","h2av02_tube_inner_half",
                 "h2av02_tube_bottom_z","h2av02_tube_top_z")

    hollow_brick("TOP_SPACER_"+label,"H2A_ServiceInterface","PEEK_VISUAL_SURROGATE",
                 xc,yc,"h2av02_spacer_half","h2av02_feedthrough_half",
                 "h2av02_tube_top_z","h2a_backside_cu_bottom")

    hollow_brick("BOTTOM_SPACER_"+label,"H2A_ServiceInterface","PEEK_VISUAL_SURROGATE",
                 xc,yc,"h2av02_spacer_half","h2av02_feedthrough_half",
                 "0.0","h2av02_tube_bottom_z")

    cx1,cx2=rng(xc,"h2av02_cable_half")
    cy1,cy2=rng(yc,"h2av02_cable_half")
    lines += brick("MICROCOAX_VERT_"+label,"H2A_ServiceRouting",
                   "H2A_MICROCOAX_ENVELOPE_SURROGATE",
                   cx1,cx2,cy1,cy2,
                   "h2av02_mmcx_bottom_z","h2av02_route_z+h2av02_cable_half")

    mx1,mx2=rng(xc,"h2av02_mmcx_half")
    my1,my2=rng(yc,"h2av02_mmcx_half")
    lines += brick("MMCX_ENV_"+label,"H2A_ServiceConnector",
                   "H2A_PACKAGE_VISUAL_SURROGATE",
                   mx1,mx2,my1,my2,
                   "h2av02_mmcx_bottom_z","h2av02_mmcx_top_z")
lines += [
"",
"    ' H2A V0.2 intentionally creates no RF port and calls no solver.",
"End Sub",""
]

DST.write_text("\n".join(lines),encoding="utf-8")
print("WROTE="+str(DST))
print("LINES="+str(len(lines)))
