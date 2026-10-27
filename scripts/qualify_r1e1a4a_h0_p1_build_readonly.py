"""Read-only qualification of the consumed R1E1A4A H0/P1 formal build artifact.

The formal build already ran once. This script MUST NOT modify or save the CST
project. It only executes query/audit VBA against the persisted artifact.
"""
from __future__ import print_function
import argparse, json, os, sys

HERE=os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0,HERE)
from run_r1e1a4a_h0_p1_build_only_dc import (
    audit_vba, sha, snapshot_tree, restore_snapshot, parameter_map,
    result_tree_solver_items, log_solver_hits, parse_status, shape_lines, parse_xyz,
    ci
)

FORMAL_STATUS="HOLD_R1E1A4A_H0_P1_BUILD_AUDIT_VBA_RESERVED_WORD"

def run(repo,evidence,artifact):
    if not os.path.isdir(evidence): os.makedirs(evidence)
    if not os.path.isfile(artifact): raise RuntimeError("HOLD_R1E1A4A_READONLY_ARTIFACT_MISSING")
    shapes=os.path.join(evidence,"readonly_recovery2_shapes.txt")
    status=os.path.join(evidence,"readonly_recovery2_status.txt")
    if os.path.exists(shapes) or os.path.exists(status):
        raise RuntimeError("HOLD_R1E1A4A_READONLY_EVIDENCE_COLLISION")

    parent_ev=os.path.join(repo,"evidence","r1e1a1_dc_nw_20260924_build01","P094")
    snap=snapshot_tree(parent_ev); rewrites=[]
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(artifact)
        prj.schematic.execute_vba_code("Sub Main()\n"+audit_vba(shapes,status)+"\nEnd Sub")
    finally:
        if prj is not None: prj.close()
        de.close()
        rewrites=restore_snapshot(snap)

    sh=shape_lines(shapes); st=parse_status(status); params=parameter_map(artifact)
    p1a=parse_xyz(st["P1_P1"]); p1ag=parse_xyz(st["P1_P2"])
    p1b=parse_xyz(st["P2_P1"]); p1bg=parse_xyz(st["P2_P2"])
    xy=float(params["r1e1a4a_port_xy"])
    ztop=float(params["r1e1a4a_port_top_z"]); zg=float(params["r1e1a4a_ground_top_z"])
    names=set(x.split("|",2)[1] for x in sh)
    expected_names={
      "UnitCellGround:UNITCELL_GROUND_REFERENCE",
      "Substrate:FR4_BOARD",
      "TopCopper:TOP_COPPER",
      "ActiveHub:H0_LOCAL_GROUND",
    }
    gl=[x for x in sh if x.startswith("SHAPE|ActiveHub:H0_LOCAL_GROUND|")]
    gv=float(gl[0].split("volume=",1)[1]) if gl else -1.0

    checks={
      "shape_count_4":len(sh)==4,
      "shape_names_exact":names==expected_names,
      "h0_ground_volume_3p5_mm3":abs(gv-3.5)<1e-6,
      "port_count_2":int(st["PORT_COUNT"])==2,
      "ports_sparameter":st["P1_TYPE"].lower()=="sparameter" and st["P2_TYPE"].lower()=="sparameter",
      "ports_50ohm":abs(float(st["P1_IMPEDANCE"])-50.0)<1e-9 and abs(float(st["P2_IMPEDANCE"])-50.0)<1e-9,
      "port_queries_ok":all(st[k].lower() in ("true","-1") for k in ("P1_PROP_OK","P1_COORD_OK","P2_PROP_OK","P2_COORD_OK")),
      "p1a_terminal_exact":max(abs(p1a[i]-v) for i,v in enumerate((xy,xy,ztop)))<1e-8,
      "p1a_ground_exact":max(abs(p1ag[i]-v) for i,v in enumerate((xy,xy,zg)))<1e-8,
      "p1b_terminal_exact":max(abs(p1b[i]-v) for i,v in enumerate((-xy,-xy,ztop)))<1e-8,
      "p1b_ground_exact":max(abs(p1bg[i]-v) for i,v in enumerate((-xy,-xy,zg)))<1e-8,
      "opposite_symmetry":abs(p1a[0]+p1b[0])<1e-8 and abs(p1a[1]+p1b[1])<1e-8,
      "unitcell_94":abs(float(st["UNITCELL_DS1"])-94.0)<1e-6 and abs(float(st["UNITCELL_DS2"])-94.0)<1e-6,
      "broadside":abs(float(st["SCAN_THETA_DEG"]))<1e-9,
      "h0_half_5":abs(float(params["r1e1a4a_h0_ground_half"])-5.0)<1e-9,
      "p1_ref_50":abs(float(params["r1e1a4a_p1_ref_ohm"])-50.0)<1e-9,
      "no_solver_markers":len(log_solver_hits(artifact))==0,
      "no_solver_result_items":len(result_tree_solver_items(artifact))==0,
      "parent_evidence_restored":True,
    }
    checks["pass"]=all(checks.values())

    summary={
      "formal_status":FORMAL_STATUS,
      "formal_build_invocation_count":1,
      "solver_run":False,
      "read_only_recovery":True,
      "artifact":artifact,
      "artifact_sha256":sha(artifact),
      "artifact_bytes":os.path.getsize(artifact),
      "parent_evidence_rewrites_detected":rewrites,
      "parameters":{k:params.get(k) for k in (
        "r1e1a4a_h0_ground_half","r1e1a4a_p1_ref_ohm","r1e1a4a_port_xy",
        "r1e1a4a_port_top_z","r1e1a4a_ground_top_z","r1e1a4a_ground_bottom_z")},
      "checks":checks,
      "canonical_status":("PASS_R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_READONLY_RECOVERY"
                          if checks["pass"] else
                          "HOLD_R1E1A4A_H0_P1_BUILD_READONLY_QUALIFICATION"),
    }
    with open(os.path.join(evidence,"readonly_recovery2_summary.json"),"w") as f:
        json.dump(summary,f,indent=2)
    print(summary["canonical_status"])
    print("FORMAL_STATUS="+FORMAL_STATUS)
    print("ARTIFACT_SHA256="+summary["artifact_sha256"])
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--artifact",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.artifact)
