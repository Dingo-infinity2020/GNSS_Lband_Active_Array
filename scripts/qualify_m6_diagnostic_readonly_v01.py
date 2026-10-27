from __future__ import print_function
import argparse, csv, cmath, json, math, re, sys, traceback
from pathlib import Path
from cst.results import ProjectFile

SOURCE_PORTS=(1,2,4,5); ALL_ROWS=(1,2,3,4,5,6); SOURCE_SIDE=(1,2,4,5)

def db(z): return 20.0*math.log10(max(abs(z),1e-300))

def read_csv(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]; d={}
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            k="S%d%d"%(i,j)
            if k+"_real" in rows[0]:
                d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
    return f,d

def choose_run(p3,paths):
    common=None; allids={}
    for p in paths:
        ids=list(p3.get_run_ids(p,False)); allids[p]=ids
        common=set(ids) if common is None else common.intersection(ids)
    if not common: raise RuntimeError("HOLD_M6_DIAG_NO_COMMON_RUN")
    return max(common),allids

def read_responses(cst):
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d(); items=p3.get_tree_items()
    paths=[r"1D Results\S-Parameters\S%d,%d"%(i,j) for j in SOURCE_PORTS for i in ALL_ROWS]
    for p in paths:
        if p not in items: raise RuntimeError("HOLD_M6_DIAG_MISSING_RESPONSE:"+p)
    rid,ids=choose_run(p3,paths)
    data={}; freqs=None
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            p=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            vals=[(float(x[0]),complex(x[1])) for x in p3.get_result_item(p,rid).get_data()]
            fs=[x[0] for x in vals]
            if freqs is None: freqs=fs
            elif len(fs)!=len(freqs) or any(abs(a-b)>1e-9 for a,b in zip(fs,freqs)): raise RuntimeError("HOLD_M6_DIAG_GRID_MISMATCH")
            data[(i,j)]=[x[1] for x in vals]
    field_paths=[x for x in items if any(k in x.lower() for k in ("h-field","hfield","surface current","surfacecurrent"))]
    return freqs,data,{"selected_run_id":rid,"response_run_ids":ids,"field_result_paths":field_paths}

def native_log(cst):
    root=Path(cst).with_suffix("")
    texts=[]
    for p in root.rglob("*.txt"):
        try: texts.append(p.read_text(encoding="utf-8",errors="ignore"))
        except: pass
    t="\n".join(texts)
    vals=[float(x) for x in re.findall(r"All\s+S-Parameters\s*=\s*([0-9.+\-Ee]+)",t,re.I)]
    fatal=bool(re.search(r"fatal\s+error|solver\s+stopped\s+with\s+error",t,re.I))
    mesh=bool(re.search(r"mesh.{0,40}(corrupt|invalid)",t,re.I))
    return vals,{"fatal_error":fatal,"mesh_corruption":mesh}

def write_csv(path,freqs,data):
    hdr=["f_GHz"]
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            k="S%d%d"%(i,j); hdr += [k+"_real",k+"_imag",k+"_dB",k+"_phase_deg"]
    with open(str(path),"w",newline="") as f:
        w=csv.writer(f); w.writerow(hdr)
        for n,fr in enumerate(freqs):
            row=[fr]
            for j in SOURCE_PORTS:
                for i in ALL_ROWS:
                    z=data[(i,j)][n]; row += [z.real,z.imag,db(z),math.degrees(cmath.phase(z))]
            w.writerow(row)

def mode_dc(data,k):
    spp=data[(1,1)][k]; spn=data[(1,4)][k]; snp=data[(4,1)][k]; snn=data[(4,4)][k]
    return 0.5*(spp-spn+snp-snn)

