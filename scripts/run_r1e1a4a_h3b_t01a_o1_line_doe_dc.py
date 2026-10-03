from __future__ import print_function
import os,sys,json,hashlib,math,csv,subprocess,shutil,traceback
from pathlib import Path

REPO=Path(r"D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold")
ROOT=Path(r"D:\GNSS_Lband_Active_Array")
EVID=REPO/"evidence"/"r1e1a4a_h3b_t01a_o1_nw_20260926_run01"
BROOT=ROOT/"_r1e1a4a_h3b_t01a_o1_build_work"
SROOT=ROOT/"_r1e1a4a_h3b_t01a_o1_screen_work"
QROOT=ROOT/"_r1e1a4a_h3b_t01a_o1_qual_work"
SELF=Path(__file__)
LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

CANDS=[(1.5,0.20),(1.5,0.30),(1.5,0.40),
       (1.8,0.20),(1.8,0.30),(1.8,0.40),
       (2.1,0.20),(2.1,0.30),(2.1,0.40)]

def git(*a): return subprocess.check_output(["git"]+list(a),cwd=str(REPO),universal_newlines=True).strip()
def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()
def body_text(txt):
    a=txt.replace("\r\n","\n").split("\n")
    return "\n".join(a[a.index("Sub Main()")+1:a.index("End Sub")])
def cid(w,g): return "W%02d_G%02d"%(round(w*10),round(g*100))
def brick(n,c,m,x1,x2,y1,y2,z1,z2):
    return ['    With Brick','        .Reset','        .Name "%s"'%n,'        .Component "%s"'%c,'        .Material "%s"'%m,
            '        .Xrange "%s", "%s"'%(x1,x2),'        .Yrange "%s", "%s"'%(y1,y2),'        .Zrange "%s", "%s"'%(z1,z2),
            '        .Create','    End With','']
def hole(n,x,y):
    return ['    With Cylinder','        .Reset','        .Name "%s"'%n,'        .Component "H3B_O1_Tools"','        .Material "Vacuum"',
            '        .OuterRadius "0.2"','        .InnerRadius "0"','        .Axis "z"','        .Zrange "-0.02", "1.02"',
            '        .Xcenter "%s"'%x,'        .Ycenter "%s"'%y,'        .Segments "0"','        .Create','    End With','']
def via(n,x,y):
    return ['    With Cylinder','        .Reset','        .Name "%s"'%n,'        .Component "H3B_O1_Via"','        .Material "PEC"',
            '        .OuterRadius "0.2"','        .InnerRadius "0.15"','        .Axis "z"','        .Zrange "0", "1"',
            '        .Xcenter "%s"'%x,'        .Ycenter "%s"'%y,'        .Segments "0"','        .Create','    End With','']
def make_macro(w,g):
    inner=w/2+g; outer=inner+2.2
    L=['Option Explicit','','\' H3B-T01A-O1 straight GCPW candidate - BUILD ONLY','Sub Main()','']
    pars={"h3b_o1_board_t":1.0,"h3b_o1_cu_t":0.035,"h3b_o1_wsig":w,"h3b_o1_gap":g,"h3b_o1_wgnd":2.2,
          "h3b_o1_rp1_y":12.0,"h3b_o1_rp2_y":-12.0,"h3b_o1_rp_spacing":24.0,
          "h3b_o1_freq_lo":1.0,"h3b_o1_freq_hi":2.0,"h3b_o1_decision_lo":1.15,"h3b_o1_decision_hi":1.65}
    for k,v in pars.items(): L.append('    StoreParameter "%s", %s'%(k,v))
    L += ['','    With Solid','        .SetAutoIntersectionCheckElMag "True"','        .SetAutoIntersectionCheckThermal "False"',
          '        .SetAutoIntersectionCheckMechanics "False"','    End With','',
          '    With Material','        .Reset','        .Name "FR4_COST_BASELINE"','        .Folder ""','        .FrqType "all"',
          '        .Type "Normal"','        .SetMaterialUnit "GHz", "mm"','        .Epsilon "4.3"','        .Mue "1.0"',
          '        .TanD "0.02"','        .TanDFreq "1.5"','        .TanDGiven "True"','        .TanDModel "ConstTanD"',
          '        .Create','    End With','']
    L += brick("REFERENCE_FR4","H3B_O1_Board","FR4_COST_BASELINE",-5,5,-16,16,0,1)
    L += brick("REF_SIG","H3B_O1_Line","PEC",-w/2,w/2,-14.5,14.5,-0.035,0)
    L += brick("REF_GND_L","H3B_O1_Line","PEC",-outer,-inner,-14.5,14.5,-0.035,0)
    L += brick("REF_GND_R","H3B_O1_Line","PEC",inner,outer,-14.5,14.5,-0.035,0)
    L += brick("REF_BACK_GND","H3B_O1_BackGround","PEC",-4,4,-14.5,14.5,1,1.035)
    for side,x in (("L",-2.3),("R",2.3)):
        for i,y in enumerate((-12,-9,-6,-3,3,6,9,12),1):
            hn="REF_VIAHOLE_%s_%d"%(side,i)
            L += hole(hn,x,y)
            L += ['    Solid.Subtract "H3B_O1_Board:REFERENCE_FR4", "H3B_O1_Tools:%s"'%hn,'']
            L += via("REF_VIA_%s_%d"%(side,i),x,y)
    L += ['','    \' BUILD ONLY: no RF ports and no solver.','End Sub','']
    return "\n".join(L)

