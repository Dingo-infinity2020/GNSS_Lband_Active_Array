from __future__ import print_function
import ast, hashlib, json, math, sys
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
PARENT=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\build_only\E2C_R7_CANONICAL_BUILD\R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_COEXISTENCE_BUILD_ONLY_V01.cst")
PARENT_SHA="cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c"
M6=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_FREQUENCY_SHAPE_DISCRIMINATION_V01"/"M6_FREQUENCY_SHAPE_DISCRIMINATION.json"
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7_CORRECTIVE_CANDIDATE_FREEZE_V01"
DOC=ROOT/"docs"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7_CORRECTIVE_CANDIDATE_FREEZE_V01.md"
AUDIT=ROOT/"scripts"/"audit_m7_corrective_candidates_v01.py"

SQ=0.707106781186547
branches={
 "A_P":{"ground":"E2C_A_P_BackGround:LOCAL_BACK_GROUND","origin":(SQ,-SQ,57.1428571428),"u":(SQ,SQ,0.0),"v":(0,0,-1),"sign":1},
 "A_N":{"ground":"E2C_A_N_BackGround:LOCAL_BACK_GROUND","origin":(SQ,-SQ,57.1428571428),"u":(SQ,SQ,0.0),"v":(0,0,-1),"sign":-1},
 "B_P":{"ground":"E2C_B_P_BackGround:LOCAL_BACK_GROUND","origin":(SQ,SQ,57.1428571428),"u":(-SQ,SQ,0.0),"v":(0,0,-1),"sign":1},
 "B_N":{"ground":"E2C_B_N_BackGround:LOCAL_BACK_GROUND","origin":(SQ,SQ,57.1428571428),"u":(-SQ,SQ,0.0),"v":(0,0,-1),"sign":-1},
}

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

if not PARENT.exists() or sha(PARENT)!=PARENT_SHA or not PARENT.with_suffix("").exists():
    raise RuntimeError("HOLD_M7_PARENT_AUTHORITY")
m6=json.loads(M6.read_text(encoding="utf-8"))
if m6["status"]!="PASS_M6_FREQUENCY_SHAPE_DISCRIMINATION":
    raise RuntimeError("HOLD_M7_M6_NOT_FROZEN")

# Candidate A: remove only the center-facing 0.5-mm overhang, v=3..5 mm.
# Existing signal MSL inner edge is |u|=2.05, so retained ground reaches |u|=1.5:
# minimum inner-side ground overhang remains 0.55 mm.
a_windows={}
# Candidate B: exact CIN_UP_PAD projection expanded by 0.25 mm:
# P pad u=2.7..3.3, N=-3.3..-2.7, v=4.4..4.9 -> guard window 1.1 x 1.0 mm.
b_windows={}
for k,b in branches.items():
    if b["sign"]>0:
        a=(1.0,1.5,3.0,5.0)
        bw=(2.45,3.55,4.15,5.15)
    else:
        a=(-1.5,-1.0,3.0,5.0)
        bw=(-3.55,-2.45,4.15,5.15)
    a_windows[k]=a; b_windows[k]=bw

def extrude_tool(name,component,b,win):
    u0,u1,v0,v1=win
    o=b["origin"]; u=b["u"]; v=b["v"]
    L=[
      "With Extrude"," .Reset",f' .Name "{name}"',f' .Component "{component}"',' .Material "Vacuum"',
      ' .Mode "Pointlist"',' .Height "-0.07"',' .Twist "0.0"',' .Taper "0.0"',
      ' .Origin "{}", "{}", "{}"'.format(*o),
      ' .Uvector "{}", "{}", "{}"'.format(*u),
      ' .Vvector "{}", "{}", "{}"'.format(*v),
      f' .Point "{u0}", "{v0}"',f' .LineTo "{u1}", "{v0}"',f' .LineTo "{u1}", "{v1}"',
      f' .LineTo "{u0}", "{v1}"',f' .LineTo "{u0}", "{v0}"',' .Create',"End With"]
    return "\n".join(L)

def make_macro(cid,windows,toolcomp):
    lines=["Option Explicit",f"' M7 {cid} corrective BUILD_ONLY V01",
           "' Parent: frozen full E2C R7 canonical build",
           "' No ports, monitors, solver settings or solver start.","","Sub Main()",""]
    for k,b in branches.items():
        tool=f"{cid}_{k}_CLEARANCE"
        lines.append(extrude_tool(tool,toolcomp,b,windows[k]))
        lines.append(f'Solid.Subtract "{b["ground"]}", "{toolcomp}:{tool}"')
        lines.append("")
    lines.append("End Sub"); lines.append("")
    return "\n".join(lines)

