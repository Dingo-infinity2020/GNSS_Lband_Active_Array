from __future__ import print_function
import os, sys, json, math, re, shutil, hashlib, subprocess, statistics, traceback
from pathlib import Path

REPO=Path(r"D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold")
ROOT=Path(r"D:\GNSS_Lband_Active_Array")
RUN="r1e1a4a_h3b_t01a_o3_o4_nw_20260926_run01"
EVID=REPO/"evidence"/RUN
O3ROOT=ROOT/"_r1e1a4a_h3b_t01a_o3_work"
O4ROOT=ROOT/"_r1e1a4a_h3b_t01a_o4_work"
ARCHIVE=ROOT/"archive"/("20260926_"+RUN)
WINNER_MACRO=REPO/"evidence"/"r1e1a4a_h3b_t01a_o2b_nw_20260926_run01"/"P20_G30_E30"/"build_macro.mcr"
REF_MACRO=REPO/"evidence"/"r1e1a4a_h3b_t01a_o1_nw_20260926_run01"/"W15_G40"/"build_macro.mcr"
PORT_TRANS=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_PORTS_V01.mcr"
PORT_REF=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_O1_PORTS_V01.mcr"
SOLVER=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_SOLVER_CONFIG_MAXPASS16_V01.mcr"
LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

COPPER_SIGMA=5.8e7
SOLDER_SIGMA=7.0e6
CORE=(1.15,1.65)
ACCEPT_RL=-12.0
PREF_RL=-15.0
ACCEPT_EXCESS=0.15
PREF_EXCESS=0.10
RECIP=0.05
S21_FLOOR=-3.0

def git(*a):
    return subprocess.check_output(["git"]+list(a),cwd=str(REPO),universal_newlines=True).strip()

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def body_text(txt):
    a=txt.replace("\r\n","\n").split("\n")
    return "\n".join(a[a.index("Sub Main()")+1:a.index("End Sub")])

def body_file(p):
    return body_text(Path(p).read_text(encoding="utf-8"))

def fmt(x):
    s=("%.6f"%x).rstrip("0").rstrip(".")
    return "0" if s in ("-0","") else s

def material_block():
    return f'''    With Material
        .Reset
        .Name "O3_COPPER"
        .Folder ""
        .FrqType "all"
        .Type "Lossy metal"
        .SetMaterialUnit "GHz", "mm"
        .Mue "1.0"
        .Sigma "{COPPER_SIGMA:.8g}"
        .Create
    End With

    With Material
        .Reset
        .Name "O3_SOLDER_PROXY"
        .Folder ""
        .FrqType "all"
        .Type "Lossy metal"
        .SetMaterialUnit "GHz", "mm"
        .Mue "1.0"
        .Sigma "{SOLDER_SIGMA:.8g}"
        .Create
    End With

'''

def apply_finite_materials(src, has_solder=True):
    marker='    With Brick'
    if marker not in src:
        raise RuntimeError("macro has no Brick marker")
    src=src.replace(marker,material_block()+marker,1)
    lines=src.splitlines()
    current=""
    out=[]
    copper_count=0; solder_count=0
    for line in lines:
        m=re.search(r'\.Name "([^"]+)"',line)
        if m: current=m.group(1)
        if '.Material "PEC"' in line:
            if has_solder and current.startswith("SOLDER_"):
                line=line.replace('"PEC"','"O3_SOLDER_PROXY"'); solder_count+=1
            else:
                line=line.replace('"PEC"','"O3_COPPER"'); copper_count+=1
        out.append(line)
    if copper_count < 4:
        raise RuntimeError("too few copper replacements")
    if has_solder and solder_count != 3:
        raise RuntimeError("expected 3 solder replacements, got %d"%solder_count)
    return "\n".join(out)+"\n", {"copper_assignments":copper_count,"solder_assignments":solder_count}

def replace_exact(src, old, new, n):
    got=src.count(old)
    if got!=n: raise RuntimeError("replace count mismatch %r got=%d expected=%d"%(old,got,n))
    return src.replace(old,new)

