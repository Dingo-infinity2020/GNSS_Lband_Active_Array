"""CPU-only log-semantics recovery; consumes immutable V01 extraction snapshots."""
import argparse
import base64
import hashlib
import json
import re
import shutil
from pathlib import Path
from m7c_direct_sample_contract_v01 import FREQUENCIES,SOURCES,classify
from evaluate_m7c_modal_restoration_readonly_v01 import read96

LOCKED_SOLVED_SHA="c21fa9f047d83f4f3776d5e6ef5718e8924aaf8e54f0ad8cbb7cb6a7c6681851"
LOCKED_OLD_CSV_SHA="711365d2f3336a5afed0cf94e2394f0ae75e0691421c8729af6dda2425a74cae"


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def direct_log_samples(text):
    pattern=r"Sample\s+(\d+)\s+of\s+(\d+)\s*\(([\d.eE+-]+) GHz\)"
    matches=list(re.finditer(pattern,text,re.I))
    rows=[]
    for n,m in enumerate(matches):
        block=text[m.end():matches[n+1].start() if n+1<len(matches) else len(text)]
        rows.append({"ordinal":int(m.group(1)),"total":int(m.group(2)),"frequency_ghz":float(m.group(3)),
                     "source_ports":[int(x) for x in re.findall(r"Excitation:\s*port\s+(\d+)",block,re.I)]})
    return rows


def main(source,old_csv,output):
    output.mkdir(parents=True,exist_ok=False)
    q=json.loads((source/"qualification_summary.json").read_text(encoding="utf-8-sig"))
    failed=[k for k,v in q["hard_checks"].items() if not v]
    if failed!=["native_logs_confirm_direct_frequencies"]:
        raise RuntimeError("HOLD_RECOVERY_NOT_ONLY_LOG_FORMAT:"+repr(failed))
    assert q["solved_sha256_before"]==q["solved_sha256_after"]==LOCKED_SOLVED_SHA
    assert sha(old_csv)==LOCKED_OLD_CSV_SHA
    raw=base64.b64decode((source/"native_output.txt.base64.txt").read_text())
    text=raw.decode("utf-8",errors="replace")
    # The rendered Windows text copy can contain translated CR/CRLF sequences.
    # Use exact base64-preserved solver bytes as the frequency evidence authority.
    blocks=direct_log_samples(text)
    for target in FREQUENCIES:
        matches=[row for row in blocks if abs(row["frequency_ghz"]-target)<=1e-9]
        if len(matches)!=1 or matches[0]["total"]!=16 or tuple(matches[0]["source_ports"])!=SOURCES:
            raise RuntimeError("HOLD_NATIVE_DIRECT_SOURCE_LOOP:"+str(target))
    direct_csv=source/"direct_response_native.csv"
    f,d=read96(direct_csv);old_f,old=read96(old_csv)
    q["hard_checks"]["native_logs_confirm_direct_frequencies"]=True
    q["hard_checks"]["native_each_diagnostic_frequency_has_all_8_excitations"]=True
    result=classify(f,d,old_f,old,all(q["hard_checks"].values()))
    q.update(status=result["status"],diagnostic=result,native_frequencies_ghz=sorted({r["frequency_ghz"] for r in blocks}|{1.8}),
             native_direct_sample_blocks=blocks,
             recovery_of="V01 log-format HOLD: direct solver writes Sample N of 16; old broadband parser expected Sample N",
             recovery_source_sha256=sha(__file__),new_build=False,new_solve=False,solver_launches=0,
             native_log_authority="exact base64-preserved solver bytes; rendered text is not byte authority",
             recovery_input_sha256={str(p):sha(p) for p in (source/"qualification_summary.json",source/"native_output.txt.base64.txt",direct_csv,old_csv)})
    for name,obj in (("qualification_summary.json",q),("diagnostic_evaluation.json",result)):
        (output/name).write_text(json.dumps(obj,indent=2)+"\n")
    shutil.copyfile(direct_csv,output/"direct_response_native.csv")
    (output/"FINAL_STATUS.txt").write_text(result["status"]+"\n")
    print(json.dumps({"status":result["status"],"hard_checks":q["hard_checks"],"diagnostic":result},indent=2))


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,required=True);p.add_argument("--old-csv",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();main(a.source,a.old_csv,a.output)