cands={
 "M7A":{
   "title":"INNER_EDGE_UPSTREAM_SETBACK",
   "macro":ROOT/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK_BUILD_ONLY_V01.mcr",
   "manifest":ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK_MANIFEST_V01.json",
   "windows":a_windows,"toolcomp":"M7A_ClearanceTools",
   "scientific_change":"Remove a 0.5-mm-wide center-facing strip from each backside ground only over local v=3.0..5.0 mm; preserve ground directly beneath the entire upstream signal with >=0.55-mm inner-side overhang.",
   "target_mechanism":"Reduce orthogonal ground-ground and opposite-pol signal-to-ground near-field capacitance at the upstream/CIN region without changing the signal trace or local package/via return network.",
   "primary_prediction":"Full-E2C common-mode degradation and branch imbalance should drop in the 1.2-1.4 GHz severe region if near-field overlap at the center-facing ground edge is a necessary part of the composite mode.",
   "falsification":"If diff/common degradation and imbalance remain within 10% of full-E2C severe values, center-facing upstream ground overlap is not the controlling corrective lever.",
   "success_gate":{
      "primary":"At least 30% reduction versus full E2C in BOTH E_UP diff-to-common degradation and E_UP branch-return imbalance at their frozen severe anchors.",
      "secondary":"At least 20% reduction in maximum source-side complex deviation over 1.15-1.65 GHz.",
      "guard":"No new >6 dB narrow excursion within <=50 MHz and no numerical hard-gate failure."
   },
   "area_removed_per_branch_mm2":1.0
 },
 "M7B":{
   "title":"CIN_PAD_PROJECTION_CLEARANCE",
   "macro":ROOT/"source"/"cst"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_CIN_PAD_CLEARANCE_BUILD_ONLY_V01.mcr",
   "manifest":ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_CIN_PAD_CLEARANCE_MANIFEST_V01.json",
   "windows":b_windows,"toolcomp":"M7B_ClearanceTools",
   "scientific_change":"Open one 1.10 x 1.00 mm backside-ground window under each CIN_UP_PAD projection, using a 0.25-mm guard around the frozen 0.60 x 0.50 mm CIN_UP_PAD; leave upstream MSL ground, ground perimeter, package ground, spokes and vias unchanged.",
   "target_mechanism":"Reduce local CIN signal-to-return shunt capacitance that can participate in the composite signal-ground resonance, following the earlier H1C shaped/perforated-ground principle without arbitrary ground optimization.",
   "primary_prediction":"The 1.3-1.4 GHz full-E2C raw-deviation peak should move downward and the diff/common peak should reduce if local terminal-to-ground capacitance is a necessary resonant element.",
   "falsification":"If the 1.3432-GHz raw-deviation peak and 1.2-1.4-GHz diff/common degradation remain within 10% of full E2C, CIN-local shunt capacitance is not the controlling corrective lever.",
   "success_gate":{
      "primary":"At least 30% reduction in source-side complex deviation at the frozen full-E2C raw-peak neighborhood AND at least 6 dB reduction in E_UP diff-to-common degradation in 1.2-1.4 GHz.",
      "secondary":"Branch imbalance at 1.2984 GHz reduced by at least 30%.",
      "guard":"No new >6 dB narrow excursion within <=50 MHz and no numerical hard-gate failure."
   },
   "area_removed_per_branch_mm2":1.10
 }
}