def fab_corner(src, w, gap):
    src=replace_exact(src,'StoreParameter "h3b_t01_wsig", 1.5','StoreParameter "h3b_t01_wsig", %s'%fmt(w),1)
    src=replace_exact(src,'StoreParameter "h3b_t01_gap", 0.4','StoreParameter "h3b_t01_gap", %s'%fmt(gap),1)
    hw=w/2.0
    src=replace_exact(src,'.Xrange "-0.75", "0.75"','.Xrange "%s", "%s"'%(fmt(-hw),fmt(hw)),2)
    return src

def shift_vertical_x(src, dx):
    names=("VERTICAL_FR4","V_SIG","V_GND_L","V_GND_R","V_BACK_GND",
           "V_PAD_SIG","V_PAD_GND_L","V_PAD_GND_R")
    lines=src.splitlines(); out=[]; current=""
    for line in lines:
        m=re.search(r'\.Name "([^"]+)"',line)
        if m: current=m.group(1)
        do_shift=current in names or current.startswith("V_VIAHOLE_") or current.startswith("V_VIA_")
        if do_shift and ".Xrange " in line:
            m=re.search(r'\.Xrange "([^"]+)", "([^"]+)"',line)
            if m:
                a=float(m.group(1))+dx; b=float(m.group(2))+dx
                line=re.sub(r'\.Xrange "([^"]+)", "([^"]+)"','.Xrange "%s", "%s"'%(fmt(a),fmt(b)),line)
        if do_shift and ".Xcenter " in line:
            m=re.search(r'\.Xcenter "([^"]+)"',line)
            if m:
                a=float(m.group(1))+dx
                line=re.sub(r'\.Xcenter "([^"]+)"','.Xcenter "%s"'%fmt(a),line)
        out.append(line)
    return "\n".join(out)+"\n"

def solder_scale(src, scale):
    y1=0.535
    y2=y1+(1.0-y1)*scale
    z2=-0.035
    z1=z2-((-0.035)-(-0.45))*scale
    lines=src.splitlines(); out=[]; current=""
    changed_y=0; changed_z=0
    for line in lines:
        m=re.search(r'\.Name "([^"]+)"',line)
        if m: current=m.group(1)
        if current.startswith("SOLDER_") and '.Yrange "0.535", "1"' in line:
            line='        .Yrange "%s", "%s"'%(fmt(y1),fmt(y2)); changed_y+=1
        if current.startswith("SOLDER_") and '.Zrange "-0.45", "-0.035"' in line:
            line='        .Zrange "%s", "%s"'%(fmt(z1),fmt(z2)); changed_z+=1
        out.append(line)
    if changed_y!=3 or changed_z!=3:
        raise RuntimeError("solder transform mismatch y=%d z=%d"%(changed_y,changed_z))
    return "\n".join(out)+"\n"

def aligned_ports(dx):
    s=PORT_TRANS.read_text(encoding="utf-8")
    s=replace_exact(s,'.SetP1 "False", "0.0", "0.535", "-12.0"',
                    '.SetP1 "False", "%s", "0.535", "-12.0"'%fmt(dx),1)
    s=replace_exact(s,'.SetP2 "False", "0.0", "-0.535", "-12.0"',
                    '.SetP2 "False", "%s", "-0.535", "-12.0"'%fmt(dx),1)
    return s

def audit_vba(shape,status,inter):
    return '''Sub Main()
On Error Resume Next
Dim f As Integer, i As Long, nm As String
f=FreeFile
Open "%s" For Output As #f
Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())
For i=0 To Solid.GetNumberOfShapes()+160
 nm=Solid.GetNameOfShapeFromIndex(i)
 If Len(nm)>0 Then Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm))
Next i
Close #f
f=FreeFile
Open "%s" For Output As #f
Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())
Close #f
f=FreeFile
Open "%s" For Output As #f
Print #f, "STARTED=TRUE"
Close #f
RunCommand "CDCheckModelIntersections"
f=FreeFile
Open "%s" For Append As #f
Print #f, "RETURNED=TRUE"
Close #f
End Sub'''%(shape,status,inter,inter)

