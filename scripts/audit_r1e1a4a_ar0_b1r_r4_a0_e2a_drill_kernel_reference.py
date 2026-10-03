from __future__ import print_function
import argparse, hashlib, json, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci

PARENT_SHA="fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e"
HOLD_SHA="573e21e893a5b8fa9a76ae3c8d5dce641c672607c2747aa1ca39f9879b63c7fc"
HISTORY_LABEL="E2A drill kernel reference V01"
PRONGS=("B0_Stalk:A_P_PRONG","B0_Stalk:A_N_PRONG")

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,line in enumerate(lines):
        if line.strip()=="Sub Main()": s=i
        elif line.strip()=="End Sub": e=i
    if s is None or e is None or e<=s: raise RuntimeError("HOLD_REF_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    sd=src.with_suffix(""); dd=dst.with_suffix("")
    if not sd.exists(): raise RuntimeError("HOLD_REF_PARENT_COMPANION_MISSING")
    if dd.exists(): shutil.rmtree(str(dd),ignore_errors=True)
    shutil.copytree(str(sd),str(dd))

def volume_vba(path):
    p=str(path).replace("\\","/")
    lines=["On Error Resume Next","Dim f As Integer","f=FreeFile",'Open "'+p+'" For Output As #f']
    for n in PRONGS:
        lines.append('Print #f, "'+n+'=" & CStr(Solid.GetVolume("'+n+'"))')
    lines+=["Close #f","On Error GoTo 0"]
    return "\n".join(lines)

def read_vol(path):
    out={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k,v=line.rsplit("=",1); out[k]=float(v)
    return out

def audit_volumes(cst,outtxt):
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(cst))
        ok=bool(p.schematic.execute_vba_code(wrap(volume_vba(outtxt))))
    finally:
        if p is not None: p.close()
        de.close()
    if not ok: raise RuntimeError("HOLD_REF_VOLUME_QUERY")
    return read_vol(outtxt)

def main(parent,hold,macro,outdir):
    parent=Path(parent); hold=Path(hold); macro=Path(macro); outdir=Path(outdir)
    if outdir.exists(): raise RuntimeError("HOLD_REF_OUTDIR_EXISTS")
    if sha(parent)!=PARENT_SHA: raise RuntimeError("HOLD_REF_PARENT_SHA")
    if sha(hold)!=HOLD_SHA: raise RuntimeError("HOLD_REF_HOLD_SHA")
    outdir.mkdir(parents=True)
    ref=outdir/"kernel_reference.cst"
    copy_project(parent,ref)

    pv=audit_volumes(ref,outdir/"parent_prong_volumes.txt")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(ref))
        p.modeler.add_to_history(HISTORY_LABEL,macro_body(macro))
        p.save()
    finally:
        if p is not None: p.close()
        de.close()

    rv=audit_volumes(ref,outdir/"reference_prong_volumes.txt")
    hv=audit_volumes(hold,outdir/"hold_prong_volumes.txt")

    ref_loss={n:pv[n]-rv[n] for n in PRONGS}
    hold_loss={n:pv[n]-hv[n] for n in PRONGS}
    delta={n:hold_loss[n]-ref_loss[n] for n in PRONGS}
    checks={
      "reference_branch_losses_symmetric":abs(ref_loss[PRONGS[0]]-ref_loss[PRONGS[1]])<=1e-9,
      "hold_branch_losses_symmetric":abs(hold_loss[PRONGS[0]]-hold_loss[PRONGS[1]])<=1e-9,
      "hold_matches_kernel_reference_P":abs(delta[PRONGS[0]])<=1e-7,
      "hold_matches_kernel_reference_N":abs(delta[PRONGS[1]])<=1e-7,
      "canonical_hold_hash_stable":sha(hold)==HOLD_SHA,
      "canonical_parent_hash_stable":sha(parent)==PARENT_SHA
    }
    status="PASS_R4_A0_E2A_DRILL_KERNEL_REFERENCE" if all(checks.values()) else "HOLD_R4_A0_E2A_DRILL_KERNEL_REFERENCE"
    result={
      "status":status,
      "formal_build_invocations":0,
      "solver_invocations":0,
      "classification":"TOOLING_RECOVERY_DIAGNOSTIC_ON_DISPOSABLE_COMPLETE_PROJECT_COPY",
      "parent_sha256":PARENT_SHA,
      "hold_artifact_sha256":HOLD_SHA,
      "reference_macro":str(macro),
      "parent_prong_volumes_mm3":pv,
      "kernel_reference_prong_volumes_mm3":rv,
      "hold_prong_volumes_mm3":hv,
      "kernel_reference_loss_mm3":ref_loss,
      "hold_loss_mm3":hold_loss,
      "hold_minus_reference_mm3":delta,
      "comparison_tolerance_mm3":1e-7,
      "checks":checks,
      "interpretation":"Compares production HOLD drill loss against CST/ACIS-native loss generated from the same canonical parent and exact drill primitives. It does not alter or reclassify the formal HOLD."
    }
    (outdir/"summary.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    (outdir/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--parent",required=True)
    ap.add_argument("--hold",required=True)
    ap.add_argument("--macro",required=True)
    ap.add_argument("--outdir",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.parent,a.hold,a.macro,a.outdir))
    except Exception:
        Path(a.outdir).mkdir(parents=True,exist_ok=True)
        Path(a.outdir,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