def metrics(freqs,data,bfreq,bdata,m):
    if len(freqs)!=len(bfreq) or any(abs(a-b)>1e-9 for a,b in zip(freqs,bfreq)): raise RuntimeError("HOLD_M6_DIAG_BASELINE_GRID")
    core=[k for k,f in enumerate(freqs) if 1.15<=f<=1.65]
    maxd=(-1,None,None,None)
    for i in SOURCE_SIDE:
        for j in SOURCE_SIDE:
            for k in core:
                d=abs(data[(i,j)][k]-bdata[(i,j)][k])
                if d>maxd[0]: maxd=(d,k,i,j)
    vmode=max((abs(mode_dc(data,k)),k) for k in core)
    bmode=max((abs(mode_dc(bdata,k)),k) for k in core)
    vmode_db=db(vmode[0]); bmode_db=db(bmode[0]); degr=vmode_db-bmode_db
    imb=max((abs(db(data[(1,1)][k])-db(data[(4,4)][k])),k) for k in core)

    reciprocity=max(abs(data[(i,j)][k]-data[(j,i)][k]) for k in range(len(freqs)) for ix,i in enumerate(SOURCE_SIDE) for j in SOURCE_SIDE[ix+1:])
    powers=[sum(abs(data[(i,j)][k])**2 for i in ALL_ROWS) for k in range(len(freqs)) for j in SOURCE_PORTS]
    full=m["attribution_metrics"]
    fr={
      "raw":maxd[0]/float(full["raw_source_side_max_complex_delta"]["full_e2c_reference"]),
      "mode":max(0.0,degr)/float(full["eup_diff_to_common_degradation_db"]["full_e2c_degradation_db"]),
      "imbalance":imb[0]/float(full["eup_branch_return_imbalance_db"]["full_e2c_reference"])
    }
    strong=sum(1 for x in fr.values() if x>=0.60)>=2
    weak=all(x<=0.30 for x in fr.values())
    cls="STRONG" if strong else ("WEAK" if weak else "INTERMEDIATE")
    return {
      "raw_source_side_max_complex_delta":{"value":maxd[0],"frequency_ghz":freqs[maxd[1]],"ports":[maxd[2],maxd[3]]},
      "eup_diff_to_common":{"variant_peak_db":vmode_db,"baseline_peak_db":bmode_db,"degradation_db":degr,"frequency_ghz":freqs[vmode[1]]},
      "eup_branch_return_imbalance":{"max_abs_db":imb[0],"frequency_ghz":freqs[imb[1]]},
      "effect_fractions":fr,"variant_classification":cls,
      "source_side_reciprocity_max_abs_complex":reciprocity,
      "loaded_column_power_max":max(powers)
    }

def qualify(manifest_path,solved,evidence):
    manifest_path=Path(manifest_path); solved=Path(solved); evidence=Path(evidence)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    freqs,data,runmeta=read_responses(solved)
    bfreq,bdata=read_csv(Path(m["response_contract"]["baseline_csv"]))
    met=metrics(freqs,data,bfreq,bdata,m)
    vals,flags=native_log(solved)
    convergence=len(vals)>=2 and vals[-2]<=0.02 and vals[-1]<=0.02
    fields=runmeta["field_result_paths"]
    monitor_presence={str(f):any(str(f)[:5] in x for x in fields) for f in m["surface_current_evidence"]["frequencies_ghz"]}
    hard={
      "response_24_terms_complete":len(data)==24,
      "native_grid_1001_1p0_1p8":len(freqs)==1001 and abs(freqs[0]-1.0)<1e-9 and abs(freqs[-1]-1.8)<1e-9,
      "final_two_native_delta_s_lte_0p02":convergence,
      "source_side_reciprocity_lte_0p02":met["source_side_reciprocity_max_abs_complex"]<=0.02,
      "loaded_column_power_lte_1p02":met["loaded_column_power_max"]<=1.02,
      "no_fatal_solver_error":not flags["fatal_error"],
      "no_mesh_corruption":not flags["mesh_corruption"]
    }
    status="PASS_M6_%s_DIAGNOSTIC_NUMERICAL_QUALIFICATION"%m["variant"] if all(hard.values()) else "HOLD_M6_%s_DIAGNOSTIC_NUMERICAL_QUALIFICATION"%m["variant"]
    field_status="FIELD_RESULT_PATHS_PRESENT" if fields else "FIELD_RESULT_PATHS_REQUIRE_MANUAL_CST_REVIEW"
    summary={"status":status,"variant":m["variant"],"formal_solver_invocations":1,"automatic_retries":0,
             "hard_checks":hard,"native_delta_sequence":vals,"native_flags":flags,
             "metrics":met,"runmeta":runmeta,"surface_current_evidence_status":field_status,
             "monitor_frequency_path_hints":monitor_presence,
             "science_boundary":"Attribution class is provisional until D1 and D2 are both numerically qualified and current-path evidence is manually reviewed."}
    write_csv(evidence/"loaded_response_native.csv",freqs,data)
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    (evidence/"FIELD_CURRENT_REVIEW.md").write_text(
      "# M6 %s Field/Surface-Current Review\n\nReview 1.2276, 1.3384, 1.57542 GHz for source excitations 1 and 4 using identical display scale.\n\nCompare observer radiator/feed current and the passive diagnostic entities. Record whether current localization is signal-dominant, ground/via-dominant, or requires the composite structure.\n"%m["variant"],encoding="utf-8")
    print(status)
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--variant-manifest",required=True); ap.add_argument("--solved",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(qualify(a.variant_manifest,a.solved,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"QUALIFICATION_EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
