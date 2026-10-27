"""R1A5F split single-port BUILD-ONLY harness for NW/DC."""
from __future__ import print_function
import argparse, hashlib, json, math, os, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci

BASE_SHA="b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa"

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""):
            h.update(c)
    return h.hexdigest()

def body(path):
    lines=open(path,"r",encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=e=None
    for i,l in enumerate(lines):
        if l.strip()=="Sub Main()": s=i
        elif l.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("macro markers")
    return "\n".join(lines[s+1:e])

def audit_macro(shape_path,param_path,status_path,label):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1A5F_%s_SHAPE_INVENTORY"'%label,
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+10",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      '  Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm)) & "|area=" & CStr(Solid.GetArea(nm))',
      " End If","Next i","Close #f",
      "f=FreeFile", 'Open "%s" For Output As #f'%param_path,
      'Print #f, "R1A5F_%s_PARAMETER_INVENTORY"'%label,
      'Print #f, "PARAM_COUNT=" & CStr(GetNumberOfParameters())',
      "For i=1 To GetNumberOfParameters()",
      ' Print #f, "PARAM|" & GetParameterName(i) & "|" & GetParameterSValue(i) & "|" & CStr(GetParameterNValue(i))',
      "Next i","Close #f",
      "f=FreeFile", 'Open "%s" For Output As #f'%status_path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "SOLVER_RUN=NO"',
      "Close #f","On Error GoTo 0"])

def shot(view,path):
    return 'Plot.RestoreView "%s"\nPlot.ZoomToStructure\nPlot.Update\nPlot.ExportImage "%s", 1800, 1400'%(view,path)

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def port_count(path):
    for x in open(path,encoding="utf-8").read().splitlines():
        if x.startswith("PORT_COUNT="):
            return int(x.split("=",1)[1])
    return None

def params(path):
    out={}
    for x in open(path,encoding="utf-8").read().splitlines():
        if not x.startswith("PARAM|"):
            continue
        parts=x.split("|")
        if len(parts)>=4 and parts[1]:
            try: out[parts[1]]=float(parts[3])
            except Exception: pass
    return out

def run_one(repo,evidence,work,base_cst,key,macro_name,cst_name):
    edir=os.path.join(evidence,key)
    os.makedirs(edir)
    dst=os.path.join(work,cst_name)
    macro=os.path.join(repo,"source","cst",macro_name)

    shutil.copy2(base_cst,dst)
    pre_sha=sha(dst)
    if pre_sha != BASE_SHA:
        raise RuntimeError("HOLD_R1A5F_%s_COPY_HASH_MISMATCH"%key)

    log=[
      "MODEL="+key,
      "BASE_CST_SHA256="+BASE_SHA,
      "PRE_PORT_COPY_SHA256="+pre_sha,
      "PORT_MACRO_SHA256="+sha(macro),
    ]

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1A5F "+key+" add one differential port",body(macro))
        prj.save()
        prj.modeler.add_to_history("R1A5F "+key+" immediate audit",audit_macro(
          os.path.join(edir,"build_object_inventory.txt"),
          os.path.join(edir,"build_parameter_inventory.txt"),
          os.path.join(edir,"build_port_status.txt"),key))
        log.append("BUILD_AUDIT_PASS")
    finally:
        if prj is not None: prj.close()
        de.close()

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1A5F "+key+" reopen audit",audit_macro(
          os.path.join(edir,"reopen_object_inventory.txt"),
          os.path.join(edir,"reopen_parameter_inventory.txt"),
          os.path.join(edir,"reopen_port_status.txt"),key))
        prj.modeler.add_to_history("R1A5F "+key+" top view",shot("Front",os.path.join(edir,"top_view.png")))
        prj.modeler.add_to_history("R1A5F "+key+" perspective",shot("Perspective",os.path.join(edir,"oblique_view.png")))
        log.append("FRESH_REOPEN_AUDIT_PASS")
    finally:
        if prj is not None: prj.close()
        de.close()

    return {
      "key":key,
      "cst":dst,
      "cst_sha256":sha(dst),
      "cst_bytes":os.path.getsize(dst),
      "pre_port_copy_sha256":pre_sha,
      "macro":macro,
      "macro_sha256":sha(macro),
      "build_port_count":port_count(os.path.join(edir,"build_port_status.txt")),
      "reopen_port_count":port_count(os.path.join(edir,"reopen_port_status.txt")),
      "build_shapes":shape_lines(os.path.join(edir,"build_object_inventory.txt")),
      "reopen_shapes":shape_lines(os.path.join(edir,"reopen_object_inventory.txt")),
      "reopen_params":params(os.path.join(edir,"reopen_parameter_inventory.txt")),
      "log":log,
    }

def close(a,b,tol=1e-9):
    return abs(a-b)<=tol

