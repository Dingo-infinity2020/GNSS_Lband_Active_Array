from __future__ import print_function
import argparse, json, os, subprocess, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bridge-evidence", required=True)
    ap.add_argument("child_argv", nargs=argparse.REMAINDER)
    a=ap.parse_args()

    child=list(a.child_argv)
    if child and child[0]=="--":
        child=child[1:]
    if not child:
        raise SystemExit("HOLD_CST_BRIDGE_NO_CHILD_ARGV")

    exe=os.environ.get("CST_PYTHON_EXECUTABLE","").strip()
    if not exe:
        raise SystemExit("HOLD_CST_BRIDGE_ENV_MISSING:CST_PYTHON_EXECUTABLE")
    p=Path(exe)
    if not p.is_absolute() or not p.exists():
        raise SystemExit("HOLD_CST_BRIDGE_EXECUTABLE_INVALID:"+exe)

    evidence=Path(a.bridge_evidence)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    payload={
      "schema_version":"gnss-cst-python-bridge-v0.1",
      "launcher_python":sys.executable,
      "cst_python_executable":str(p),
      "child_argv":child,
      "shell":False
    }
    evidence.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print("CST_BRIDGE_EXECUTABLE="+str(p))
    print("CST_BRIDGE_CHILD_ARGV="+json.dumps(child))
    proc=subprocess.run([str(p)]+child, shell=False)
    return int(proc.returncode)

if __name__=="__main__":
    sys.exit(main())
