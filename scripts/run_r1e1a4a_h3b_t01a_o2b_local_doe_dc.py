from __future__ import print_function
import os,sys,json,hashlib,math,subprocess,shutil,statistics,traceback
from pathlib import Path
REPO=Path(r"D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold"); ROOT=Path(r"D:\GNSS_Lband_Active_Array")
EVID=REPO/"evidence"/"r1e1a4a_h3b_t01a_o2b_nw_20260926_run01"; BROOT=ROOT/"_r1e1a4a_h3b_t01a_o2b_build_work"; SROOT=ROOT/"_r1e1a4a_h3b_t01a_o2b_screen_work"; QROOT=ROOT/"_r1e1a4a_h3b_t01a_o2b_qual_work"
BASEMAC=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_O2A_W15G40_BUILD_ONLY_V01.mcr"; PORTS=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_PORTS_V01.mcr"; HISOL=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_SOLVER_CONFIG_MAXPASS16_V01.mcr"
SCREEN=REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_O1_SCREEN_SOLVER_V01.mcr"; REF=ROOT/"_r1e1a4a_h3b_t01a_o1_qual_work"/"W15_G40"/"W15_G40_QUAL.cst"; REF_SHA="2050bba69d0a21a2a295c378d0a36a5408ad80e7399ba7403025a94a5694a604"; SELF=Path(__file__)
LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile
CANDS=[("P22_G25_E00_BASE",2.2,.25,0.0)]
for p in (2.0,2.4):
  for g in (.20,.30):
    for e in (0.0,.30): CANDS.append(("P%02d_G%02d_E%02d"%(round(p*10),round(g*100),round(e*100)),p,g,e))
def git(*a): return subprocess.check_output(["git"]+list(a),cwd=str(REPO),universal_newlines=True).strip()
def sha(p):
  h=hashlib.sha256()
  with open(str(p),"rb") as f:
    for c in iter(lambda:f.read(65536),b""): h.update(c)
  return h.hexdigest()
def body_text(txt):
  a=txt.replace("\r\n","\n").split("\n"); return "\n".join(a[a.index("Sub Main()")+1:a.index("End Sub")])
def body(p): return body_text(Path(p).read_text(encoding="utf-8"))
def fmt(x):
  s=("%.12g"%x); return s
def replace_count(s,old,new,n):
  if s.count(old)!=n: raise RuntimeError("replace count %r expected %d got %d"%(old,n,s.count(old)))
  return s.replace(old,new)
def make_macro(padw,gap,ext):
  s=BASEMAC.read_text(encoding="utf-8")
  if padw==2.2 and abs(gap-.25)<1e-12 and abs(ext)<1e-12: return s
  hp=padw/2.0; inner=hp+gap; outer=inner+2.4; hy=1.5+ext; vz=-1.2-ext
  s=replace_count(s,'StoreParameter "h3b_t01_pad_sig", 2.2','StoreParameter "h3b_t01_pad_sig", %s'%fmt(padw),1)
  s=replace_count(s,'StoreParameter "h3b_t01_pad_gap", 0.25','StoreParameter "h3b_t01_pad_gap", %s'%fmt(gap),1)
  s=replace_count(s,'.Xrange "-1.1", "1.1"','.Xrange "-%s", "%s"'%(fmt(hp),fmt(hp)),4)
  s=replace_count(s,'.Xrange "-3.75", "-1.35"','.Xrange "-%s", "-%s"'%(fmt(outer),fmt(inner)),4)
  s=replace_count(s,'.Xrange "1.35", "3.75"','.Xrange "%s", "%s"'%(fmt(inner),fmt(outer)),4)
  if ext>0:
    s=replace_count(s,'.Yrange "1.5", "14.5"','.Yrange "%s", "14.5"'%fmt(hy),4)
    s=replace_count(s,'.Zrange "-14.5", "-1.2"','.Zrange "-14.5", "%s"'%fmt(vz),4)
    s=replace_count(s,'.Yrange "0.5", "1.5"','.Yrange "0.5", "%s"'%fmt(hy),3)
    s=replace_count(s,'.Zrange "-1.2", "-0.035"','.Zrange "%s", "-0.035"'%fmt(vz),3)
  return s
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
    if item not in tree: raise RuntimeError("missing "+item)
    out["S%d%d"%(i,j)]=[(float(r[0]),20*math.log10(max(abs(complex(r[1])),1e-300))) for r in p3.get_result_item(item).get_data()]
  return out