def run(repo,evidence,work,base_cst):
    if os.path.exists(evidence):
        raise RuntimeError("HOLD_R1A5F_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work):
        raise RuntimeError("HOLD_R1A5F_WORK_DIR_ALREADY_EXISTS")
    if not os.path.isfile(base_cst):
        raise RuntimeError("HOLD_R1A5F_BASE_CST_MISSING")
    base_sha=sha(base_cst)
    if base_sha != BASE_SHA:
        raise RuntimeError("HOLD_R1A5F_BASE_CST_HASH_MISMATCH:"+base_sha)

    os.makedirs(evidence)
    os.makedirs(work)

    A=run_one(repo,evidence,work,base_cst,"A",
      "R1A5F_POLA_SINGLE_PORT_BUILD_ONLY_V01.mcr",
      "R1A5F_POLA_SINGLE_PORT_V01.cst")
    B=run_one(repo,evidence,work,base_cst,"B",
      "R1A5F_POLB_SINGLE_PORT_BUILD_ONLY_V01.mcr",
      "R1A5F_POLB_SINGLE_PORT_V01.cst")

    base_inventory=os.path.join(repo,"evidence","r1a3_dc_nw_20260924_build01","object_inventory.txt")
    base_shapes=shape_lines(base_inventory)

    pa=A["reopen_params"]; pb=B["reopen_params"]
    required=("r1a5f_p1_x","r1a5f_p1_y","r1a5f_p2_x","r1a5f_p2_y","r1a5f_rotation_deg","port_ref_impedance")
    if not all(x in pa and x in pb for x in required):
        raise RuntimeError("HOLD_R1A5F_RUNTIME_ENDPOINT_PARAMS_MISSING")

    rotation_ok=(
      close(pb["r1a5f_p1_x"],-pa["r1a5f_p1_y"]) and
      close(pb["r1a5f_p1_y"], pa["r1a5f_p1_x"]) and
      close(pb["r1a5f_p2_x"],-pa["r1a5f_p2_y"]) and
      close(pb["r1a5f_p2_y"], pa["r1a5f_p2_x"]) and
      close(pa["r1a5f_rotation_deg"],0.0) and
      close(pb["r1a5f_rotation_deg"],90.0)
    )

    checks={
      "base_hash_match":base_sha==BASE_SHA,
      "A_pre_copy_hash_match":A["pre_port_copy_sha256"]==BASE_SHA,
      "B_pre_copy_hash_match":B["pre_port_copy_sha256"]==BASE_SHA,
      "A_build_port_count_1":A["build_port_count"]==1,
      "A_reopen_port_count_1":A["reopen_port_count"]==1,
      "B_build_port_count_1":B["build_port_count"]==1,
      "B_reopen_port_count_1":B["reopen_port_count"]==1,
      "A_geometry_unchanged_vs_r1a3":A["build_shapes"]==base_shapes and A["reopen_shapes"]==base_shapes,
      "B_geometry_unchanged_vs_r1a3":B["build_shapes"]==base_shapes and B["reopen_shapes"]==base_shapes,
      "A_B_geometry_identical":A["reopen_shapes"]==B["reopen_shapes"],
      "runtime_exact_rz90_relation":rotation_ok,
      "same_100ohm_reference":close(pa["port_ref_impedance"],100.0) and close(pb["port_ref_impedance"],100.0),
    }
    checks["pass"]=all(checks.values())

    summary={
      "base_cst":base_cst,
      "base_sha256":base_sha,
      "A":{k:v for k,v in A.items() if k not in ("build_shapes","reopen_shapes","reopen_params")},
      "B":{k:v for k,v in B.items() if k not in ("build_shapes","reopen_shapes","reopen_params")},
      "runtime_endpoints":{
        "A":{"p1":[pa["r1a5f_p1_x"],pa["r1a5f_p1_y"]],"p2":[pa["r1a5f_p2_x"],pa["r1a5f_p2_y"]],"rotation_deg":pa["r1a5f_rotation_deg"]},
        "B":{"p1":[pb["r1a5f_p1_x"],pb["r1a5f_p1_y"]],"p2":[pb["r1a5f_p2_x"],pb["r1a5f_p2_y"]],"rotation_deg":pb["r1a5f_rotation_deg"]},
      },
      "checks":checks,
      "solver_run":False,
    }
    with open(os.path.join(evidence,"harness_summary.json"),"w") as f:
        json.dump(summary,f,indent=2)
    with open(os.path.join(evidence,"harness_log.txt"),"w") as f:
        f.write("\n".join(A["log"]+B["log"])+"\n")

    status="PASS_R1A5F_SPLIT_SINGLE_PORT_BUILD_ONLY" if checks["pass"] else "HOLD_R1A5F_RUNTIME_AUDIT"
    print(status)
    print("A_CST_PATH="+A["cst"])
    print("A_CST_SHA256="+A["cst_sha256"])
    print("B_CST_PATH="+B["cst"])
    print("B_CST_SHA256="+B["cst_sha256"])
    print("A_REOPEN_PORT_COUNT="+str(A["reopen_port_count"]))
    print("B_REOPEN_PORT_COUNT="+str(B["reopen_port_count"]))
    print("RUNTIME_RZ90="+str(rotation_ok))
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--base-cst",required=True)
    a=ap.parse_args()
    try:
        run(a.repo,a.evidence,a.work,a.base_cst)
    except Exception as e:
        print("HOLD_R1A5F_CST_RUNTIME")
        print(type(e).__name__+":"+str(e))
        raise