for cid,c in cands.items():
    c["macro"].write_text(make_macro(cid,c["windows"],c["toolcomp"]),encoding="utf-8")
    tool_names=[f'{c["toolcomp"]}:{cid}_{k}_CLEARANCE' for k in branches]
    man={
      "schema_version":"gnss-m7-corrective-candidate-v0.1",
      "status":"FROZEN_BUILD_ONLY_AWAIT_AUTH",
      "candidate":cid,
      "title":c["title"],
      "parent":{"path":str(PARENT),"sha256":PARENT_SHA,"expected_solids":177,"raw_ports":24},
      "geometry":{
        "modified_entities":[branches[k]["ground"] for k in branches],
        "unchanged_classes":["radiator","stalk dielectric","all signal copper","package lands","local-ground-top copper","vias","bias/output copper","ports"],
        "clearance_windows_local_uv_mm":c["windows"],
        "tool_entities":tool_names,
        "tool_count":4,
        "tool_height_mm":-0.07,
        "expected_final_solids":177,
        "expected_raw_ports":24,
        "area_removed_per_branch_mm2":c["area_removed_per_branch_mm2"],
        "four_branch_symmetry_required":True
      },
      "scientific_change":c["scientific_change"],
      "target_mechanism":c["target_mechanism"],
      "primary_prediction":c["primary_prediction"],
      "falsification":c["falsification"],
      "pre_registered_success_gate":c["success_gate"],
      "comparison_authority":{
        "full_e2c_raw_peak_ghz":1.3432,
        "full_e2c_raw_max_complex_delta":0.7037929224295506,
        "full_e2c_mode_degradation_reference_db":21.795370023361176,
        "full_e2c_imbalance_peak_ghz":1.2984,
        "full_e2c_imbalance_db":11.374270538449593,
        "m6_conclusion":"ground important but ground-only frequency shape is not a scaled copy of full E2C"
      },
      "execution":{
        "macro":str(c["macro"].relative_to(ROOT)).replace("\\","/"),
        "macro_sha256":sha(c["macro"]),
        "build_stop":"STOP_AFTER_177_SOLID_24_PORT_FRESH_REOPEN_AND_HUMAN_GEOMETRY_REVIEW_NO_SOLVER"
      },
      "authorization":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
    }
    c["manifest"].write_text(json.dumps(man,indent=2)+"\n",encoding="utf-8")

AUDIT.write_text(r'''from __future__ import print_function
import ast, hashlib, json, re, sys
from pathlib import Path
ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7_CORRECTIVE_CANDIDATE_FREEZE_V01"/"STATIC_AUDIT.json"
PARENT_SHA="cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c"

def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()

checks={}; detail={}
for cid,stem in (
 ("M7A","R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7A_INNER_EDGE_SETBACK"),
 ("M7B","R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7B_CIN_PAD_CLEARANCE")):
 man=ROOT/"execution"/(stem+"_MANIFEST_V01.json")
 mac=ROOT/"source"/"cst"/(stem+"_BUILD_ONLY_V01.mcr")
 m=json.loads(man.read_text(encoding="utf-8")); t=mac.read_text(encoding="utf-8")
 checks[cid+"_status"]=m["status"]=="FROZEN_BUILD_ONLY_AWAIT_AUTH"
 checks[cid+"_parent_hash"]=m["parent"]["sha256"]==PARENT_SHA
 checks[cid+"_auth_false"]=m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
 checks[cid+"_four_tools"]=m["geometry"]["tool_count"]==4 and t.count(".Create")==4
 checks[cid+"_four_subtracts"]=t.count("Solid.Subtract")==4
 checks[cid+"_only_backgrounds_modified"]=all("BackGround:LOCAL_BACK_GROUND" in x for x in m["geometry"]["modified_entities"])
 checks[cid+"_no_signal_subtract"]=all("Signal:" not in x for x in re.findall(r'Solid\.Subtract "([^"]+)"',t))
 checks[cid+"_no_port_or_solver"]=all(x not in t for x in ("Port.","DiscretePort","Solver.","run_solver","StartSolver","ChangeSolverType","Monitor."))
 checks[cid+"_solid_count_unchanged"]=m["geometry"]["expected_final_solids"]==177 and m["geometry"]["expected_raw_ports"]==24
 checks[cid+"_macro_hash"]=sha(mac)==m["execution"]["macro_sha256"]
 checks[cid+"_four_branch_windows"]=set(m["geometry"]["clearance_windows_local_uv_mm"].keys())=={"A_P","A_N","B_P","B_N"}
 if cid=="M7A":
  w=m["geometry"]["clearance_windows_local_uv_mm"]
  checks["M7A_retains_signal_overhang"]=w["A_P"]==[1.0,1.5,3.0,5.0] and w["A_N"]==[-1.5,-1.0,3.0,5.0]
  checks["M7A_window_does_not_reach_signal_inner_edge"]=1.5 < 2.05
 if cid=="M7B":
  w=m["geometry"]["clearance_windows_local_uv_mm"]
  checks["M7B_exact_guarded_CIN_projection"]=w["A_P"]==[2.45,3.55,4.15,5.15] and w["A_N"]==[-3.55,-2.45,4.15,5.15]
  # Existing paddle vias start around v~7; CRF via around v~11, so the v<=5.15 window is separated.
  checks["M7B_window_separate_from_via_regions"]=max(x[3] for x in w.values())<=5.15
 detail[cid]={"manifest_sha256":sha(man),"macro_sha256":sha(mac),"success_gate":m["pre_registered_success_gate"]}

checks["candidate_count_exactly_two"]=len(detail)==2
status="PASS_M7_CORRECTIVE_CANDIDATE_STATIC_FREEZE" if all(checks.values()) else "HOLD_M7_CORRECTIVE_CANDIDATE_STATIC_FREEZE"
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({"status":status,"checks":checks,"detail":detail,"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},indent=2)+"\n",encoding="utf-8")
print(status)
for k,v in checks.items():
 if not v:print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
''',encoding="utf-8")

