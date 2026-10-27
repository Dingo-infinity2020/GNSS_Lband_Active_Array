#!/usr/bin/env python3
"""Generate R1E1A0-R1 parameterization-clean derived CST macros.

Historical source macros are never modified. Only frozen declaration substitutions are allowed.
"""
from pathlib import Path
import argparse, hashlib

ROOT=Path(__file__).resolve().parents[1]

SOURCES={
 "geometry":{
   "path":ROOT/"source/cst/R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr",
   "sha":"1e5bb3188c5d19146b673ec54372d0c35ae572abc775512529f71db71cfad5be",
   "out":ROOT/"source/cst/R1E1A0R1_PITCH_READY_R1A3_GEOMETRY_V01.mcr",
 },
 "periodic":{
   "path":ROOT/"source/cst/R1E0A_PERIODIC_BROADSIDE_BUILD_ONLY_V01.mcr",
   "sha":"eaa9c714978c76381424747307d635397084078ddbf235103d54c3b51275f7ff",
   "out":ROOT/"source/cst/R1E1A0R1_PARAMETER_READY_PERIODIC_BROADSIDE_V01.mcr",
 },
}

def sha_text(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replace_once(text,old,new,label):
    n=text.count(old)
    if n!=1:
        raise RuntimeError("%s expected one occurrence, found %d: %s"%(label,n,old))
    return text.replace(old,new,1)

def geometry_text():
    s=SOURCES["geometry"]
    if sha_text(s["path"])!=s["sha"]:
        raise RuntimeError("R1A3 historical macro hash mismatch")
    t=s["path"].read_text(encoding="utf-8").replace("\r\n","\n")
    t=replace_once(t,
      '    StoreParameter "unit_cell_pitch_nominal", 94.0',
      '    MakeSureParameterExists "unit_cell_pitch_nominal", "94.0"',
      "geometry pitch declaration")
    t=replace_once(t,
      '    StoreParameter "ground_reference_span", "unit_cell_pitch_nominal"',
      '    MakeSureParameterExists "ground_reference_span", "unit_cell_pitch_nominal"',
      "geometry dependent span declaration")
    marker="Option Explicit\n"
    note=("Option Explicit\n\n"
          "' R1E1A0-R1 derived from frozen R1A3 macro.\n"
          "' Only unit_cell_pitch_nominal / ground_reference_span declaration semantics changed.\n"
          "' Historical R1A3 source remains untouched.\n")
    t=replace_once(t,marker,note,"geometry provenance header")
    return t if t.endswith("\n") else t+"\n"

def periodic_text():
    s=SOURCES["periodic"]
    if sha_text(s["path"])!=s["sha"]:
        raise RuntimeError("R1E0A historical macro hash mismatch")
    t=s["path"].read_text(encoding="utf-8").replace("\r\n","\n")
    t=replace_once(t,
      '    StoreParameter "R1E0_pitch_nominal_mm", 94.0',
      '    MakeSureParameterExists "R1E0_pitch_nominal_mm", "unit_cell_pitch_nominal"',
      "periodic pitch metadata declaration")
    t=replace_once(t,
      '    StoreParameter "R1E0_scan_theta_deg", 0.0',
      '    MakeSureParameterExists "R1E0_scan_theta_deg", "0.0"',
      "periodic theta declaration")
    t=replace_once(t,
      '    StoreParameter "R1E0_scan_phi_deg", 45.0',
      '    MakeSureParameterExists "R1E0_scan_phi_deg", "45.0"',
      "periodic phi declaration")
    marker="Option Explicit\n"
    note=("Option Explicit\n\n"
          "' R1E1A0-R1 derived from frozen R1E0A periodic macro.\n"
          "' Parameter declarations are sweep-ready; boundary physics is unchanged.\n"
          "' Historical R1E0A source remains untouched.\n")
    t=replace_once(t,marker,note,"periodic provenance header")
    return t if t.endswith("\n") else t+"\n"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    a=ap.parse_args()
    generated={
      "geometry":geometry_text(),
      "periodic":periodic_text(),
    }
    mismatch=[]
    for k,t in generated.items():
        out=SOURCES[k]["out"]
        if a.check:
            if not out.exists() or out.read_text(encoding="utf-8").replace("\r\n","\n")!=t:
                mismatch.append(str(out))
        else:
            out.write_bytes(t.encode("utf-8"))
            print("WROTE="+str(out))
    if a.check:
        if mismatch:
            print("HOLD_R1E1A0R1_GENERATED_MACROS_DRIFT")
            for x in mismatch: print(x)
            raise SystemExit(3)
        print("PASS_R1E1A0R1_GENERATED_MACROS_MATCH")

if __name__=="__main__": main()
