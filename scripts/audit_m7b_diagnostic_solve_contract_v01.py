from __future__ import print_function
import ast,hashlib,json,sys
from pathlib import Path
ROOT=Path(r"D:\GNSS_R4A0E1_20260928");MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_DIAGNOSTIC_SOLVE_MANIFEST_V01.json";GATE=ROOT/"execution"/"M7B_HUMAN_GEOMETRY_REVIEW_PASS.json";RUN=ROOT/"scripts"/"run_m7b_diagnostic_solve_v01.py";EVAL=ROOT/"scripts"/"evaluate_m7b_corrective_readonly_v01.py";PKT=ROOT/"scripts"/"make_m7b_diagnostic_solve_packet_v01.py";OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_DIAGNOSTIC_SOLVE_PREP_V01"/"STATIC_AUDIT.json"
def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def rcalls(p):
 t=ast.parse(p.read_text(encoding="utf-8"));c=[]
 for x in ast.walk(t):
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=="run_solver":c.append(x)
 return t,c
m=json.loads(MAN.read_text(encoding="utf-8"));g=json.loads(GATE.read_text(encoding="utf-8-sig"));t,c=rcalls(RUN);inloop=any(isinstance(n,(ast.For,ast.While)) and any(z is c[0] for z in ast.walk(n)) for n in ast.walk(t)) if c else False
checks={"stage":m["stage"]=="R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_DIAGNOSTIC_SOLVE","source_sha":m["canonical_build"]["sha256"]=="5498e9c447fdd4eeb969c02701d27886e839144ebe9941c4e7f56bc7419c69ea","source_exists":Path(m["canonical_build"]["path"]).exists(),"human_gate":g["status"]=="PASS_M7B_HUMAN_GEOMETRY_REVIEW" and g["artifact_sha256"]==m["canonical_build"]["sha256"],"auth_false":m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},"twelve_port_sources":m["solve_network"]["source_ports"]==[1,2,4,5,7,8,10,11],"loads":m["solve_network"]["load_only_ports"]==[3,6,9,12],"solver_fidelity":m["solve_network"]["max_delta_s"]==0.02 and m["solve_network"]["consecutive_passes_required"]==2 and m["solve_network"]["max_passes"]==16,"raw_gate":m["corrective_gate"]["primary"]["raw"]["anchor_ghz"]==1.3432 and m["corrective_gate"]["primary"]["raw"]["minimum_reduction_fraction"]==0.30,"mode_gate":m["corrective_gate"]["primary"]["mode"]["search_band_ghz"]==[1.2,1.4] and m["corrective_gate"]["primary"]["mode"]["minimum_reduction_db"]==6.0,"imbalance_gate":m["corrective_gate"]["secondary"]["anchor_ghz"]==1.2984 and m["corrective_gate"]["secondary"]["minimum_reduction_fraction"]==0.30,"falsification_frozen":m["corrective_gate"]["falsification"]["maximum_primary_fraction_for_reject"]==0.10,"guard_frozen":m["corrective_gate"]["guard"]["max_new_excursion_db"]==6.0 and m["corrective_gate"]["guard"]["window_mhz"]==50.0,"runner_one_solver":len(c)==1 and not inloop,"evaluator_zero_solver":len(rcalls(EVAL)[1])==0,"packet_zero_solver":len(rcalls(PKT)[1])==0,"packet_v02":'"schema_version":"runner-task-v0.2"' in PKT.read_text(encoding="utf-8"),"packet_solve_launch":'"kind":"SOLVE_LAUNCH"' in PKT.read_text(encoding="utf-8"),"packet_failclosed":"HOLD_M7B_LIVE_SOLVE_GRANT" in PKT.read_text(encoding="utf-8"),"config_no_monitor":"Monitor" not in (ROOT/m["execution"]["config_macro"]).read_text(encoding="utf-8")}
status="PASS_M7B_DIAGNOSTIC_SOLVE_STATIC_CONTRACT" if all(checks.values()) else "HOLD_M7B_DIAGNOSTIC_SOLVE_STATIC_CONTRACT";OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps({"status":status,"checks":checks,"runner_sha256":sha(RUN),"evaluator_sha256":sha(EVAL),"packet_sha256":sha(PKT),"manifest_sha256":sha(MAN),"formal_solver_invocations":0},indent=2)+"\n",encoding="utf-8");print(status)
for k,v in checks.items():
 if not v:print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
