"""R1A4 differential-port BUILD-ONLY harness for NW/DC."""
import argparse, hashlib, json, os, shutil, sys

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

def audit_macro(shape_path,param_path,status_path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer","Dim i As Long","Dim nm As String",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1A4_SHAPE_INVENTORY"',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+10",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      '  Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm)) & "|area=" & CStr(Solid.GetArea(nm))',
      " End If","Next i","Close #f",
      "f=FreeFile", 'Open "%s" For Output As #f'%param_path,
      'Print #f, "R1A4_PARAMETER_INVENTORY"',
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

def run(repo,evidence,work,base_cst):
    if os.path.exists(evidence):
        raise RuntimeError("HOLD_R1A4_EVIDENCE_DIR_ALREADY_EXISTS")
    if os.path.exists(work):
        raise RuntimeError("HOLD_R1A4_WORK_DIR_ALREADY_EXISTS")
    if not os.path.isfile(base_cst):
        raise RuntimeError("HOLD_R1A4_BASE_CST_MISSING")
    base_sha=sha(base_cst)
    if base_sha != BASE_SHA:
        raise RuntimeError("HOLD_R1A4_BASE_CST_HASH_MISMATCH:"+base_sha)

    os.makedirs(evidence)
    os.makedirs(work)
    macro=os.path.join(repo,"source","cst","R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.mcr")
    dst=os.path.join(work,"R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst")
    shutil.copy2(base_cst,dst)
    pre_port_sha=sha(dst)
    if pre_port_sha != base_sha:
        raise RuntimeError("HOLD_R1A4_COPY_HASH_MISMATCH")

    log=[
      "BASE_CST_SHA256="+base_sha,
      "PRE_PORT_COPY_SHA256="+pre_port_sha,
      "PORT_MACRO_SHA256="+sha(macro),
    ]

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1A4 add two ideal differential ports",body(macro))
        prj.save()
        log.append("PORT_BUILD_SAVE_PASS")
        prj.modeler.add_to_history("R1A4 immediate audit",audit_macro(
          os.path.join(evidence,"build_object_inventory.txt"),
          os.path.join(evidence,"build_parameter_inventory.txt"),
          os.path.join(evidence,"build_port_status.txt")))
        log.append("BUILD_AUDIT_PASS")
    finally:
        if prj is not None: prj.close()
        de.close()

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1A4 reopen audit",audit_macro(
          os.path.join(evidence,"reopen_object_inventory.txt"),
          os.path.join(evidence,"reopen_parameter_inventory.txt"),
          os.path.join(evidence,"reopen_port_status.txt")))
        prj.modeler.add_to_history("R1A4 top view",shot("Front",os.path.join(evidence,"top_view.png")))
        prj.modeler.add_to_history("R1A4 perspective",shot("Perspective",os.path.join(evidence,"oblique_view.png")))
        log.append("FRESH_REOPEN_AUDIT_PASS")
    finally:
        if prj is not None: prj.close()
        de.close()

    base_inventory=os.path.join(repo,"evidence","r1a3_dc_nw_20260924_build01","object_inventory.txt")
    base_shapes=shape_lines(base_inventory)
    build_shapes=shape_lines(os.path.join(evidence,"build_object_inventory.txt"))
    reopen_shapes=shape_lines(os.path.join(evidence,"reopen_object_inventory.txt"))
    build_ports=port_count(os.path.join(evidence,"build_port_status.txt"))
    reopen_ports=port_count(os.path.join(evidence,"reopen_port_status.txt"))

    checks={
      "base_hash_match": base_sha==BASE_SHA,
      "copy_hash_match_before_port": pre_port_sha==BASE_SHA,
      "build_port_count_2": build_ports==2,
      "reopen_port_count_2": reopen_ports==2,
      "geometry_unchanged_vs_r1a3": build_shapes==base_shapes,
      "fresh_reopen_geometry_same": reopen_shapes==build_shapes,
    }
    checks["pass"]=all(checks.values())
    summary={
      "base_cst":base_cst,
      "base_sha256":base_sha,
      "pre_port_copy_sha256":pre_port_sha,
      "port_macro_sha256":sha(macro),
      "r1a4_cst":dst,
      "r1a4_cst_sha256":sha(dst),
      "r1a4_cst_bytes":os.path.getsize(dst),
      "build_port_count":build_ports,
      "reopen_port_count":reopen_ports,
      "checks":checks,
      "log":log,
      "solver_run":False,
    }
    open(os.path.join(evidence,"harness_summary.json"),"w").write(json.dumps(summary,indent=2))
    open(os.path.join(evidence,"harness_log.txt"),"w").write("\n".join(log)+"\n")
    status="PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY" if checks["pass"] else "HOLD_R1A4_RUNTIME_AUDIT"
    print(status)
    print("R1A4_CST_PATH="+dst)
    print("R1A4_CST_SHA256="+summary["r1a4_cst_sha256"])
    print("R1A4_CST_BYTES="+str(summary["r1a4_cst_bytes"]))
    print("BUILD_PORT_COUNT="+str(build_ports))
    print("REOPEN_PORT_COUNT="+str(reopen_ports))
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
        print("HOLD_R1A4_CST_RUNTIME")
        print(type(e).__name__+":"+str(e))
        raise
