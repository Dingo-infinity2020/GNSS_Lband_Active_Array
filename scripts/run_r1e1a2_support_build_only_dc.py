"""R1E1A2 P094 mechanical-support BUILD-ONLY harness.
Creates six immutable support-inclusive scan-state sources. No solver API is called.
"""
from __future__ import print_function
import argparse, hashlib, json, os, shutil, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e"
REGISTRY=[
 ("S1_BONDED_B0","S1",0.0,45.0),
 ("S1_BONDED_C60P45","S1",60.0,45.0),
 ("S1_BONDED_C60P135","S1",60.0,135.0),
 ("S4_PEC_B0","S4",0.0,45.0),
]
SOLVER_MARKERS=("meshing successful","adaptive mesh refinement pass","running solver","excitation: port")

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def support_vba(kind):
    common=[
      'StoreParameter "support_center_abs", 30.0',
      'StoreParameter "support_post_half", 2.0',
      'StoreParameter "support_bond_half", 2.5',
      'StoreParameter "support_bond_t", 0.10',
    ]
    if kind=="S1":
        body=[
          'StoreParameter "support_foam_er", 1.05',
          'StoreParameter "support_foam_tand", 0.0002',
          'StoreParameter "support_adh_er", 4.0',
          'StoreParameter "support_adh_tand", 0.03',
          'With Material', '.Reset', '.Name "ROHACELL_31HF_LBAND_BASELINE"', '.Folder ""',
          '.FrqType "all"', '.Type "Normal"', '.SetMaterialUnit "GHz", "mm"',
          '.Epsilon "support_foam_er"', '.Mue "1.0"', '.TanD "support_foam_tand"',
          '.TanDFreq "0.0"', '.TanDGiven "False"', '.TanDModel "ConstTanD"', '.Create', 'End With',
          'With Material', '.Reset', '.Name "ADHESIVE_CONSERVATIVE_SURROGATE"', '.Folder ""',
          '.FrqType "all"', '.Type "Normal"', '.SetMaterialUnit "GHz", "mm"',
          '.Epsilon "support_adh_er"', '.Mue "1.0"', '.TanD "support_adh_tand"',
          '.TanDFreq "0.0"', '.TanDGiven "False"', '.TanDModel "ConstTanD"', '.Create', 'End With',
        ]
        for i,(sx,sy) in enumerate(((1,1),(-1,1),(-1,-1),(1,-1)),1):
            body += brick("FOAM_%d"%i,"ROHACELL_31HF_LBAND_BASELINE",sx,sy,
                          "support_post_half","support_bond_t","height_ground-support_bond_t")
            body += brick("BOND_BOT_%d"%i,"ADHESIVE_CONSERVATIVE_SURROGATE",sx,sy,
                          "support_bond_half","0","support_bond_t")
            body += brick("BOND_TOP_%d"%i,"ADHESIVE_CONSERVATIVE_SURROGATE",sx,sy,
                          "support_bond_half","height_ground-support_bond_t","height_ground")
        return "\n".join(common+body)

    if kind=="S4":
        body=[]
        for i,(sx,sy) in enumerate(((1,1),(-1,1),(-1,-1),(1,-1)),1):
            body += brick("PEC_POST_%d"%i,"PEC",sx,sy,"support_post_half","0","height_ground")
        return "\n".join(common+body)
    raise RuntimeError("unknown support kind")

def brick(name,mat,sx,sy,half,z1,z2):
    xc="support_center_abs" if sx>0 else "-support_center_abs"
    yc="support_center_abs" if sy>0 else "-support_center_abs"
    return [
      "With Brick", ".Reset", '.Name "%s"'%name, '.Component "SupportAssembly"',
      '.Material "%s"'%mat,
      '.Xrange "%s-%s", "%s+%s"'%(xc,half,xc,half),
      '.Yrange "%s-%s", "%s+%s"'%(yc,half,yc,half),
      '.Zrange "%s", "%s"'%(z1,z2), ".Create", "End With"
    ]

def scan_vba(theta,phi):
    return "\n".join([
      'StoreParameter "R1E1A2_scan_theta_deg", %g'%theta,
      'StoreParameter "R1E1A2_scan_phi_deg", %g'%phi,
      "With Boundary",
      '.SetPeriodicBoundaryAngles "R1E1A2_scan_theta_deg", "R1E1A2_scan_phi_deg"',
      '.SetPeriodicBoundaryAnglesDirection "outward"',
      "End With",
    ])

def audit_vba(shape_path,status_path,label):
    return "\n".join([
      "On Error Resume Next","Dim f As Integer","Dim i As Long","Dim nm As String",
      "Dim th As Double, ph As Double, idir As Long, scanok As Boolean",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "R1E1A2_%s_SHAPE_INVENTORY"'%label,
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+20"," nm=Solid.GetNameOfShapeFromIndex(i)",
      ' If Len(nm)>0 Then Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm))',
      "Next i","Close #f",
      "scanok = Boundary.GetUnitCellScanAngle(th, ph, idir)",
      "f=FreeFile", 'Open "%s" For Output As #f'%status_path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      'Print #f, "SCAN_VALID=" & CStr(scanok)',
      'Print #f, "SCAN_THETA_DEG=" & CStr(th)',
      'Print #f, "SCAN_PHI_DEG=" & CStr(ph)',
      'Print #f, "SCAN_DIRECTION=" & CStr(idir)',
      'Print #f, "UNITCELL_DS1=" & CStr(Boundary.GetUnitCellDs1)',
      'Print #f, "UNITCELL_DS2=" & CStr(Boundary.GetUnitCellDs2)',
      "Close #f","On Error GoTo 0"
    ])

