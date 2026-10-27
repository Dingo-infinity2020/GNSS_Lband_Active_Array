from __future__ import print_function
import json, sys
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
from cst.results import ProjectFile

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
ART={
"D1":Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\M6_D1_DIAGNOSTIC_SOLVE_V01\R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_DIAGNOSTIC_SOLVED_V01.cst"),
"D2":Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\M6_D2_DIAGNOSTIC_SOLVE_V01\R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_DIAGNOSTIC_SOLVED_V01.cst"),
}
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_FIELD_RESULT_DISCOVERY_V01"
OUT.mkdir(parents=True,exist_ok=True)
res={}
needles=("field","current","1.2276","1.3384","1.57542","m6_","monitor","2d/3d","3d results","h-field","hfield")
for key,p in ART.items():
    p3=ProjectFile(str(p),allow_interactive=True).get_3d()
    items=list(p3.get_tree_items())
    matches=[x for x in items if any(n in x.lower() for n in needles)]
    top={}
    for x in items:
        root=x.split("\\",1)[0]
        top[root]=top.get(root,0)+1
    runinfo={}
    for x in matches:
        try:
            runinfo[x]=list(p3.get_run_ids(x,False))
        except Exception as ex:
            runinfo[x]={"error":repr(ex)}
    res[key]={"tree_item_count":len(items),"top_level_counts":top,"matches":matches,"run_ids":runinfo}
    (OUT/(key+"_TREE_ALL.txt")).write_text("\n".join(items)+"\n",encoding="utf-8")
    (OUT/(key+"_TREE_MATCHES.txt")).write_text("\n".join(matches)+"\n",encoding="utf-8")
status="PASS_M6_FIELD_RESULT_PATHS_DISCOVERED" if all(res[k]["matches"] for k in res) else "HOLD_M6_FIELD_RESULT_PATHS_NOT_DISCOVERED"
summary={"schema_version":"gnss-m6-field-result-discovery-v0.1","status":status,"results":res,
         "solver_invocations":0,"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