PORTS='''Option Explicit
Sub Main()
    StoreParameter "h3b_o1_port_z0", 50.0
    With DiscretePort
        .Reset
        .PortNumber "1"
        .Type "SParameter"
        .Impedance "h3b_o1_port_z0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "0.0", "12.0", "-0.035"
        .SetP2 "False", "0.0", "12.0", "1.035"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With
    With DiscretePort
        .Reset
        .PortNumber "2"
        .Type "SParameter"
        .Impedance "h3b_o1_port_z0"
        .Voltage "1.0"
        .Current "1.0"
        .SetP1 "False", "0.0", "-12.0", "-0.035"
        .SetP2 "False", "0.0", "-12.0", "1.035"
        .InvertDirection "False"
        .Monitor "False"
        .Radius "0.0"
        .Create
    End With
End Sub
'''
SCREEN_SOLVER='''Option Explicit
Sub Main()
    Solver.FrequencyRange "1.0", "2.0"
    With Boundary
        .Xmin "open"
        .Xmax "open"
        .Ymin "open"
        .Ymax "open"
        .Zmin "open"
        .Zmax "open"
        .Xsymmetry "none"
        .Ysymmetry "none"
        .Zsymmetry "none"
        .ApplyInAllDirections "False"
    End With
    With Background
        .ResetBackground
        .XminSpace "30"
        .XmaxSpace "30"
        .YminSpace "30"
        .YmaxSpace "30"
        .ZminSpace "30"
        .ZmaxSpace "30"
        .ApplyInAllDirections "False"
    End With
    ChangeSolverType "HF Frequency Domain"
    With MeshSettings
        .SetMeshType "Tet"
        .Set "CurvatureOrder", "3"
    End With
    FDSolver.OrderTet "Second"
    FDSolver.SetMethod "Tetrahedral", "General purpose"
    With MeshAdaption3D
        .SetType "HighFrequencyTet"
        .SetAdaptionStrategy "ExpertSystem"
        .MinPasses "4"
        .MaxPasses "4"
        .MaxDeltaS "0.10"
        .NumberOfDeltaSChecks "1"
        .SetLinearGrowthLimitation "40"
    End With
    FDSolver.MeshAdaptionTet "True"
    PostProcess1D.ActivateOperation "yz-matrices", "TRUE"
End Sub
'''
def audit_vba(shape,status,inter):
    return '''Sub Main()
On Error Resume Next
Dim f As Integer, i As Long, nm As String
f=FreeFile
Open "%s" For Output As #f
Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())
For i=0 To Solid.GetNumberOfShapes()+80
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
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d(); tree=p3.get_tree_items()
    hits=[x for x in tree if "Adaptive Meshing" in x and x.endswith(r"S-Parameters\Delta\All S-Parameters")]
    if not hits: return []
    return [{"pass":int(round(float(r[0]))),"delta_s":float(complex(r[1]).real)} for r in p3.get_result_item(hits[0]).get_data()]
def metrics(data):
    core=(1.15,1.65)
    s11=[r[1] for r in data["S11"] if core[0]<=r[0]<=core[1]]
    s22=[r[1] for r in data["S22"] if core[0]<=r[0]<=core[1]]
    s21=[r[1] for r in data["S21"] if core[0]<=r[0]<=core[1]]
    return {"worst_core_return_db":max(max(s11),max(s22)),
            "core_s21_min_db":min(s21),"core_s21_max_db":max(s21),
            "reciprocity_max_abs_db":max(abs(a[1]-b[1]) for a,b in zip(data["S21"],data["S12"]))}
def fresh_solve(src,dst,solver_text,evid_dir,qual=False):
    shutil.copy2(str(src),str(dst))
    pre=sha(dst)
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(dst))
        prj.modeler.add_to_history("H3B-T01A-O1 ports",body_text(PORTS))
        prj.modeler.add_to_history("H3B-T01A-O1 solver",body_text(solver_text))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()
    configured=sha(dst)
    ps=evid_dir/"presolve_status.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(dst)); prj.schematic.execute_vba_code(port_vba(str(ps)))
    finally:
        if prj is not None: prj.close()
        de.close()
    if "PORT_COUNT=2" not in ps.read_text() or sha(dst)!=configured: raise RuntimeError("presolve audit failed "+str(dst))
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(dst)); prj.modeler.run_solver(); prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()
    d=read_s(dst); m=metrics(d); ad=read_adapt(dst)
    out={"source_build_sha256":pre,"configured_sha256":configured,"solved_sha256":sha(dst),
         "metrics":m,"adaptive_delta_sequence":ad,"formal_solver_invocations":1}
    if qual:
        out["numerically_qualified"]=len(ad)>=2 and ad[-1]["delta_s"]<=0.02 and ad[-2]["delta_s"]<=0.02
        out["final_two_delta_s"]=[ad[-2]["delta_s"],ad[-1]["delta_s"]] if len(ad)>=2 else None
        out["passes_executed"]=ad[-1]["pass"] if ad else None
    return out,d
def close_auth(stage,nextstage,status,extra=None):
    for k in stage["authorization"]: stage["authorization"][k]=False
    stage["execution"]["current_stage"]="R1E1A4A_"+nextstage+"_AWAIT_AUTH"
    stage["scientific_freeze"]["o1_status"]=status
    stage["scientific_freeze"]["next_stage"]=nextstage
    stage["scientific_freeze"]["stop_boundary"]="AWAIT NEXT-STAGE AUTHORIZATION; NO BUILD NO SOLVE"
    if extra: stage["scientific_freeze"].update(extra)
    (REPO/"execution"/"stage_contract.json").write_text(json.dumps(stage,indent=2)+"\n",encoding="utf-8")

SOURCE_HEAD=git("rev-parse","HEAD")
if git("status","--porcelain"): raise RuntimeError("working tree not clean")
stage=json.load(open(str(REPO/"execution"/"stage_contract.json"),encoding="utf-8"))
if stage["execution"]["current_stage"]!="R1E1A4A_H3B_T01A_O1_LINE_CROSS_SECTION_FREEZE_AWAIT_AUTH": raise RuntimeError("wrong stage")
for p in (EVID,BROOT,SROOT,QROOT):
    if p.exists(): raise RuntimeError("destination exists: "+str(p))

stage["project"]["source_commit"]=SOURCE_HEAD
for k in stage["authorization"]: stage["authorization"][k]=False
stage["authorization"]["BUILD_AUTHORIZED"]=True
stage["authorization"]["SOLVE_AUTHORIZED"]=True
stage["execution"]["current_stage"]="R1E1A4A_H3B_T01A_O1_EXECUTING"
stage["scientific_freeze"]["o1_released_variables"]={"Wsig_mm":[1.5,1.8,2.1],"Gcpw_mm":[0.20,0.30,0.40]}
stage["scientific_freeze"]["o1_fixed_variables"]="O0 geometry/material/RP/via/ports/boundary; ground rail 2.2 mm; backing ground 8 mm"
stage["scientific_freeze"]["o1_screening_fidelity"]="second-order tetrahedral; exactly 4 adaptive passes; PEC/FR4; 1-2 GHz"
stage["scientific_freeze"]["o1_qualification_fidelity"]="O0 high-fidelity: second-order tetrahedral; MaxDeltaS 0.02; 2 checks; MaxPasses 16"
stage["scientific_freeze"]["o1_winner_rule"]="screen top3 by lowest worst-core S11/S22 dB; tie by S21 then larger gap; final winner among numerically qualified candidates must meet >=12 dB worst-core return loss; prefer >=15 dB"
(REPO/"execution"/"stage_contract.json").write_text(json.dumps(stage,indent=2)+"\n",encoding="utf-8")
freeze=REPO/"docs"/"R1E1A4A_H3B_T01A_O1_LINE_CROSS_SECTION_FREEZE_V01.md"
freeze.write_text('''# H3B-T01A O1 Line Cross-Section Freeze V0.1