def read_adapt(cst):
  p3=ProjectFile(str(cst),allow_interactive=True).get_3d(); tree=p3.get_tree_items(); hits=[x for x in tree if "Adaptive Meshing" in x and x.endswith(r"S-Parameters\Delta\All S-Parameters")]
  if hits:
    try:
      return [{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)} for r in p3.get_result_item(hits[0]).get_data()]
    except ValueError:
      pass
  # CST may delete run-id 0 after parameterized frequency-sample updates while leaving the native solver log authoritative.
  import re
  out=Path(os.path.splitext(str(cst))[0])/"Result"/"output.txt"
  if not out.exists(): return []
  seq=[]; cur=None
  for line in out.read_text(encoding="utf-8",errors="ignore").splitlines():
    m=re.search(r"Adaptive mesh refinement pass\s+(\d+)",line)
    if m: cur=int(m.group(1)); continue
    m=re.search(r"All S-Parameters\s*=\s*([0-9.eE+-]+)",line)
    if m and cur is not None: seq.append({"pass":cur,"delta_s":float(m.group(1))})
  dedup={}
  for row in seq: dedup[row["pass"]]=row["delta_s"]
  return [{"pass":p,"delta_s":dedup[p]} for p in sorted(dedup)]
def interp(vals,x):
  vals=sorted(vals)
  if x<=vals[0][0]: return vals[0][1]
  if x>=vals[-1][0]: return vals[-1][1]
  for a,b in zip(vals,vals[1:]):
    if a[0]<=x<=b[0]:
      t=(x-a[0])/(b[0]-a[0]); return a[1]+t*(b[1]-a[1])
def metrics(data,ref):
  core=(1.15,1.65); s11=[r[1] for r in data["S11"] if core[0]<=r[0]<=core[1]]; s22=[r[1] for r in data["S22"] if core[0]<=r[0]<=core[1]]; s21=[r[1] for r in data["S21"] if core[0]<=r[0]<=core[1]]
  ex=[interp(ref["S21"],r[0])-r[1] for r in data["S21"] if core[0]<=r[0]<=core[1]]
  return {"worst_core_return_db":max(max(s11),max(s22)),"core_s21_min_db":min(s21),"core_s21_max_db":max(s21),"reciprocity_max_abs_db":max(abs(a[1]-b[1]) for a,b in zip(data["S21"],data["S12"])),"junction_excess_min_db":min(ex),"junction_excess_max_db":max(ex),"junction_excess_median_db":statistics.median(ex)}
def balanced(m):
  return max(0.0,(m["worst_core_return_db"]+15.0)/3.0,(m["junction_excess_max_db"]-.10)/.05)
def fresh_solve(src,dst,solver,evid,ref,qual=False):
  shutil.copy2(str(src),str(dst)); source_sha=sha(dst)
  de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
  try:
    prj=de.open_project(str(dst)); prj.modeler.add_to_history("H3B-T01A-O2B ports",body(PORTS)); prj.modeler.add_to_history("H3B-T01A-O2B solver",body(solver)); prj.save()
  finally:
    if prj is not None: prj.close()
    de.close()
  configured=sha(dst); ps=evid/"presolve_status.txt"
  de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
  try:
    prj=de.open_project(str(dst)); prj.schematic.execute_vba_code(port_vba(str(ps)))
  finally:
    if prj is not None: prj.close()
    de.close()
  if "PORT_COUNT=2" not in ps.read_text() or sha(dst)!=configured: raise RuntimeError("presolve reopen failed")
  de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
  try:
    prj=de.open_project(str(dst)); prj.modeler.run_solver(); prj.save()
  finally:
    if prj is not None: prj.close()
    de.close()
  d=read_s(dst); ad=read_adapt(dst); m=metrics(d,ref); out={"source_build_sha256":source_sha,"configured_sha256":configured,"solved_sha256":sha(dst),"metrics":m,"balance_score":balanced(m),"adaptive_delta_sequence":ad,"formal_solver_invocations":1}
  if qual:
    out["numerically_qualified"]=len(ad)>=2 and ad[-2]["delta_s"]<=.02 and ad[-1]["delta_s"]<=.02; out["passes_executed"]=ad[-1]["pass"] if ad else None; out["final_two_delta_s"]=[ad[-2]["delta_s"],ad[-1]["delta_s"]] if len(ad)>=2 else None
  return out
