from __future__ import print_function
import argparse, csv, hashlib, json, math, cmath, re, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

from cst.results import ProjectFile

SOURCE_PORTS=(1,2,4,5,7,8,10,11)
LOAD_ONLY_PORTS=(3,6,9,12)
ALL_ROWS=tuple(range(1,13))
CORE=(1.15,1.65)
S2=1.0/math.sqrt(2.0)

POL_MAP={
  "PolA":{"combined":[1,2,4,5],"baseline":[1,2,4,5]},
  "PolB":{"combined":[7,8,10,11],"baseline":[1,2,4,5]},
}

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def db(z):
    return 20.0*math.log10(max(abs(z),1e-300))

def copy_native(cst,evidence):
    result=Path(cst).with_suffix("")/"Result"
    copied=[]
    for n in ("output.txt","Model.log","log.tet"):
        p=result/n
        if p.exists():
            dst=Path(evidence)/("native_"+n.replace(".","_"))
            shutil.copy2(str(p),str(dst)); copied.append(str(dst))
    return copied

def native_text(evidence):
    out=""
    for n in ("native_output_txt","native_Model_log","native_log_tet"):
        p=Path(evidence)/n
        if p.exists():
            out+="\n"+p.read_text(encoding="utf-8",errors="ignore")
    return out

def native_flags(evidence):
    lo=native_text(evidence).lower()
    return {
      "fatal_error":("fatal error" in lo or "solver failed" in lo or "aborted due to" in lo),
      "mesh_corruption":("corrupt mesh" in lo or "mesh near the lumped element" in lo),
      "large_reflection_warning":"input reflection seems to be large" in lo,
      "disconnected_conductor_warning":"not connected to any good conductor" in lo
    }

def native_delta_sequence(evidence):
    txt=native_text(evidence)
    pats=[
      r"All\s+S-Parameters\s*=\s*([0-9.+Ee-]+)",
      r"Maximum difference of S-parameters[^=]*=\s*([0-9.+Ee-]+)",
      r"DeltaS\s*=\s*([0-9.+Ee-]+)"
    ]
    vals=[]
    for pat in pats:
        found=re.findall(pat,txt,re.I)
        if found:
            vals=[float(v) for v in found]; break
    return [{"ordinal":i+1,"delta_s":v} for i,v in enumerate(vals)]

def required_paths():
    return [r"1D Results\S-Parameters\S%d,%d"%(i,j)
            for j in SOURCE_PORTS for i in ALL_ROWS]

def choose_common_run(p3,paths):
    common=None; ids={}
    for path in paths:
        rids=list(p3.get_run_ids(path,False)); ids[path]=rids
        common=set(rids) if common is None else common.intersection(rids)
    if not common:
        raise RuntimeError("HOLD_E2C_S0_NO_COMMON_RESPONSE_RUN")
    return max(common),ids

def read_responses(cst):
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
    items=p3.get_tree_items(); paths=required_paths()
    missing=[x for x in paths if x not in items]
    if missing:
        raise RuntimeError("HOLD_E2C_S0_MISSING_RESPONSES:"+json.dumps(missing[:8]))
    rid,ids=choose_common_run(p3,paths)
    data={}; freqs=None
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            path=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            vals=[(float(x[0]),complex(x[1])) for x in p3.get_result_item(path,rid).get_data()]
            f=[x[0] for x in vals]
            if freqs is None: freqs=f
            elif len(f)!=len(freqs) or any(abs(a-b)>1e-9 for a,b in zip(f,freqs)):
                raise RuntimeError("HOLD_E2C_S0_GRID_MISMATCH:"+path)
            data[(i,j)]=vals
    return data,{"selected_run_id":rid,"response_run_ids":ids,
                 "frequency_count":len(freqs),"frequency_min_ghz":min(freqs),
                 "frequency_max_ghz":max(freqs)}
