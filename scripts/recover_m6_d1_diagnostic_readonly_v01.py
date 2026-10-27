from __future__ import print_function
import csv, cmath, hashlib, json, math, re, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
from cst.results import ProjectFile

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
SOLVED=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\M6_D1_DIAGNOSTIC_SOLVE_V01\R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_DIAGNOSTIC_SOLVED_V01.cst")
EXPECTED_SOLVED_SHA="b2f73c1007e0c37681e7685b367be0a4493356ebdfdf288e16a51c84bf2916c8"
BASE=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\E2A_S0L_SOLVE_20260929\evidence\loaded_response_native.csv")
EXPECTED_BASE_SHA="a759ac6135a297429a8a166b6a01a39a66b5ec3a861267ed0f05d53ff605fae4"
MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_DIAGNOSTIC_SOLVE_MANIFEST_V01.json"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_DIAGNOSTIC_READONLY_RECOVERY_V01"

SOURCE_PORTS=(1,2,4,5)
ALL_ROWS=(1,2,3,4,5,6)
SOURCE_SIDE=(1,2,4,5)

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def db(z):
    return 20.0*math.log10(max(abs(z),1e-300))

def read_baseline(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    freqs=[float(r["f_GHz"]) for r in rows]
    data={}
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            k="S%d%d"%(i,j)
            data[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
    return freqs,data

def choose_common_run(p3,paths):
    common=None; ids={}
    for p in paths:
        rids=list(p3.get_run_ids(p,False)); ids[p]=rids
        common=set(rids) if common is None else common.intersection(rids)
    if not common:
        raise RuntimeError("HOLD_RECOVERY_NO_COMMON_RESPONSE_RUN")
    return max(common),ids

def read_solved(path):
    pf=ProjectFile(str(path),allow_interactive=True)
    p3=pf.get_3d()
    items=p3.get_tree_items()
    paths=[r"1D Results\S-Parameters\S%d,%d"%(i,j) for j in SOURCE_PORTS for i in ALL_ROWS]
    for p in paths:
        if p not in items:
            raise RuntimeError("HOLD_RECOVERY_MISSING_RESPONSE:"+p)
    rid,allids=choose_common_run(p3,paths)
    freqs=None; data={}
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            p=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            vals=[(float(x[0]),complex(x[1])) for x in p3.get_result_item(p,rid).get_data()]
            fs=[x[0] for x in vals]
            if freqs is None:
                freqs=fs
            elif len(fs)!=len(freqs) or any(abs(a-b)>1e-10 for a,b in zip(fs,freqs)):
                raise RuntimeError("HOLD_RECOVERY_RESPONSE_GRID_MISMATCH")
            data[(i,j)]=[x[1] for x in vals]

    conv_paths=[x for x in items if "Convergence" in x and "S-Parameters" in x]
    conv={}
    for p in conv_paths:
        try:
            ids=list(p3.get_run_ids(p,False))
            per=[]
            for rr in ids:
                vals=[(float(x[0]),complex(x[1])) for x in p3.get_result_item(p,rr).get_data()]
                per.append({"run_id":rr,"values":[{"x":x,"real":z.real,"imag":z.imag} for x,z in vals]})
            conv[p]=per
        except Exception as ex:
            conv[p]={"error":repr(ex)}

    field_paths=[x for x in items if any(k in x.lower() for k in ("h-field","hfield","surface current","surfacecurrent","magnetic field"))]
    monitor_named=[x for x in items if "M6_HFIELD_SURFCURRENT" in x]
    return freqs,data,{
      "selected_response_run_id":rid,
      "response_run_ids":allids,
      "tree_item_count":len(items),
      "convergence_paths":conv,
      "field_paths":field_paths,
      "monitor_named_paths":monitor_named
    }

def interp_complex(xs,ys,x):
    if x < xs[0]-1e-12 or x > xs[-1]+1e-12:
        raise RuntimeError("HOLD_RECOVERY_EXTRAPOLATION")
    if x <= xs[0]+1e-15: return ys[0]
    if x >= xs[-1]-1e-15: return ys[-1]
    lo=0; hi=len(xs)-1
    while hi-lo>1:
        mid=(lo+hi)//2
        if xs[mid] <= x: lo=mid
        else: hi=mid
    a=(x-xs[lo])/(xs[hi]-xs[lo])
    return ys[lo]+a*(ys[hi]-ys[lo])

def interp_dataset(src_f,src_d,target_f):
    out={}
    for key,ys in src_d.items():
        out[key]=[interp_complex(src_f,ys,x) for x in target_f]
    return out

def mode_dc(d,k):
    return 0.5*(d[(1,1)][k]-d[(1,4)][k]+d[(4,1)][k]-d[(4,4)][k])

def compute_metrics(freqs,var,base,m):
    core=[k for k,f in enumerate(freqs) if 1.15-1e-12<=f<=1.65+1e-12]
    best=(-1,None,None,None)
    for i in SOURCE_SIDE:
        for j in SOURCE_SIDE:
            for k in core:
                v=abs(var[(i,j)][k]-base[(i,j)][k])
                if v>best[0]: best=(v,k,i,j)
    vp=max((abs(mode_dc(var,k)),k) for k in core)
    bp=max((abs(mode_dc(base,k)),k) for k in core)
    vdb=db(vp[0]); bdb=db(bp[0]); degr=vdb-bdb
    imb=max((abs(db(var[(1,1)][k])-db(var[(4,4)][k])),k) for k in core)

    reciprocity=max(abs(var[(i,j)][k]-var[(j,i)][k])
                    for k in range(len(freqs))
                    for ix,i in enumerate(SOURCE_SIDE)
                    for j in SOURCE_SIDE[ix+1:])
    powers=[sum(abs(var[(i,j)][k])**2 for i in ALL_ROWS)
            for k in range(len(freqs)) for j in SOURCE_PORTS]

    am=m["attribution_metrics"]
    fr={
      "raw":best[0]/float(am["raw_source_side_max_complex_delta"]["full_e2c_reference"]),
      "mode":max(0.0,degr)/float(am["eup_diff_to_common_degradation_db"]["full_e2c_degradation_db"]),
      "imbalance":imb[0]/float(am["eup_branch_return_imbalance_db"]["full_e2c_reference"])
    }
    strong=sum(1 for x in fr.values() if x>=0.60)>=2
    weak=all(x<=0.30 for x in fr.values())
    cls="STRONG" if strong else ("WEAK" if weak else "INTERMEDIATE")
    return {
      "raw_source_side_max_complex_delta":{"value":best[0],"frequency_ghz":freqs[best[1]],"ports":[best[2],best[3]]},
      "eup_diff_to_common":{"variant_peak_db":vdb,"baseline_peak_db":bdb,"degradation_db":degr,"frequency_ghz":freqs[vp[1]]},
      "eup_branch_return_imbalance":{"max_abs_db":imb[0],"frequency_ghz":freqs[imb[1]]},
      "source_side_reciprocity_max_abs_complex":reciprocity,
      "loaded_column_power_max":max(powers),
      "loaded_column_power_min":min(powers),
      "effect_fractions":fr,
      "variant_classification":cls
    }

def native_logs(companion):
    rec=[]
    for p in companion.rglob("*.txt"):
        try:
            t=p.read_text(encoding="utf-8",errors="ignore")
        except Exception:
            continue
        vals=[float(x) for x in re.findall(r"All\s+S-Parameters\s*=\s*([0-9.+\-Ee]+)",t,re.I)]
        if vals:
            rec.append({"path":str(p),"values":vals})
    return rec

def flatten_convergence(meta):
    candidates=[]
    for p,v in meta["convergence_paths"].items():
        if not isinstance(v,list): continue
        for run in v:
            vals=[]
            for q in run["values"]:
                # Convergence tree convention: x=pass, real=value.
                vals.append({"pass":q["x"],"delta_s":q["real"]})
            if vals:
                candidates.append({"path":p,"run_id":run["run_id"],"values":vals})
    return candidates

def main():
    if sha(SOLVED)!=EXPECTED_SOLVED_SHA:
        raise RuntimeError("HOLD_RECOVERY_SOLVED_SHA")
    if sha(BASE)!=EXPECTED_BASE_SHA:
        raise RuntimeError("HOLD_RECOVERY_BASE_SHA")
    if OUT.exists():
        raise RuntimeError("HOLD_RECOVERY_OUT_EXISTS")
    OUT.mkdir(parents=True)

    m=json.loads(MAN.read_text(encoding="utf-8"))
    bf,bd=read_baseline(BASE)
    sf,sd,meta=read_solved(SOLVED)

    if min(sf)>min(bf)+1e-9 or max(sf)<max(bf)-1e-9:
        raise RuntimeError("HOLD_RECOVERY_SOLVED_GRID_DOES_NOT_COVER_BASELINE")
    # Canonical comparison grid is immutable E2A 1001-point baseline grid.
    var_on_base=interp_dataset(sf,sd,bf)
    met=compute_metrics(bf,var_on_base,bd,m)

    logs=native_logs(SOLVED.with_suffix(""))
    conv=flatten_convergence(meta)
    all_log_vals=[]
    for x in logs: all_log_vals.extend(x["values"])

    # Strict frozen convergence authority:
    # PASS only if result-tree convergence OR one native log sequence shows final two <= 0.02.
    conv_pass_candidates=[]
    for x in conv:
        vals=[q["delta_s"] for q in x["values"]]
        if len(vals)>=2:
            conv_pass_candidates.append({"source":"result_tree","path":x["path"],"run_id":x["run_id"],
                                         "final_two":vals[-2:],"pass":vals[-2]<=0.02 and vals[-1]<=0.02})
    for x in logs:
        vals=x["values"]
        if len(vals)>=2:
            conv_pass_candidates.append({"source":"native_log","path":x["path"],
                                         "final_two":vals[-2:],"pass":vals[-2]<=0.02 and vals[-1]<=0.02})
    convergence_pass=any(x["pass"] for x in conv_pass_candidates)

    hard={
      "immutable_solved_sha":sha(SOLVED)==EXPECTED_SOLVED_SHA,
      "baseline_sha":sha(BASE)==EXPECTED_BASE_SHA,
      "response_24_terms_complete":len(sd)==24,
      "solved_grid_covers_baseline_1p0_1p8":min(sf)<=1.0+1e-9 and max(sf)>=1.8-1e-9,
      "canonical_comparison_grid_1001_1p0_1p8":len(bf)==1001 and abs(bf[0]-1.0)<1e-9 and abs(bf[-1]-1.8)<1e-9,
      "source_side_reciprocity_lte_0p02":met["source_side_reciprocity_max_abs_complex"]<=0.02,
      "loaded_column_power_lte_1p02":met["loaded_column_power_max"]<=1.02,
      "final_two_delta_s_lte_0p02_proven":convergence_pass
    }

    numeric_status="PASS_M6_D1_READONLY_RECOVERY_NUMERICAL" if all(hard.values()) else "HOLD_M6_D1_READONLY_RECOVERY_NUMERICAL"
    field_status="PASS_FIELD_PATHS_PRESENT" if (meta["field_paths"] or meta["monitor_named_paths"]) else "HOLD_FIELD_PATHS_NOT_DISCOVERED"

    result={
      "schema_version":"gnss-m6-d1-readonly-recovery-v0.1",
      "status":numeric_status,
      "classification":"READONLY_POSTSOLVE_RECOVERY_NO_RERUN",
      "formal_solver_invocations":1,
      "recovery_solver_invocations":0,
      "automatic_retries":0,
      "solved_artifact_sha256":EXPECTED_SOLVED_SHA,
      "baseline_sha256":EXPECTED_BASE_SHA,
      "grid":{
        "solved_count":len(sf),"solved_min_ghz":min(sf),"solved_max_ghz":max(sf),
        "baseline_count":len(bf),"baseline_min_ghz":min(bf),"baseline_max_ghz":max(bf),
        "comparison":"complex-linear interpolation of solved D1 responses onto immutable E2A 1001-point grid"
      },
      "hard_checks":hard,
      "convergence_candidates":conv_pass_candidates,
      "native_log_sequences":logs,
      "metrics":met,
      "field_evidence":{
        "status":field_status,
        "field_paths":meta["field_paths"],
        "monitor_named_paths":meta["monitor_named_paths"]
      },
      "science_interpretation_authority":(
        "ATTRIBUTION_CLASS_AUTHORITATIVE_FOR_D1_NUMERIC_METRICS"
        if all(hard.values()) else
        "ATTRIBUTION_CLASS_PROVISIONAL_ONLY_NUMERICAL_GATE_NOT_PROVEN"
      ),
      "boundary":"No rerun, no D2 solve, and no geometry optimization is authorized by this recovery."
    }
    (OUT/"summary.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    (OUT/"FINAL_STATUS.txt").write_text(numeric_status+"\n",encoding="utf-8")
    with open(str(OUT/"d1_response_on_e2a_grid.csv"),"w",newline="") as f:
        w=csv.writer(f)
        hdr=["f_GHz"]
        for j in SOURCE_PORTS:
            for i in ALL_ROWS:
                k="S%d%d"%(i,j); hdr += [k+"_real",k+"_imag",k+"_dB",k+"_phase_deg"]
        w.writerow(hdr)
        for n,fr in enumerate(bf):
            row=[fr]
            for j in SOURCE_PORTS:
                for i in ALL_ROWS:
                    z=var_on_base[(i,j)][n]
                    row += [z.real,z.imag,db(z),math.degrees(cmath.phase(z))]
            w.writerow(row)
    print(json.dumps(result,indent=2))
    return 0

if __name__=="__main__":
    try:
        sys.exit(main())
    except Exception:
        OUT.mkdir(parents=True,exist_ok=True)
        (OUT/"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
