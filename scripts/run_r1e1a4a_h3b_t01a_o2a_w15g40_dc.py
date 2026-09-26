from __future__ import print_function
import os,sys,json,hashlib,math,subprocess,shutil,statistics,traceback
from pathlib import Path

REPO=Path(r"D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold")
ROOT=Path(r"D:\GNSS_Lband_Active_Array")
EVID=REPO/"evidence"/"r1e1a4a_h3b_t01a_o2a_nw_20260926_run01"
BWORK=ROOT/"_r1e1a4a_h3b_t01a_o2a_build_work"
SWORK=ROOT/"_r1e1a4a_h3b_t01a_o2a_solve_work"
BUILD=BWORK/"R1E1A4A_H3B_T01A_O2A_W15G40_BUILD_ONLY_V01.cst"
SOLVED=SWORK/"R1E1A4A_H3B_T01A_O2A_W15G40_BASELINE_V01.cst"
REF=ROOT/"_r1e1a4a_h3b_t01a_o1_qual_work"/"W15_G40"/"W15_G40_QUAL.cst"
REF_SHA="2050bba69d0a21a2a295c378d0a36a5408ad80e7399ba7403025a94a5694a604"
SRCMAC=REPO/"source"/"cst"/"R1E1A4A_H3B_T01_ORTHOGONAL_TRANSITION_BUILD_ONLY_V01.mcr"
OUTMAC=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_O2A_W15G40_BUILD_ONLY_V01.mcr"
PORTS=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_PORTS_V01.mcr"
SOLVER=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_SOLVER_CONFIG_MAXPASS16_V01.mcr"
SELF=Path(__file__)
LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

def git(*a): return subprocess.check_output(["git"]+list(a),cwd=str(REPO),universal_newlines=True).strip()
def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()
def body(p):
    a=Path(p).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    return "\n".join(a[a.index("Sub Main()")+1:a.index("End Sub")])
def transform_macro(src):
    rules=[
      ('StoreParameter "h3b_t01_wsig", 1.8','StoreParameter "h3b_t01_wsig", 1.5',1),
      ('StoreParameter "h3b_t01_gap", 0.3','StoreParameter "h3b_t01_gap", 0.4',1),
      ('.Xrange "-0.9", "0.9"','.Xrange "-0.75", "0.75"',2),
      ('.Xrange "-3.4", "-1.2"','.Xrange "-3.35", "-1.15"',2),
      ('.Xrange "1.2", "3.4"','.Xrange "1.15", "3.35"',2),
    ]
    out=src
    for old,new,n in rules:
        if out.count(old)!=n: raise RuntimeError("transform source count mismatch: %s got %d"%(old,out.count(old)))
        out=out.replace(old,new)
    rev=out
    for old,new,n in reversed(rules):
        if rev.count(new)!=n: raise RuntimeError("reverse count mismatch: "+new)
        rev=rev.replace(new,old)
    if rev!=src: raise RuntimeError("transform not reversible")
    return out,{old:{"new":new,"count":n} for old,new,n in rules}
