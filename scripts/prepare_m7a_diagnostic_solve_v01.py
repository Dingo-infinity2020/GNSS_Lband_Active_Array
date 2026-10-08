from __future__ import print_function
import ast, csv, hashlib, json, math, os, sys
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
M7BUILD=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\build_only\M7A_INNER_EDGE_SETBACK_V01\R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK_BUILD_ONLY_V01.cst")
M7SHA="f9706d9f1be0c352690b150fdc0f4f8a64448d526b9772c0a59b9eb7c3bbc896"
GATE=ROOT/"execution"/"M7A_HUMAN_GEOMETRY_REVIEW_PASS.json"
BASEMAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_SENTINEL_MANIFEST_V01.json"
INV=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_INVENTORY_V01.json"
CONFIG=ROOT/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_COEXISTENCE_CONFIG_V01.mcr"
FULLCSV=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\E2C_S0_COEXISTENCE_20261002_V01\evidence\qualification\loaded_response_native.csv")
MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_DIAGNOSTIC_SOLVE_MANIFEST_V01.json"
RUN=ROOT/"scripts"/"run_m7a_diagnostic_solve_v01.py"
EVAL=ROOT/"scripts"/"evaluate_m7a_corrective_readonly_v01.py"
PKT=ROOT/"scripts"/"make_m7a_diagnostic_solve_packet_v01.py"
AUDIT=ROOT/"scripts"/"audit_m7a_diagnostic_solve_contract_v01.py"
DOC=ROOT/"docs"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_DIAGNOSTIC_SOLVE_FREEZE_V01.md"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_DIAGNOSTIC_SOLVE_PREP_V01"

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

if sha(M7BUILD)!=M7SHA or not M7BUILD.with_suffix("").exists():
    raise RuntimeError("HOLD_M7A_BUILD_AUTHORITY")
g=json.loads(GATE.read_text(encoding="utf-8-sig"))
if g["status"]!="PASS_M7A_HUMAN_GEOMETRY_REVIEW" or g["artifact_sha256"]!=M7SHA:
    raise RuntimeError("HOLD_M7A_HUMAN_GATE")
base=json.loads(BASEMAN.read_text(encoding="utf-8"))
if not FULLCSV.exists():
    raise RuntimeError("HOLD_FULL_E2C_RESPONSE_MISSING")
full_csv_sha=sha(FULLCSV)