def port_vba(p):
    return '''Sub Main()
Dim f As Integer
f=FreeFile
Open "%s" For Output As #f
Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())
Close #f
End Sub'''%p

def get_result_data(p3,item):
    errs=[]
    for rid in [None,0,1,2,3,4,5]:
        try:
            obj=p3.get_result_item(item) if rid is None else p3.get_result_item(item,rid)
            return obj.get_data()
        except Exception as e:
            errs.append(str(e))
    raise RuntimeError("cannot read result %s: %s"%(item," | ".join(errs[-3:])))

def read_s(cst):
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
    tree=p3.get_tree_items(); out={}
    for i,j in ((1,1),(1,2),(2,1),(2,2)):
        item=r"1D Results\S-Parameters\S%d,%d"%(i,j)
        if item not in tree: raise RuntimeError("missing "+item)
        dat=get_result_data(p3,item)
        out["S%d%d"%(i,j)]=[(float(r[0]),complex(r[1])) for r in dat]
    return out

def read_adapt(cst):
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
    tree=p3.get_tree_items()
    hits=[x for x in tree if "Adaptive Meshing" in x and x.endswith(r"S-Parameters\Delta\All S-Parameters")]
    for h in hits:
        try:
            dat=get_result_data(p3,h)
            if dat:
                return [{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real),"source":"api"} for r in dat]
        except Exception:
            pass
    out=Path(os.path.splitext(str(cst))[0])/"Result"/"output.txt"
    if not out.exists(): return []
    seq=[]; cur=None
    for line in out.read_text(encoding="utf-8",errors="ignore").splitlines():
        m=re.search(r"Adaptive mesh refinement pass\s+(\d+)",line)
        if m: cur=int(m.group(1)); continue
        m=re.search(r"All S-Parameters\s*=\s*([0-9.eE+-]+)",line)
        if m and cur is not None: seq.append({"pass":cur,"delta_s":float(m.group(1)),"source":"native_log"})
    dedup={}
    for row in seq: dedup[row["pass"]]=row
    return [dedup[p] for p in sorted(dedup)]

def interp_complex(vals,x):
    vals=sorted(vals,key=lambda r:r[0])
    if x<=vals[0][0]: return vals[0][1]
    if x>=vals[-1][0]: return vals[-1][1]
    for a,b in zip(vals,vals[1:]):
        if a[0]<=x<=b[0]:
            t=(x-a[0])/(b[0]-a[0])
            return a[1]+t*(b[1]-a[1])

def db(z):
    return 20*math.log10(max(abs(z),1e-300))

def metrics(data,ref=None):
    s11=[db(z) for f,z in data["S11"] if CORE[0]<=f<=CORE[1]]
    s22=[db(z) for f,z in data["S22"] if CORE[0]<=f<=CORE[1]]
    s21=[db(z) for f,z in data["S21"] if CORE[0]<=f<=CORE[1]]
    rec=[]
    for (f,a),(g,b) in zip(data["S21"],data["S12"]):
        rec.append(abs(db(a)-db(b)))
    m={"worst_core_return_db":max(max(s11),max(s22)),
       "core_s21_min_db":min(s21),"core_s21_max_db":max(s21),
       "reciprocity_max_abs_db":max(rec)}
    if ref is not None:
        ex=[]
        for f,z in data["S21"]:
            if CORE[0]<=f<=CORE[1]:
                ex.append(db(interp_complex(ref["S21"],f))-db(z))
        m.update({"junction_excess_min_db":min(ex),
                  "junction_excess_max_db":max(ex),
                  "junction_excess_median_db":statistics.median(ex)})
    return m

