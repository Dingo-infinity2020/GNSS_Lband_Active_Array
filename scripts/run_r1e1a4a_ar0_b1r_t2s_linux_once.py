#!/usr/bin/env python3
import argparse, hashlib, json, os, shutil, subprocess, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

CST_EXECUTABLE="/opt/cst/CST_Studio_Suite_2022/cst_design_environment"
CONTAINER="cst2022"
UID="1004"
HOST_ROOT=Path("/data/jlding")
CONTAINER_ROOT="/work"
MIN_FREE_BYTES=1099511627776

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def atomic(path,obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=str(path.parent))
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            json.dump(obj,f,indent=2,sort_keys=True); f.write("\n")
        os.replace(tmp,str(path))
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def h2c(path):
    p=Path(path).resolve()
    rel=p.relative_to(HOST_ROOT)
    s=rel.as_posix()
    return CONTAINER_ROOT if s=="." else CONTAINER_ROOT+"/"+s

def active(container=False):
    cmd=["docker","exec","--user",UID,CONTAINER,"ps","-eo","state=,comm="] if container else ["ps","-eo","state=,comm="]
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
    if p.returncode: raise RuntimeError("process inspection failed: "+p.stdout)
    keep=[]
    for line in p.stdout.splitlines():
        q=line.strip().split(None,1)
        if len(q)<2 or q[0].startswith("Z"): continue
        c=q[1]
        if c.lower().startswith("cst_design_en") or c.startswith("modeler_AMD64") or c.startswith("Solver_HF_Tet") or c.startswith("TetMesh"):
            keep.append(line)
    return "\n".join(keep)

def run(a):
    if os.getuid()!=int(UID): raise RuntimeError("runner UID must be 1004")
    src=Path(a.project).resolve(); rundir=Path(a.run_dir).resolve()
    if not src.is_file() or sha(src)!=a.expected_sha256: raise RuntimeError("source identity failed")
    if rundir.exists() and any(rundir.iterdir()): raise RuntimeError("run dir not fresh")
    rundir.mkdir(parents=True,exist_ok=True)
    if shutil.disk_usage(str(rundir)).free < MIN_FREE_BYTES: raise RuntimeError("free space <1TiB")
    if active(False): raise RuntimeError("active CST on host")
    if active(True): raise RuntimeError("active CST in container")
    uid=subprocess.check_output(["docker","exec","--user",UID,CONTAINER,"id","-u"],universal_newlines=True).strip()
    if uid!=UID: raise RuntimeError("container UID mismatch")
    dst=rundir/src.name; shutil.copy2(str(src),str(dst)); dst.chmod(0o644)
    if sha(dst)!=a.expected_sha256: raise RuntimeError("staged copy hash mismatch")
    crun=h2c(rundir); cproj=crun+"/"+dst.name
    cmd=["docker","exec","--user",UID,"--workdir",crun,CONTAINER,CST_EXECUTABLE,"-m",cproj,"-f","--num-threads",str(a.threads)]
    status_path=rundir/"runtime_status.json"; log_path=rundir/"solver.log"
    status={"schema":"gnss_ar0_b1r_t2s_runtime_v1","status":"PREFLIGHT_PASS","source_sha256":a.expected_sha256,
            "project":str(dst),"container_project":cproj,"exact_command":cmd,"threads":a.threads,
            "solver_started":False,"actual_solver_launches":0,"retry_authorized":False,"start_utc":None,"end_utc":None}
    atomic(status_path,status)
    status.update({"status":"RUNNING","solver_started":True,"actual_solver_launches":1,"start_utc":now()}); atomic(status_path,status)
    with log_path.open("w",encoding="utf-8") as log:
        log.write("STAGE=AR0_B1R_T2S_TRANSITION_EM_QUALIFICATION\nSTART_UTC="+status["start_utc"]+"\nEXACT_COMMAND="+" ".join(cmd)+"\n")
        log.flush()
        p=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,universal_newlines=True)
        status["docker_exec_host_pid"]=p.pid; atomic(status_path,status)
        rc=p.wait()
    status.update({"status":"COMPLETED" if rc==0 else "HOLD_OUTER_EXIT_NONZERO","end_utc":now(),
                   "outer_exit_code":int(rc),"solver_finished":True,"post_run_project_sha256":sha(dst),
                   "post_run_project_size_bytes":dst.stat().st_size})
    atomic(status_path,status)
    print(json.dumps(status,indent=2,sort_keys=True))
    return int(rc)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",required=True); ap.add_argument("--expected-sha256",required=True)
    ap.add_argument("--run-dir",required=True); ap.add_argument("--threads",type=int,default=16)
    ap.add_argument("--execute",action="store_true"); ap.add_argument("--authorize-t2s",action="store_true")
    a=ap.parse_args()
    if not a.execute:
        print(json.dumps({"execute":False,"max_solver_launches":1,"retry":False},indent=2)); raise SystemExit(0)
    if not a.authorize_t2s: ap.error("--execute requires --authorize-t2s")
    raise SystemExit(run(a))
