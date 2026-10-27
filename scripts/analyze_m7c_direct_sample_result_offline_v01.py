"""Compare already-extracted direct points to frozen broadband output, offline."""
import argparse
import cmath
import csv
import hashlib
import json
import math
from pathlib import Path
from evaluate_m7c_modal_restoration_readonly_v01 import read96,db
from m7c_direct_sample_contract_v01 import FREQUENCIES,exact_index,classify


def main(direct_csv,old_csv,qualification,output,plots):
    output.mkdir(parents=True,exist_ok=False)
    f,d=read96(direct_csv)
    old_f,old=read96(old_csv)
    q=json.loads(qualification.read_text(encoding="utf-8-sig"))
    result=classify(f,d,old_f,old,all(q["hard_checks"].values()))
    if result!=q["diagnostic"]:
        raise RuntimeError("HOLD_DIAGNOSTIC_REPLAY_MISMATCH")
    rows=[]
    pairs=((2,5),(5,2),(6,2),(4,2),(2,4),(8,11),(11,8))
    for x in FREQUENCIES:
        k,oldk=exact_index(f,x),exact_index(old_f,x)
        for ij in pairs:
            new,z=d[ij][k],old[ij][oldk]
            rows.append({"f_ghz":x,"response_port":ij[0],"source_port":ij[1],
                         "direct_real":new.real,"direct_imag":new.imag,"direct_db":db(new),
                         "old_real":z.real,"old_imag":z.imag,"old_db":db(z),
                         "abs_complex_change":abs(new-z)})
    with (output/"DIRECT_VS_BROADBAND.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    k,oldk=exact_index(f,1.2096),exact_index(old_f,1.2096)
    primary={"S%d_%d"%ij:{"direct_db":db(d[ij][k]),"old_db":db(old[ij][oldk]),
                                      "abs_complex_change":abs(d[ij][k]-old[ij][oldk])} for ij in ((2,5),(5,2))}
    result.update(at_1p2096_ghz=primary,input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (direct_csv,old_csv,qualification)})
    (output/"OFFLINE_REPLAY.json").write_text(json.dumps(result,indent=2)+"\n")
    if plots:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        matplotlib.rcParams.update({"svg.fonttype":"none","svg.hashsalt":"m7c-direct-v01"})
        fig,axes=plt.subplots(2,2,figsize=(11,7),constrained_layout=True)
        for a,ij in zip(axes.flat,((2,5),(5,2),(4,2),(2,4))):
            ids=[k for k,x in enumerate(old_f) if 1.15<=x<=1.26]
            a.plot([old_f[k] for k in ids],[db(old[ij][k]) for k in ids],label="Old broadband representation")
            a.scatter(f,[db(z) for z in d[ij]],color="#d44c2f",s=22,label="New directly solved points",zorder=3)
            a.set(title="S%d,%d"%ij,xlabel="Frequency (GHz)",ylabel="20 log10 |S| (dB)")
            a.grid(alpha=.25);a.legend(fontsize=8)
        fig.suptitle("M7C same-geometry direct-sample diagnostic; old scientific HOLD retained")
        fig.savefig(output/"DIRECT_VS_BROADBAND.svg",metadata={"Date":None})
        fig.savefig(output/"DIRECT_VS_BROADBAND.png",dpi=140)
        plt.close(fig)
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for n in ("direct-csv","old-csv","qualification","output"):p.add_argument("--"+n,type=Path,required=True)
    p.add_argument("--plots",action="store_true");a=p.parse_args()
    main(a.direct_csv,a.old_csv,a.qualification,a.output,a.plots)