def audit_vba(shape,status,inter):
    return '''Sub Main()
On Error Resume Next
Dim f As Integer, i As Long, nm As String
f=FreeFile
Open "%s" For Output As #f
Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())
For i=0 To Solid.GetNumberOfShapes()+120
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
def read_s(cst):
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d(); tree=p3.get_tree_items(); out={}
    for i,j in ((1,1),(1,2),(2,1),(2,2)):
        item=r"1D Results\S-Parameters\S%d,%d"%(i,j)
        if item not in tree: raise RuntimeError("missing result "+item)
        out["S%d%d"%(i,j)]=[(float(r[0]),20*math.log10(max(abs(complex(r[1])),1e-300))) for r in p3.get_result_item(item).get_data()]
    return out
def read_adapt(cst):
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d(); tree=p3.get_tree_items()
    hits=[x for x in tree if "Adaptive Meshing" in x and x.endswith(r"S-Parameters\Delta\All S-Parameters")]
    if not hits: return []
    return [{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)} for r in p3.get_result_item(hits[0]).get_data()]
def interp(vals,x):
    vals=sorted(vals)
    if x<=vals[0][0]: return vals[0][1]
    if x>=vals[-1][0]: return vals[-1][1]
    for a,b in zip(vals,vals[1:]):
        if a[0]<=x<=b[0]:
            t=(x-a[0])/(b[0]-a[0]); return a[1]+t*(b[1]-a[1])
def metric(data):
    core=(1.15,1.65)
    s11=[r[1] for r in data["S11"] if core[0]<=r[0]<=core[1]]
    s22=[r[1] for r in data["S22"] if core[0]<=r[0]<=core[1]]
    s21=[r[1] for r in data["S21"] if core[0]<=r[0]<=core[1]]
    return {"worst_core_return_db":max(max(s11),max(s22)),
            "core_s21_min_db":min(s21),"core_s21_max_db":max(s21),
            "reciprocity_max_abs_db":max(abs(a[1]-b[1]) for a,b in zip(data["S21"],data["S12"]))}
def close(stage,status,nextstage,extra):
    for k in stage["authorization"]: stage["authorization"][k]=False
    stage["execution"]["current_stage"]="R1E1A4A_"+nextstage+"_AWAIT_AUTH"
    stage["execution"]["formal_o2a_solve_invocation_count"]=1
    sf=stage["scientific_freeze"]; sf["o2a_status"]=status; sf["next_stage"]=nextstage
    sf["stop_boundary"]="AWAIT NEXT-STAGE AUTHORIZATION; NO BUILD NO SOLVE"; sf.update(extra)
    (REPO/"execution"/"stage_contract.json").write_text(json.dumps(stage,indent=2)+"\n",encoding="utf-8")

HEAD=git("rev-parse","HEAD")
if git("status","--porcelain"): raise RuntimeError("working tree not clean")
stage=json.load(open(str(REPO/"execution"/"stage_contract.json"),encoding="utf-8"))
if stage["execution"]["current_stage"]!="R1E1A4A_H3B_T01A_O2_JUNCTION_OPTIMIZATION_FREEZE_AWAIT_AUTH": raise RuntimeError("wrong stage")
if not REF.exists() or sha(REF)!=REF_SHA: raise RuntimeError("O1 reference authority mismatch")
for p in (EVID,BWORK,SWORK):
    if p.exists(): raise RuntimeError("destination exists: "+str(p))
src=SRCMAC.read_text(encoding="utf-8")
newmac,rules=transform_macro(src)
OUTMAC.write_text(newmac,encoding="utf-8")
freeze=REPO/"docs"/"R1E1A4A_H3B_T01A_O2A_W15G40_BASELINE_FREEZE_V01.md"
freeze.write_text('''# H3B-T01A O2A W15/G40 Junction Baseline Freeze V0.1

Status: AUTHORIZED BUILD + ONE-SHOT SOLVE ON NW

Purpose: determine whether the original 90-degree junction already meets the frozen O2 targets after applying the O1 winning line cross-section.

Only released change versus the qualified T01-A geometry:
- straight GCPW Wsig: 1.8 -> 1.5 mm;
- straight GCPW gap: 0.30 -> 0.40 mm;
- corresponding straight-line signal/ground rail x extents change deterministically.

Frozen without change:
- transition signal pad width 2.2 mm;
- transition pad gap 0.25 mm;
- transition pad lengths;
- transition ground pads;
- edge caps;
- solder envelopes;
- via locations/pitch/diameters;
- both boards, FR4, backing grounds;
- RP1/RP2, 50-ohm discrete ports;
- 1.0-2.0 GHz solve / 1.15-1.65 GHz decision band;
- second-order tetrahedral, MaxDeltaS 0.02, two checks, MaxPasses 16.

Reference authority: O1 W15_G40 high-fidelity straight line, SHA256 2050bba69d0a21a2a295c378d0a36a5408ad80e7399ba7403025a94a5694a604.

