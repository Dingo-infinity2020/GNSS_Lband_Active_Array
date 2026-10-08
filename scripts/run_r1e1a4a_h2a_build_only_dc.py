"""H2A Universal Center Structure V0.1 — one-shot BUILD-ONLY harness."""
from __future__ import print_function
import argparse,hashlib,json,os,shutil,sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e"
SOLVER_MARKERS=("meshing successful","adaptive mesh refinement pass","running solver","excitation: port")

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def macro_body(path):
    lines=open(path,encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=lines.index("Sub Main()"); e=lines.index("End Sub")
    return "\n".join(lines[s+1:e])

def snapshot_tree(root):
    snap=[]
    if not os.path.isdir(root): return snap
    for d,_,files in os.walk(root):
        for name in files:
            q=os.path.join(d,name)
            with open(q,"rb") as f: snap.append((q,f.read()))
    return snap

def restore_snapshot(snap):
    changed=[]
    for q,data in snap:
        cur=None
        if os.path.isfile(q):
            with open(q,"rb") as f: cur=f.read()
        if cur!=data: changed.append(q)
        with open(q,"wb") as f: f.write(data)
    for q,data in snap:
        with open(q,"rb") as f:
            if f.read()!=data: raise RuntimeError("HOLD_H2A_PARENT_EVIDENCE_RESTORE_FAILED:"+q)
    return changed

def parameter_map(cstfile):
    q=os.path.join(os.path.splitext(cstfile)[0],"Model","Parameters.json")
    data=json.load(open(q,encoding="utf-8")); out={}
    def walk(x):
        if isinstance(x,dict):
            if "name" in x and "value" in x: out[str(x["name"])]=str(x["value"])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(data); return out

def solver_tree_items(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    return [x for x in pf.get_3d().get_tree_items()
            if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\Excitation" in x)]

def solver_log_hits(cstfile):
    q=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(q): return []
    low=open(q,encoding="utf-8",errors="ignore").read().lower()
    return [m for m in SOLVER_MARKERS if m in low]

def audit_vba(shape_path,status_path):
    return "\n".join([
      "On Error Resume Next","Dim f As Integer, i As Long, nm As String",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "H2A_SHAPE_INVENTORY"',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+40",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      ' If Len(nm)>0 Then Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm))',
      "Next i","Close #f",
      "scanok=Boundary.GetUnitCellScanAngle(th,ph,idir)",
      "f=FreeFile", 'Open "%s" For Output As #f'%status_path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "SCAN_VALID=" & CStr(scanok)',
      'Print #f, "THETA=" & CStr(th)', 'Print #f, "PHI=" & CStr(ph)',
      'Print #f, "DS1=" & CStr(Boundary.GetUnitCellDs1)',
      'Print #f, "DS2=" & CStr(Boundary.GetUnitCellDs2)',
      "Close #f","On Error GoTo 0"
    ])

def parse_kv(path):
    d={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); d[k.strip()]=v.strip()
    return d

def shape_rows(path):
    out=[]
    for line in open(path,encoding="utf-8").read().splitlines():
        if line.startswith("SHAPE|"):
            _,name,vol=line.split("|",2)
            out.append((name,float(vol.split("=",1)[1])))
    return out

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_H2A_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_H2A_WORK_EXISTS")
    if not os.path.isfile(source) or sha(source)!=SOURCE_SHA:
        raise RuntimeError("HOLD_H2A_SOURCE_HASH_MISMATCH")

    macro=os.path.join(repo,"source","cst","R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY_V01.mcr")
    if not os.path.isfile(macro): raise RuntimeError("HOLD_H2A_MACRO_MISSING")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY_V01.cst")
    shutil.copy2(source,dst)
    if sha(dst)!=SOURCE_SHA: raise RuntimeError("HOLD_H2A_COPY_HASH_MISMATCH")

    parent_ev=os.path.join(repo,"evidence","r1e1a1_dc_nw_20260924_build01","P094")
    snap=snapshot_tree(parent_ev); rewrites=[]
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("H2A Universal Center Structure V0.1",macro_body(macro))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    shapes=os.path.join(evidence,"reopen_shapes.txt")
    status=os.path.join(evidence,"reopen_status.txt")
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.schematic.execute_vba_code("Sub Main()\n"+audit_vba(shapes,status)+"\nEnd Sub")
    finally:
        if prj is not None: prj.close()
        de.close()
        rewrites=restore_snapshot(snap)

    rows=shape_rows(shapes); names={x[0] for x in rows}; st=parse_kv(status); params=parameter_map(dst)
    expected={
      "UnitCellGround:UNITCELL_GROUND_REFERENCE","Substrate:FR4_BOARD","TopCopper:TOP_COPPER",
      "H2A_FeedModule:GROUND_N","H2A_FeedModule:GROUND_S","H2A_FeedModule:GROUND_E","H2A_FeedModule:GROUND_W",
      "H2A_FeedModule:PAD_NE","H2A_FeedModule:PAD_NW","H2A_FeedModule:PAD_SW","H2A_FeedModule:PAD_SE",
      "H2A_FeedModule:PIN_NE","H2A_FeedModule:PIN_NW","H2A_FeedModule:PIN_SW","H2A_FeedModule:PIN_SE",
      "H2A_PopulationEnvelope:LNA_ENV_NE","H2A_PopulationEnvelope:LNA_ENV_NW",
      "H2A_PopulationEnvelope:LNA_ENV_SW","H2A_PopulationEnvelope:LNA_ENV_SE",
      "H2A_Shield:SHIELD_N","H2A_Shield:SHIELD_S","H2A_Shield:SHIELD_E","H2A_Shield:SHIELD_W","H2A_Shield:SHIELD_LID",
      "H2A_Carrier:CARRIER_N","H2A_Carrier:CARRIER_S","H2A_Carrier:CARRIER_E","H2A_Carrier:CARRIER_W",
    }
    checks={
      "shape_count_28":len(rows)==28,
      "shape_names_exact":names==expected,
      "port_count_zero":int(st["PORT_COUNT"])==0,
      "unitcell_94":abs(float(st["DS1"])-94.0)<1e-6 and abs(float(st["DS2"])-94.0)<1e-6,
      "broadside":abs(float(st["THETA"]))<1e-9,
      "ground_outer_20":abs(float(params["h2a_ground_outer_half"])-10.0)<1e-9,
      "clear_window_8":abs(float(params["h2a_clear_half"])-4.0)<1e-9,
      "pad_0p9":abs(float(params["h2a_pad_half"])-0.45)<1e-9,
      "pin_0p3":abs(float(params["h2a_pin_half"])-0.15)<1e-9,
      "package_r_6p2":abs(float(params["h2a_package_r"])-6.2)<1e-9,
      "shield_outer_18":abs(float(params["h2a_shield_outer_half"])-9.0)<1e-9,
      "carrier_outer_30":abs(float(params["h2a_carrier_outer_half"])-15.0)<1e-9,
      "carrier_inner_21":abs(float(params["h2a_carrier_inner_half"])-10.5)<1e-9,
      "no_solver_markers":len(solver_log_hits(dst))==0,
      "no_solver_result_items":len(solver_tree_items(dst))==0,
      "parent_evidence_restored":True,
    }
    checks["pass"]=all(checks.values())

    summary={"mode":"R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY","solver_run":False,
      "source_sha256":SOURCE_SHA,"result_cst":dst,"result_sha256":sha(dst),
      "result_bytes":os.path.getsize(dst),"parent_evidence_rewrites_detected":rewrites,
      "shape_count":len(rows),"parameters":{k:params.get(k) for k in (
        "h2a_ground_outer_half","h2a_clear_half","h2a_pad_half","h2a_pin_half",
        "h2a_terminal_xy","h2a_package_r","h2a_package_xy","h2a_package_h",
        "h2a_shield_outer_half","h2a_shield_wall","h2a_shield_depth",
        "h2a_carrier_outer_half","h2a_carrier_inner_half")},"checks":checks}
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    print("PASS_R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY" if checks["pass"] else "HOLD_R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY")
    print("RESULT_SHA256="+summary["result_sha256"])
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True); ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work,a.source_cst)