def write_s2p(path,data):
    # Touchstone 1.0, GHz, S, RI, 50 ohm; order S11 S21 S12 S22.
    rows=[]
    n=min(len(data["S11"]),len(data["S21"]),len(data["S12"]),len(data["S22"]))
    rows.append("! T01-A finite-conductivity nominal export")
    rows.append("# GHZ S RI R 50")
    for k in range(n):
        f=data["S11"][k][0]
        vals=[data["S11"][k][1],data["S21"][k][1],data["S12"][k][1],data["S22"][k][1]]
        rows.append(("%.12g "%f)+" ".join("%.12g %.12g"%(v.real,v.imag) for v in vals))
    Path(path).write_text("\n".join(rows)+"\n",encoding="utf-8")

def build_model(name,macro_text,work_root,evid_dir,expected_shapes):
    work=work_root/name; work.mkdir(parents=True)
    cst=work/(name+"_BUILD_ONLY.cst")
    macrofile=evid_dir/"build_macro.mcr"; macrofile.write_text(macro_text,encoding="utf-8")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.new_mws(); prj.modeler.add_to_history(name+" build",body_text(macro_text))
        prj.save(str(cst),include_results=False)
    finally:
        if prj is not None: prj.close()
        de.close()
    bh=sha(cst); shape=evid_dir/"build_shapes.txt"; stat=evid_dir/"build_status.txt"; inter=evid_dir/"intersection_status.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(cst)); ok=bool(prj.schematic.execute_vba_code(audit_vba(str(shape),str(stat),str(inter))))
    finally:
        if prj is not None: prj.close()
        de.close()
    rows=[x for x in shape.read_text().splitlines() if x.startswith("SHAPE|")]
    vols=[float(x.split("volume=",1)[1]) for x in rows]
    tree=ProjectFile(str(cst),allow_interactive=True).get_3d().get_tree_items()
    outp=Path(os.path.splitext(str(cst))[0])/"Result"/"output.txt"
    checks={"shape_count":len(rows)==expected_shapes,"shape_count_observed":len(rows),
            "all_volumes_positive":all(v>0 for v in vols),
            "port_count_zero":"PORT_COUNT=0" in stat.read_text(),
            "intersection_returned":ok and "RETURNED=TRUE" in inter.read_text(),
            "no_solver_output":not outp.exists(),
            "no_solver_results":not any("S-Parameters" in x or "Adaptive Meshing" in x for x in tree),
            "reopen_hash_stable":sha(cst)==bh}
    json.dump({"build_sha256":bh,"checks":checks},open(str(evid_dir/"build_summary.json"),"w"),indent=2)
    if not (checks["shape_count"] and checks["all_volumes_positive"] and checks["port_count_zero"] and
            checks["intersection_returned"] and checks["no_solver_output"] and checks["no_solver_results"] and checks["reopen_hash_stable"]):
        raise RuntimeError("BUILD_HOLD %s %s"%(name,json.dumps(checks)))
    return cst,bh

def solve_model(name,build_cst,ports_text,work_root,evid_dir,ref=None):
    solved=work_root/name/(name+"_SOLVED.cst")
    shutil.copy2(str(build_cst),str(solved))
    buildsha=sha(build_cst)
    if sha(solved)!=buildsha: raise RuntimeError("immutable copy mismatch "+name)
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(solved)); prj.modeler.add_to_history(name+" ports",body_text(ports_text))
        prj.modeler.add_to_history(name+" solver",body_file(SOLVER)); prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()
    configured=sha(solved); ps=evid_dir/"presolve_status.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(solved)); prj.schematic.execute_vba_code(port_vba(str(ps)))
    finally:
        if prj is not None: prj.close()
        de.close()
    if "PORT_COUNT=2" not in ps.read_text() or sha(solved)!=configured:
        raise RuntimeError("presolve reopen audit failed "+name)
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(solved)); prj.modeler.run_solver(); prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()
    data=read_s(solved); ad=read_adapt(solved); m=metrics(data,ref)
    num=len(ad)>=2 and ad[-2]["delta_s"]<=0.02 and ad[-1]["delta_s"]<=0.02
    out={"build_sha256":buildsha,"configured_sha256":configured,"solved_sha256":sha(solved),
         "formal_solver_invocations":1,"adaptive_delta_sequence":ad,"numerically_qualified":num,
         "passes_executed":ad[-1]["pass"] if ad else None,
         "final_two_delta_s":[ad[-2]["delta_s"],ad[-1]["delta_s"]] if len(ad)>=2 else None,
         "metrics":m}
    json.dump(out,open(str(evid_dir/"solve_summary.json"),"w"),indent=2)
    return solved,data,out

