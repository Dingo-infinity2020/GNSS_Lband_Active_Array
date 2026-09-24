#!/usr/bin/env python3
"""Read-only recovery qualification for the completed R1E0A build artifact/evidence."""
from __future__ import print_function
import argparse, hashlib, json, os

EXPECTED_CST_SHA="48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223"
EXPECTED_SOURCE_SHA="74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce"

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""):
            h.update(c)
    return h.hexdigest()

def parse_status(path):
    out={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" not in line:
            continue
        k,v=line.split("=",1)
        out[k.strip()]=v.strip()
    return out

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def close(a,b,tol=1e-9):
    return abs(a-b)<=tol

def boolish(v):
    return v.strip().lower() in ("true","1","-1")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--artifact",required=True)
    ap.add_argument("--source",required=True)
    a=ap.parse_args()

    build_status=parse_status(os.path.join(a.evidence,"build_periodic_status.txt"))
    reopen_status=parse_status(os.path.join(a.evidence,"reopen_periodic_status.txt"))
    build_shapes=shape_lines(os.path.join(a.evidence,"build_object_inventory.txt"))
    reopen_shapes=shape_lines(os.path.join(a.evidence,"reopen_object_inventory.txt"))
    source_shapes=shape_lines(os.path.join(
        a.repo,"evidence","r1a5f_dc_nw_20260924_build01","A","reopen_object_inventory.txt"))

    artifact_sha=sha(a.artifact)
    source_sha=sha(a.source)
    stem=os.path.splitext(a.artifact)[0]
    output_exists=os.path.isfile(os.path.join(stem,"Result","output.txt"))

    xspan=float(reopen_status["STRUCTURE_XMAX"])-float(reopen_status["STRUCTURE_XMIN"])
    yspan=float(reopen_status["STRUCTURE_YMAX"])-float(reopen_status["STRUCTURE_YMIN"])

    checks={
      "artifact_sha_match":artifact_sha==EXPECTED_CST_SHA,
      "source_sha_match":source_sha==EXPECTED_SOURCE_SHA,
      "build_reopen_status_identical":build_status==reopen_status,
      "geometry_unchanged_build":build_shapes==source_shapes,
      "geometry_unchanged_reopen":reopen_shapes==source_shapes,
      "port_count_1":int(reopen_status["PORT_COUNT"])==1,
      "x_boundaries_unit_cell":reopen_status["BOUNDARY_XMIN"].lower()=="unit cell" and reopen_status["BOUNDARY_XMAX"].lower()=="unit cell",
      "y_boundaries_unit_cell":reopen_status["BOUNDARY_YMIN"].lower()=="unit cell" and reopen_status["BOUNDARY_YMAX"].lower()=="unit cell",
      "z_boundaries_expanded_open":reopen_status["BOUNDARY_ZMIN"].lower()=="expanded open" and reopen_status["BOUNDARY_ZMAX"].lower()=="expanded open",
      "structure_query_ok":int(reopen_status["STRUCTURE_QUERY_ERR"])==0,
      "structure_x_span_94mm":close(xspan,94.0,1e-6),
      "structure_y_span_94mm":close(yspan,94.0,1e-6),
      "scan_query_ok":int(reopen_status["SCAN_QUERY_ERR"])==0,
      "scan_valid_boolean_nonzero":boolish(reopen_status["SCAN_VALID"]),
      "theta_0":close(float(reopen_status["SCAN_THETA_DEG"]),0.0),
      "phi_45":close(float(reopen_status["SCAN_PHI_DEG"]),45.0),
      "direction_outward":int(reopen_status["SCAN_DIRECTION"])==1,
      "unitcell_ds1_94":close(float(reopen_status["UNITCELL_DS1"]),94.0,1e-6),
      "unitcell_ds2_94":close(float(reopen_status["UNITCELL_DS2"]),94.0,1e-6),
      "unitcell_angle_90":close(float(reopen_status["UNITCELL_ANGLE"]),90.0),
      "no_solver_output":not output_exists,
    }
    checks["pass"]=all(checks.values())

    summary={
      "mode":"READ_ONLY_RECOVERY_QUALIFICATION",
      "formal_cst_rerun":False,
      "original_formal_status":"HOLD_R1E0A_PERIODIC_CONFIG_AUDIT",
      "hold_classification":"AUDIT_BOOLEAN_ENCODING_MISMATCH",
      "artifact":a.artifact,
      "artifact_sha256":artifact_sha,
      "artifact_bytes":os.path.getsize(a.artifact),
      "source":a.source,
      "source_sha256":source_sha,
      "reopen_status":reopen_status,
      "structure_span_mm":{"x":xspan,"y":yspan},
      "checks":checks,
    }
    out=os.path.join(a.evidence,"requalification_summary.json")
    with open(out,"w") as f:
        json.dump(summary,f,indent=2)

    if checks["pass"]:
        print("PASS_R1E0A_PERIODIC_CONFIG_BUILD_ONLY_READONLY_RECOVERY")
    else:
        print("HOLD_R1E0A_READONLY_RECOVERY")
    print("ARTIFACT_SHA256="+artifact_sha)
    print("SCAN_VALID_RAW="+reopen_status["SCAN_VALID"])
    print("SCAN_VALID_INTERPRETED="+str(boolish(reopen_status["SCAN_VALID"])))
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    main()
