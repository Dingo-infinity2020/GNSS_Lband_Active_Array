#!/usr/bin/env python3
"""Read-only qualification of already-built R1E0C scan-state CST artifacts."""
from __future__ import print_function
import argparse, hashlib, json, math, os, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
from cst.results import ProjectFile

STATES=[
  ("C30P45",30.0,45.0,"e68bbe11a61c988debd34503ede5cb952cd44f93f5db2a43f53a31344f7a30f2"),
  ("C45P45",45.0,45.0,"ed3c6cbe0d570e7ff4dc4d093d7e3630b3356684ae96569b6f2a20251ffa34ed"),
  ("C60P45",60.0,45.0,"94360ee2c40d4e5236b7b7a1fee79b46739da2aaec70054e4aa707a123853e01"),
  ("C60P135",60.0,135.0,"c8270338b8a0e0bef9263460cad97a83e1ff2a59c0b29aaaab682d8212836ec1"),
]

SOLVER_MARKERS=(
  "meshing successful",
  "adaptive mesh refinement pass",
  "mesh adaptation sample",
  "excitation: port",
  "all broadband sweep convergence criteria",
  "running solver",
)

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""):
            h.update(c)
    return h.hexdigest()

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def parse_status(path):
    out={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k.strip()]=v.strip()
    return out

def boolish(v):
    return v.strip().lower() in ("true","1","-1")

def close(a,b,tol=1e-9):
    return abs(a-b)<=tol

def status_checks(st,theta,phi):
    xspan=float(st["STRUCTURE_XMAX"])-float(st["STRUCTURE_XMIN"])
    yspan=float(st["STRUCTURE_YMAX"])-float(st["STRUCTURE_YMIN"])
    return {
      "port_count_1":int(st["PORT_COUNT"])==1,
      "x_boundaries_unit_cell":st["BOUNDARY_XMIN"].lower()=="unit cell" and st["BOUNDARY_XMAX"].lower()=="unit cell",
      "y_boundaries_unit_cell":st["BOUNDARY_YMIN"].lower()=="unit cell" and st["BOUNDARY_YMAX"].lower()=="unit cell",
      "z_boundaries_expanded_open":st["BOUNDARY_ZMIN"].lower()=="expanded open" and st["BOUNDARY_ZMAX"].lower()=="expanded open",
      "structure_query_ok":int(st["STRUCTURE_QUERY_ERR"])==0,
      "xspan_94":close(xspan,94.0,1e-6),
      "yspan_94":close(yspan,94.0,1e-6),
      "scan_query_ok":int(st["SCAN_QUERY_ERR"])==0,
      "scan_valid":boolish(st["SCAN_VALID"]),
      "theta_match":close(float(st["SCAN_THETA_DEG"]),theta,1e-9),
      "phi_match":close(float(st["SCAN_PHI_DEG"]),phi,1e-9),
      "direction_outward":int(st["SCAN_DIRECTION"])==1,
      "unitcell_ds1_94":close(float(st["UNITCELL_DS1"]),94.0,1e-6),
      "unitcell_ds2_94":close(float(st["UNITCELL_DS2"]),94.0,1e-6),
      "unitcell_angle_90":close(float(st["UNITCELL_ANGLE"]),90.0,1e-9),
      "status_claims_no_solver":st.get("SOLVER_RUN","").upper()=="NO",
    }