def close_auth(st):
    for k in st["authorization"]: st["authorization"][k]=False

def archive_work():
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    moved=[]
    for p in (O3ROOT,O4ROOT):
        if p.exists():
            dst=ARCHIVE/p.name
            if dst.exists(): raise RuntimeError("archive destination exists "+str(dst))
            shutil.move(str(p),str(dst)); moved.append(str(dst))
    (EVID/"ARCHIVE_MANIFEST.txt").write_text("\n".join(moved)+"\n",encoding="utf-8")

# ---------- preflight ----------
HEAD=git("rev-parse","HEAD")
if git("status","--porcelain"): raise RuntimeError("working tree not clean at start")
st=json.loads((REPO/"execution"/"stage_contract.json").read_text(encoding="utf-8"))
if st["execution"]["current_stage"]!="R1E1A4A_H3B_T01A_O3_PHYSICAL_FIDELITY_QUALIFICATION_AUTHORIZED":
    raise RuntimeError("wrong stage: "+st["execution"]["current_stage"])
if not st["authorization"].get("BUILD_AUTHORIZED") or not st["authorization"].get("SOLVE_AUTHORIZED"):
    raise RuntimeError("O3/O4 authorization not open")
for p in (EVID,O3ROOT,O4ROOT):
    if p.exists(): raise RuntimeError("destination exists "+str(p))
EVID.mkdir(parents=True); O3ROOT.mkdir(); O4ROOT.mkdir()

winner_src=WINNER_MACRO.read_text(encoding="utf-8")
ref_src=REF_MACRO.read_text(encoding="utf-8")
nom_macro,nom_mat=apply_finite_materials(winner_src,True)
ref_macro,ref_mat=apply_finite_materials(ref_src,False)

# Freeze text evidence before build.
freeze={"source_head":HEAD,"candidate":"P20_G30_E30",
        "copper_sigma_s_per_m":COPPER_SIGMA,"solder_proxy_sigma_s_per_m":SOLDER_SIGMA,
        "o3_acceptance":{"acceptable_return_db":ACCEPT_RL,"preferred_return_db":PREF_RL,
                         "acceptable_excess_db":ACCEPT_EXCESS,"preferred_excess_db":PREF_EXCESS,
                         "s21_floor_db":S21_FLOOR,"reciprocity_db":RECIP},
        "o4_cases":["FAB_LOWZ","FAB_HIGHZ","ALIGN_P020","ALIGN_M020","SOLDER_SMALL","SOLDER_LARGE"]}
json.dump(freeze,open(str(EVID/"FREEZE.json"),"w"),indent=2)

