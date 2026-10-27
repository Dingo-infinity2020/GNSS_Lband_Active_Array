from __future__ import print_function
import os, subprocess, sys

def main():
    exe=os.environ.get("CST_PYTHON_EXECUTABLE","").strip()
    if not exe or not os.path.isabs(exe) or not os.path.exists(exe):
        raise SystemExit("HOLD_CST_BUNDLED_RUNTIME_INVALID")
    child=sys.argv[1:]
    if not child:
        raise SystemExit("HOLD_CST_BUNDLED_RUNTIME_NO_CHILD")
    return subprocess.call([exe]+child, shell=False)

if __name__=="__main__":
    sys.exit(main())