def parse_status(path):
    out={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k.strip()]=v.strip()
    return out

def shape_lines(path):
    return [x for x in open(path,encoding="utf-8").read().splitlines() if x.startswith("SHAPE|")]

def parameter_map(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Model","Parameters.json")
    data=json.load(open(p,encoding="utf-8")); out={}
    def walk(x):
        if isinstance(x,dict):
            if "name" in x and "value" in x: out[str(x["name"])]=str(x["value"])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(data); return out

def result_tree_solver_items(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    items=pf.get_3d().get_tree_items()
    return [x for x in items if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def log_solver_hits(cstfile):
    p=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(p): return []
    low=open(p,encoding="utf-8",errors="ignore").read().lower()
    return [m for m in SOLVER_MARKERS if m in low]

def run_one(evidence,work,source,label,kind,theta,phi):
    edir=os.path.join(evidence,label); os.makedirs(edir)
    dst=os.path.join(work,"R1E1A2_%s_BUILD_ONLY_V01.cst"%label)
    shutil.copy2(source,dst)
    if sha(dst)!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A2_COPY_HASH_MISMATCH_"+label)
    bs=os.path.join(edir,"build_shapes.txt"); bt=os.path.join(edir,"build_status.txt")
    rs=os.path.join(edir,"reopen_shapes.txt"); rt=os.path.join(edir,"reopen_status.txt")
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("R1E1A2 support assembly "+kind,support_vba(kind))
        prj.modeler.add_to_history("R1E1A2 scan metadata",scan_vba(theta,phi))
        prj.modeler.add_to_history("R1E1A2 build audit",audit_vba(bs,bt,label))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    params_build=parameter_map(dst)
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.schematic.execute_vba_code("Sub Main()\n"+audit_vba(rs,rt,label)+"\nEnd Sub")
    finally:
        if prj is not None: prj.close()
        de.close()
    bsh=shape_lines(bs); rsh=shape_lines(rs); st=parse_status(rt); params=parameter_map(dst)
    expected=15 if kind=="S1" else 7
    checks={
      "shape_count_build":len(bsh)==expected,
      "shape_count_reopen":len(rsh)==expected,
      "build_reopen_shapes_identical":bsh==rsh,
      "port_count_1":int(st["PORT_COUNT"])==1,
      "theta_match":abs(float(st["SCAN_THETA_DEG"])-theta)<1e-9,
      "phi_match":abs(float(st["SCAN_PHI_DEG"])-phi)<1e-9,
      "unitcell_94":abs(float(st["UNITCELL_DS1"])-94.0)<1e-6 and abs(float(st["UNITCELL_DS2"])-94.0)<1e-6,
      "support_center_30":abs(float(params["support_center_abs"])-30.0)<1e-9,
      "support_post_half_2":abs(float(params["support_post_half"])-2.0)<1e-9,
      "no_solver_markers":len(log_solver_hits(dst))==0,
      "no_solver_result_items":len(result_tree_solver_items(dst))==0,
    }
    if kind=="S1":
        checks.update({
          "foam_er_1p05":abs(float(params["support_foam_er"])-1.05)<1e-9,
          "foam_tand_0p0002":abs(float(params["support_foam_tand"])-0.0002)<1e-12,
          "adh_er_4":abs(float(params["support_adh_er"])-4.0)<1e-9,
          "adh_tand_0p03":abs(float(params["support_adh_tand"])-0.03)<1e-12,
        })
    checks["pass"]=all(checks.values())
    return {"label":label,"kind":kind,"theta":theta,"phi":phi,"cst":dst,
            "sha256":sha(dst),"bytes":os.path.getsize(dst),"checks":checks,
            "parameters":{k:params.get(k) for k in ("support_center_abs","support_post_half","support_bond_half","support_bond_t","support_foam_er","support_foam_tand","support_adh_er","support_adh_tand")}}

def run(evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_R1E1A2_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_R1E1A2_WORK_EXISTS")
    if not os.path.isfile(source): raise RuntimeError("HOLD_R1E1A2_SOURCE_MISSING")
    if sha(source)!=SOURCE_SHA: raise RuntimeError("HOLD_R1E1A2_SOURCE_HASH_MISMATCH")
    os.makedirs(evidence); os.makedirs(work)
    results=[run_one(evidence,work,source,*x) for x in REGISTRY]
    top={"count_4":len(results)==4,"all_pass":all(x["checks"]["pass"] for x in results),
         "hashes_unique":len(set(x["sha256"] for x in results))==4}
    top["pass"]=all(top.values())
    summary={"mode":"R1E1A2_SUPPORT_BUILD_ONLY","solver_run":False,"results":results,"checks":top}
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    print("PASS_R1E1A2_SUPPORT_BUILD_ONLY" if top["pass"] else "HOLD_R1E1A2_SUPPORT_BUILD_ONLY")
    for x in results: print(x["label"]+"_SHA256="+x["sha256"])
    print(json.dumps(top,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence",required=True); ap.add_argument("--work",required=True); ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.evidence,a.work,a.source_cst)