def close(stage,status,nextstage,extra):
  for k in stage["authorization"]: stage["authorization"][k]=False
  stage["execution"]["current_stage"]="R1E1A4A_"+nextstage+"_AWAIT_AUTH"; stage["execution"]["formal_o2b_screen_invocation_count"]=9; stage["execution"]["formal_o2b_qualification_invocation_count"]=3
  sf=stage["scientific_freeze"]; sf["o2b_status"]=status; sf["next_stage"]=nextstage; sf["stop_boundary"]="AWAIT NEXT-STAGE AUTHORIZATION; NO BUILD NO SOLVE"; sf.update(extra)
  (REPO/"execution"/"stage_contract.json").write_text(json.dumps(stage,indent=2)+"\n",encoding="utf-8")
HEAD=git("rev-parse","HEAD")
if git("status","--porcelain"): raise RuntimeError("working tree not clean")
stage=json.load(open(str(REPO/"execution"/"stage_contract.json"),encoding="utf-8"))
if stage["execution"]["current_stage"]!="R1E1A4A_H3B_T01A_O2B_LOCAL_JUNCTION_DOE_FREEZE_AWAIT_AUTH": raise RuntimeError("wrong stage")
if not REF.exists() or sha(REF)!=REF_SHA: raise RuntimeError("reference authority mismatch")
for p in (EVID,BROOT,SROOT,QROOT):
  if p.exists(): raise RuntimeError("destination exists "+str(p))