m=json.loads(json.dumps(base))
m["schema_version"]="gnss-m7a-diagnostic-solve-v0.1"
m["status"]="FROZEN_READY_AWAIT_SOLVE_AUTH"
m["stage"]="R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_DIAGNOSTIC_SOLVE"
m["canonical_build"]={
    "path":str(M7BUILD),"sha256":M7SHA,"shape_count":177,"raw_port_count":24,
    "human_review":"PASS_M7A_HUMAN_GEOMETRY_REVIEW"
}
m["full_e2c_reference"]={
    "response_csv":str(FULLCSV),"response_csv_sha256":full_csv_sha,
    "raw_peak_ghz":1.3432,"raw_max_complex_delta":0.7037929224295506,
    "imbalance_anchor_ghz":1.2984,"imbalance_db":11.374270538449593
}
m["corrective_gate"]={
    "primary":{
      "definition":"For BOTH PolA and PolB: >=30% reduction versus full E2C in E_diff_to_common degradation at each full-E2C polarization's own severe peak anchor, AND >=30% reduction in E_UP branch-return imbalance at 1.2984 GHz.",
      "minimum_reduction_fraction":0.30,
      "require_both_polarizations":True
    },
    "secondary":{
      "definition":"Worst own-pol source-side complex deviation versus isolated baseline over 1.15-1.65 GHz is >=20% lower than frozen full-E2C worst reference.",
      "minimum_reduction_fraction":0.20
    },
    "guard":{
      "definition":"For every off-diagonal solved response, no <=50 MHz window may gain >6 dB excursion relative to the same full-E2C trace/window.",
      "max_new_excursion_db":6.0,"window_mhz":50.0
    },
    "classification":{
      "PASS_M7A_CORRECTIVE":"numerical hard gates pass AND primary pass AND guard pass",
      "REVIEW_M7A_PARTIAL_CORRECTION":"numerical hard gates pass AND guard pass AND primary fails but at least one primary reduction >=10% or secondary passes",
      "REJECT_M7A_INNER_EDGE_LEVER":"numerical hard gates pass AND guard pass AND primary fails with no >=10% primary improvement and secondary fails",
      "HOLD_M7A_CORRECTIVE_GUARD":"numerical hard gates pass but guard fails",
      "HOLD_M7A_NUMERICAL":"numerical hard gates fail"
    }
}
m["execution"]={
    "config_macro":str(CONFIG.relative_to(ROOT)).replace("\\","/"),
    "config_macro_sha256":sha(CONFIG),
    "inventory_contract":str(INV.relative_to(ROOT)).replace("\\","/"),
    "inventory_contract_sha256":sha(INV),
    "runner":"scripts/run_m7a_diagnostic_solve_v01.py",
    "evaluator":"scripts/evaluate_m7a_corrective_readonly_v01.py",
    "target_root":r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\M7A_DIAGNOSTIC_SOLVE_V01",
    "artifact_name":"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_DIAGNOSTIC_SOLVED_V01.cst",
    "formal_solver_budget":1,"automatic_retries":0,
    "stop_boundary":"STOP_AFTER_ONE_M7A_12PORT_SOLVE_READONLY_QUALIFICATION_AND_CORRECTIVE_GATE_NO_RETRY_NO_M7B"
}
m["authorization"]={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
MAN.write_text(json.dumps(m,indent=2)+"\n",encoding="utf-8")

EVAL.write_text(r'''from __future__ import print_function
import csv, json, math, sys, traceback
from pathlib import Path

SOURCE_PORTS=(1,2,4,5,7,8,10,11)
ALL_ROWS=tuple(range(1,13))
CORE=(1.15,1.65)
S2=1.0/math.sqrt(2.0)
T=[[S2,-S2,0,0],[S2,S2,0,0],[0,0,S2,-S2],[0,0,S2,S2]]
POL={"PolA":{"c":[1,2,4,5],"b":[1,2,4,5]},
     "PolB":{"c":[7,8,10,11],"b":[1,2,4,5]}}

def db(z): return 20.0*math.log10(max(abs(z),1e-300))
def matmul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return [list(x) for x in zip(*a)]

def read96(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]; d={}
    for j in SOURCE_PORTS:
      for i in ALL_ROWS:
        k="S%d_%d"%(i,j)
        d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
    return f,d

def read16(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]; d={}
    for j in (1,2,4,5):
      for i in (1,2,4,5):
        k="S%d%d"%(i,j)
        d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
    return f,d

def interp(xs,ys,x):
    if x<xs[0]-1e-10 or x>xs[-1]+1e-10: raise RuntimeError("HOLD_M7A_EXTRAPOLATION")
    if x<=xs[0]+1e-15:return ys[0]
    if x>=xs[-1]-1e-15:return ys[-1]
    lo=0;hi=len(xs)-1
    while hi-lo>1:
      mid=(lo+hi)//2
      if xs[mid]<=x:lo=mid
      else:hi=mid
    a=(x-xs[lo])/(xs[hi]-xs[lo])
    return ys[lo]+a*(ys[hi]-ys[lo])

def interp_set(sf,sd,tf):
    return {k:[interp(sf,v,x) for x in tf] for k,v in sd.items()}

def mixed(d,k,ports):
    ep,pp,en,pn=ports; order=[ep,en,pp,pn]
    s=[[d[(i,j)][k] for j in order] for i in order]
    return matmul(matmul(T,s),tr(T))

def mode_dc(d,k,ports): return mixed(d,k,ports)[1][0]

def nearest(freqs,x): return min(range(len(freqs)),key=lambda k:abs(freqs[k]-x))

def own_delta(d,b,cp,bp,idx):
    best=0.0
    for ci,bi in zip(cp,bp):
      for cj,bj in zip(cp,bp):
        for k in idx: best=max(best,abs(d[(ci,cj)][k]-b[(bi,bj)][k]))
    return best

def imbalance(d,k,ep,en): return abs(db(d[(ep,ep)][k])-db(d[(en,en)][k]))

def local_excursion_guard(cand,full,freqs,max_new=6.0,width=0.05):
    idx=[k for k,f in enumerate(freqs) if CORE[0]-1e-12<=f<=CORE[1]+1e-12]
    worst={"new_excursion_db":-1e99}
    for j in SOURCE_PORTS:
      for i in ALL_ROWS:
        if i==j: continue
        cv=[db(cand[(i,j)][k]) for k in idx]; fv=[db(full[(i,j)][k]) for k in idx]
        b=0
        for a in range(len(idx)):
          if b<a:b=a
          while b+1<len(idx) and freqs[idx[b+1]]-freqs[idx[a]]<=width+1e-12:b+=1
          if b<=a:continue
          ce=max(cv[a:b+1])-min(cv[a:b+1]); fe=max(fv[a:b+1])-min(fv[a:b+1])
          gain=ce-fe
          if gain>worst["new_excursion_db"]:
            worst={"new_excursion_db":gain,"candidate_excursion_db":ce,"full_excursion_db":fe,
                   "f_start_ghz":freqs[idx[a]],"f_end_ghz":freqs[idx[b]],
                   "response_port":i,"source_port":j}
    worst["pass"]=worst["new_excursion_db"]<=max_new
    return worst

def main(candidate_csv,manifest_path,numerical_summary,evidence):
    candidate_csv=Path(candidate_csv); manifest_path=Path(manifest_path)
    numerical_summary=Path(numerical_summary); evidence=Path(evidence); evidence.mkdir(parents=True,exist_ok=True)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    num=json.loads(numerical_summary.read_text(encoding="utf-8"))
    numerical_pass=all(num["hard_checks"].values())

    cf,cd=read96(candidate_csv)
    ff,fd=read96(Path(m["full_e2c_reference"]["response_csv"]))
    # Compare on immutable full-E2C 1001 point grid; interpolation is read-only if candidate differs.
    if len(cf)!=len(ff) or any(abs(a-b)>1e-9 for a,b in zip(cf,ff)):
        cd=interp_set(cf,cd,ff); cf=ff
        comparison_grid="candidate complex responses linearly interpolated onto full-E2C grid"
    else: comparison_grid="native grids identical"
    idx=[k for k,f in enumerate(ff) if CORE[0]-1e-12<=f<=CORE[1]+1e-12]

    polout={}
    primary_reductions=[]
    for pol in ("PolA","PolB"):
      bm=m["isolated_baselines"][pol]; bf,bd=read16(Path(bm["csv_path"]))
      if len(bf)!=len(ff) or any(abs(a-b)>1e-9 for a,b in zip(bf,ff)):
        bd=interp_set(bf,bd,ff); bf=ff
      cp=POL[pol]["c"]; bp=POL[pol]["b"]
      # Freeze mode anchor from full-E2C itself: peak |E_diff->common| in core.
      ak=max(idx,key=lambda k:abs(mode_dc(fd,k,cp)))
      anchor=ff[ak]
      full_deg=db(mode_dc(fd,ak,cp))-db(mode_dc(bd,ak,bp))
      cand_deg=db(mode_dc(cd,ak,cp))-db(mode_dc(bd,ak,bp))
      mode_red=(full_deg-cand_deg)/full_deg if full_deg>1e-12 else 0.0

      ik=nearest(ff,float(m["full_e2c_reference"]["imbalance_anchor_ghz"]))
      full_imb=imbalance(fd,ik,cp[0],cp[2]); cand_imb=imbalance(cd,ik,cp[0],cp[2])
      imb_red=(full_imb-cand_imb)/full_imb if full_imb>1e-12 else 0.0

      fraw=own_delta(fd,bd,cp,bp,idx); craw=own_delta(cd,bd,cp,bp,idx)
      raw_red=(fraw-craw)/fraw if fraw>1e-12 else 0.0
      polout[pol]={
        "mode_anchor_ghz":anchor,"full_mode_degradation_db":full_deg,
        "candidate_mode_degradation_db":cand_deg,"mode_reduction_fraction":mode_red,
        "imbalance_anchor_ghz":ff[ik],"full_imbalance_db":full_imb,
        "candidate_imbalance_db":cand_imb,"imbalance_reduction_fraction":imb_red,
        "full_own_pol_max_complex_delta":fraw,"candidate_own_pol_max_complex_delta":craw,
        "raw_reduction_fraction":raw_red
      }
      primary_reductions += [mode_red,imb_red]

    worst_full_raw=max(polout[p]["full_own_pol_max_complex_delta"] for p in polout)
    worst_cand_raw=max(polout[p]["candidate_own_pol_max_complex_delta"] for p in polout)
    secondary_red=(worst_full_raw-worst_cand_raw)/worst_full_raw
    primary_pass=min(primary_reductions)>=float(m["corrective_gate"]["primary"]["minimum_reduction_fraction"])
    secondary_pass=secondary_red>=float(m["corrective_gate"]["secondary"]["minimum_reduction_fraction"])
    guard=local_excursion_guard(cd,fd,ff,float(m["corrective_gate"]["guard"]["max_new_excursion_db"]),
                                 float(m["corrective_gate"]["guard"]["window_mhz"])/1000.0)
    if not numerical_pass: status="HOLD_M7A_NUMERICAL"
    elif not guard["pass"]: status="HOLD_M7A_CORRECTIVE_GUARD"
    elif primary_pass: status="PASS_M7A_CORRECTIVE"
    elif max(primary_reductions)>=0.10 or secondary_pass: status="REVIEW_M7A_PARTIAL_CORRECTION"
    else: status="REJECT_M7A_INNER_EDGE_LEVER"

    out={"schema_version":"gnss-m7a-corrective-evaluation-v0.1","status":status,
         "numerical_pass":numerical_pass,"comparison_grid":comparison_grid,
         "primary_pass":primary_pass,"secondary_pass":secondary_pass,"guard_pass":guard["pass"],
         "polarizations":polout,
         "secondary":{"worst_full_raw_delta":worst_full_raw,"worst_candidate_raw_delta":worst_cand_raw,
                      "reduction_fraction":secondary_red},
         "guard":guard,
         "boundary":"No M7B BUILD or further SOLVE is authorized by this result."}
    (evidence/"corrective_evaluation.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status); print(json.dumps(out,indent=2))
    return 0 if numerical_pass else 4

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--candidate-csv",required=True); ap.add_argument("--manifest",required=True)
    ap.add_argument("--numerical-summary",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.candidate_csv,a.manifest,a.numerical_summary,a.evidence))
    except Exception:
      Path(a.evidence).mkdir(parents=True,exist_ok=True)
      Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
      traceback.print_exc(); sys.exit(9)
''',encoding="utf-8")

RUN.write_text(r'''from __future__ import print_function
import argparse, json, sys, traceback
from pathlib import Path
LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
import configure_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_presolve as presolve
import qualify_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_readonly as qualifier
import evaluate_m7a_corrective_readonly_v01 as evaluator

def emit(phase,state,boundary,message=""):
    o={"schema_version":"simops-project-event-v0.1","event":"PHASE","phase":phase,"state":state,"production_boundary":boundary}
    if message:o["message"]=message
    print("SIMOPS_EVENT "+json.dumps(o,separators=(",",":")),flush=True)

def main(manifest_path,out,evidence):
    manifest_path=Path(manifest_path); out=Path(out); evidence=Path(evidence)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    source=Path(m["canonical_build"]["path"]); config=ROOT/m["execution"]["config_macro"]; inv=ROOT/m["execution"]["inventory_contract"]
    # Reuse the proven full-E2C 12-port presolve implementation, rebound only to the reviewed M7A source SHA.
    presolve.EXPECTED_SOURCE_SHA256=m["canonical_build"]["sha256"]
    presolve.HISTORY_LABEL="R4-A0-E2C-S0 M7A diagnostic presolve config V01"

    emit("presolve_config","START","NOT_OBSERVED")
    rc=presolve.main(source,config,inv,manifest_path,out,evidence/"presolve")
    if rc!=0:
        emit("presolve_config","HOLD","NOT_OBSERVED"); return 9
    emit("presolve_config","PASS","NOT_OBSERVED")
    evidence.mkdir(parents=True,exist_ok=True)
    invoc={"formal_solver_invocations":1,"automatic_retries":0,"retry_authorized":False,
           "solver_started":False,"source_sha256":m["canonical_build"]["sha256"]}
    (evidence/"solver_invocation.json").write_text(json.dumps(invoc,indent=2)+"\n",encoding="utf-8")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
      p=de.open_project(str(out))
      invoc["solver_started"]=True; (evidence/"solver_invocation.json").write_text(json.dumps(invoc,indent=2)+"\n",encoding="utf-8")
      emit("solver_run","START","OBSERVED")
      p.modeler.run_solver()
      p.save()
      emit("solver_run","PASS","OBSERVED")
    finally:
      if p is not None:p.close()
      de.close()

    invoc["solver_completed"]=True; invoc["solved_artifact_sha256"]=presolve.sha(out)
    (evidence/"solver_invocation.json").write_text(json.dumps(invoc,indent=2)+"\n",encoding="utf-8")
    emit("qualification","START","OBSERVED")
    qrc=qualifier.main(out,manifest_path,evidence/"qualification")
    qsum=evidence/"qualification"/"qualification_summary.json"
    if not qsum.exists():
      emit("qualification","HOLD","OBSERVED","missing numerical summary"); return 9
    emit("corrective_evaluation","START","OBSERVED")
    erc=evaluator.main(evidence/"qualification"/"loaded_response_native.csv",manifest_path,qsum,evidence/"corrective")
    final=(evidence/"corrective"/"FINAL_STATUS.txt").read_text(encoding="utf-8").strip()
    (evidence/"FINAL_STATUS.txt").write_text(final+"\n",encoding="utf-8")
    summary={"status":final,"formal_solver_invocations":1,"automatic_retries":0,
             "solved_artifact_sha256":presolve.sha(out),
             "numerical_qualification":str(qsum),
             "corrective_evaluation":str(evidence/"corrective"/"corrective_evaluation.json"),
             "next_boundary":"M7A_RESULT_REVIEW_NO_AUTOMATIC_M7B"}
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    emit("corrective_evaluation","PASS" if not final.startswith("HOLD_") else "HOLD","OBSERVED",final)
    emit("complete","PASS" if qrc==0 and erc==0 else "HOLD","OBSERVED",final)
    print(final); print("SOLVED_SHA256="+presolve.sha(out))
    return 0 if qrc==0 and erc==0 else 4

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--manifest",required=True); ap.add_argument("--out",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.manifest,a.out,a.evidence))
    except Exception:
      ev=Path(a.evidence); ev.mkdir(parents=True,exist_ok=True)
      marker=ev/"solver_invocation.json"; started=False
      if marker.exists():
        try:started=bool(json.loads(marker.read_text(encoding="utf-8")).get("solver_started"))
        except:started=True
      status="HOLD_M7A_POSTSOLVE_EXECUTION" if started else "HOLD_M7A_PRESOLVE_EXECUTION"
      (ev/"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
      (ev/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
      emit("complete","HOLD","OBSERVED" if started else "NOT_OBSERVED",status)
      traceback.print_exc(); sys.exit(9)
''',encoding="utf-8")

PKT.write_text(r'''from __future__ import print_function
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--project-root",required=True);ap.add_argument("--manifest",required=True)
 ap.add_argument("--packet",required=True);ap.add_argument("--state-root",required=True);ap.add_argument("--result-packet",required=True);ap.add_argument("--cst-python",required=True)
 a=ap.parse_args();root=Path(a.project_root).resolve();mp=Path(a.manifest).resolve();m=json.loads(mp.read_text(encoding="utf-8"))
 cpath=root/"execution"/"stage_contract.json";c=json.loads(cpath.read_text(encoding="utf-8-sig"))
 runner=root/"scripts"/"run_m7a_diagnostic_solve_v01.py";launcher=root/"scripts"/"cst_bundled_python_launcher_v01.py"
 evalp=root/"scripts"/"evaluate_m7a_corrective_readonly_v01.py";g=c.get("authorization",{}).get("active_grant")
 if subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip():raise SystemExit("HOLD_M7A_PROJECT_DIRTY")
 head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
 fail=[]
 if c["authorization"]["BUILD_AUTHORIZED"] is not False:fail.append("build_false")
 if c["authorization"]["SOLVE_AUTHORIZED"] is not True:fail.append("solve_live")
 if not isinstance(g,dict):fail.append("active_grant")
 if isinstance(g,dict):
  if g.get("kind")!="SOLVE":fail.append("grant_kind")
  if g.get("state")!="GRANTED":fail.append("grant_state")
  if g.get("stage")!=m["stage"]:fail.append("grant_stage")
  if g.get("entrypoint_sha256")!=sha(runner):fail.append("entrypoint_sha")
  if g.get("source_commit")!=c["project"]["source_commit"]:fail.append("source_commit")
 if c["execution"]["current_stage"]!=m["stage"]:fail.append("current_stage")
 if fail:raise SystemExit("HOLD_M7A_LIVE_SOLVE_GRANT:"+",".join(fail))
 target=Path(m["execution"]["target_root"]);artifact=target/m["execution"]["artifact_name"];evidence=target/"evidence"
 rel=lambda p:str(p.relative_to(root)).replace("\\","/")
 packet={"schema_version":"runner-task-v0.2","packet_id":"GNSS-M7A-DIAGNOSTIC-SOLVE-V01",
  "project":{"name":"GNSS_Lband_Active_Array","repository":"Dingo-infinity2020/GNSS_Lband_Active_Array","source_commit":c["project"]["source_commit"],"model_identity":m["stage"]},
  "stage":{"name":m["stage"],"kind":"SOLVE_LAUNCH","control_host_alias":"NW","working_directory":str(root),"stop_boundary":m["execution"]["stop_boundary"]},
  "transport":{"type":"local","ssh_alias":"","remote_shell":""},
  "preflight":{"fail_closed":True,"checks":[
   {"id":"git_clean","type":"git_clean","path":"."},{"id":"git_head","type":"git_head_equals","path":".","commit":head},
   {"id":"runner_hash","type":"file_sha256_equals","path":rel(runner),"sha256":sha(runner)},
   {"id":"evaluator_hash","type":"file_sha256_equals","path":rel(evalp),"sha256":sha(evalp)},
   {"id":"launcher_hash","type":"file_sha256_equals","path":rel(launcher),"sha256":sha(launcher)},
   {"id":"manifest_hash","type":"file_sha256_equals","path":rel(mp),"sha256":sha(mp)},
   {"id":"config_hash","type":"file_sha256_equals","path":m["execution"]["config_macro"],"sha256":m["execution"]["config_macro_sha256"]},
   {"id":"inventory_hash","type":"file_sha256_equals","path":m["execution"]["inventory_contract"],"sha256":m["execution"]["inventory_contract_sha256"]},
   {"id":"contract_hash","type":"file_sha256_equals","path":"execution/stage_contract.json","sha256":sha(cpath)},
   {"id":"source_hash","type":"file_sha256_equals","path":m["canonical_build"]["path"],"sha256":m["canonical_build"]["sha256"]},
   {"id":"full_e2c_hash","type":"file_sha256_equals","path":m["full_e2c_reference"]["response_csv"],"sha256":m["full_e2c_reference"]["response_csv_sha256"]},
   {"id":"target_absent","type":"path_absent","path":str(target)},{"id":"result_absent","type":"result_path_absent"},
   {"id":"cst_gui_absent","type":"process_absent","name":"CST DESIGN ENVIRONMENT_AMD64.exe","ignore_case":True},
   {"id":"cst_modeler_absent","type":"process_absent","name":"modeler_AMD64.exe","ignore_case":True}]},
  "entrypoint":{"argv":["python",rel(launcher),rel(runner),"--manifest",rel(mp),"--out",str(artifact),"--evidence",str(evidence)],
    "environment":{"CST_PYTHON_EXECUTABLE":str(Path(a.cst_python).resolve())},"timeout_seconds":9000},
  "authorization":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":True,"grant_snapshot":{"grant_id":g["grant_id"],"kind":g["kind"],"state":g["state"],"stage":g["stage"],"source_commit":g["source_commit"],"entrypoint_path":rel(runner),"entrypoint_sha256":sha(runner),"stage_contract_path":"execution/stage_contract.json","stage_contract_sha256":sha(cpath),"granted_at":g["granted_at"],"expires_at":g.get("expires_at"),"entrypoint_arg_index":2}},
  "dc_call_budget":{"target_calls":1,"polling_policy":"no_polling","remote_mcp_calls_target":3},
  "expected_outputs":[{"path":str(artifact),"required":True,"sha256":True},{"path":str(evidence/"solver_invocation.json"),"required":True,"sha256":True},{"path":str(evidence/"qualification"/"loaded_response_native.csv"),"required":True,"sha256":True},{"path":str(evidence/"corrective"/"corrective_evaluation.json"),"required":True,"sha256":True},{"path":str(evidence/"summary.json"),"required":True,"sha256":True},{"path":str(evidence/"FINAL_STATUS.txt"),"required":True,"sha256":True}],
  "result":{"state_root":str(Path(a.state_root).resolve()),"result_packet_path":str(Path(a.result_packet).resolve())}}
 p=Path(a.packet);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(packet,indent=2)+"\n",encoding="utf-8");print("PASS_M7A_SOLVE_PACKET_GENERATED");return 0
if __name__=="__main__":sys.exit(main())
''',encoding="utf-8")

AUDIT.write_text(r'''from __future__ import print_function
import ast, hashlib, json, sys
from pathlib import Path
ROOT=Path(r"D:\GNSS_R4A0E1_20260928"); MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_DIAGNOSTIC_SOLVE_MANIFEST_V01.json"
RUN=ROOT/"scripts"/"run_m7a_diagnostic_solve_v01.py"; EVAL=ROOT/"scripts"/"evaluate_m7a_corrective_readonly_v01.py"; PKT=ROOT/"scripts"/"make_m7a_diagnostic_solve_packet_v01.py"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_DIAGNOSTIC_SOLVE_PREP_V01"/"STATIC_AUDIT.json"
def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def rcalls(p):
 t=ast.parse(p.read_text(encoding="utf-8"));calls=[]
 for x in ast.walk(t):
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=="run_solver":calls.append(x)
 return t,calls
m=json.loads(MAN.read_text(encoding="utf-8"));t,c=rcalls(RUN)
inloop=False
if c:
 for n in ast.walk(t):
  if isinstance(n,(ast.For,ast.While)) and any(z is c[0] for z in ast.walk(n)):inloop=True
checks={
 "stage":m["stage"]=="R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_DIAGNOSTIC_SOLVE",
 "source_sha":m["canonical_build"]["sha256"]=="f9706d9f1be0c352690b150fdc0f4f8a64448d526b9772c0a59b9eb7c3bbc896",
 "source_exists":Path(m["canonical_build"]["path"]).exists(),
 "auth_false":m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},
 "twelve_port_sources":m["solve_network"]["source_ports"]==[1,2,4,5,7,8,10,11],
 "loads":m["solve_network"]["load_only_ports"]==[3,6,9,12],
 "solver_fidelity":m["solve_network"]["max_delta_s"]==0.02 and m["solve_network"]["consecutive_passes_required"]==2 and m["solve_network"]["max_passes"]==16,
 "primary_frozen":m["corrective_gate"]["primary"]["minimum_reduction_fraction"]==0.30 and m["corrective_gate"]["primary"]["require_both_polarizations"] is True,
 "secondary_frozen":m["corrective_gate"]["secondary"]["minimum_reduction_fraction"]==0.20,
 "guard_frozen":m["corrective_gate"]["guard"]["max_new_excursion_db"]==6.0 and m["corrective_gate"]["guard"]["window_mhz"]==50.0,
 "runner_one_solver":len(c)==1 and not inloop,
 "evaluator_zero_solver":len(rcalls(EVAL)[1])==0,
 "packet_zero_solver":len(rcalls(PKT)[1])==0,
 "packet_v02":'"schema_version":"runner-task-v0.2"' in PKT.read_text(encoding="utf-8"),
 "packet_solve_launch":'"kind":"SOLVE_LAUNCH"' in PKT.read_text(encoding="utf-8"),
 "packet_failclosed":"HOLD_M7A_LIVE_SOLVE_GRANT" in PKT.read_text(encoding="utf-8"),
 "config_no_monitor":"Monitor" not in (ROOT/m["execution"]["config_macro"]).read_text(encoding="utf-8")
}
status="PASS_M7A_DIAGNOSTIC_SOLVE_STATIC_CONTRACT" if all(checks.values()) else "HOLD_M7A_DIAGNOSTIC_SOLVE_STATIC_CONTRACT"
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps({"status":status,"checks":checks,"runner_sha256":sha(RUN),"evaluator_sha256":sha(EVAL),"packet_sha256":sha(PKT),"manifest_sha256":sha(MAN),"formal_solver_invocations":0},indent=2)+"\n",encoding="utf-8")
print(status)
for k,v in checks.items():
 if not v:print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
''',encoding="utf-8")

DOC.write_text("""# M7A Diagnostic SOLVE Freeze V0.1

M7A is solved with the exact full-E2C S0 12-port coexistence network: 12 retained ports, sources 1/2/4/5/7/8/10/11, passive 50-ohm loads 3/6/9/12, 1.0-1.8 GHz, second-order tetrahedral adaptive mesh, MaxDeltaS 0.02 for two consecutive checks, max 16 passes.

No H-field monitor is added. This intentionally preserves the full-E2C adaptive path and avoids the monitor-driven adaptation expansion seen in M6.

Corrective gates are frozen before solve:
- Primary: BOTH polarizations must show >=30% reduction versus full E2C in E_diff->common degradation at each full-E2C polarization's own severe mode peak frequency, AND >=30% reduction in branch-return imbalance at 1.2984 GHz.
- Secondary: worst own-pol source-side complex deviation over 1.15-1.65 GHz decreases >=20%.
- Guard: no off-diagonal solved response gains >6 dB local excursion relative to full E2C in any <=50 MHz window.

Exactly one formal solver invocation. No retry. M7B remains unauthorized.
""",encoding="utf-8")
print("PREPARED_M7A_DIAGNOSTIC_SOLVE")
print("FULL_E2C_CSV_SHA="+full_csv_sha)
print("RUNNER_SHA="+sha(RUN))