try:
    # ---------- O3: build both before solving ----------
    nom_e=EVID/"O3_NOMINAL"; ref_e=EVID/"O3_STRAIGHT_REF"; nom_e.mkdir(); ref_e.mkdir()
    nom_build,nom_bsha=build_model("O3_NOMINAL",nom_macro,O3ROOT,nom_e,38)
    ref_build,ref_bsha=build_model("O3_STRAIGHT_REF",ref_macro,O3ROOT,ref_e,21)

    # Solve reference first, then nominal paired against it.
    ref_solved,ref_data,ref_res=solve_model("O3_STRAIGHT_REF",ref_build,PORT_REF.read_text(encoding="utf-8"),O3ROOT,ref_e,None)
    nom_solved,nom_data,nom_res=solve_model("O3_NOMINAL",nom_build,PORT_TRANS.read_text(encoding="utf-8"),O3ROOT,nom_e,ref_data)
    mm=nom_res["metrics"]
    o3_pass=(ref_res["numerically_qualified"] and nom_res["numerically_qualified"] and
             mm["worst_core_return_db"]<=ACCEPT_RL and mm["junction_excess_max_db"]<=ACCEPT_EXCESS and
             mm["core_s21_min_db"]>=S21_FLOOR and mm["reciprocity_max_abs_db"]<=RECIP)
    o3_pref=(mm["worst_core_return_db"]<=PREF_RL and mm["junction_excess_max_db"]<=PREF_EXCESS)
    o3={"status":"PASS" if o3_pass else "HOLD","preferred_gate":o3_pref,
        "nominal":nom_res,"straight_reference":ref_res,"materials":freeze}
    json.dump(o3,open(str(EVID/"O3_SUMMARY.json"),"w"),indent=2)
    if not o3_pass:
        status="HOLD_R1E1A4A_H3B_T01A_O3_PHYSICAL_FIDELITY"
        (EVID/"FINAL_STATUS.txt").write_text(status+"\n")
        close_auth(st)
        st["scientific_freeze"]["o3_status"]=status
        st["scientific_freeze"]["next_stage"]="H3B_T01A_O3_REVIEW"
        st["scientific_freeze"]["stop_boundary"]="HOLD: O3 acceptable gate failed; O4 not executed; O2C may be reopened only if failure is return-path/via/solder attributable"
        st["execution"]["current_stage"]="R1E1A4A_H3B_T01A_O3_REVIEW_AWAIT_AUTH"
        (REPO/"execution"/"stage_contract.json").write_text(json.dumps(st,indent=2)+"\n",encoding="utf-8")
        raise SystemExit(20)

    # ---------- O4: generate exactly six frozen sentinels ----------
    base=winner_src
    cases={}
    cases["FAB_LOWZ"]=(fab_corner(base,1.6,0.35),PORT_TRANS.read_text(encoding="utf-8"))
    cases["FAB_HIGHZ"]=(fab_corner(base,1.4,0.45),PORT_TRANS.read_text(encoding="utf-8"))
    cases["ALIGN_P020"]=(shift_vertical_x(base,0.20),aligned_ports(0.20))
    cases["ALIGN_M020"]=(shift_vertical_x(base,-0.20),aligned_ports(-0.20))
    cases["SOLDER_SMALL"]=(solder_scale(base,0.75),PORT_TRANS.read_text(encoding="utf-8"))
    cases["SOLDER_LARGE"]=(solder_scale(base,1.25),PORT_TRANS.read_text(encoding="utf-8"))

    builds={}
    for name,(geom,ports) in cases.items():
        e=EVID/name; e.mkdir()
        macro,mat=apply_finite_materials(geom,True)
        cst,bh=build_model(name,macro,O4ROOT,e,38)
        (e/"ports.mcr").write_text(ports,encoding="utf-8")
        builds[name]=(cst,ports,bh)

    sentinel=[]
    for name in ["FAB_LOWZ","FAB_HIGHZ","ALIGN_P020","ALIGN_M020","SOLDER_SMALL","SOLDER_LARGE"]:
        e=EVID/name; cst,ports,bh=builds[name]
        solved,data,res=solve_model(name,cst,ports,O4ROOT,e,ref_data)
        m=res["metrics"]
        passed=(res["numerically_qualified"] and m["worst_core_return_db"]<=ACCEPT_RL and
                m["core_s21_min_db"]>=S21_FLOOR and m["reciprocity_max_abs_db"]<=RECIP)
        row={"case":name,"pass":passed,**res}
        sentinel.append(row)

    o4_pass=all(x["pass"] for x in sentinel)
    json.dump({"status":"PASS" if o4_pass else "HOLD","sentinels":sentinel},
              open(str(EVID/"O4_SUMMARY.json"),"w"),indent=2)

    if not o4_pass:
        status="HOLD_R1E1A4A_H3B_T01A_O4_TOLERANCE"
        (EVID/"FINAL_STATUS.txt").write_text(status+"\n")
        close_auth(st)
        st["scientific_freeze"]["o3_status"]="PASS_R1E1A4A_H3B_T01A_O3_PHYSICAL_FIDELITY"
        st["scientific_freeze"]["o4_status"]=status
        st["scientific_freeze"]["o4_results"]=sentinel
        st["scientific_freeze"]["next_stage"]="H3B_T01A_O4_REVIEW"
        st["scientific_freeze"]["stop_boundary"]="HOLD: one or more O4 manufacturing sentinels failed acceptable gate"
        st["execution"]["current_stage"]="R1E1A4A_H3B_T01A_O4_REVIEW_AWAIT_AUTH"
        (REPO/"execution"/"stage_contract.json").write_text(json.dumps(st,indent=2)+"\n",encoding="utf-8")
        raise SystemExit(21)

    # ---------- T01-A FREEZE ----------
    write_s2p(EVID/"T01A_P20_G30_E30_FINITE_CONDUCTIVITY.s2p",nom_data)
    write_s2p(EVID/"T01A_W15_G40_STRAIGHT_FINITE_CONDUCTIVITY.s2p",ref_data)
    freeze_status="PASS_R1E1A4A_H3B_T01A_FREEZE"
    (EVID/"FINAL_STATUS.txt").write_text(freeze_status+"\n")
    report=["# H3B-T01A O3/O4 Final Qualification and Freeze","",
            "Canonical status: "+freeze_status+".","",
            "## O3 nominal physical-fidelity result",
            "- geometry: P20_G30_E30",
            "- copper sigma: %.3e S/m"%COPPER_SIGMA,
            "- solder proxy sigma: %.3e S/m"%SOLDER_SIGMA,
            "- worst core return: %.4f dB"%mm["worst_core_return_db"],
            "- core S21 minimum: %.4f dB"%mm["core_s21_min_db"],
            "- junction excess maximum: %.4f dB"%mm["junction_excess_max_db"],
            "- junction excess median: %.4f dB"%mm["junction_excess_median_db"],
            "- reciprocity max: %.6g dB"%mm["reciprocity_max_abs_db"],
            "- preferred gate: %s"%("PASS" if o3_pref else "MISS (acceptable PASS)"),"",
            "## O4 sentinels"]
    for x in sentinel:
        m=x["metrics"]
        report.append("- %s: %s; worst return %.4f dB; S21 min %.4f dB"%(x["case"],"PASS" if x["pass"] else "HOLD",m["worst_core_return_db"],m["core_s21_min_db"]))
    report += ["","O2C remains DEFERRED_CONTINGENCY_ONLY.","T01-C remains deferred.",
               "Next mainline node: H3B Complete Passive Unit, then H3B-I01."]
    (EVID/"QUALIFICATION.md").write_text("\n".join(report)+"\n",encoding="utf-8")

    close_auth(st)
    sf=st["scientific_freeze"]
    sf["o3_status"]="PASS_R1E1A4A_H3B_T01A_O3_PHYSICAL_FIDELITY"
    sf["o3_preferred_gate"]=o3_pref
    sf["o3_nominal_metrics"]=mm
    sf["o3_nominal_solved_sha256"]=nom_res["solved_sha256"]
    sf["o3_reference_solved_sha256"]=ref_res["solved_sha256"]
    sf["o4_status"]="PASS_R1E1A4A_H3B_T01A_O4_MINIMAL_SENTINELS"
    sf["o4_results"]=sentinel
    sf["t01a_freeze_status"]=freeze_status
    sf["t01a_frozen_geometry"]="P20_G30_E30_WITH_FINITE_COPPER_AND_EXPLICIT_SOLDER_PROXY"
    sf["o2c_status"]="DEFERRED_CONTINGENCY_CLOSED_AFTER_O3_O4_PASS"
    sf["next_stage"]="H3B_COMPLETE_PASSIVE_UNIT_FREEZE"
    sf["h3bi01_status"]="READY_AFTER_H3B_COMPLETE_PASSIVE_UNIT"
    sf["stop_boundary"]="T01-A FROZEN; AWAIT H3B COMPLETE PASSIVE UNIT AUTHORIZATION"
    st["execution"]["current_stage"]="R1E1A4A_H3B_COMPLETE_PASSIVE_UNIT_FREEZE_AWAIT_AUTH"
    st["execution"]["formal_o3_solve_invocation_count"]=2
    st["execution"]["formal_o4_solve_invocation_count"]=6
    (REPO/"execution"/"stage_contract.json").write_text(json.dumps(st,indent=2)+"\n",encoding="utf-8")

    sim=["# SIM_EXECUTION","","## Protocol","Minimum compatible SimulationOps protocol: 0.2.7","",
         "## Current stage","R1E1A4A_H3B_COMPLETE_PASSIVE_UNIT_FREEZE_AWAIT_AUTH","",
         "BUILD_AUTHORIZED: false","SOLVE_AUTHORIZED: false","PRODUCTION_SOLVE_AUTHORIZED: false",
         "LNA_INTEGRATION_AUTHORIZED: false","CST251_AUTHORIZED: false","",
         "## T01-A",freeze_status,
         "O3: PASS_R1E1A4A_H3B_T01A_O3_PHYSICAL_FIDELITY",
         "O4: PASS_R1E1A4A_H3B_T01A_O4_MINIMAL_SENTINELS",
         "O2C: DEFERRED_CONTINGENCY_CLOSED_AFTER_O3_O4_PASS","",
         "## Immediate next node","H3B_COMPLETE_PASSIVE_UNIT_FREEZE","",
         "No BUILD or SOLVE authorization is currently open.","T01-C remains deferred."]
    (REPO/"docs"/"SIM_EXECUTION.md").write_text("\n".join(sim)+"\n",encoding="utf-8")