def parameter_map(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Model","Parameters.json")
    data=json.load(open(p,encoding="utf-8"))
    out={}
    def walk(x):
        if isinstance(x,dict):
            if "name" in x and "value" in x:
                out[str(x["name"])]=str(x["value"])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(data)
    return out

def log_evidence(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(p):
        return {"exists":False,"solver_marker_hits":[],"warning_lines":[]}
    text=open(p,encoding="utf-8",errors="ignore").read()
    low=text.lower()
    hits=[m for m in SOLVER_MARKERS if m in low]
    warnings=[x.strip() for x in text.splitlines() if "warning" in x.lower() or "prevented attempt" in x.lower()]
    return {"exists":True,"solver_marker_hits":hits,"warning_lines":warnings}

def result_tree_evidence(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    items=pf.get_3d().get_tree_items()
    solver=[x for x in items if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]
    return {"solver_result_item_count":len(solver),"solver_result_items":solver}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    a=ap.parse_args()

    source_shapes=shape_lines(os.path.join(a.repo,"evidence","r1e0a_dc_nw_20260924_build01","reopen_object_inventory.txt"))
    results=[]
    for state,theta,phi,expected_sha in STATES:
        cst=os.path.join(a.work,"R1E0C_%s_SCANSTATE_BUILD_ONLY_V01.cst"%state)
        edir=os.path.join(a.evidence,state)
        bshape=shape_lines(os.path.join(edir,"build_object_inventory.txt"))
        rshape=shape_lines(os.path.join(edir,"reopen_object_inventory.txt"))
        bst=parse_status(os.path.join(edir,"build_periodic_status.txt"))
        rst=parse_status(os.path.join(edir,"reopen_periodic_status.txt"))
        bc=status_checks(bst,theta,phi)
        rc=status_checks(rst,theta,phi)
        params=parameter_map(cst)
        logs=log_evidence(cst)
        tree=result_tree_evidence(cst)
        actual_sha=sha(cst)
        checks={
          "artifact_sha_match":actual_sha==expected_sha,
          "build_geometry_unchanged":bshape==source_shapes,
          "reopen_geometry_unchanged":rshape==source_shapes,
          "build_status_pass":all(bc.values()),
          "reopen_status_pass":all(rc.values()),
          "build_reopen_status_identical":bst==rst,
          "theta_parameter_match":close(float(params["R1E0_scan_theta_deg"]),theta,1e-9),
          "phi_parameter_match":close(float(params["R1E0_scan_phi_deg"]),phi,1e-9),
          "no_solver_markers_in_message_log":len(logs["solver_marker_hits"])==0,
          "no_solver_result_tree_items":tree["solver_result_item_count"]==0,
        }
        checks["pass"]=all(checks.values())
        results.append({
          "state":state,"theta_deg":theta,"phi_deg":phi,
          "artifact":cst,"artifact_sha256":actual_sha,"artifact_bytes":os.path.getsize(cst),
          "build_status":bst,"reopen_status":rst,
          "scan_parameters":{"theta":params["R1E0_scan_theta_deg"],"phi":params["R1E0_scan_phi_deg"]},
          "message_log":logs,"result_tree":tree,"checks":checks,
        })

    top={
      "state_count_4":len(results)==4,
      "all_state_hashes_unique":len(set(x["artifact_sha256"] for x in results))==4,
      "all_states_pass":all(x["checks"]["pass"] for x in results),
    }
    top["pass"]=all(top.values())
    summary={
      "mode":"READ_ONLY_EXISTING_ARTIFACT_QUALIFICATION",
      "cst_rebuild":False,
      "solver_run":False,
      "original_recovery_status":"HOLD_R1E0C_A_RECOVERY_NO_SOLVER_PREDICATE",
      "hold_classification":"NO_SOLVER_PREDICATE_FILE_EXISTENCE_MISMATCH",
      "states":results,"checks":top,
    }
    out=os.path.join(a.evidence,"read_only_qualification.json")
    with open(out,"w") as f: json.dump(summary,f,indent=2)
    if top["pass"]:
        print("PASS_R1E0C_SCANSTATE_BUILD_ONLY_READONLY_QUALIFICATION")
    else:
        print("HOLD_R1E0C_SCANSTATE_READONLY_QUALIFICATION")
    for x in results:
        print(x["state"]+"_SHA256="+x["artifact_sha256"])
        print(x["state"]+"_PARAMS="+x["scan_parameters"]["theta"]+","+x["scan_parameters"]["phi"])
        print(x["state"]+"_SOLVER_MARKERS="+str(len(x["message_log"]["solver_marker_hits"])))
        print(x["state"]+"_SOLVER_RESULT_ITEMS="+str(x["result_tree"]["solver_result_item_count"]))
    print(json.dumps(top,sort_keys=True))

if __name__=="__main__":
    main()
