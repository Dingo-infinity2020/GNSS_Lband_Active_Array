from __future__ import print_function
import argparse, json, os, queue, subprocess, sys, threading, time

PREFIX="SIMOPS_EVENT "

def emit_phase(phase,state,boundary,message=None):
    obj={"schema_version":"simops-project-event-v0.1","event":"PHASE",
         "phase":phase,"state":state,"production_boundary":boundary}
    if message: obj["message"]=message
    print(PREFIX+json.dumps(obj,separators=(",",":")),flush=True)

def emit_provenance(component,data):
    print(PREFIX+json.dumps({"schema_version":"simops-project-event-v0.1",
      "event":"PROVENANCE","component":component,"data":data},separators=(",",":")),flush=True)

def kill_tree(pid):
    if os.name=="nt":
        subprocess.run(["taskkill","/PID",str(pid),"/T","/F"],
                       stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=False)
    else:
        try: os.kill(pid,9)
        except Exception: pass

def reader(stream,kind,q):
    try:
        for line in iter(stream.readline,""):
            q.put((kind,line))
    finally:
        q.put((kind,None))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--startup-timeout",type=float,default=90.0)
    ap.add_argument("--phase-budgets-json",required=True)
    ap.add_argument("child_argv",nargs=argparse.REMAINDER)
    a=ap.parse_args()
    child=list(a.child_argv)
    if child and child[0]=="--": child=child[1:]
    if not child: raise SystemExit("HOLD_WATCHDOG_NO_CHILD_ARGV")
    exe=os.environ.get("CST_PYTHON_EXECUTABLE","").strip()
    if not exe or not os.path.isabs(exe) or not os.path.exists(exe):
        raise SystemExit("HOLD_WATCHDOG_CST_RUNTIME_INVALID")
    budgets=json.loads(a.phase_budgets_json)
    emit_provenance("e2c_cst_watchdog",{"cst_python":exe,"child_argv":child,"budgets_seconds":budgets})
    proc=subprocess.Popen([exe]+child,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          text=True,bufsize=1,shell=False)
    q=queue.Queue()
    threading.Thread(target=reader,args=(proc.stdout,"stdout",q),daemon=True).start()
    threading.Thread(target=reader,args=(proc.stderr,"stderr",q),daemon=True).start()
    deadline=time.monotonic()+a.startup_timeout
    current_phase="startup"
    boundary="UNKNOWN"
    ended=set()
    while True:
        now=time.monotonic()
        if proc.poll() is None and deadline is not None and now>deadline:
            emit_phase(current_phase,"HOLD",boundary,"phase watchdog timeout")
            kill_tree(proc.pid)
            try: proc.wait(timeout=10)
            except Exception: pass
            return 124
        if proc.poll() is not None and len(ended)==2 and q.empty():
            return int(proc.returncode or 0)
        try:
            kind,line=q.get(timeout=0.2)
        except queue.Empty:
            continue
        if line is None:
            ended.add(kind); continue
        if kind=="stderr":
            sys.stderr.write(line); sys.stderr.flush(); continue
        sys.stdout.write(line); sys.stdout.flush()
        if not line.startswith(PREFIX): continue
        try:
            ev=json.loads(line[len(PREFIX):])
        except Exception:
            continue
        if ev.get("event")!="PHASE": continue
        pb=ev.get("production_boundary","UNKNOWN")
        if boundary!="OBSERVED":
            boundary=pb
        state=ev.get("state"); phase=ev.get("phase")
        if state in ("START","PROGRESS"):
            current_phase=phase
            budget=float(budgets.get(phase,budgets.get("default",300)))
            deadline=time.monotonic()+budget
        elif state in ("PASS","HOLD") and phase==current_phase:
            deadline=time.monotonic()+float(budgets.get("between_phases",60))
    return 0

if __name__=="__main__":
    sys.exit(main())
