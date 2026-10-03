from __future__ import print_function
import ast, hashlib, json, re, sys
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1D2_PREBUILD_V01"/"STATIC_AUDIT.json"
RUNNER=ROOT/"scripts"/"run_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_m6_attribution_build_only_v01.py"
PKT=ROOT/"scripts"/"make_r1e1a4a_ar0_b1r_r4_a0_e2c_s0_m6_build_packet_v01.py"
PARENT_SHA="78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804"

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def solver_calls(path):
    tree=ast.parse(Path(path).read_text(encoding="utf-8"))
    n=0
    for x in ast.walk(tree):
        if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=="run_solver": n+=1
    return n

def names_in_macro(txt):
    blocks=[]; comp=name=None
    for line in txt.splitlines():
        m=re.match(r'\s*\.Component\s+"([^"]+)"',line)
        if m: comp=m.group(1)
        m=re.match(r'\s*\.Name\s+"([^"]+)"',line)
        if m: name=m.group(1)
        if ".Create" in line and comp and name:
            blocks.append(comp+":"+name); comp=name=None
    return blocks

checks={}
details={}
for key,base,count,drills,subs in (
 ("D1","R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_SIG",6,0,0),
 ("D2","R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_GND",34,8,8)):
    mp=ROOT/"source"/"cst"/(base+"_BUILD_ONLY_V01.mcr")
    jp=ROOT/"execution"/(base+"_BUILD_MANIFEST_V01.json")
    m=json.loads(jp.read_text(encoding="utf-8")); txt=mp.read_text(encoding="utf-8")
    created=names_in_macro(txt)
    final=set(m["geometry"]["added_final_entities"]); tools=set(m["geometry"]["drill_tool_entities"])
    checks[key+"_parent_hash_declared"]=m["parent"]["sha256"]==PARENT_SHA
    checks[key+"_added_count"]=len(final)==count
    checks[key+"_expected_shape_count"]=m["geometry"]["expected_final_shape_count"]==107+count
    checks[key+"_created_final_exact"]=set(created)==(final|tools)
    checks[key+"_tool_count"]=len(tools)==drills
    checks[key+"_created_tools_exact"]=tools.issubset(set(created))
    checks[key+"_subtract_count"]=txt.count("Solid.Subtract")==subs
    checks[key+"_no_port_mutation"]=all(x not in txt for x in ("DiscretePort","Port.","Solver.","ChangeSolverType","Monitor."))
    checks[key+"_no_solver_tokens"]=all(x not in txt for x in ("run_solver","StartSolver","Solver.Start"))
    checks[key+"_auth_false"]=m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
    checks[key+"_future_monitors_frozen"]=m["future_solve_contract"]["surface_current_monitors_ghz"]==[1.2276,1.3384,1.57542]
    details[key]={"macro_sha256":sha(mp),"manifest_sha256":sha(jp),"created_count":len(created),"created":created}

d2txt=(ROOT/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_GND_BUILD_ONLY_V01.mcr").read_text(encoding="utf-8")
checks["D2_subtract_targets_only_B_prongs"]=all(
    ("B0_Stalk:B_P_PRONG" in line or "B0_Stalk:B_N_PRONG" in line)
    for line in d2txt.splitlines() if "Solid.Subtract" in line)
checks["D2_no_solid_delete"]="Solid.Delete" not in d2txt
checks["runner_ast_zero_run_solver"]=solver_calls(RUNNER)==0
checks["packet_generator_ast_zero_run_solver"]=solver_calls(PKT)==0
checks["runner_has_fresh_reopen"]="post_inventory.txt" in RUNNER.read_text(encoding="utf-8")
checks["runner_checks_port_invariance"]="ports_byte_semantics_unchanged" in RUNNER.read_text(encoding="utf-8")
checks["runner_no_pairwise_explosion"]="Solid.Intersect" not in RUNNER.read_text(encoding="utf-8")
checks["packet_schema_v02"]='"schema_version":"runner-task-v0.2"' in PKT.read_text(encoding="utf-8")
status="PASS_M6_D1D2_PREBUILD_STATIC_CONTRACT" if all(checks.values()) else "HOLD_M6_D1D2_PREBUILD_STATIC_CONTRACT"
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({"status":status,"checks":checks,"details":details,
                           "formal_build_invocations":0,"solver_invocations":0,
                           "BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},indent=2)+"\n",encoding="utf-8")
print(status)
for k,v in checks.items():
    if not v: print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
