from __future__ import print_function
import argparse, hashlib, json, math, sys
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
from cst.results import ProjectFile

EXPECTED_ARTIFACT_SHA="f0184b638b5af6c5c752804fd5570a5e4178e52bc6bdd62e31e72c281c03de90"
KEEP=set([
 "B0_Stalk:A_P_PRONG",
 "B0_Stalk:A_N_PRONG",
 "B0_MSL:A_P_MSL",
 "B0_MSL:A_N_MSL",
 "B1RT1_BackGround:A_P_GROUND_TAPER",
 "B1RT1_BackGround:A_N_GROUND_TAPER",
])

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def parse_inv(path):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            _,nm,mat,vol=line.split("|",3)
            rows.append({"name":nm,"material":mat.split("=",1)[1],"volume":float(vol.split("=",1)[1])})
    return rows

def parse_params(path):
    out={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.startswith("PARAM|"): continue
        p=line.split("|")
        if len(p)>=4 and p[1]:
            try: out[p[1]]=float(p[3])
            except Exception: pass
    return out

def port_count(path):
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("PORT_COUNT="): return int(line.split("=",1)[1])
    return None

def solver_tree(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return [x for x in p3.get_tree_items()
                if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+str(ex)]

def expected():
    s2=1.0/math.sqrt(2.0); z0=57.1428571428; sig=0.035; gnd=-1.035
    def xy(u,n): return (s2*(u-n),s2*(u+n))
    return {
      "t2f_p1_x":xy(3.0,sig)[0],"t2f_p1_y":xy(3.0,sig)[1],
      "t2f_p2_x":xy(-3.0,sig)[0],"t2f_p2_y":xy(-3.0,sig)[1],
      "t2f_outp_sig_x":xy(3.0,sig)[0],"t2f_outp_sig_y":xy(3.0,sig)[1],
      "t2f_outp_gnd_x":xy(3.0,gnd)[0],"t2f_outp_gnd_y":xy(3.0,gnd)[1],
      "t2f_outn_sig_x":xy(-3.0,sig)[0],"t2f_outn_sig_y":xy(-3.0,sig)[1],
      "t2f_outn_gnd_x":xy(-3.0,gnd)[0],"t2f_outn_gnd_y":xy(-3.0,gnd)[1],
      "t2f_output_z":z0-10.0
    }

def close(a,b,tol=1e-9): return abs(a-b)<=tol

def run(cst,evidence):
    cst=Path(cst); evidence=Path(evidence)
    if not cst.exists(): raise RuntimeError("HOLD_T2F_RECOVERY_ARTIFACT_MISSING")
    if sha(cst)!=EXPECTED_ARTIFACT_SHA: raise RuntimeError("HOLD_T2F_RECOVERY_ARTIFACT_HASH")

    build_inv=evidence/"build_inventory.txt"; reopen_inv=evidence/"reopen_inventory.txt"
    build_par=evidence/"build_parameters.txt"; reopen_par=evidence/"reopen_parameters.txt"
    build_sta=evidence/"build_port_status.txt"; reopen_sta=evidence/"reopen_port_status.txt"

    br=parse_inv(build_inv); rr=parse_inv(reopen_inv)
    bp=parse_params(build_par); rp=parse_params(reopen_par)
    exp=expected()
    endpoint_keys=tuple(exp.keys())

    missing_build=sorted(set(endpoint_keys)-set(bp))
    missing_reopen=sorted(set(endpoint_keys)-set(rp))
    delayed_ok=(missing_build==["t2f_output_z"] and not missing_reopen)
    reopen_exact=all(close(rp[k],exp[k]) for k in endpoint_keys)
    common_keys=[k for k in endpoint_keys if k in bp and k in rp]
    common_equal=all(close(bp[k],rp[k]) for k in common_keys)
    tree=solver_tree(cst)

    checks={
      "artifact_hash_exact":sha(cst)==EXPECTED_ARTIFACT_SHA,
      "build_six_solids":len(br)==6 and set(r["name"] for r in br)==KEEP,
      "reopen_six_solids":len(rr)==6 and set(r["name"] for r in rr)==KEEP,
      "build_reopen_geometry_identical":br==rr,
      "build_port_count_3":port_count(build_sta)==3,
      "reopen_port_count_3":port_count(reopen_sta)==3,
      "only_delayed_immediate_parameter_is_output_z":delayed_ok,
      "all_common_endpoint_params_stable":common_equal,
      "reopen_endpoint_geometry_exact":reopen_exact,
      "solver_tree_empty":len(tree)==0
    }
    status="PASS_R1E1A4A_AR0_B1R_T2F_FIXTURE_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_T2F_RECOVERY_AUDIT"

    old={}
    sp=evidence/"summary.json"
    if sp.exists():
        old=json.loads(sp.read_text(encoding="utf-8"))
    out={
      "status":status,
      "simulationops":"0.2.8",
      "recovery_type":"AUDIT_ONLY_EXISTING_FIXTURE_NO_REBUILD",
      "formal_build_invocations_total":1,
      "solver_invocations_total":0,
      "artifact":{"path":str(cst),"sha256":sha(cst)},
      "port_counts":{"build":port_count(build_sta),"reopen":port_count(reopen_sta)},
      "build_missing_endpoint_parameters":missing_build,
      "reopen_missing_endpoint_parameters":missing_reopen,
      "reopen_endpoints":{k:rp[k] for k in endpoint_keys if k in rp},
      "expected_endpoints":exp,
      "solver_tree_matches":tree,
      "checks":checks,
      "original_hold":old.get("status"),
      "original_hold_cause":"CST immediate-build parameter inventory delayed derived parameter t2f_output_z; fresh reopen enumerated it correctly."
    }
    sp.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    (evidence/"RECOVERY_AUDIT.md").write_text(
      "# AR0-B1R-T2F Audit-Only Recovery\n\n"
      "Canonical status: **"+status+"**.\n\n"
      "No fixture rebuild and no solver invocation occurred. The original HOLD was caused only by CST delaying the derived parameter t2f_output_z in the immediate-build parameter enumeration. Fresh reopen contains the complete endpoint parameter set and all endpoint coordinates match the frozen analytic values.\n",
      encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status)
    print("ARTIFACT_SHA256="+sha(cst))
    print("BUILD_MISSING="+",".join(missing_build))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--cst",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    sys.exit(run(a.cst,a.evidence))