Status: AUTHORIZED TWO-LEVEL DOE ON NW

Released variables only:
- Wsig = 1.5 / 1.8 / 2.1 mm
- Gcpw = 0.20 / 0.30 / 0.40 mm

All other O0 geometry, FR4, RP spacing, ground-rail width, backing ground, via rule, ports, boundary and frequency range are frozen.

Screening:
- build and fresh-reopen audit all 9 candidates before solving;
- second-order tetrahedral, exactly 4 adaptive passes;
- screening results are ranking-only and can never be promoted to final PASS;
- select 3 finalists by lowest worst-case core-band S11/S22 dB; tie-break by S21, then larger gap.

Qualification:
- finalists are fresh-run from their clean build artifacts;
- second-order tetrahedral, DeltaS <= 0.02 for two checks, MaxPasses 16;
- no silent retry;
- an O1 winner must be numerically qualified and achieve at least 12 dB worst-case return loss across 1.15-1.65 GHz;
- 15 dB or better is preferred.
- no S21 notch below -3 dB and reciprocity <=0.05 dB.

Stop after O1 line-cross-section freeze. No junction optimization, T01-C, H3B integration or LNA work is authorized.
''',encoding="utf-8")
(REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_O1_SCREEN_SOLVER_V01.mcr").write_text(SCREEN_SOLVER,encoding="utf-8")
(REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_O1_PORTS_V01.mcr").write_text(PORTS,encoding="utf-8")
shutil.copy2(str(SELF),str(REPO/"scripts"/"run_r1e1a4a_h3b_t01a_o1_line_doe_dc.py"))
subprocess.check_call(["git","add","docs","execution","source/cst","scripts/run_r1e1a4a_h3b_t01a_o1_line_doe_dc.py"],cwd=str(REPO))
subprocess.check_call(["git","commit","-m","Freeze H3B T01A O1 line cross-section DOE"],cwd=str(REPO))
subprocess.check_call(["git","push","origin","project/r0-charts-scaffold"],cwd=str(REPO))
FREEZE_HEAD=git("rev-parse","HEAD")

EVID.mkdir(parents=True); BROOT.mkdir(); SROOT.mkdir(); QROOT.mkdir()
high_solver=(REPO/"source"/"cst"/"R1E1A4A_H3B_T01A_SOLVER_CONFIG_MAXPASS16_V01.mcr").read_text(encoding="utf-8")
manifest=[]; good=[]; finalists=[]; screening=[]; quals=[]; extra={}
try:
    for w,g in CANDS:
        name=cid(w,g); edir=EVID/name; edir.mkdir()
        macro=make_macro(w,g); (edir/"build_macro.mcr").write_text(macro,encoding="utf-8")
        bdir=BROOT/name; bdir.mkdir(); bfile=bdir/(name+"_BUILD_ONLY.cst")
        de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
        try:
            prj=de.new_mws(); prj.modeler.add_to_history("H3B-T01A-O1 "+name,body_text(macro))
            prj.save(str(bfile),include_results=False)
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
        rows=[x for x in shape.read_text().splitlines() if x.startswith("SHAPE|")]
        vols=[float(x.split("volume=",1)[1]) for x in rows]
        outp=Path(os.path.splitext(str(bfile))[0])/"Result"/"output.txt"
        tree=ProjectFile(str(bfile),allow_interactive=True).get_3d().get_tree_items()
        checks={"shape_count_21":len(rows)==21,"positive_volumes":all(v>0 for v in vols),
                "port_count_zero":"PORT_COUNT=0" in stat.read_text(),
                "intersection_returned":ok and "RETURNED=TRUE" in inter.read_text(),
                "no_solver_output":not outp.exists(),
                "no_solver_results":not any("S-Parameters" in x or "Adaptive Meshing" in x for x in tree),
                "hash_stable":sha(bfile)==bh}
        json.dump({"candidate":name,"Wsig_mm":w,"Gcpw_mm":g,"build_sha256":bh,"checks":checks},
                  open(str(edir/"build_summary.json"),"w"),indent=2)
        if not all(checks.values()): raise RuntimeError("BUILD_HOLD %s %s"%(name,json.dumps(checks)))
        manifest.append({"candidate":name,"Wsig_mm":w,"Gcpw_mm":g,"build_file":str(bfile),"build_sha256":bh})
    json.dump(manifest,open(str(EVID/"candidate_manifest.json"),"w"),indent=2)

    for c in manifest:
        name=c["candidate"]; edir=EVID/name; sed=edir/"screen"; sed.mkdir()
        sdir=SROOT/name; sdir.mkdir(); dst=sdir/(name+"_SCREEN.cst")
        res,data=fresh_solve(Path(c["build_file"]),dst,SCREEN_SOLVER,sed,qual=False)
        row={"candidate":name,"Wsig_mm":c["Wsig_mm"],"Gcpw_mm":c["Gcpw_mm"],**res["metrics"],
             "solved_sha256":res["solved_sha256"],"formal_solver_invocations":1}
        screening.append(row); json.dump(res,open(str(sed/"summary.json"),"w"),indent=2)
    screening.sort(key=lambda r:(r["worst_core_return_db"],-r["core_s21_min_db"],-r["Gcpw_mm"],abs(r["Wsig_mm"]-1.8)))
    finalists=screening[:3]
    json.dump({"screening_rank":screening,"finalists":[x["candidate"] for x in finalists]},
              open(str(EVID/"screening_summary.json"),"w"),indent=2)

    for rank,c in enumerate(finalists,1):
        name=c["candidate"]; m=next(x for x in manifest if x["candidate"]==name)
        qed=EVID/name/"qual"; qed.mkdir()
        qdir=QROOT/name; qdir.mkdir(); dst=qdir/(name+"_QUAL.cst")
        res,data=fresh_solve(Path(m["build_file"]),dst,high_solver,qed,qual=True)
        mm=res["metrics"]
        pass_rf=(mm["worst_core_return_db"]<=-12.0 and mm["core_s21_min_db"]>=-3.0 and mm["reciprocity_max_abs_db"]<=0.05)
        res["rf_acceptance_pass"]=pass_rf
        res["candidate"]=name; res["Wsig_mm"]=m["Wsig_mm"]; res["Gcpw_mm"]=m["Gcpw_mm"]; res["screen_rank"]=rank
        res["qualified_pass"]=bool(res["numerically_qualified"] and pass_rf)
        json.dump(res,open(str(qed/"summary.json"),"w"),indent=2)
        quals.append(res)
    good=[q for q in quals if q["qualified_pass"]]
    good.sort(key=lambda q:(q["metrics"]["worst_core_return_db"],-q["metrics"]["core_s21_min_db"],-q["Gcpw_mm"],abs(q["Wsig_mm"]-1.8)))
    if not good:
        status="HOLD_R1E1A4A_H3B_T01A_O1_NO_ACCEPTABLE_LINE"
        extra={"o1_screening_rank":screening,"o1_finalists":[x["candidate"] for x in finalists],"o1_qualification":quals}
        close_auth(stage,"H3B_T01A_O1_REVIEW",status,extra)
    else:
        win=good[0]; pref=win["metrics"]["worst_core_return_db"]<=-15.0
        status="PASS_R1E1A4A_H3B_T01A_O1_LINE_CROSS_SECTION"
        extra={"o1_screening_rank":screening,"o1_finalists":[x["candidate"] for x in finalists],
               "o1_qualification":quals,"o1_winner":{"candidate":win["candidate"],"Wsig_mm":win["Wsig_mm"],
               "Gcpw_mm":win["Gcpw_mm"],"worst_core_return_db":win["metrics"]["worst_core_return_db"],
               "core_s21_min_db":win["metrics"]["core_s21_min_db"],"preferred_15db_met":pref,
               "solved_sha256":win["solved_sha256"]}}
        close_auth(stage,"H3B_T01A_O2_JUNCTION_OPTIMIZATION_FREEZE",status,extra)
    (EVID/"FINAL_STATUS.txt").write_text(status+"\n")
    final={"status":status,"freeze_head":FREEZE_HEAD,"screening_rank":screening,
           "finalists":[x["candidate"] for x in finalists],"qualification":quals,
           "screen_solver_invocations":len(screening),"qualification_solver_invocations":len(quals)}
    if good: final["winner"]=extra["o1_winner"]
    json.dump(final,open(str(EVID/"summary.json"),"w"),indent=2)
    lines=["# H3B-T01A O1 Qualification","", "Canonical status: "+status+".","",
           "Screening used all 9 frozen Wsig/Gcpw points at exactly four adaptive passes.",
           "Only the top three screening candidates were rerun from clean build artifacts at full O0 numerical fidelity.","",
           "Screening finalists: "+", ".join(x["candidate"] for x in finalists)+"."]
    if good:
        lines += ["","Qualified O1 winner: %s (Wsig %.2f mm, gap %.2f mm)."%(win["candidate"],win["Wsig_mm"],win["Gcpw_mm"]),
                  "Worst core-band return: %.3f dB."%win["metrics"]["worst_core_return_db"],
                  "Core-band minimum S21: %.3f dB."%win["metrics"]["core_s21_min_db"],
                  "Preferred 15 dB match target met: %s."%("YES" if pref else "NO"),
                  "Next node: H3B_T01A_O2_JUNCTION_OPTIMIZATION_FREEZE."]
    else:
        lines += ["","No finalist simultaneously passed native convergence and the frozen >=12 dB worst-core return-loss acceptance.","Next node is O1 review HOLD."]
    (EVID/"QUALIFICATION.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    if good:
        nxt="H3B_T01A_O2_JUNCTION_OPTIMIZATION_FREEZE"
        details=["O1 winner: %s"%win["candidate"],"Wsig: %.2f mm"%win["Wsig_mm"],"Gcpw: %.2f mm"%win["Gcpw_mm"],
                 "Worst core return: %.3f dB"%win["metrics"]["worst_core_return_db"],"Core minimum S21: %.3f dB"%win["metrics"]["core_s21_min_db"]]
    else:
        nxt="H3B_T01A_O1_REVIEW"; details=["No acceptable O1 winner."]
    sim=["# SIM_EXECUTION","","## Protocol","Minimum compatible SimulationOps protocol: 0.2.7","",
         "## Current stage","R1E1A4A_"+nxt+"_AWAIT_AUTH","",
         "BUILD_AUTHORIZED: false","SOLVE_AUTHORIZED: false","PRODUCTION_SOLVE_AUTHORIZED: false",
         "LNA_INTEGRATION_AUTHORIZED: false","CST251_AUTHORIZED: false","",
         "## T01-A baseline","PASS_R1E1A4A_H3B_T01A_NUMERICALLY_CONVERGED_MAXPASS16","",
         "## O0","PASS_R1E1A4A_H3B_T01A_O0_STRAIGHT_REFERENCE","",
         "## O1",status]+details+["","## Immediate next node",nxt,"","No BUILD or SOLVE authorization is currently open.","T01-C remains deferred."]
    (REPO/"docs"/"SIM_EXECUTION.md").write_text("\n".join(sim)+"\n",encoding="utf-8")
except Exception as e:
    status="HOLD_R1E1A4A_H3B_T01A_O1_EXECUTION_EXCEPTION"
    EVID.mkdir(parents=True,exist_ok=True)
    (EVID/"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
    (EVID/"FINAL_STATUS.txt").write_text(status+"\n")
    close_auth(stage,"H3B_T01A_O1_REVIEW",status,{"o1_hold_reason":str(e)})
    raise
finally:
    try:
        st=json.load(open(str(REPO/"execution"/"stage_contract.json"),encoding="utf-8"))
        for k in st["authorization"]: st["authorization"][k]=False
        (REPO/"execution"/"stage_contract.json").write_text(json.dumps(st,indent=2)+"\n",encoding="utf-8")
    except Exception: pass

subprocess.check_call(["git","add","docs","execution","evidence","source/cst","scripts/run_r1e1a4a_h3b_t01a_o1_line_doe_dc.py"],cwd=str(REPO))
subprocess.check_call(["git","commit","-m","Execute H3B T01A O1 line cross-section DOE"],cwd=str(REPO))
subprocess.check_call(["git","push","origin","project/r0-charts-scaffold"],cwd=str(REPO))
print(status)
if good: print("WINNER="+json.dumps(extra["o1_winner"],sort_keys=True))
print("SCREEN_FINALISTS="+",".join(x["candidate"] for x in finalists))
print("HEAD="+git("rev-parse","HEAD"))