Decision:
- preferred: worst-core return >=15 dB AND max junction excess loss <=0.10 dB;
- acceptable: worst-core return >=12 dB AND max junction excess loss <=0.15 dB;
- reciprocity <=0.05 dB; no S21 notch below -3 dB.
If preferred is already met, do not automatically launch a broad O2 DOE.
''',encoding="utf-8")
shutil.copy2(str(SELF),str(REPO/"scripts"/"run_r1e1a4a_h3b_t01a_o2a_w15g40_dc.py"))
stage["project"]["source_commit"]=HEAD
for k in stage["authorization"]: stage["authorization"][k]=False
stage["authorization"]["BUILD_AUTHORIZED"]=True; stage["authorization"]["SOLVE_AUTHORIZED"]=True
stage["execution"]["current_stage"]="R1E1A4A_H3B_T01A_O2A_W15G40_EXECUTING"
stage["scientific_freeze"]["o2a_definition"]="O1_W15G40_LINE_ON_ORIGINAL_T01A_JUNCTION"
stage["scientific_freeze"]["o2a_transform_rules"]=rules
(REPO/"execution"/"stage_contract.json").write_text(json.dumps(stage,indent=2)+"\n",encoding="utf-8")
subprocess.check_call(["git","add","docs","execution","source/cst","scripts/run_r1e1a4a_h3b_t01a_o2a_w15g40_dc.py"],cwd=str(REPO))
subprocess.check_call(["git","commit","-m","Freeze H3B T01A O2A W15G40 baseline"],cwd=str(REPO))
subprocess.check_call(["git","push","origin","project/r0-charts-scaffold"],cwd=str(REPO))
FREEZE_HEAD=git("rev-parse","HEAD")

EVID.mkdir(parents=True); BWORK.mkdir(); SWORK.mkdir()
# Build-only
de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
try:
    prj=de.new_mws(); prj.modeler.add_to_history("H3B-T01A-O2A W15G40 build",body(OUTMAC))
    prj.save(str(BUILD),include_results=False)
finally:
    if prj is not None: prj.close()
    de.close()
bsha=sha(BUILD); shape=EVID/"build_shapes.txt"; stat=EVID/"build_status.txt"; inter=EVID/"intersection_status.txt"
de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
try:
    prj=de.open_project(str(BUILD)); ok=bool(prj.schematic.execute_vba_code(audit_vba(str(shape),str(stat),str(inter))))
finally:
    if prj is not None: prj.close()
    de.close()
rows=[x for x in shape.read_text().splitlines() if x.startswith("SHAPE|")]
vols=[float(x.split("volume=",1)[1]) for x in rows]
tree=ProjectFile(str(BUILD),allow_interactive=True).get_3d().get_tree_items()
outp=Path(os.path.splitext(str(BUILD))[0])/"Result"/"output.txt"
checks={"shape_count_38":len(rows)==38,"positive_volumes":all(v>0 for v in vols),
        "port_count_zero":"PORT_COUNT=0" in stat.read_text(),
        "intersection_returned":ok and "RETURNED=TRUE" in inter.read_text(),
        "no_solver_output":not outp.exists(),
        "no_solver_results":not any("S-Parameters" in x or "Adaptive Meshing" in x for x in tree),
        "reopen_hash_stable":sha(BUILD)==bsha}
json.dump({"source_macro_sha256":sha(SRCMAC),"o2a_macro_sha256":sha(OUTMAC),"build_sha256":bsha,
           "transform_rules":rules,"checks":checks},open(str(EVID/"build_summary.json"),"w"),indent=2)
if not all(checks.values()): raise RuntimeError("O2A BUILD HOLD "+json.dumps(checks))

# Immutable solve copy
shutil.copy2(str(BUILD),str(SOLVED))
if sha(SOLVED)!=bsha: raise RuntimeError("copy hash mismatch")
de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
try:
    prj=de.open_project(str(SOLVED)); prj.modeler.add_to_history("H3B-T01A-O2A ports",body(PORTS))
    prj.modeler.add_to_history("H3B-T01A-O2A solver",body(SOLVER)); prj.save()
finally:
    if prj is not None: prj.close()
    de.close()
configured=sha(SOLVED); ps=EVID/"presolve_status.txt"
de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
try:
    prj=de.open_project(str(SOLVED)); prj.schematic.execute_vba_code(port_vba(str(ps)))
finally:
    if prj is not None: prj.close()
    de.close()
if "PORT_COUNT=2" not in ps.read_text() or sha(SOLVED)!=configured: raise RuntimeError("presolve reopen audit failed")

# One formal solve
de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
try:
    prj=de.open_project(str(SOLVED)); prj.modeler.run_solver(); prj.save()
finally:
    if prj is not None: prj.close()
    de.close()
trans=read_s(SOLVED); ref=read_s(REF); ad=read_adapt(SOLVED); m=metric(trans)
numok=len(ad)>=2 and ad[-2]["delta_s"]<=0.02 and ad[-1]["delta_s"]<=0.02
core=[r for r in trans["S21"] if 1.15<=r[0]<=1.65]
ex=[interp(ref["S21"],r[0])-r[1] for r in core]
em={"junction_excess_min_db":min(ex),"junction_excess_max_db":max(ex),"junction_excess_median_db":statistics.median(ex)}
preferred=(m["worst_core_return_db"]<=-15.0 and em["junction_excess_max_db"]<=0.10 and m["core_s21_min_db"]>=-3.0 and m["reciprocity_max_abs_db"]<=0.05)
acceptable=(m["worst_core_return_db"]<=-12.0 and em["junction_excess_max_db"]<=0.15 and m["core_s21_min_db"]>=-3.0 and m["reciprocity_max_abs_db"]<=0.05)
if not numok:
    status="HOLD_R1E1A4A_H3B_T01A_O2A_NUMERICAL"
    nextstage="H3B_T01A_O2A_NUMERICAL_REVIEW"
elif preferred:
    status="PASS_R1E1A4A_H3B_T01A_O2A_PREFERRED"
    nextstage="H3B_T01A_O3_FULL_FIDELITY_FREEZE"
elif acceptable:
    status="PASS_R1E1A4A_H3B_T01A_O2A_ACCEPTABLE"
    nextstage="H3B_T01A_O2B_LOCAL_JUNCTION_DOE_FREEZE"
else:
    status="HOLD_R1E1A4A_H3B_T01A_O2A_RF"
    nextstage="H3B_T01A_O2B_LOCAL_JUNCTION_DOE_FREEZE"
solsha=sha(SOLVED)
summary={"status":status,"freeze_head":FREEZE_HEAD,"formal_solver_invocations":1,
         "build_sha256":bsha,"configured_sha256":configured,"solved_sha256":solsha,
         "reference_sha256":REF_SHA,"metrics":m,"excess_loss":em,"adaptive_delta_sequence":ad,
         "numerically_qualified":numok,"preferred_gate":preferred,"acceptable_gate":acceptable,
         "passes_executed":ad[-1]["pass"] if ad else None,
         "final_two_delta_s":[ad[-2]["delta_s"],ad[-1]["delta_s"]] if len(ad)>=2 else None}
json.dump(summary,open(str(EVID/"summary.json"),"w"),indent=2)
(EVID/"FINAL_STATUS.txt").write_text(status+"\n")
q=["# H3B-T01A O2A W15/G40 Baseline Qualification","",
   "Canonical status: "+status+".","",
   "Only the O1-winning straight-line cross-section was applied to the original T01-A junction.",
   "Wsig = 1.50 mm; Gcpw = 0.40 mm. Junction pads, solder, vias and mechanics remained frozen.","",
   "Worst core-band return = %.4f dB."%m["worst_core_return_db"],
   "Core-band S21 = %.4f to %.4f dB."%(m["core_s21_min_db"],m["core_s21_max_db"]),
   "Junction excess loss versus qualified W15_G40 straight reference = %.4f to %.4f dB; median %.4f dB."%(em["junction_excess_min_db"],em["junction_excess_max_db"],em["junction_excess_median_db"]),
   "Reciprocity max difference = %.6g dB."%m["reciprocity_max_abs_db"],
   "Native convergence: %s."%("PASS" if numok else "HOLD")]
if len(ad)>=2: q.append("Final two DeltaS = %.8f, %.8f."%(ad[-2]["delta_s"],ad[-1]["delta_s"]))
q += ["","Preferred gate met: %s."%("YES" if preferred else "NO"),
      "Acceptable gate met: %s."%("YES" if acceptable else "NO"),
      "Next node: "+nextstage+"."]
(EVID/"QUALIFICATION.md").write_text("\n".join(q)+"\n",encoding="utf-8")
extra={"o2a_build_sha256":bsha,"o2a_solved_sha256":solsha,"o2a_metrics":m,"o2a_excess_loss":em,
       "o2a_preferred_gate":preferred,"o2a_acceptable_gate":acceptable}
close(stage,status,nextstage,extra)
sim=["# SIM_EXECUTION","","## Protocol","Minimum compatible SimulationOps protocol: 0.2.7","",
     "## Current stage","R1E1A4A_"+nextstage+"_AWAIT_AUTH","",
     "BUILD_AUTHORIZED: false","SOLVE_AUTHORIZED: false","PRODUCTION_SOLVE_AUTHORIZED: false",
     "LNA_INTEGRATION_AUTHORIZED: false","CST251_AUTHORIZED: false","",
     "## O1 line freeze","PASS_R1E1A4A_H3B_T01A_O1_LINE_CROSS_SECTION","Wsig = 1.50 mm; Gcpw = 0.40 mm","",
     "## O2A baseline",status,
     "Worst core return: %.4f dB"%m["worst_core_return_db"],
     "Junction excess max: %.4f dB"%em["junction_excess_max_db"],
     "Junction excess median: %.4f dB"%em["junction_excess_median_db"],
     "Preferred gate: %s"%("PASS" if preferred else "FAIL"),"",
     "## Immediate next node",nextstage,"","No BUILD or SOLVE authorization is currently open.","T01-C remains deferred."]
(REPO/"docs"/"SIM_EXECUTION.md").write_text("\n".join(sim)+"\n",encoding="utf-8")
subprocess.check_call(["git","add","docs","execution","evidence","source/cst","scripts/run_r1e1a4a_h3b_t01a_o2a_w15g40_dc.py"],cwd=str(REPO))
subprocess.check_call(["git","commit","-m","Execute H3B T01A O2A W15G40 baseline"],cwd=str(REPO))
subprocess.check_call(["git","push","origin","project/r0-charts-scaffold"],cwd=str(REPO))
print(status)
print("METRICS="+json.dumps(m,sort_keys=True))
print("EXCESS="+json.dumps(em,sort_keys=True))
print("FINAL_TWO="+json.dumps(summary["final_two_delta_s"]))
print("SOLVED_SHA256="+solsha)
print("HEAD="+git("rev-parse","HEAD"))