def read_baseline_csv(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    freqs=[float(r["f_GHz"]) for r in rows]
    data={}
    for j in (1,2,4,5):
        for i in (1,2,4,5):
            key="S%d%d"%(i,j)
            data[(i,j)]=[(freqs[k],complex(float(r[key+"_real"]),float(r[key+"_imag"])))
                         for k,r in enumerate(rows)]
    return freqs,data

def assert_same_grid(a,b,label,tol=1e-9):
    if len(a)!=len(b) or any(abs(x-y)>tol for x,y in zip(a,b)):
        raise RuntimeError("HOLD_E2C_S0_BASELINE_GRID_MISMATCH:"+label)

def core_indices(freqs):
    out=[k for k,f in enumerate(freqs) if CORE[0]-1e-12<=f<=CORE[1]+1e-12]
    if not out: raise RuntimeError("HOLD_E2C_S0_NO_CORE_SAMPLES")
    return out

def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def transpose(a):
    return [list(x) for x in zip(*a)]

T=[
 [S2,-S2,0,0],
 [S2, S2,0,0],
 [0,0,S2,-S2],
 [0,0,S2, S2],
]

def mixed_at(data,k,ports):
    # incoming semantic order = E_P, P_IN_P, E_N, P_IN_N
    e_p,p_p,e_n,p_n=ports
    order=[e_p,e_n,p_p,p_n]
    s=[[data[(i,j)][k][1] for j in order] for i in order]
    return matmul(matmul(T,s),transpose(T))

MODE_TERMS={
  "E_diff_to_common":(1,0),
  "E_common_to_diff":(0,1),
  "E_diff_to_PIN_common":(3,0),
  "E_common_to_PIN_diff":(2,1),
  "PIN_diff_to_common":(3,2),
  "PIN_common_to_diff":(2,3),
}

def peak_db_mixed(data,freqs,ports,indices):
    out={}
    mats={k:mixed_at(data,k,ports) for k in indices}
    for name,(i,j) in MODE_TERMS.items():
        pts=[(freqs[k],mats[k][i][j]) for k in indices]
        f,z=max(pts,key=lambda x:abs(x[1]))
        out[name]={"peak_db":db(z),"frequency_ghz":f}
    return out

def own_pol_delta(combined,baseline,freqs,cports,bports,indices):
    best={"max_abs_complex":-1.0}
    for ci,bi in zip(cports,bports):
        for cj,bj in zip(cports,bports):
            for k in indices:
                d=abs(combined[(ci,cj)][k][1]-baseline[(bi,bj)][k][1])
                if d>best["max_abs_complex"]:
                    best={"max_abs_complex":d,"frequency_ghz":freqs[k],
                          "combined_ports":[ci,cj],"baseline_ports":[bi,bj]}
    return best

def return_imbalance(data,freqs,e_p,e_n,indices):
    best={"max_abs_db":-1.0}
    for k in indices:
        d=abs(db(data[(e_p,e_p)][k][1])-db(data[(e_n,e_n)][k][1]))
        if d>best["max_abs_db"]:
            best={"max_abs_db":d,"frequency_ghz":freqs[k]}
    return best

def source_reciprocity(data,freqs):
    best={"max_abs_complex":-1.0}
    src=list(SOURCE_PORTS)
    for a in range(len(src)):
        for b in range(a+1,len(src)):
            i,j=src[a],src[b]
            for k,f in enumerate(freqs):
                d=abs(data[(i,j)][k][1]-data[(j,i)][k][1])
                if d>best["max_abs_complex"]:
                    best={"max_abs_complex":d,"frequency_ghz":f,"ports":[i,j]}
    best["pass"]=best["max_abs_complex"]<=0.02
    return best

def power_closure(data,freqs):
    hi={"sum_abs_s_sq":-1.0}; lo={"sum_abs_s_sq":1e99}
    for j in SOURCE_PORTS:
        for k,f in enumerate(freqs):
            p=sum(abs(data[(i,j)][k][1])**2 for i in ALL_ROWS)
            row={"sum_abs_s_sq":p,"frequency_ghz":f,"source_port":j}
            if p>hi["sum_abs_s_sq"]: hi=row
            if p<lo["sum_abs_s_sq"]: lo=row
    return {"max":hi,"min":lo,"pass":hi["sum_abs_s_sq"]<=1.02}
def cross_pol_device_coupling(data,freqs,indices):
    terms=[]
    # P_IN sources from one polarization into P_IN/P_OUT-load nodes of the other.
    for j in (2,5):
        for i in (8,9,11,12):
            terms.append((i,j))
    for j in (8,11):
        for i in (2,3,5,6):
            terms.append((i,j))
    best={"peak_db":-1e99}
    for i,j in terms:
        for k in indices:
            v=db(data[(i,j)][k][1])
            if v>best["peak_db"]:
                best={"peak_db":v,"frequency_ghz":freqs[k],"response_port":i,"source_port":j}
    return best

def resonance_scan(data,freqs,indices,width_ghz=0.05):
    # Pre-frozen deterministic detector: any off-diagonal solved trace with
    # >=10 dB max-min excursion inside any <=50 MHz core-band window.
    best={"excursion_db":-1.0}
    idx=list(indices)
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            if i==j: continue
            vals=[db(data[(i,j)][k][1]) for k in idx]
            for a in range(len(idx)):
                b=a
                while b+1<len(idx) and freqs[idx[b+1]]-freqs[idx[a]]<=width_ghz+1e-12:
                    b+=1
                if b<=a: continue
                window=vals[a:b+1]; exc=max(window)-min(window)
                if exc>best["excursion_db"]:
                    best={"excursion_db":exc,"f_start_ghz":freqs[idx[a]],
                          "f_end_ghz":freqs[idx[b]],"response_port":i,"source_port":j}
    return best

def write_response_csv(path,data):
    freqs=[x[0] for x in data[(1,1)]]
    header=["f_GHz"]
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            p="S%d_%d"%(i,j)
            header += [p+"_real",p+"_imag",p+"_dB",p+"_phase_deg"]
    with open(str(path),"w",newline="") as f:
        w=csv.writer(f);w.writerow(header)
        for k,fr in enumerate(freqs):
            row=[fr]
            for j in SOURCE_PORTS:
                for i in ALL_ROWS:
                    z=data[(i,j)][k][1]
                    row += [z.real,z.imag,db(z),math.degrees(cmath.phase(z))]
            w.writerow(row)

def analyze(combined,runmeta,manifest,evidence):
    freqs=[x[0] for x in combined[(1,1)]]
    idx=core_indices(freqs)

    baselines={}
    comparisons={}
    for pol in ("PolA","PolB"):
        bmeta=manifest["isolated_baselines"][pol]
        bpath=Path(bmeta["csv_path"])
        if not bpath.exists() or sha(bpath)!=bmeta["csv_sha256"]:
            raise RuntimeError("HOLD_E2C_S0_BASELINE_HASH:"+pol)
        bf,bdata=read_baseline_csv(bpath)
        assert_same_grid(freqs,bf,pol)
        baselines[pol]={"path":str(bpath),"sha256":sha(bpath)}
        cports=POL_MAP[pol]["combined"]; bports=POL_MAP[pol]["baseline"]
        delta=own_pol_delta(combined,bdata,freqs,cports,bports,idx)
        cmix=peak_db_mixed(combined,freqs,cports,idx)
        bmix=peak_db_mixed(bdata,bf,bports,idx)
        mode={}
        for name in MODE_TERMS:
            degradation=cmix[name]["peak_db"]-bmix[name]["peak_db"]
            mode[name]={"combined":cmix[name],"isolated":bmix[name],
                        "degradation_db":degradation}
        imb=return_imbalance(combined,freqs,cports[0],cports[2],idx)
        comparisons[pol]={"own_pol_complex_delta":delta,
                          "mode_conversion":mode,
                          "eup_return_imbalance":imb}

    recip=source_reciprocity(combined,freqs)
    power=power_closure(combined,freqs)
    cross=cross_pol_device_coupling(combined,freqs,idx)
    resonance=resonance_scan(combined,freqs,idx,0.05)

    t=manifest["review_thresholds"]
    review=[]; severe=[]
    for pol,c in comparisons.items():
        d=c["own_pol_complex_delta"]["max_abs_complex"]
        if d>t["own_pol_complex_delta_severe"]: severe.append(pol+":OWN_POL_COMPLEX_DELTA")
        elif d>t["own_pol_complex_delta_review"]: review.append(pol+":OWN_POL_COMPLEX_DELTA")
        for name,m in c["mode_conversion"].items():
            ddb=m["degradation_db"]
            if ddb>t["mode_conversion_degradation_severe_db"]: severe.append(pol+":"+name)
            elif ddb>t["mode_conversion_degradation_review_db"]: review.append(pol+":"+name)
        if c["eup_return_imbalance"]["max_abs_db"]>t["branch_eup_return_imbalance_review_db"]:
            review.append(pol+":EUP_RETURN_IMBALANCE")

    if cross["peak_db"]>t["cross_pol_device_coupling_severe_db"]:
        severe.append("CROSS_POL_DEVICE_COUPLING")
    elif cross["peak_db"]>t["cross_pol_device_coupling_review_db"]:
        review.append("CROSS_POL_DEVICE_COUPLING")
    if resonance["excursion_db"]>=t["resonance_excursion_db"]:
        review.append("NARROW_RESONANCE_MECHANISM")

    return {"baselines":baselines,"comparisons":comparisons,
            "source_side_reciprocity":recip,"loaded_power_closure":power,
            "cross_pol_device_coupling":cross,"resonance":resonance,
            "review_triggers":sorted(set(review)),
            "severe_triggers":sorted(set(severe))}
def main(solved_cst,sentinel_manifest,evidence):
    solved_cst=Path(solved_cst); sentinel_manifest=Path(sentinel_manifest); evidence=Path(evidence)
    evidence.mkdir(parents=True,exist_ok=True)
    manifest=json.loads(sentinel_manifest.read_text(encoding="utf-8"))

    if not solved_cst.exists() or not solved_cst.with_suffix("").exists():
        raise RuntimeError("HOLD_E2C_S0_SOLVED_ARTIFACT_MISSING")

    copied=copy_native(solved_cst,evidence)
    flags=native_flags(evidence)
    native_seq=native_delta_sequence(evidence)
    data,runmeta=read_responses(solved_cst)
    write_response_csv(evidence/"loaded_response_native.csv",data)
    science=analyze(data,runmeta,manifest,evidence)

    hard_checks={
      "required_96_responses_extracted":len(data)==96,
      "native_grid_1001_1p0_1p8":runmeta["frequency_count"]==1001 and abs(runmeta["frequency_min_ghz"]-1.0)<=1e-9 and abs(runmeta["frequency_max_ghz"]-1.8)<=1e-9,
      "native_final_two_delta_s_lte_0p02":len(native_seq)>=2 and native_seq[-2]["delta_s"]<=0.02 and native_seq[-1]["delta_s"]<=0.02,
      "source_side_reciprocity":science["source_side_reciprocity"]["pass"],
      "loaded_power_closure":science["loaded_power_closure"]["pass"],
      "no_fatal_solver_error":not flags["fatal_error"],
      "no_mesh_corruption":not flags["mesh_corruption"]
    }
    hard_pass=all(hard_checks.values())
    severe=bool(science["severe_triggers"])
    review=bool(science["review_triggers"])

    if not hard_pass:
        status="HOLD_E2C_S0_NUMERICAL_OR_RESPONSE_INTEGRITY"
        disposition="HOLD"
    elif severe:
        status="HOLD_E2C_S0_SEVERE_COEXISTENCE_REVIEW"
        disposition="SEVERE_REVIEW"
    elif review:
        status="REVIEW_E2C_S0_COEXISTENCE_SENTINEL"
        disposition="REVIEW"
    else:
        status="PASS_E2C_S0_COEXISTENCE_SENTINEL"
        disposition="DIRECT_PASS"

    summary={
      "status":status,"disposition":disposition,"simulationops":"0.2.25",
      "solved_artifact":str(solved_cst),"solved_artifact_sha256":sha(solved_cst),
      "sentinel_manifest_sha256":sha(sentinel_manifest),
      "formal_solver_invocations_expected":1,"automatic_retries_expected":0,
      "native_files_copied":copied,"native_delta_sequence":native_seq,
      "native_flags":flags,"runmeta":runmeta,"hard_checks":hard_checks,
      "science":science,
      "interpretation_boundary":[
        "This is a passive coexistence sentinel, not product input-match authority.",
        "C_IN and QPL9547 remain absent from the CST network.",
        "A non-severe REVIEW is classified offline before any geometry retune or network escalation.",
        "A severe trigger or hard numerical failure blocks C1 promotion."
      ]
    }
    (evidence/"qualification_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status)
    print("SOLVED_SHA256="+sha(solved_cst))
    return 0 if hard_pass else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--solved-cst",required=True)
    ap.add_argument("--sentinel-manifest",required=True)
    ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.solved_cst,a.sentinel_manifest,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_E2C_S0_READONLY_QUALIFICATION_EXECUTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