# Freeze before any result is visible
stage["project"]["source_commit"]=HEAD
for k in stage["authorization"]: stage["authorization"][k]=False
stage["authorization"]["BUILD_AUTHORIZED"]=True; stage["authorization"]["SOLVE_AUTHORIZED"]=True; stage["execution"]["current_stage"]="R1E1A4A_H3B_T01A_O2B_EXECUTING"
sf=stage["scientific_freeze"]; sf["o2b_released_variables"]={"signal_pad_width_mm":[2.0,2.4],"pad_gap_mm":[.20,.30],"transition_extension_mm":[0.0,.30],"baseline":[2.2,.25,0.0]}; sf["o2b_fixed"]="O1 W15/G40 line; ground-pad width 2.4; solder y/z envelope; vias; boards; RP; FR4; PEC screening model"
sf["o2b_screening_fidelity"]="second-order tetrahedral exactly 4 adaptive passes; ranking only"; sf["o2b_qualification_fidelity"]="second-order tetrahedral MaxDeltaS 0.02 x2; MaxPasses16"; sf["o2b_selection"]="top3 by normalized max shortfall from frozen preferred return/excess gates; ties by return, excess, larger gap, smaller extension"
(REPO/"execution"/"stage_contract.json").write_text(json.dumps(stage,indent=2)+"\n",encoding="utf-8")
freeze=REPO/"docs"/"R1E1A4A_H3B_T01A_O2B_LOCAL_JUNCTION_DOE_FREEZE_V01.md"
freeze.write_text('''# H3B-T01A O2B Local Junction DOE Freeze V0.1

Status: AUTHORIZED BUILD + TWO-LEVEL SOLVE ON NW

Baseline: O2A with O1 line cross-section Wsig=1.50 mm / Gcpw=0.40 mm.

Released variables:
- transition signal-pad width: 2.0 / 2.4 mm;
- transition signal-to-ground pad gap: 0.20 / 0.30 mm;
- transition-region extension: 0.00 / 0.30 mm.
Also include unchanged O2A baseline 2.2 / 0.25 / 0.00 as reference.

The extension moves the pad-to-normal-GCPW boundary and backing-ground boundary together, preserving electrical continuity and RP spacing.

Frozen:
- transition ground-pad width = 2.4 mm;
- solder envelope in y/z and via geometry/locations;
- edge/castellation concept;
- boards, FR4, W15/G40 normal GCPW, RP1/RP2 and ports;
- T01-C and all active/LNA work.

All 9 geometries must pass build-only fresh-reopen/intersection checks before any solve.
Screen all 9 at exactly four adaptive passes. Screening cannot become final PASS.
Select three finalists using normalized maximum shortfall from preferred gates (15 dB worst-core return, 0.10 dB max junction excess); ties: better return, lower excess, larger gap, smaller extension.
Fresh-run only the three finalists at full O0 fidelity, DeltaS<=0.02 twice, MaxPasses16, no silent retry.

Preferred final gate: worst-core return >=15 dB AND max junction excess <=0.10 dB.
Acceptable gate: worst-core return >=12 dB AND max junction excess <=0.15 dB.
Also require no S21 notch below -3 dB and reciprocity <=0.05 dB.
Stop after O2B qualification.
''',encoding="utf-8")
shutil.copy2(str(SELF),str(REPO/"scripts"/"run_r1e1a4a_h3b_t01a_o2b_local_doe_dc.py"))
subprocess.check_call(["git","add","docs","execution","scripts/run_r1e1a4a_h3b_t01a_o2b_local_doe_dc.py"],cwd=str(REPO)); subprocess.check_call(["git","commit","-m","Freeze H3B T01A O2B local junction DOE"],cwd=str(REPO)); subprocess.check_call(["git","push","origin","project/r0-charts-scaffold"],cwd=str(REPO)); FREEZE_HEAD=git("rev-parse","HEAD")
EVID.mkdir(parents=True); BROOT.mkdir(); SROOT.mkdir(); QROOT.mkdir(); ref=read_s(REF)
manifest=[]; screening=[]; quals=[]; good=[]; finalists=[]
try:
  # Build all 9 first
  for name,p,g,e in CANDS:
    edir=EVID/name; edir.mkdir(); macro=make_macro(p,g,e); (edir/"build_macro.mcr").write_text(macro,encoding="utf-8"); bdir=BROOT/name; bdir.mkdir(); bfile=bdir/(name+"_BUILD_ONLY.cst")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
      prj=de.new_mws(); prj.modeler.add_to_history("H3B-T01A-O2B "+name,body_text(macro)); prj.save(str(bfile),include_results=False)
    finally:
      if prj is not None: prj.close()
      de.close()
    bh=sha(bfile); shape=edir/"build_shapes.txt"; stat=edir/"build_status.txt"; inter=edir/"intersection_status.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
      prj=de.open_project(str(bfile)); ok=bool(prj.schematic.execute_vba_code(audit_vba(str(shape),str(stat),str(inter))))
    finally:
      if prj is not None: prj.close()
      de.close()
    rows=[x for x in shape.read_text().splitlines() if x.startswith("SHAPE|")]; vols=[float(x.split("volume=",1)[1]) for x in rows]; tree=ProjectFile(str(bfile),allow_interactive=True).get_3d().get_tree_items(); outp=Path(os.path.splitext(str(bfile))[0])/"Result"/"output.txt"
    checks={"shape_count_38":len(rows)==38,"positive_volumes":all(v>0 for v in vols),"port_count_zero":"PORT_COUNT=0" in stat.read_text(),"intersection_returned":ok and "RETURNED=TRUE" in inter.read_text(),"no_solver_output":not outp.exists(),"no_solver_results":not any("S-Parameters" in x or "Adaptive Meshing" in x for x in tree),"hash_stable":sha(bfile)==bh}
    json.dump({"candidate":name,"pad_width_mm":p,"pad_gap_mm":g,"extension_mm":e,"build_sha256":bh,"checks":checks},open(str(edir/"build_summary.json"),"w"),indent=2)
    if not all(checks.values()): raise RuntimeError("BUILD_HOLD "+name+" "+json.dumps(checks))
    manifest.append({"candidate":name,"pad_width_mm":p,"pad_gap_mm":g,"extension_mm":e,"build_file":str(bfile),"build_sha256":bh})
  json.dump(manifest,open(str(EVID/"candidate_manifest.json"),"w"),indent=2)
  # Screening
  for c in manifest:
    name=c["candidate"]; sed=EVID/name/"screen"; sed.mkdir(); sdir=SROOT/name; sdir.mkdir(); dst=sdir/(name+"_SCREEN.cst")
    res=fresh_solve(Path(c["build_file"]),dst,SCREEN,sed,ref,False); row={"candidate":name,"pad_width_mm":c["pad_width_mm"],"pad_gap_mm":c["pad_gap_mm"],"extension_mm":c["extension_mm"],**res["metrics"],"balance_score":res["balance_score"],"solved_sha256":res["solved_sha256"]}
    screening.append(row); json.dump(res,open(str(sed/"summary.json"),"w"),indent=2)
  screening.sort(key=lambda r:(r["balance_score"],r["worst_core_return_db"],r["junction_excess_max_db"],-r["pad_gap_mm"],r["extension_mm"],abs(r["pad_width_mm"]-2.2)))
  finalists=screening[:3]; json.dump({"screening_rank":screening,"finalists":[x["candidate"] for x in finalists]},open(str(EVID/"screening_summary.json"),"w"),indent=2)
  # Qualification
  for rank,c in enumerate(finalists,1):
    m=next(x for x in manifest if x["candidate"]==c["candidate"]); qed=EVID/c["candidate"]/"qual"; qed.mkdir(); qdir=QROOT/c["candidate"]; qdir.mkdir(); dst=qdir/(c["candidate"]+"_QUAL.cst")
    res=fresh_solve(Path(m["build_file"]),dst,HISOL,qed,ref,True); mm=res["metrics"]; acceptable=mm["worst_core_return_db"]<=-12 and mm["junction_excess_max_db"]<=.15 and mm["core_s21_min_db"]>=-3 and mm["reciprocity_max_abs_db"]<=.05; preferred=mm["worst_core_return_db"]<=-15 and mm["junction_excess_max_db"]<=.10 and mm["core_s21_min_db"]>=-3 and mm["reciprocity_max_abs_db"]<=.05
    res.update({"candidate":c["candidate"],"pad_width_mm":m["pad_width_mm"],"pad_gap_mm":m["pad_gap_mm"],"extension_mm":m["extension_mm"],"screen_rank":rank,"acceptable_gate":acceptable,"preferred_gate":preferred,"qualified_pass":bool(res["numerically_qualified"] and acceptable)})
    json.dump(res,open(str(qed/"summary.json"),"w"),indent=2); quals.append(res)
  good=[q for q in quals if q["qualified_pass"]]
  good.sort(key=lambda q:(not q["preferred_gate"],q["balance_score"],q["metrics"]["worst_core_return_db"],q["metrics"]["junction_excess_max_db"],-q["pad_gap_mm"],q["extension_mm"]))
  if not good:
    status="HOLD_R1E1A4A_H3B_T01A_O2B_NO_ACCEPTABLE_JUNCTION"; nextstage="H3B_T01A_O2B_REVIEW"
  else:
    win=good[0]
    if win["preferred_gate"]: status="PASS_R1E1A4A_H3B_T01A_O2B_PREFERRED"; nextstage="H3B_T01A_O3_FULL_FIDELITY_FREEZE"
    else: status="PASS_R1E1A4A_H3B_T01A_O2B_ACCEPTABLE"; nextstage="H3B_T01A_O2C_GROUND_VIA_SOLDER_REVIEW_FREEZE"
  extra={"o2b_screening_rank":screening,"o2b_finalists":[x["candidate"] for x in finalists],"o2b_qualification":quals}
  if good: extra["o2b_winner"]={"candidate":win["candidate"],"pad_width_mm":win["pad_width_mm"],"pad_gap_mm":win["pad_gap_mm"],"extension_mm":win["extension_mm"],"preferred_gate":win["preferred_gate"],"worst_core_return_db":win["metrics"]["worst_core_return_db"],"junction_excess_max_db":win["metrics"]["junction_excess_max_db"],"core_s21_min_db":win["metrics"]["core_s21_min_db"],"solved_sha256":win["solved_sha256"]}
  close(stage,status,nextstage,extra); (EVID/"FINAL_STATUS.txt").write_text(status+"\n")
  final={"status":status,"freeze_head":FREEZE_HEAD,"screening_rank":screening,"finalists":[x["candidate"] for x in finalists],"qualification":quals,"screen_solver_invocations":9,"qualification_solver_invocations":3}
  if good: final["winner"]=extra["o2b_winner"]
  json.dump(final,open(str(EVID/"summary.json"),"w"),indent=2)
  lines=["# H3B-T01A O2B Qualification","", "Canonical status: "+status+".","", "Nine frozen local-junction geometries were build-audited before any solve, then screened at exactly four adaptive passes.","Finalists: "+", ".join(x["candidate"] for x in finalists)+"."]
  if good:
    lines += ["","Winner: %s."%win["candidate"],"Pad width %.2f mm; gap %.2f mm; extension %.2f mm."%(win["pad_width_mm"],win["pad_gap_mm"],win["extension_mm"]),"Worst core return %.4f dB."%win["metrics"]["worst_core_return_db"],"Max junction excess %.4f dB."%win["metrics"]["junction_excess_max_db"],"Core S21 min %.4f dB."%win["metrics"]["core_s21_min_db"],"Preferred gate: %s."%("PASS" if win["preferred_gate"] else "FAIL"),"Next node: "+nextstage+"."]
  else: lines += ["","No finalist met frozen acceptable gates after high-fidelity qualification.","Next node: "+nextstage+"."]
  (EVID/"QUALIFICATION.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
  sim=["# SIM_EXECUTION","","## Protocol","Minimum compatible SimulationOps protocol: 0.2.7","","## Current stage","R1E1A4A_"+nextstage+"_AWAIT_AUTH","","BUILD_AUTHORIZED: false","SOLVE_AUTHORIZED: false","PRODUCTION_SOLVE_AUTHORIZED: false","LNA_INTEGRATION_AUTHORIZED: false","CST251_AUTHORIZED: false","","## O1","PASS_R1E1A4A_H3B_T01A_O1_LINE_CROSS_SECTION — Wsig 1.50 mm / Gcpw 0.40 mm","","## O2A","PASS_R1E1A4A_H3B_T01A_O2A_ACCEPTABLE","","## O2B",status]
  if good: sim += ["Winner: "+win["candidate"],"Worst core return: %.4f dB"%win["metrics"]["worst_core_return_db"],"Max junction excess: %.4f dB"%win["metrics"]["junction_excess_max_db"],"Preferred gate: %s"%("PASS" if win["preferred_gate"] else "FAIL")]
  sim += ["","## Immediate next node",nextstage,"","No BUILD or SOLVE authorization is currently open.","T01-C remains deferred."]
  (REPO/"docs"/"SIM_EXECUTION.md").write_text("\n".join(sim)+"\n",encoding="utf-8")
except Exception as e:
  EVID.mkdir(parents=True,exist_ok=True); status="HOLD_R1E1A4A_H3B_T01A_O2B_EXECUTION_EXCEPTION"; (EVID/"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8"); (EVID/"FINAL_STATUS.txt").write_text(status+"\n"); close(stage,status,"H3B_T01A_O2B_REVIEW",{"o2b_hold_reason":str(e)}); raise
finally:
  try:
    st=json.load(open(str(REPO/"execution"/"stage_contract.json"),encoding="utf-8"))
    for k in st["authorization"]: st["authorization"][k]=False
    (REPO/"execution"/"stage_contract.json").write_text(json.dumps(st,indent=2)+"\n",encoding="utf-8")
  except Exception: pass
subprocess.check_call(["git","add","docs","execution","evidence","scripts/run_r1e1a4a_h3b_t01a_o2b_local_doe_dc.py"],cwd=str(REPO)); subprocess.check_call(["git","commit","-m","Execute H3B T01A O2B local junction DOE"],cwd=str(REPO)); subprocess.check_call(["git","push","origin","project/r0-charts-scaffold"],cwd=str(REPO))
print(status)
if good: print("WINNER="+json.dumps(extra["o2b_winner"],sort_keys=True))
print("FINALISTS="+",".join(x["candidate"] for x in finalists)); print("HEAD="+git("rev-parse","HEAD"))
