from __future__ import print_function
import argparse, hashlib, json, shutil, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci

EXPECTED_SHA="e242416cd3037cb23f57513f60c6de29c97ba277ad754da1574954240eb4bd73"

PAIRS=[]
for pol in ("A","B"):
    own="B1M_LowerStalk:%s_LOWER_BODY"%pol
    opp="B1M_LowerStalk:%s_LOWER_BODY"%("B" if pol=="A" else "A")
    for side in ("P","N"):
        g="D2M0_BackGround:%s_%s_LOWER_RAIL"%(pol,side)
        PAIRS.append(("own_fr4",pol+"_"+side,g,own))
        PAIRS.append(("opposite_stalk",pol+"_"+side,g,opp))
    g="D2M0_BackGround:%s_COMMON_BRIDGE"%pol
    PAIRS.append(("own_fr4",pol+"_BRIDGE",g,own))
    PAIRS.append(("opposite_stalk",pol+"_BRIDGE",g,opp))

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def one_pair(source,tmp,out,ground,target):
    shutil.copy2(str(source),str(tmp))
    body="\n".join([
      "Dim f As Integer, v As Double",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(out).replace("\\","/"),
      "On Error Resume Next",
      "Err.Clear",
      'Print #f, "GROUND_BEFORE=" & CStr(Solid.GetVolume("%s"))'%ground,
      'Print #f, "TARGET_BEFORE=" & CStr(Solid.GetVolume("%s"))'%target,
      "Err.Clear",
      'Solid.Intersect "%s", "%s"'%(ground,target),
      'Print #f, "INTERSECT_ERR=" & CStr(Err.Number)',
      "Err.Clear",
      'v=Solid.GetVolume("%s")'%ground,
      "If Err.Number <> 0 Then",
      ' Print #f, "GROUND_EXISTS_AFTER=0"',
      ' Print #f, "INTERSECTION_VOLUME=0"',
      " Err.Clear",
      "Else",
      ' Print #f, "GROUND_EXISTS_AFTER=1"',
      ' Print #f, "INTERSECTION_VOLUME=" & CStr(v)',
      "End If",
      "On Error GoTo 0",
      "Close #f"
    ])
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(tmp))
        p.schematic.execute_vba_code(wrap(body))
    finally:
        if p is not None: p.close()
        de.close()

def parse(path):
    kv={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k,v=line.split("=",1); kv[k]=v
    return kv

def cleanup(tmp):
    try: tmp.unlink()
    except Exception: pass
    d=tmp.with_suffix("")
    if d.exists(): shutil.rmtree(str(d),ignore_errors=True)

def main(source,work,evidence):
    source=Path(source); work=Path(work); evidence=Path(evidence)
    if not source.exists() or sha(source)!=EXPECTED_SHA:
        raise RuntimeError("HOLD_D2M0_PAIRWISE_SOURCE_HASH")
    if work.exists(): shutil.rmtree(str(work),ignore_errors=True)
    work.mkdir(parents=True)
    evidence.mkdir(parents=True,exist_ok=True)
    results=[]
    for mode,tag,g,t in PAIRS:
        tmp=work/("%s_%s.cst"%(mode,tag))
        out=evidence/("pairwise_%s_%s.txt"%(mode,tag))
        if out.exists(): out.unlink()
        try:
            one_pair(source,tmp,out,g,t)
            kv=parse(out)
            err=int(kv.get("INTERSECT_ERR","999999"))
            vol=float(kv.get("INTERSECTION_VOLUME","nan"))
            passed=(err==0 and abs(vol)<=1e-12)
            results.append({"mode":mode,"tag":tag,"ground":g,"target":t,
                            "intersect_err":err,"intersection_volume_mm3":vol,"pass_zero_overlap":passed})
        except Exception as ex:
            results.append({"mode":mode,"tag":tag,"ground":g,"target":t,
                            "error":str(ex),"pass_zero_overlap":False})
        finally:
            cleanup(tmp)
    allpass=all(r["pass_zero_overlap"] for r in results)
    summary={
      "status":"PASS_R1E1A4A_AR0_B1R_R3_D2_M0_PAIRWISE_OVERLAP_RECOVERY" if allpass else "HOLD_R1E1A4A_AR0_B1R_R3_D2_M0_PAIRWISE_OVERLAP",
      "recovery_type":"READ_ONLY_PAIRWISE_DESTRUCTIVE_BOOLEAN_ON_TEMPORARY_COPIES",
      "formal_rebuild":False,
      "solver_invocations":0,
      "canonical_sha256":EXPECTED_SHA,
      "pair_count":len(results),
      "all_zero_overlap":allpass,
      "results":results
    }
    (evidence/"pairwise_overlap_recovery.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(summary["status"])
    print(json.dumps(summary,indent=2))
    return 0 if allpass else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-cst",required=True); ap.add_argument("--work",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.source_cst,a.work,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"pairwise_overlap_recovery_EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
