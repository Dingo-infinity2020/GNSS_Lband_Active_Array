"""H2A V0.2 Service Architecture — one-shot BUILD-ONLY harness."""
from __future__ import print_function
import argparse,hashlib,json,os,shutil,sys
from collections import Counter

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
            if f.read()!=data: raise RuntimeError("HOLD_H2AV02_PARENT_EVIDENCE_RESTORE_FAILED:"+q)
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
      'Print #f, "H2AV02_SHAPE_INVENTORY"',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+80",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      ' If Len(nm)>0 Then Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm))',
      "Next i","Close #f",
      "scanok=Boundary.GetUnitCellScanAngle(th,ph,idir)",
      "f=FreeFile", 'Open "%s" For Output As #f'%status_path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "SCAN_VALID=" & CStr(scanok)',
      'Print #f, "THETA=" & CStr(th)','Print #f, "PHI=" & CStr(ph)',
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

def component_counts(rows):
    c=Counter()
    for name,_ in rows:
        comp=name.split(":",1)[0]
        c[comp]+=1
    return dict(c)

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_H2AV02_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_H2AV02_WORK_EXISTS")
    if not os.path.isfile(source) or sha(source)!=SOURCE_SHA:
        raise RuntimeError("HOLD_H2AV02_SOURCE_HASH_MISMATCH")

    macro=os.path.join(repo,"source","cst","R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY_V01.mcr")
    if not os.path.isfile(macro): raise RuntimeError("HOLD_H2AV02_MACRO_MISSING")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY_V01.cst")
    shutil.copy2(source,dst)
    if sha(dst)!=SOURCE_SHA: raise RuntimeError("HOLD_H2AV02_COPY_HASH_MISMATCH")

    parent_ev=os.path.join(repo,"evidence","r1e1a1_dc_nw_20260924_build01","P094")
    snap=snapshot_tree(parent_ev); rewrites=[]
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("H2A V0.2 Service Architecture",macro_body(macro))
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

    rows=shape_rows(shapes); counts=component_counts(rows)
    st=parse_kv(status); params=parameter_map(dst)

    expected_counts={
      "UnitCellGround":1,
      "Substrate":1,
      "TopCopper":1,
      "H2A_FeedModule":12,
      "H2A_PopulationEnvelope":4,
      "H2A_Shield":5,
      "H2A_ServiceConnector":8,
      "H2A_ServiceRouting":12,
      "H2A_ServiceTube":4,
      "H2A_ServiceInterface":8,
    }
    checks={
      "shape_count_56":len(rows)==56,
      "component_counts_exact":all(counts.get(k,0)==v for k,v in expected_counts.items()) and
                               set(counts)==set(expected_counts),
      "no_old_carrier_component":"H2A_Carrier" not in counts,
      "no_tools_remaining":"H2A_Tools" not in counts,
      "port_count_zero":int(st["PORT_COUNT"])==0,
      "unitcell_94":abs(float(st["DS1"])-94.0)<1e-6 and abs(float(st["DS2"])-94.0)<1e-6,
      "broadside":abs(float(st["THETA"]))<1e-9,
      "mhf_radius_9":abs(float(params["h2av02_mhf_r"])-9.0)<1e-9,
      "tube_radius_13p5":abs(float(params["h2av02_tube_r"])-13.5)<1e-9,
      "tube_outer_3mm":abs(float(params["h2av02_tube_outer_half"])-1.5)<1e-9,
      "tube_inner_1p4mm":abs(float(params["h2av02_tube_inner_half"])-0.7)<1e-9,
      "microcoax_0p81":abs(2*float(params["h2av02_cable_half"])-0.81)<1e-9,
      "spacer_t_0p5":abs(float(params["h2av02_spacer_t"])-0.5)<1e-9,
      "mmcx_envelope_5mm":abs(float(params["h2av02_mmcx_half"])-2.5)<1e-9,
      "no_solver_markers":len(solver_log_hits(dst))==0,
      "no_solver_result_items":len(solver_tree_items(dst))==0,
      "parent_evidence_restored":True,
    }
    checks["pass"]=all(checks.values())

    summary={
      "mode":"R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY",
      "solver_run":False,
      "source_sha256":SOURCE_SHA,
      "result_cst":dst,
      "result_sha256":sha(dst),
      "result_bytes":os.path.getsize(dst),
      "parent_evidence_rewrites_detected":rewrites,
      "shape_count":len(rows),
      "component_counts":counts,
      "parameters":{k:params.get(k) for k in (
        "h2av02_mhf_r","h2av02_mhf_half","h2av02_tube_r",
        "h2av02_tube_outer_half","h2av02_tube_inner_half",
        "h2av02_spacer_t","h2av02_feedthrough_half",
        "h2av02_cable_half","h2av02_mmcx_half")},
      "checks":checks,
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f:
        json.dump(summary,f,indent=2)
    print("PASS_R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY" if checks["pass"]
          else "HOLD_R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY")
    print("RESULT_SHA256="+summary["result_sha256"])
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work,a.source_cst)