except SystemExit:
    raise
except Exception as e:
    status="HOLD_R1E1A4A_H3B_T01A_O3_O4_EXECUTION_EXCEPTION"
    (EVID/"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
    (EVID/"FINAL_STATUS.txt").write_text(status+"\n")
    close_auth(st)
    st["scientific_freeze"]["o3_o4_execution_hold"]=str(e)
    st["scientific_freeze"]["next_stage"]="H3B_T01A_O3_O4_REVIEW"
    st["scientific_freeze"]["stop_boundary"]="HOLD: execution exception; no silent retry"
    st["execution"]["current_stage"]="R1E1A4A_H3B_T01A_O3_O4_REVIEW_AWAIT_AUTH"
    (REPO/"execution"/"stage_contract.json").write_text(json.dumps(st,indent=2)+"\n",encoding="utf-8")
    raise
finally:
    # Always checkpoint text evidence before attempting archive/commit.
    try:
        st2=json.loads((REPO/"execution"/"stage_contract.json").read_text(encoding="utf-8"))
        for k in st2["authorization"]: st2["authorization"][k]=False
        (REPO/"execution"/"stage_contract.json").write_text(json.dumps(st2,indent=2)+"\n",encoding="utf-8")
    except Exception:
        pass

# Archive CST work only after successful O3/O4 freeze.
archive_work()
subprocess.check_call(["git","add","docs","execution","evidence",str(Path(__file__).relative_to(REPO))],cwd=str(REPO))
subprocess.check_call(["git","commit","-m","Execute O3 O4 and freeze T01A physical transition"],cwd=str(REPO))
subprocess.check_call(["git","push","origin","project/r0-charts-scaffold"],cwd=str(REPO))
print(freeze_status)
print("O3_METRICS="+json.dumps(mm,sort_keys=True))
print("O4="+json.dumps([{"case":x["case"],"pass":x["pass"],"metrics":x["metrics"]} for x in sentinel],sort_keys=True))
print("ARCHIVE="+str(ARCHIVE))
print("HEAD="+git("rev-parse","HEAD"))
