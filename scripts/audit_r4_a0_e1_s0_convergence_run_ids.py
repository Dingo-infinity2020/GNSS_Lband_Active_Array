from __future__ import print_function
import argparse, json, sys
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
from cst.results import ProjectFile

def seq(item):
    return [{"x":float(r[0]),"value_real":float(complex(r[1]).real),"value_imag":float(complex(r[1]).imag)}
            for r in item.get_data()]

def main(cst,out):
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
    conv=r"1D Results\Convergence\S-Parameters\All S-Parameters"
    s11=r"1D Results\S-Parameters\S1,1"
    result={"convergence_path":conv,"s11_path":s11,"runs":{}}
    cids=list(p3.get_run_ids(conv,False))
    sids=list(p3.get_run_ids(s11,False))
    result["convergence_run_ids"]=cids
    result["s11_run_ids"]=sids
    for rid in sorted(set(cids+sids)):
        d={}
        if rid in cids:
            d["convergence"]=seq(p3.get_result_item(conv,rid))
        if rid in sids:
            vals=p3.get_result_item(s11,rid).get_data()
            d["s11_count"]=len(vals)
            if vals:
                d["s11_f_min"]=float(vals[0][0]); d["s11_f_max"]=float(vals[-1][0])
        result["runs"][str(rid)]=d
    Path(out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--cst",required=True); ap.add_argument("--out",required=True)
    a=ap.parse_args(); main(a.cst,a.out)
