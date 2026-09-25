"""H3B-T01A one-shot passive baseline solve on NW."""
from __future__ import print_function
import argparse, csv, hashlib, json, math, os, shutil, sys
LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOURCE_SHA="f321b678d390470a2420df40fd6d0cf6553cc041f9219bfcd011c7e41fbadf3d"

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def macro_body(path):
    lines=open(path,encoding="utf-8").read().replace("\r\n","\n").split("\n")
    return "\n".join(lines[lines.index("Sub Main()")+1:lines.index("End Sub")])

def port_count_vba(out):
    return "\n".join([
      "Dim f As Integer","f=FreeFile",
      'Open "%s" For Output As #f'%out,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f"
    ])

def parse_kv(path):
    d={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); d[k.strip()]=v.strip()
    return d

def read_s(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    p3=pf.get_3d(); tree=p3.get_tree_items()
    out={}
    for i,j in ((1,1),(1,2),(2,1),(2,2)):
        item=r"1D Results\S-Parameters\S%d,%d"%(i,j)
        if item not in tree:
            raise RuntimeError("HOLD_T01A_MISSING_RESULT:"+item)
        raw=p3.get_result_item(item).get_data()
        vals=[]
        for row in raw:
            f=float(row[0]); c=complex(row[1]); mag=abs(c)
            db=20*math.log10(max(mag,1e-300))
            vals.append((f,c.real,c.imag,mag,db))
        out["S%d%d"%(i,j)]=vals
    return out

def interp_nearest(vals,f0):
    return min(vals,key=lambda r:abs(r[0]-f0))

def summarize(data):
    core=(1.15,1.65)
    out={}
    for key,vals in data.items():
        cv=[r for r in vals if core[0]-1e-9<=r[0]<=core[1]+1e-9]
        out[key]={
          "samples":{str(f0):{"f_ghz":interp_nearest(vals,f0)[0],"db":interp_nearest(vals,f0)[4]} for f0 in (1.0,1.15,1.4,1.65,2.0)},
          "core_db_min":min(r[4] for r in cv),
          "core_db_max":max(r[4] for r in cv),
        }
    # Reciprocity in complex magnitude dB.
    diffs=[]
    for a,b in zip(data["S21"],data["S12"]):
        if abs(a[0]-b[0])<1e-9: diffs.append(abs(a[4]-b[4]))
    out["reciprocity_max_abs_db"]=max(diffs) if diffs else None
    out["core_s21_min_db"]=min(r[4] for r in data["S21"] if core[0]<=r[0]<=core[1])
    out["core_s21_max_db"]=max(r[4] for r in data["S21"] if core[0]<=r[0]<=core[1])
    out["core_s11_worst_db"]=max(r[4] for r in data["S11"] if core[0]<=r[0]<=core[1])
    out["core_s22_worst_db"]=max(r[4] for r in data["S22"] if core[0]<=r[0]<=core[1])
    return out

def write_csv(path,data):
    freqs=[r[0] for r in data["S11"]]
    with open(path,"w",newline="") as f:
        w=csv.writer(f); w.writerow(["f_GHz","S11_dB","S21_dB","S12_dB","S22_dB"])
        for n,fr in enumerate(freqs):
            w.writerow([fr,data["S11"][n][4],data["S21"][n][4],data["S12"][n][4],data["S22"][n][4]])

def run(repo,evidence,work,source):
    if os.path.exists(evidence): raise RuntimeError("HOLD_T01A_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_T01A_WORK_EXISTS")
    if not os.path.isfile(source) or sha(source)!=SOURCE_SHA:
        raise RuntimeError("HOLD_T01A_SOURCE_HASH_MISMATCH")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H3B_T01A_PASSIVE_BASELINE_V01.cst")
    shutil.copy2(source,dst)
    if sha(dst)!=SOURCE_SHA: raise RuntimeError("HOLD_T01A_COPY_HASH_MISMATCH")
    ports=os.path.join(repo,"source","cst","R1E1A4A_H3B_T01A_PORTS_V01.mcr")
    solver=os.path.join(repo,"source","cst","R1E1A4A_H3B_T01A_SOLVER_CONFIG_V01.mcr")

    # Configure solve copy only.
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.add_to_history("H3B-T01A Ports V0.1",macro_body(ports))
        prj.modeler.add_to_history("H3B-T01A Solver Config V0.1",macro_body(solver))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    configured_sha=sha(dst)
    pstatus=os.path.join(evidence,"presolve_status.txt")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.schematic.execute_vba_code("Sub Main()\n"+port_count_vba(pstatus)+"\nEnd Sub")
    finally:
        if prj is not None: prj.close()
        de.close()
    ps=parse_kv(pstatus)
    if int(ps.get("PORT_COUNT","-1"))!=2: raise RuntimeError("HOLD_T01A_PORT_COUNT_NOT_2")
    if sha(dst)!=configured_sha: raise RuntimeError("HOLD_T01A_CONFIG_CHANGED_DURING_REOPEN")

    # ONE formal solver invocation.
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(dst)
        prj.modeler.run_solver()
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    data=read_s(dst); summ=summarize(data)
    write_csv(os.path.join(evidence,"sparams.csv"),data)
    scientific={
      "preferred_return_loss_all_core": summ["core_s11_worst_db"]<=-15 and summ["core_s22_worst_db"]<=-15,
      "acceptable_return_loss_all_core": summ["core_s11_worst_db"]<=-10 and summ["core_s22_worst_db"]<=-10,
      "strong_return_loss_concern": summ["core_s11_worst_db"]>-3 or summ["core_s22_worst_db"]>-3,
      "preferred_insertion_loss": summ["core_s21_min_db"]>=-0.20,
      "insertion_loss_concern": summ["core_s21_min_db"]<-0.50,
      "topology_notch_concern": summ["core_s21_min_db"]<-3.0,
      "reciprocity_ok_0p1db": summ["reciprocity_max_abs_db"] is not None and summ["reciprocity_max_abs_db"]<=0.1
    }
    result={
      "mode":"H3B_T01A_PASSIVE_BASELINE_SOLVE",
      "simulationops":"0.2.6",
      "formal_solver_invocations":1,
      "source_build_sha256":SOURCE_SHA,
      "configured_copy_sha256":configured_sha,
      "solved_cst_sha256":sha(dst),
      "solved_cst":dst,
      "port_count":2,
      "frequency_ghz":[1.0,2.0],
      "decision_band_ghz":[1.15,1.65],
      "summary":summ,
      "scientific_diagnostics":scientific,
      "numerical_pass":"DEFER_TO_NATIVE_ADAPTATION_QUALIFICATION"
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(result,f,indent=2)
    with open(os.path.join(evidence,"FORMAL_STATUS.txt"),"w") as f: f.write("PASS_R1E1A4A_H3B_T01A_PASSIVE_BASELINE_SOLVE\n")
    print("PASS_R1E1A4A_H3B_T01A_PASSIVE_BASELINE_SOLVE")
    print("SOLVED_SHA256="+result["solved_cst_sha256"])
    print(json.dumps({"summary":summ,"scientific_diagnostics":scientific},sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True); ap.add_argument("--source-cst",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work,a.source_cst)
