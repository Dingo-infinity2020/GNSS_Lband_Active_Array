#!/usr/bin/env python3
"""Generate R1E0C-A scan-state build-only macros."""
from __future__ import print_function
import argparse
from pathlib import Path

STATES=[
  ("C30P45",30.0,45.0),
  ("C45P45",45.0,45.0),
  ("C60P45",60.0,45.0),
  ("C60P135",60.0,135.0),
]

def macro(state,theta,phi):
    return """Option Explicit

' R1E0C-A {state} scan-state BUILD-ONLY.
' Only scan metadata changes. No boundary-type, geometry, material, port, or solver changes.

Sub Main()

    StoreParameter "R1E0_scan_theta_deg", {theta}
    StoreParameter "R1E0_scan_phi_deg", {phi}

    With Boundary
        .SetPeriodicBoundaryAngles "R1E0_scan_theta_deg", "R1E0_scan_phi_deg"
        .SetPeriodicBoundaryAnglesDirection "outward"
    End With

End Sub
""".format(state=state,theta=theta,phi=phi)

def expected():
    return {s:macro(s,t,p) for s,t,p in STATES}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",default="source/cst")
    ap.add_argument("--check",action="store_true")
    a=ap.parse_args()
    out=Path(a.outdir)
    exp=expected()
    names={s:"R1E0C_%s_SCANSTATE_BUILD_ONLY_V01.mcr"%s for s,_,_ in STATES}
    if a.check:
        ok=True
        for s,name in names.items():
            p=out/name
            if not p.exists() or p.read_text(encoding="utf-8").replace("\r\n","\n") != exp[s].replace("\r\n","\n"):
                print("MISMATCH="+str(p)); ok=False
        if not ok: raise SystemExit(3)
        print("PASS_R1E0C_SCAN_MACROS_MATCH_GENERATOR")
        return
    out.mkdir(parents=True,exist_ok=True)
    for s,name in names.items():
        (out/name).write_text(exp[s],encoding="utf-8")
        print("WROTE="+str(out/name))

if __name__=="__main__":
    main()
