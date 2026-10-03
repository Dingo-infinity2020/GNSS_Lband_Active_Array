#!/usr/bin/env python3
"""Generate the two R1A5F single-port CST macros from one canonical endpoint definition."""
from __future__ import print_function
import argparse
import math
from pathlib import Path

S2=1.0/math.sqrt(2.0)
A_P1=(+1,+1)
A_P2=(-1,-1)

def rot90(v):
    x,y=v
    return (-y,x)

def expr(sign,axis="port_terminal_xy"):
    return axis if sign>0 else "-"+axis

def macro(pol,p1,p2,rotation_deg):
    return """Option Explicit

' R1A5F {pol} single differential port - PORT ONLY
' Generated from scripts/generate_r1a5f_single_port_macros.py
' No geometry, material, solver, monitor, or optimization commands.

Sub Main()

    StoreParameter "port_ref_impedance", 100.0
    StoreParameter "port_s2", 0.7071067811865476
    StoreParameter "port_terminal_xy", "terminal_r*port_s2"
    StoreParameter "port_terminal_z", "copper_top_z"
    StoreParameter "r1a5f_rotation_deg", {rot}
    StoreParameter "r1a5f_p1_x", "{p1x}"
    StoreParameter "r1a5f_p1_y", "{p1y}"
    StoreParameter "r1a5f_p2_x", "{p2x}"
    StoreParameter "r1a5f_p2_y", "{p2y}"

    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "port_ref_impedance"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "r1a5f_p1_x", "r1a5f_p1_y", "port_terminal_z"
        .SetP2 "False", "r1a5f_p2_x", "r1a5f_p2_y", "port_terminal_z"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With

End Sub
""".format(
      pol=pol,rot=rotation_deg,
      p1x=expr(p1[0]),p1y=expr(p1[1]),
      p2x=expr(p2[0]),p2y=expr(p2[1]))

def expected():
    b1=rot90(A_P1)
    b2=rot90(A_P2)
    return {
      "A":macro("Pol-A_NE_TO_SW",A_P1,A_P2,0),
      "B":macro("Pol-B_NW_TO_SE",b1,b2,90),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",default="source/cst")
    ap.add_argument("--check",action="store_true")
    a=ap.parse_args()
    out=Path(a.outdir)
    names={
      "A":"R1A5F_POLA_SINGLE_PORT_BUILD_ONLY_V01.mcr",
      "B":"R1A5F_POLB_SINGLE_PORT_BUILD_ONLY_V01.mcr",
    }
    exp=expected()
    if a.check:
        ok=True
        for key,name in names.items():
            p=out/name
            if not p.exists() or p.read_text(encoding="utf-8").replace("\r\n","\n") != exp[key].replace("\r\n","\n"):
                print("MISMATCH="+str(p))
                ok=False
        if not ok:
            raise SystemExit(3)
        print("PASS_R1A5F_GENERATED_MACROS_MATCH")
        return
    out.mkdir(parents=True,exist_ok=True)
    for key,name in names.items():
        (out/name).write_text(exp[key],encoding="utf-8")
        print("WROTE="+str(out/name))

if __name__=="__main__":
    main()
