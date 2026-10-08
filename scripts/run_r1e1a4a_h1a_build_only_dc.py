"""R1E1A4A-H1A OFFSET_GROUND_G2P0 BUILD-ONLY harness."""
from __future__ import print_function
import argparse,json,os,shutil,sys

HERE=os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0,HERE)
from run_r1e1a4a_h0_p1_build_only_dc import (
    ci,sha,macro_body,snapshot_tree,restore_snapshot,parameter_map,
    result_tree_solver_items,log_solver_hits,parse_status,shape_lines,audit_vba,parse_xyz
)

SOURCE_SHA="fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e"

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_R1E1A4A_H1A_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_R1E1A4A_H1A_WORK_EXISTS")
    if not os.path.isfile(source): raise RuntimeError("HOLD_R1E1A4A_H1A_SOURCE_MISSING")
    if sha(source)!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A4A_H1A_SOURCE_HASH_MISMATCH")

    macro=os.path.join(repo,"source","cst","R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY_V01.mcr")
    if not os.path.isfile(macro): raise RuntimeError("HOLD_R1E1A4A_H1A_MACRO_MISSING")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY_V01.cst")
    shutil.copy2(source,dst)
    if sha(dst)!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A4A_H1A_COPY_HASH_MISMATCH")

    parent_ev=os.path.join(repo,"evidence","r1e1a1_dc_nw_20260924_build01","P094")
    snap=snapshot_tree(parent_ev)
    bs=os.path.join(evidence,"build_shapes.txt"); bt=os.path.join(evidence,"build_status.txt")
    rs=os.path.join(evidence,"reopen_shapes.txt"); rt=os.path.join(evidence,"reopen_status.txt")
    rewrites=[]

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E1A4A H1A offset-ground reference plane",macro_body(macro))
        prj.modeler.add_to_history("R1E1A4A H1A build audit",audit_vba(bs,bt))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.schematic.execute_vba_code("Sub Main()\n"+audit_vba(rs,rt)+"\nEnd Sub")
    finally:
        if prj is not None: prj.close()
        de.close()
        rewrites=restore_snapshot(snap)

    bsh=shape_lines(bs); rsh=shape_lines(rs); st=parse_status(rt); params=parameter_map(dst)
    p1a=parse_xyz(st["P1_P1"]); p1ag=parse_xyz(st["P1_P2"])
    p1b=parse_xyz(st["P2_P1"]); p1bg=parse_xyz(st["P2_P2"])
    xy=float(params["r1e1a4a_h1a_port_xy"])
    ztop=float(params["r1e1a4a_h1a_port_top_z"]); zg=float(params["r1e1a4a_h1a_ground_top_z"])
    gbot=float(params["r1e1a4a_h1a_ground_bottom_z"]); gap=float(params["r1e1a4a_h1a_air_gap"])
    names=set(x.split("|",2)[1] for x in rsh)
    expected={
      "UnitCellGround:UNITCELL_GROUND_REFERENCE",
      "Substrate:FR4_BOARD",
      "TopCopper:TOP_COPPER",
      "ActiveHub:H1A_OFFSET_LOCAL_GROUND",
    }
    gl=[x for x in rsh if x.startswith("SHAPE|ActiveHub:H1A_OFFSET_LOCAL_GROUND|")]
    gv=float(gl[0].split("volume=",1)[1]) if gl else -1.0
    checks={
      "shape_count_4_build":len(bsh)==4,
      "shape_count_4_reopen":len(rsh)==4,
      "build_reopen_shapes_identical":bsh==rsh,
      "shape_names_exact":names==expected,
      "ground_volume_3p5_mm3":abs(gv-3.5)<1e-6,
      "air_gap_2mm":abs(gap-2.0)<1e-9,
      "ground_top_exact":abs(zg-(57.142857143-2.0))<1e-6,
      "ground_thickness_0p035":abs((zg-gbot)-0.035)<1e-9,
      "port_count_2":int(st["PORT_COUNT"])==2,
      "ports_sparameter":st["P1_TYPE"].lower()=="sparameter" and st["P2_TYPE"].lower()=="sparameter",
      "ports_50ohm":abs(float(st["P1_IMPEDANCE"])-50.0)<1e-9 and abs(float(st["P2_IMPEDANCE"])-50.0)<1e-9,
      "port_queries_ok":all(st[k].lower() in ("true","-1") for k in ("P1_PROP_OK","P1_COORD_OK","P2_PROP_OK","P2_COORD_OK")),
      "p1a_terminal_exact":max(abs(p1a[i]-v) for i,v in enumerate((xy,xy,ztop)))<1e-8,
      "p1a_ground_exact":max(abs(p1ag[i]-v) for i,v in enumerate((xy,xy,zg)))<1e-8,
      "p1b_terminal_exact":max(abs(p1b[i]-v) for i,v in enumerate((-xy,-xy,ztop)))<1e-8,
      "p1b_ground_exact":max(abs(p1bg[i]-v) for i,v in enumerate((-xy,-xy,zg)))<1e-8,
      "opposite_symmetry":abs(p1a[0]+p1b[0])<1e-8 and abs(p1a[1]+p1b[1])<1e-8,
      "port_length_3p035mm":abs((ztop-zg)-3.035)<1e-6,
      "unitcell_94":abs(float(st["UNITCELL_DS1"])-94.0)<1e-6 and abs(float(st["UNITCELL_DS2"])-94.0)<1e-6,
      "broadside":abs(float(st["SCAN_THETA_DEG"]))<1e-9,
      "no_solver_markers":len(log_solver_hits(dst))==0,
      "no_solver_result_items":len(result_tree_solver_items(dst))==0,
      "parent_evidence_restored":True,
    }
    checks["pass"]=all(checks.values())
    summary={
      "mode":"R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY",
      "solver_run":False,
      "source_sha256":SOURCE_SHA,
      "result_cst":dst,
      "result_sha256":sha(dst),
      "result_bytes":os.path.getsize(dst),
      "parent_evidence_rewrites_detected":rewrites,
      "parameters":{k:params.get(k) for k in (
        "r1e1a4a_h1a_ground_half","r1e1a4a_h1a_air_gap","r1e1a4a_h1a_p1_ref_ohm",
        "r1e1a4a_h1a_port_xy","r1e1a4a_h1a_port_top_z",
        "r1e1a4a_h1a_ground_top_z","r1e1a4a_h1a_ground_bottom_z")},
      "checks":checks,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    print("PASS_R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY" if checks["pass"] else "HOLD_R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY")
    print("RESULT_SHA256="+summary["result_sha256"])
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work,a.source_cst)