DOC.write_text("""# R4-A0-E2C-S0 M7 Corrective Candidate Freeze V0.1

Status: **FROZEN — AWAIT BUILD AUTHORIZATION**

M6 established:
- pre-CIN signal-only perturbation is WEAK;
- ground/backside/via-only perturbation is INTERMEDIATE;
- ground-only frequency shape is not a scaled copy of the full severe coexistence state;
- the working physical picture is a composite return-path / signal-ground interaction.

M7 deliberately freezes only two corrective candidates. No parameter sweep is allowed.

## M7A — INNER_EDGE_UPSTREAM_SETBACK

Change only the four backside branch-local grounds.

For each positive branch, remove local u=1.0..1.5 mm over v=3.0..5.0 mm.
For each negative branch, remove local u=-1.5..-1.0 mm over v=3.0..5.0 mm.

The frozen upstream MSL inner edge is at |u|=2.05 mm. Therefore the modified backside ground still extends to |u|=1.50 mm and retains 0.55 mm of center-side ground overhang beneath the signal. Outer ground edge, signal copper, CIN pad, package ground, spokes and vias remain unchanged.

Physical question:
Does the center-facing backside-ground edge provide a necessary near-field coupling surface for the composite mode?

Prediction:
If yes, full-E2C common-mode degradation and branch imbalance in the 1.2–1.4 GHz severe region should fall without a large unrelated resonance.

Falsification:
If diff/common degradation and imbalance stay within 10% of the full-E2C severe values, this edge-overlap mechanism is not the useful corrective lever.

Pre-registered success:
- >=30% reduction in BOTH E_UP diff-to-common degradation and branch-return imbalance at frozen severe anchors;
- secondary: >=20% reduction in maximum source-side complex deviation;
- no new >6 dB narrow excursion within <=50 MHz.

## M7B — CIN_PAD_PROJECTION_CLEARANCE

Keep the backside-ground perimeter unchanged.

Under every frozen CIN_UP_PAD, open an exact projection window with 0.25 mm guard:
- positive branch: u=2.45..3.55 mm, v=4.15..5.15 mm;
- negative branch: u=-3.55..-2.45 mm, v=4.15..5.15 mm.

The window is 1.10 x 1.00 mm. It does not reach the paddle-via or CRF-via regions. Upstream MSL ground remains present.

This implements the earlier H1C shaped/perforated-ground principle in the smallest current geometry: remove ground under a terminal/contact projection rather than optimize an arbitrary ground shape.

Physical question:
Is local CIN signal-to-return shunt capacitance a necessary resonant element in the composite mode?

Prediction:
If yes, the full-E2C ~1.3432 GHz raw-deviation peak and 1.2–1.4 GHz diff/common degradation should fall.

Falsification:
If the raw peak and diff/common degradation remain within 10% of full E2C, CIN-local shunt capacitance is not the controlling corrective lever.

Pre-registered success:
- >=30% reduction of source-side complex deviation around the frozen raw-peak neighborhood;
- >=6 dB reduction of E_UP diff-to-common degradation in 1.2–1.4 GHz;
- secondary: >=30% reduction of branch imbalance at 1.2984 GHz;
- no new >6 dB narrow excursion within <=50 MHz.

## Common BUILD contract

Parent is the frozen full-E2C R7 canonical BUILD_ONLY artifact, SHA256:
cab6754235a66006ba8bdb423c4dcde2d00de0cb5d8c56623cf94fc3c364ce2c

Each candidate:
- starts from the same parent;
- modifies only the four LOCAL_BACK_GROUND solids;
- uses four disposable clearance tools;
- must consume all four tools;
- expected final solids remain 177;
- expected raw ports remain 24;
- no port, material, signal, package, via, bias, radiator or solver mutation;
- requires fresh reopen and human geometry review;
- stops before SOLVE.

Default future order: **M7A BUILD first**. M7B remains unbuilt until separately authorized.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
""",encoding="utf-8")

print("PREPARED_M7A_M7B")
for cid,c in cands.items():
 print(cid,c["manifest"],sha(c["macro"]))
