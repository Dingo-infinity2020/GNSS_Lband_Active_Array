from __future__ import print_function
import ast, csv, hashlib, json, math, os, re, subprocess, sys
from pathlib import Path

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
D1_BUILD=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\build_only\M6_D1_SIG_ATTRIBUTION_V01\R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_SIG_BUILD_ONLY_V01.cst")
D2_BUILD=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\build_only\M6_D2_GND_ATTRIBUTION_V01\R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_GND_BUILD_ONLY_V01.cst")
D1_SHA="37abf12c415de2418d5d204811f1bc31e9a24cdc30b6538fc2d7d2ce659de7af"
D2_SHA="c2a935e8d3a9e2d1f8b1ee7d58320e8ffd6d8f0513a859a01869f4f757855f2a"
D1_GATE=ROOT/"execution"/"M6_D1_HUMAN_GEOMETRY_REVIEW_PASS.json"
D2_GATE=ROOT/"execution"/"M6_D2_HUMAN_GEOMETRY_REVIEW_PASS.json"
D1_BUILD_MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1_SIG_BUILD_MANIFEST_V01.json"
D2_BUILD_MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D2_GND_BUILD_MANIFEST_V01.json"
E2A_SOLVE_MAN=ROOT/"execution"/"R1E1A4A_AR0_B1R_R4_A0_E2A_S0L_LOADED_SOURCE_SOLVE_MANIFEST_V01.json"
E2A_BASELINE=Path(r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\E2A_S0L_SOLVE_20260929\evidence\loaded_response_native.csv")
E2A_BASELINE_SHA="a759ac6135a297429a8a166b6a01a39a66b5ec3a861267ed0f05d53ff605fae4"
M1M2=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1D2_PREBUILD_V01"/"STATIC_AUDIT.json"
FULL_M12=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M1M2_V01"/"M1_M2_ANALYSIS.json"
OUTE=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1D2_DIAGNOSTIC_SOLVE_PREP_V01"
DOC=ROOT/"docs"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1D2_DIAGNOSTIC_SOLVE_FREEZE_V01.md"

PRESOLVE=ROOT/"scripts"/"configure_m6_diagnostic_presolve_v01.py"
QUAL=ROOT/"scripts"/"qualify_m6_diagnostic_readonly_v01.py"
RUNNER=ROOT/"scripts"/"run_m6_diagnostic_solve_v01.py"
PKTGEN=ROOT/"scripts"/"make_m6_diagnostic_solve_packet_v01.py"
AUDIT=ROOT/"scripts"/"audit_m6_d1d2_diagnostic_solve_contract_v01.py"

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

if not D1_BUILD.exists() or sha(D1_BUILD)!=D1_SHA or not D1_BUILD.with_suffix("").exists():
    raise RuntimeError("D1_BUILD_AUTHORITY")
if not D2_BUILD.exists() or sha(D2_BUILD)!=D2_SHA or not D2_BUILD.with_suffix("").exists():
    raise RuntimeError("D2_BUILD_AUTHORITY")
if not D1_GATE.exists() or not D2_GATE.exists():
    raise RuntimeError("HUMAN_REVIEW_GATES")
if sha(E2A_BASELINE)!=E2A_BASELINE_SHA:
    raise RuntimeError("E2A_BASELINE_HASH")

d1bm=json.loads(D1_BUILD_MAN.read_text(encoding="utf-8"))
d2bm=json.loads(D2_BUILD_MAN.read_text(encoding="utf-8"))
full=json.loads(FULL_M12.read_text(encoding="utf-8"))
pola=full["m2"]["polarizations"]["PolA"]
full_raw=float(pola["own_pol_max_delta"]["delta_mag"])
full_mode_peak=float(pola["combined_modal_peaks"]["E_diff_to_common"]["db"])
base_mode_peak=float(pola["baseline_modal_peaks"]["E_diff_to_common"]["db"])
full_mode_degr=full_mode_peak-base_mode_peak
full_imb=float(pola["eup_return_imbalance"]["max_abs_db"])
if not (full_raw>0.2 and full_mode_degr>3 and full_imb>1):
    raise RuntimeError("FULL_E2C_REFERENCE_NOT_SEVERE")

MONITORS=[
 ("L2",1.2276),
 ("MIXED_WORST",1.3384),
 ("L1",1.57542),
]

CONFIG_TEMPLATE="""Option Explicit
' GNSS_Lband_Active_Array
' M6 diagnostic solve-copy configuration V01
' VARIANT: {variant}
' SOURCE BUILD SHA256: {source_sha}
'
' E2A observer semantics are preserved exactly.
' Raw 12 audit ports -> 6 solve ports.
' Sources: 1,2,4,5. Passive 50-ohm loads only: 3,6.
' H-field monitors are used because CST's HF workflow derives surface-current
' evidence on conducting surfaces from the H-field monitor result.
' No solver start in this macro.

Sub Main()

    Port.Delete 12
    Port.Delete 11
    Port.Delete 10
    Port.Delete 6
    Port.Delete 5
    Port.Delete 4

    Port.Rename 7, 4
    Port.Rename 8, 5
    Port.Rename 9, 6

    Solver.FrequencyRange "1.0", "1.8"

    With Boundary
        .Xmin "open"
        .Xmax "open"
        .Ymin "open"
        .Ymax "open"
        .Zmin "open"
        .Zmax "open"
        .Xsymmetry "none"
        .Ysymmetry "none"
        .Zsymmetry "none"
        .ApplyInAllDirections "False"
    End With

    With Background
        .ResetBackground
        .XminSpace "30"
        .XmaxSpace "30"
        .YminSpace "30"
        .YmaxSpace "30"
        .ZminSpace "30"
        .ZmaxSpace "30"
        .ApplyInAllDirections "False"
    End With

    ChangeSolverType "HF Frequency Domain"

    With MeshSettings
        .SetMeshType "Tet"
        .Set "CurvatureOrder", "3"
    End With

    With FDSolver
        .SetMethod "Tetrahedral", "General purpose"
        .OrderTet "Second"
        .Stimulation "List", "List"
        .ResetExcitationList
        .AddToExcitationList "1", "1"
        .AddToExcitationList "2", "1"
        .AddToExcitationList "4", "1"
        .AddToExcitationList "5", "1"
        .AutoNormImpedance "True"
        .NormingImpedance "50"
        .ModesOnly "False"
        .MeshAdaptionTet "True"
        .StoreAllResults "True"
        .StoreResultsInCache "False"
        .CalcPowerLoss "True"
        .CalcPowerLossPerComponent "False"
    End With

    With MeshAdaption3D
        .SetType "HighFrequencyTet"
        .SetAdaptionStrategy "ExpertSystem"
        .MinPasses "3"
        .MaxPasses "16"
        .MaxDeltaS "0.02"
        .NumberOfDeltaSChecks "2"
        .SetLinearGrowthLimitation "40"
    End With

    PostProcess1D.ActivateOperation "yz-matrices", "TRUE"

{monitor_blocks}

End Sub
"""

def mon_block(label,f):
    return """    With Monitor
        .Reset
        .Name "M6_HFIELD_SURFCURRENT_{label}_{freqname}"
        .Dimension "Volume"
        .Domain "Frequency"
        .FieldType "Hfield"
        .Frequency "{freq}"
        .UseSubvolume "False"
        .Create
    End With
""".format(label=label,freqname=str(f).replace(".","p"),freq=("%.5f"%f).rstrip("0").rstrip("."))

variants={}
for key,build,build_sha,bm,gate in (
    ("D1",D1_BUILD,D1_SHA,d1bm,D1_GATE),
    ("D2",D2_BUILD,D2_SHA,d2bm,D2_GATE),
):
    config=ROOT/"source"/"cst"/("R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_%s_DIAGNOSTIC_SOLVE_CONFIG_V01.mcr"%key)
    monitor_blocks="\n".join(mon_block(a,b) for a,b in MONITORS)
    config.write_text(CONFIG_TEMPLATE.format(variant=key,source_sha=build_sha,monitor_blocks=monitor_blocks),encoding="utf-8")
    stage="R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_%s_DIAGNOSTIC_SOLVE"%key
    manifest=ROOT/"execution"/("R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_%s_DIAGNOSTIC_SOLVE_MANIFEST_V01.json"%key)
    target=r"D:\GNSS_Lband_Active_Array\runs\formal\solver_runs\M6_%s_DIAGNOSTIC_SOLVE_V01"%key
    human=json.loads(gate.read_text(encoding="utf-8-sig"))
    m={
      "schema_version":"gnss-m6-diagnostic-solve-v0.1",
      "status":"FROZEN_READY_AWAIT_SOLVE_AUTH",
      "variant":key,
      "stage":stage,
      "scientific_role":"ONE_POLARIZATION_OBSERVER_ATTRIBUTION",
      "source_build":{
        "path":str(build),"sha256":build_sha,
        "shape_count":int(bm["geometry"]["expected_final_shape_count"]),
        "raw_ports":12,
        "human_review_gate":str(gate.relative_to(ROOT)).replace("\\","/"),
        "human_review_status":human["status"],
        "human_review_artifact_sha256":human["artifact_sha256"]
      },
      "observer_semantics":{
        "inherited_from":"E2A-S0L",
        "solve_ports":[
          {"n":1,"name":"A_E_UP","role":"SOURCE"},
          {"n":2,"name":"A_P_IN","role":"SOURCE_DEVICE_INPUT_PLANE"},
          {"n":3,"name":"A_P_OUT_LOAD50","role":"MATCHED_50OHM_LOAD_ONLY"},
          {"n":4,"name":"B_E_UP","role":"SOURCE"},
          {"n":5,"name":"B_P_IN","role":"SOURCE_DEVICE_INPUT_PLANE"},
          {"n":6,"name":"B_P_OUT_LOAD50","role":"MATCHED_50OHM_LOAD_ONLY"}
        ],
        "source_excitation_set":[1,2,4,5],
        "matched_load_only_set":[3,6],
        "removed_raw_ports":[4,5,6,10,11,12],
        "polB_diagnostic_ports":"NONE"
      },
      "solver":{
        "band_ghz":[1.0,1.8],"decision_band_ghz":[1.15,1.65],
        "type":"CST HF Frequency Domain","mesh":"second-order tetrahedral adaptive",
        "max_delta_s":0.02,"consecutive_passes_required":2,"max_passes":16,
        "formal_solver_budget":1,"automatic_retries":0
      },
      "surface_current_evidence":{
        "implementation":"Hfield frequency monitors; CST HF monitor yields H-field/surface-current result on conducting surfaces",
        "frequencies_ghz":[x[1] for x in MONITORS],
        "labels":[x[0] for x in MONITORS],
        "required_for_mechanism_interpretation":True,
        "not_a_numerical_convergence_gate":True,
        "manual_review_scope":[
          "observer Pol-A radiator/feed current distribution",
          "added passive Pol-B diagnostic entities",
          "symmetry/antisymmetry of E_UP branch current paths",
          "whether current localizes on signal metal, ground/vias, or only composite paths"
        ]
      },
      "response_contract":{
        "complex_traces":24,"source_side_4x4_terms":16,"output_load_pickup_terms":8,
        "common_native_grid_required":True,
        "baseline_csv":str(E2A_BASELINE),"baseline_sha256":E2A_BASELINE_SHA
      },
      "hard_numerical_gates":{
        "six_ports_exact":True,"selected_source_excitation_exact":True,
        "load_ports_never_excited":True,"response_24_terms_complete":True,
        "final_two_native_delta_s_lte_0p02":True,
        "source_side_reciprocity_max_abs_complex_lte_0p02":True,
        "loaded_column_power_lte_1p02":True,
        "no_fatal_solver_error":True,"no_mesh_corruption":True
      },
      "attribution_metrics":{
        "raw_source_side_max_complex_delta":{
          "baseline":"E2A isolated","full_e2c_reference":full_raw
        },
        "eup_diff_to_common_degradation_db":{
          "baseline_peak_db":base_mode_peak,
          "full_e2c_peak_db":full_mode_peak,
          "full_e2c_degradation_db":full_mode_degr
        },
        "eup_branch_return_imbalance_db":{
          "full_e2c_reference":full_imb
        },
        "fractions":{
          "raw":"variant_raw_delta/full_e2c_raw_delta",
          "mode":"max(0,variant_mode_degradation_db)/full_e2c_mode_degradation_db",
          "imbalance":"variant_imbalance_db/full_e2c_imbalance_db"
        },
        "variant_classification":{
          "STRONG":"at least 2 of 3 effect fractions >= 0.60",
          "WEAK":"all 3 effect fractions <= 0.30",
          "INTERMEDIATE":"otherwise"
        }
      },
      "cross_variant_decision_logic":{
        "D1_STRONG_D2_WEAK":"PRE_CIN_SIGNAL_PATH_PRIMARY",
        "D1_WEAK_D2_STRONG":"GROUND_RETURN_PATH_PRIMARY",
        "D1_WEAK_D2_WEAK":"SIGNAL_GROUND_INTERACTION_OR_COMPOSITE_MODE_PRIMARY",
        "D1_STRONG_D2_STRONG":"BOTH_CLASSES_INDEPENDENTLY_STRONG",
        "otherwise":"MIXED_OR_INCONCLUSIVE_REQUIRES_FIELD_CURRENT_REVIEW"
      },
      "execution":{
        "config_macro":str(config.relative_to(ROOT)).replace("\\","/"),
        "target_root":target,
        "artifact_name":"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_%s_DIAGNOSTIC_SOLVED_V01.cst"%key,
        "stop_boundary":"STOP_AFTER_ONE_DIAGNOSTIC_SOLVE_AND_READONLY_QUALIFICATION_NO_RETRY_NO_GEOMETRY_OPTIMIZATION"
      },
      "authorization":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
    }
    config_sha=sha(config); m["execution"]["config_macro_sha256"]=config_sha
    manifest.write_text(json.dumps(m,indent=2)+"\n",encoding="utf-8")
    variants[key]={"manifest":manifest,"config":config,"data":m}

PRESOLVE.write_text(r'''from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from pathlib import Path
from collections import Counter

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

S2=1.0/math.sqrt(2.0)
Z0=57.1428571428
PORT_LOCAL={1:(3.0,4.650),2:(3.0,6.085),3:(3.0,7.915),4:(-3.0,4.650),5:(-3.0,6.085),6:(-3.0,7.915)}
SOURCE_PORTS=(1,2,4,5); LOAD_ONLY=(3,6)

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def wrap(body): return "Sub Main()\n"+body+"\nEnd Sub"

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,x in enumerate(lines):
        if x.strip()=="Sub Main()": s=i
        elif x.strip()=="End Sub": e=i
    if s is None or e is None or e<=s: raise RuntimeError("HOLD_M6_DIAG_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    s=src.with_suffix(""); d=dst.with_suffix("")
    if not s.exists(): raise RuntimeError("HOLD_M6_DIAG_SOURCE_COMPANION")
    if d.exists(): shutil.rmtree(str(d),ignore_errors=True)
    shutil.copytree(str(s),str(d))

def inventory_named_vba(path,names):
    p=str(path).replace("\\","/")
    q=lambda s:s.replace('"','""')
    z=["On Error Resume Next","Dim f As Integer, nm As String, mat As String, vol As Double, em As Long, ev As Long",
       "f=FreeFile",'Open "'+p+'" For Output As #f','Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
       'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())']
    for n in names:
        z += ['nm="'+q(n)+'"',"Err.Clear","mat=Solid.GetMaterialNameForShape(nm)","em=Err.Number",
              "Err.Clear","vol=Solid.GetVolume(nm)","ev=Err.Number",
              'Print #f, "SHAPE|" & nm & "|MAT_ERR=" & CStr(em) & "|VOL_ERR=" & CStr(ev) & "|material=" & mat & "|volume=" & CStr(vol)']
    z += ["Close #f","On Error GoTo 0"]
    return "\n".join(z)

def port_vba(path,count):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Integer, stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",'Open "'+p+'" For Output As #f','Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "For i=1 To %d"%count,
      " Err.Clear"," pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P|" & CStr(i) & "|PROP_OK=" & CStr(pok) & "|ERR=" & CStr(Err.Number) & "|TYPE=" & stype & "|ZREF=" & CStr(zref)',
      " Err.Clear"," cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "C|" & CStr(i) & "|COORD_OK=" & CStr(cok) & "|ERR=" & CStr(Err.Number) & "|P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0) & "|P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i","Close #f","On Error GoTo 0"])

def parse_inv(path):
    rows={}; meta={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            p=line.split("|"); d={}
            for x in p[2:]:
                k,v=x.split("=",1); d[k]=v
            rows[p[1]]={"material":d["material"],"volume":float(d["volume"]),
                        "mat_err":int(d["MAT_ERR"]),"vol_err":int(d["VOL_ERR"])}
        elif "=" in line:
            k,v=line.split("=",1); meta[k]=v
    return rows,meta

def parse_ports(path):
    out={"count":None,"properties":{},"coordinates":{}}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("PORT_COUNT="): out["count"]=int(line.split("=",1)[1])
        elif line.startswith(("P|","C|")):
            p=line.split("|"); kind=p[0]; idx=int(p[1]); d={}
            for x in p[2:]:
                k,v=x.split("=",1); d[k]=v
            out["properties" if kind=="P" else "coordinates"][idx]=d
    return out

def xyz(s): return tuple(float(x) for x in s.split(","))

def expected_xyz(i):
    u,v=PORT_LOCAL[i]; z=Z0-v
    return (S2*u,S2*u,z),(S2*(u+1.0),S2*(u-1.0),z)

def ports6_exact(data,tol=2e-8):
    if data["count"]!=6: return False
    for i in range(1,7):
        p=data["properties"].get(i,{}); c=data["coordinates"].get(i,{})
        if p.get("PROP_OK") not in ("True","TRUE","1","-1"): return False
        if c.get("COORD_OK") not in ("True","TRUE","1","-1"): return False
        if p.get("TYPE")!="SParameter" or abs(float(p.get("ZREF","nan"))-50)>tol: return False
        e1,e2=expected_xyz(i)
        if any(abs(a-b)>tol for a,b in zip(xyz(c["P1"]),e1)): return False
        if any(abs(a-b)>tol for a,b in zip(xyz(c["P2"]),e2)): return False
    return True

def sig(rows): return {k:(v["material"],round(v["volume"],12)) for k,v in rows.items()}

def result_solver_paths(cst):
    try:
        items=ProjectFile(str(cst),allow_interactive=True).get_3d().get_tree_items()
        return [x for x in items if ("S-Parameters" in x or "Convergence" in x or "Adaptive Meshing" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+repr(ex)]

def configure(manifest_path,out,evidence):
    manifest_path=Path(manifest_path); out=Path(out); evidence=Path(evidence)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    src=Path(m["source_build"]["path"])
    config=Path(ROOT/m["execution"]["config_macro"]) if not Path(m["execution"]["config_macro"]).is_absolute() else Path(m["execution"]["config_macro"])
    names=json.loads(Path(ROOT/("execution/R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_%s_%s_BUILD_MANIFEST_V01.json"%(
      m["variant"],"SIG" if m["variant"]=="D1" else "GND"))).read_text(encoding="utf-8"))["geometry"]["expected_final_names"]
    if sha(src)!=m["source_build"]["sha256"] or not src.with_suffix("").exists(): raise RuntimeError("HOLD_M6_DIAG_SOURCE")
    if sha(config)!=m["execution"]["config_macro_sha256"]: raise RuntimeError("HOLD_M6_DIAG_CONFIG_SHA")
    if out.exists() or out.with_suffix("").exists() or evidence.exists(): raise RuntimeError("HOLD_M6_DIAG_DEST_EXISTS")
    evidence.mkdir(parents=True)
    copy_project(src,out)

    bi=evidence/"before_inventory.txt"; bp=evidence/"before_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inventory_named_vba(bi,names))): raise RuntimeError("HOLD_M6_DIAG_BEFORE_INV")
        if not p.schematic.execute_vba_code(wrap(port_vba(bp,12))): raise RuntimeError("HOLD_M6_DIAG_BEFORE_PORTS")
    finally:
        if p is not None: p.close()
        de.close()
    br,bm=parse_inv(bi)
    if int(bm.get("SHAPE_COUNT","-1"))!=m["source_build"]["shape_count"] or int(bm.get("PORT_COUNT","-1"))!=12 or len(br)!=len(names):
        raise RuntimeError("HOLD_M6_DIAG_SOURCE_GATE")
    if any(v["mat_err"] or v["vol_err"] for v in br.values()): raise RuntimeError("HOLD_M6_DIAG_SOURCE_QUERY")
    before=sig(br)
    if result_solver_paths(out): raise RuntimeError("HOLD_M6_DIAG_SOURCE_HAS_RESULTS")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out)); p.modeler.add_to_history("M6 %s diagnostic presolve config V01"%m["variant"],macro_body(config)); p.save()
    finally:
        if p is not None: p.close()
        de.close()
    configured_sha=sha(out)

    ai=evidence/"configured_inventory.txt"; ap=evidence/"configured_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        if not p.schematic.execute_vba_code(wrap(inventory_named_vba(ai,names))): raise RuntimeError("HOLD_M6_DIAG_AFTER_INV")
        if not p.schematic.execute_vba_code(wrap(port_vba(ap,6))): raise RuntimeError("HOLD_M6_DIAG_AFTER_PORTS")
    finally:
        if p is not None: p.close()
        de.close()
    ar,am=parse_inv(ai); pd=parse_ports(ap)
    hist=out.with_suffix("")/"Model"/"3D"/"Model.mod"
    ht=hist.read_text(encoding="utf-8",errors="replace") if hist.exists() else ""
    required=[
      'Port.Delete 12','Port.Delete 11','Port.Delete 10','Port.Delete 6','Port.Delete 5','Port.Delete 4',
      'Port.Rename 7, 4','Port.Rename 8, 5','Port.Rename 9, 6',
      '.AddToExcitationList "1", "1"','.AddToExcitationList "2", "1"',
      '.AddToExcitationList "4", "1"','.AddToExcitationList "5", "1"',
      '.FieldType "Hfield"','.Frequency "1.2276"','.Frequency "1.3384"','.Frequency "1.57542"']
    checks={
      "source_hash_exact":sha(src)==m["source_build"]["sha256"],
      "shape_count_unchanged":int(am.get("SHAPE_COUNT","-1"))==m["source_build"]["shape_count"],
      "geometry_signature_unchanged":sig(ar)==before,
      "six_ports_exact":ports6_exact(pd),
      "history_tokens_exact":all(x in ht for x in required),
      "load_ports_not_excited":'.AddToExcitationList "3", "1"' not in ht and '.AddToExcitationList "6", "1"' not in ht,
      "three_hfield_monitors":ht.count('.FieldType "Hfield"')>=3,
      "result_tree_empty_before_solve":len(result_solver_paths(out))==0,
      "configured_hash_stable":sha(out)==configured_sha
    }
    (evidence/"presolve_summary.json").write_text(json.dumps({"status":"PASS_M6_DIAG_PRESOLVE" if all(checks.values()) else "HOLD_M6_DIAG_PRESOLVE","checks":checks,"configured_sha256":configured_sha},indent=2)+"\n",encoding="utf-8")
    if not all(checks.values()): raise RuntimeError("HOLD_M6_DIAG_PRESOLVE")
    return {"configured_sha256":configured_sha,"source_sha256":m["source_build"]["sha256"]}

ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--variant-manifest",required=True); ap.add_argument("--out",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        print(json.dumps(configure(a.variant_manifest,a.out,a.evidence),indent=2))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
''',encoding="utf-8")

QUAL.write_text(r'''from __future__ import print_function
import argparse, csv, cmath, json, math, re, sys, traceback
from pathlib import Path
from cst.results import ProjectFile

SOURCE_PORTS=(1,2,4,5); ALL_ROWS=(1,2,3,4,5,6); SOURCE_SIDE=(1,2,4,5)

def db(z): return 20.0*math.log10(max(abs(z),1e-300))

def read_csv(path):
    rows=list(csv.DictReader(open(str(path),"r",newline="")))
    f=[float(r["f_GHz"]) for r in rows]; d={}
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            k="S%d%d"%(i,j)
            if k+"_real" in rows[0]:
                d[(i,j)]=[complex(float(r[k+"_real"]),float(r[k+"_imag"])) for r in rows]
    return f,d

def choose_run(p3,paths):
    common=None; allids={}
    for p in paths:
        ids=list(p3.get_run_ids(p,False)); allids[p]=ids
        common=set(ids) if common is None else common.intersection(ids)
    if not common: raise RuntimeError("HOLD_M6_DIAG_NO_COMMON_RUN")
    return max(common),allids

def read_responses(cst):
    p3=ProjectFile(str(cst),allow_interactive=True).get_3d(); items=p3.get_tree_items()
    paths=[r"1D Results\S-Parameters\S%d,%d"%(i,j) for j in SOURCE_PORTS for i in ALL_ROWS]
    for p in paths:
        if p not in items: raise RuntimeError("HOLD_M6_DIAG_MISSING_RESPONSE:"+p)
    rid,ids=choose_run(p3,paths)
    data={}; freqs=None
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            p=r"1D Results\S-Parameters\S%d,%d"%(i,j)
            vals=[(float(x[0]),complex(x[1])) for x in p3.get_result_item(p,rid).get_data()]
            fs=[x[0] for x in vals]
            if freqs is None: freqs=fs
            elif len(fs)!=len(freqs) or any(abs(a-b)>1e-9 for a,b in zip(fs,freqs)): raise RuntimeError("HOLD_M6_DIAG_GRID_MISMATCH")
            data[(i,j)]=[x[1] for x in vals]
    field_paths=[x for x in items if any(k in x.lower() for k in ("h-field","hfield","surface current","surfacecurrent"))]
    return freqs,data,{"selected_run_id":rid,"response_run_ids":ids,"field_result_paths":field_paths}

def native_log(cst):
    root=Path(cst).with_suffix("")
    texts=[]
    for p in root.rglob("*.txt"):
        try: texts.append(p.read_text(encoding="utf-8",errors="ignore"))
        except: pass
    t="\n".join(texts)
    vals=[float(x) for x in re.findall(r"All\s+S-Parameters\s*=\s*([0-9.+\-Ee]+)",t,re.I)]
    fatal=bool(re.search(r"fatal\s+error|solver\s+stopped\s+with\s+error",t,re.I))
    mesh=bool(re.search(r"mesh.{0,40}(corrupt|invalid)",t,re.I))
    return vals,{"fatal_error":fatal,"mesh_corruption":mesh}

def write_csv(path,freqs,data):
    hdr=["f_GHz"]
    for j in SOURCE_PORTS:
        for i in ALL_ROWS:
            k="S%d%d"%(i,j); hdr += [k+"_real",k+"_imag",k+"_dB",k+"_phase_deg"]
    with open(str(path),"w",newline="") as f:
        w=csv.writer(f); w.writerow(hdr)
        for n,fr in enumerate(freqs):
            row=[fr]
            for j in SOURCE_PORTS:
                for i in ALL_ROWS:
                    z=data[(i,j)][n]; row += [z.real,z.imag,db(z),math.degrees(cmath.phase(z))]
            w.writerow(row)

def mode_dc(data,k):
    spp=data[(1,1)][k]; spn=data[(1,4)][k]; snp=data[(4,1)][k]; snn=data[(4,4)][k]
    return 0.5*(spp-spn+snp-snn)

def metrics(freqs,data,bfreq,bdata,m):
    if len(freqs)!=len(bfreq) or any(abs(a-b)>1e-9 for a,b in zip(freqs,bfreq)): raise RuntimeError("HOLD_M6_DIAG_BASELINE_GRID")
    core=[k for k,f in enumerate(freqs) if 1.15<=f<=1.65]
    maxd=(-1,None,None,None)
    for i in SOURCE_SIDE:
        for j in SOURCE_SIDE:
            for k in core:
                d=abs(data[(i,j)][k]-bdata[(i,j)][k])
                if d>maxd[0]: maxd=(d,k,i,j)
    vmode=max((abs(mode_dc(data,k)),k) for k in core)
    bmode=max((abs(mode_dc(bdata,k)),k) for k in core)
    vmode_db=db(vmode[0]); bmode_db=db(bmode[0]); degr=vmode_db-bmode_db
    imb=max((abs(db(data[(1,1)][k])-db(data[(4,4)][k])),k) for k in core)

    reciprocity=max(abs(data[(i,j)][k]-data[(j,i)][k]) for k in range(len(freqs)) for ix,i in enumerate(SOURCE_SIDE) for j in SOURCE_SIDE[ix+1:])
    powers=[sum(abs(data[(i,j)][k])**2 for i in ALL_ROWS) for k in range(len(freqs)) for j in SOURCE_PORTS]
    full=m["attribution_metrics"]
    fr={
      "raw":maxd[0]/float(full["raw_source_side_max_complex_delta"]["full_e2c_reference"]),
      "mode":max(0.0,degr)/float(full["eup_diff_to_common_degradation_db"]["full_e2c_degradation_db"]),
      "imbalance":imb[0]/float(full["eup_branch_return_imbalance_db"]["full_e2c_reference"])
    }
    strong=sum(1 for x in fr.values() if x>=0.60)>=2
    weak=all(x<=0.30 for x in fr.values())
    cls="STRONG" if strong else ("WEAK" if weak else "INTERMEDIATE")
    return {
      "raw_source_side_max_complex_delta":{"value":maxd[0],"frequency_ghz":freqs[maxd[1]],"ports":[maxd[2],maxd[3]]},
      "eup_diff_to_common":{"variant_peak_db":vmode_db,"baseline_peak_db":bmode_db,"degradation_db":degr,"frequency_ghz":freqs[vmode[1]]},
      "eup_branch_return_imbalance":{"max_abs_db":imb[0],"frequency_ghz":freqs[imb[1]]},
      "effect_fractions":fr,"variant_classification":cls,
      "source_side_reciprocity_max_abs_complex":reciprocity,
      "loaded_column_power_max":max(powers)
    }

def qualify(manifest_path,solved,evidence):
    manifest_path=Path(manifest_path); solved=Path(solved); evidence=Path(evidence)
    m=json.loads(manifest_path.read_text(encoding="utf-8"))
    freqs,data,runmeta=read_responses(solved)
    bfreq,bdata=read_csv(Path(m["response_contract"]["baseline_csv"]))
    met=metrics(freqs,data,bfreq,bdata,m)
    vals,flags=native_log(solved)
    convergence=len(vals)>=2 and vals[-2]<=0.02 and vals[-1]<=0.02
    fields=runmeta["field_result_paths"]
    monitor_presence={str(f):any(str(f)[:5] in x for x in fields) for f in m["surface_current_evidence"]["frequencies_ghz"]}
    hard={
      "response_24_terms_complete":len(data)==24,
      "native_grid_1001_1p0_1p8":len(freqs)==1001 and abs(freqs[0]-1.0)<1e-9 and abs(freqs[-1]-1.8)<1e-9,
      "final_two_native_delta_s_lte_0p02":convergence,
      "source_side_reciprocity_lte_0p02":met["source_side_reciprocity_max_abs_complex"]<=0.02,
      "loaded_column_power_lte_1p02":met["loaded_column_power_max"]<=1.02,
      "no_fatal_solver_error":not flags["fatal_error"],
      "no_mesh_corruption":not flags["mesh_corruption"]
    }
    status="PASS_M6_%s_DIAGNOSTIC_NUMERICAL_QUALIFICATION"%m["variant"] if all(hard.values()) else "HOLD_M6_%s_DIAGNOSTIC_NUMERICAL_QUALIFICATION"%m["variant"]
    field_status="FIELD_RESULT_PATHS_PRESENT" if fields else "FIELD_RESULT_PATHS_REQUIRE_MANUAL_CST_REVIEW"
    summary={"status":status,"variant":m["variant"],"formal_solver_invocations":1,"automatic_retries":0,
             "hard_checks":hard,"native_delta_sequence":vals,"native_flags":flags,
             "metrics":met,"runmeta":runmeta,"surface_current_evidence_status":field_status,
             "monitor_frequency_path_hints":monitor_presence,
             "science_boundary":"Attribution class is provisional until D1 and D2 are both numerically qualified and current-path evidence is manually reviewed."}
    write_csv(evidence/"loaded_response_native.csv",freqs,data)
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    (evidence/"FIELD_CURRENT_REVIEW.md").write_text(
      "# M6 %s Field/Surface-Current Review\n\nReview 1.2276, 1.3384, 1.57542 GHz for source excitations 1 and 4 using identical display scale.\n\nCompare observer radiator/feed current and the passive diagnostic entities. Record whether current localization is signal-dominant, ground/via-dominant, or requires the composite structure.\n"%m["variant"],encoding="utf-8")
    print(status)
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--variant-manifest",required=True); ap.add_argument("--solved",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(qualify(a.variant_manifest,a.solved,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"QUALIFICATION_EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
''',encoding="utf-8")

RUNNER.write_text(r'''from __future__ import print_function
import argparse, json, sys, traceback
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from configure_m6_diagnostic_presolve_v01 import configure
from qualify_m6_diagnostic_readonly_v01 import qualify

PREFIX="SIMOPS_EVENT "
def emit(phase,state,boundary,message=""):
    o={"schema_version":"simops-project-event-v0.1","event":"PHASE","phase":phase,"state":state,"production_boundary":boundary}
    if message: o["message"]=message
    print(PREFIX+json.dumps(o,separators=(",",":")),flush=True)

def main(manifest,out,evidence):
    manifest=Path(manifest); out=Path(out); evidence=Path(evidence)
    emit("presolve_config","START","NOT_OBSERVED")
    cfg=configure(manifest,out,evidence)
    emit("presolve_config","PASS","NOT_OBSERVED")

    (evidence/"solver_invocation.json").write_text(json.dumps({
      "formal_solver_invocations":1,"automatic_retries":0,"retry_authorized":False,
      "configured_sha256":cfg["configured_sha256"],"source_sha256":cfg["source_sha256"]},indent=2)+"\n",encoding="utf-8")

    emit("solver_run","START","OBSERVED")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(out))
        p.modeler.run_solver()
        p.save()
    finally:
        if p is not None: p.close()
        de.close()
    emit("solver_run","PASS","OBSERVED")

    emit("qualification","START","OBSERVED")
    rc=qualify(manifest,out,evidence)
    emit("qualification","PASS" if rc==0 else "HOLD","OBSERVED")
    emit("complete","PASS" if rc==0 else "HOLD","OBSERVED")
    return rc

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--variant-manifest",required=True); ap.add_argument("--out",required=True); ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try: sys.exit(main(a.variant_manifest,a.out,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_M6_DIAGNOSTIC_SOLVE_EXECUTION\n",encoding="utf-8")
        traceback.print_exc(); sys.exit(9)
''',encoding="utf-8")

PKTGEN.write_text(r'''from __future__ import print_function
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",required=True); ap.add_argument("--variant-manifest",required=True)
    ap.add_argument("--packet",required=True); ap.add_argument("--state-root",required=True); ap.add_argument("--result-packet",required=True)
    ap.add_argument("--cst-python",required=True)
    a=ap.parse_args()
    root=Path(a.project_root).resolve(); vm=Path(a.variant_manifest).resolve()
    m=json.loads(vm.read_text(encoding="utf-8")); cpath=root/"execution"/"stage_contract.json"
    runner=root/"scripts"/"run_m6_diagnostic_solve_v01.py"; launcher=root/"scripts"/"cst_bundled_python_launcher_v01.py"
    pres=root/"scripts"/"configure_m6_diagnostic_presolve_v01.py"; qual=root/"scripts"/"qualify_m6_diagnostic_readonly_v01.py"
    if subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True).strip(): raise SystemExit("HOLD_M6_DIAG_PROJECT_DIRTY")
    head=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    c=json.loads(cpath.read_text(encoding="utf-8-sig")); g=c.get("authorization",{}).get("active_grant")
    failed=[]
    if c.get("authorization",{}).get("BUILD_AUTHORIZED") is not False: failed.append("build_false")
    if c.get("authorization",{}).get("SOLVE_AUTHORIZED") is not True: failed.append("solve_live")
    if not isinstance(g,dict): failed.append("active_grant")
    if isinstance(g,dict):
        if g.get("kind")!="SOLVE": failed.append("grant_kind")
        if g.get("state")!="GRANTED": failed.append("grant_state")
        if g.get("stage")!=m["stage"]: failed.append("grant_stage")
        if g.get("entrypoint_sha256")!=sha(runner): failed.append("entrypoint_sha")
        if g.get("source_commit")!=c.get("project",{}).get("source_commit"): failed.append("source_commit")
    if c.get("execution",{}).get("current_stage")!=m["stage"]: failed.append("current_stage")
    if failed: raise SystemExit("HOLD_M6_DIAG_LIVE_SOLVE_GRANT:"+",".join(failed))

    target=Path(m["execution"]["target_root"]); artifact=target/m["execution"]["artifact_name"]; evidence=target/"evidence"
    rel=lambda p:str(p.relative_to(root)).replace("\\","/")
    packet={
      "schema_version":"runner-task-v0.2",
      "packet_id":"GNSS-M6-%s-DIAGNOSTIC-SOLVE-V01"%m["variant"],
      "project":{"name":"GNSS_Lband_Active_Array","repository":"Dingo-infinity2020/GNSS_Lband_Active_Array","source_commit":c["project"]["source_commit"],"model_identity":m["stage"]},
      "stage":{"name":m["stage"],"kind":"SOLVE","control_host_alias":"NW","working_directory":str(root),"stop_boundary":m["execution"]["stop_boundary"]},
      "transport":{"type":"local","ssh_alias":"","remote_shell":""},
      "preflight":{"fail_closed":True,"checks":[
        {"id":"git_clean","type":"git_clean","path":"."},
        {"id":"git_head","type":"git_head_equals","path":".","commit":head},
        {"id":"runner_hash","type":"file_sha256_equals","path":rel(runner),"sha256":sha(runner)},
        {"id":"presolve_hash","type":"file_sha256_equals","path":rel(pres),"sha256":sha(pres)},
        {"id":"qualifier_hash","type":"file_sha256_equals","path":rel(qual),"sha256":sha(qual)},
        {"id":"launcher_hash","type":"file_sha256_equals","path":rel(launcher),"sha256":sha(launcher)},
        {"id":"variant_manifest_hash","type":"file_sha256_equals","path":rel(vm),"sha256":sha(vm)},
        {"id":"config_hash","type":"file_sha256_equals","path":m["execution"]["config_macro"],"sha256":m["execution"]["config_macro_sha256"]},
        {"id":"stage_contract_hash","type":"file_sha256_equals","path":"execution/stage_contract.json","sha256":sha(cpath)},
        {"id":"source_build_hash","type":"file_sha256_equals","path":m["source_build"]["path"],"sha256":m["source_build"]["sha256"]},
        {"id":"baseline_hash","type":"file_sha256_equals","path":m["response_contract"]["baseline_csv"],"sha256":m["response_contract"]["baseline_sha256"]},
        {"id":"target_absent","type":"path_absent","path":str(target)},
        {"id":"result_absent","type":"result_path_absent"},
        {"id":"cst_gui_absent","type":"process_absent","name":"CST DESIGN ENVIRONMENT_AMD64.exe","ignore_case":True},
        {"id":"cst_modeler_absent","type":"process_absent","name":"modeler_AMD64.exe","ignore_case":True}
      ]},
      "entrypoint":{"argv":["python",rel(launcher),rel(runner),"--variant-manifest",rel(vm),"--out",str(artifact),"--evidence",str(evidence)],
                    "environment":{"CST_PYTHON_EXECUTABLE":str(Path(a.cst_python).resolve())},"timeout_seconds":9000},
      "authorization":{"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":True,
        "grant_snapshot":{"grant_id":g["grant_id"],"kind":g["kind"],"state":g["state"],"stage":g["stage"],"source_commit":g["source_commit"],
          "entrypoint_path":rel(runner),"entrypoint_sha256":sha(runner),"stage_contract_path":"execution/stage_contract.json",
          "stage_contract_sha256":sha(cpath),"granted_at":g["granted_at"],"expires_at":g.get("expires_at"),"entrypoint_arg_index":2}},
      "dc_call_budget":{"target_calls":1,"polling_policy":"no_polling","remote_mcp_calls_target":3},
      "expected_outputs":[
        {"path":str(artifact),"required":True,"sha256":True},
        {"path":str(evidence/"solver_invocation.json"),"required":True,"sha256":True},
        {"path":str(evidence/"loaded_response_native.csv"),"required":True,"sha256":True},
        {"path":str(evidence/"summary.json"),"required":True,"sha256":True},
        {"path":str(evidence/"FINAL_STATUS.txt"),"required":True,"sha256":True},
        {"path":str(evidence/"FIELD_CURRENT_REVIEW.md"),"required":True,"sha256":True}],
      "result":{"state_root":str(Path(a.state_root).resolve()),"result_packet_path":str(Path(a.result_packet).resolve())}
    }
    p=Path(a.packet); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(packet,indent=2)+"\n",encoding="utf-8")
    print("PASS_M6_DIAGNOSTIC_SOLVE_PACKET_GENERATED")
    return 0
if __name__=="__main__": sys.exit(main())
''',encoding="utf-8")

AUDIT.write_text(r'''from __future__ import print_function
import ast, hashlib, json, re, sys
from pathlib import Path
ROOT=Path(r"D:\GNSS_R4A0E1_20260928")
OUT=ROOT/"evidence"/"R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_D1D2_DIAGNOSTIC_SOLVE_PREP_V01"/"STATIC_AUDIT.json"
files={
 "presolve":ROOT/"scripts"/"configure_m6_diagnostic_presolve_v01.py",
 "qualifier":ROOT/"scripts"/"qualify_m6_diagnostic_readonly_v01.py",
 "runner":ROOT/"scripts"/"run_m6_diagnostic_solve_v01.py",
 "packet":ROOT/"scripts"/"make_m6_diagnostic_solve_packet_v01.py"}
def sha(p):
 h=hashlib.sha256()
 with open(str(p),"rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def run_calls(p):
 tree=ast.parse(p.read_text(encoding="utf-8")); calls=[]
 for x in ast.walk(tree):
  if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=="run_solver": calls.append(x)
 return tree,calls
checks={}; detail={}
for key in ("D1","D2"):
 man=ROOT/"execution"/("R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M6_%s_DIAGNOSTIC_SOLVE_MANIFEST_V01.json"%key)
 m=json.loads(man.read_text(encoding="utf-8")); cfg=ROOT/m["execution"]["config_macro"]; t=cfg.read_text(encoding="utf-8")
 checks[key+"_auth_false"]=m["authorization"]=={"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False}
 checks[key+"_source_exists_hash"]=Path(m["source_build"]["path"]).exists() and sha(Path(m["source_build"]["path"]))==m["source_build"]["sha256"]
 checks[key+"_human_review_pass"]=m["source_build"]["human_review_status"].startswith("PASS_")
 checks[key+"_baseline_hash"]=sha(Path(m["response_contract"]["baseline_csv"]))==m["response_contract"]["baseline_sha256"]
 checks[key+"_six_port_delete_map"]=all(x in t for x in ('Port.Delete 12','Port.Delete 11','Port.Delete 10','Port.Delete 6','Port.Delete 5','Port.Delete 4','Port.Rename 7, 4','Port.Rename 8, 5','Port.Rename 9, 6'))
 checks[key+"_sources_exact"]=all(('.AddToExcitationList "%d", "1"'%p) in t for p in (1,2,4,5)) and all(('.AddToExcitationList "%d", "1"'%p) not in t for p in (3,6))
 checks[key+"_solver_fidelity"]=all(x in t for x in ('ChangeSolverType "HF Frequency Domain"','.OrderTet "Second"','.MaxPasses "16"','.MaxDeltaS "0.02"','.NumberOfDeltaSChecks "2"'))
 checks[key+"_three_hfield_monitors"]=t.count('.FieldType "Hfield"')==3 and all(('Frequency "%s"'%str(f)) in t for f in (1.2276,1.3384,1.57542))
 checks[key+"_no_solver_start_in_config"]=all(x not in t for x in ("run_solver","Solver.Start","StartSolver"))
 checks[key+"_thresholds_frozen"]=m["attribution_metrics"]["variant_classification"]["STRONG"].startswith("at least 2") and m["attribution_metrics"]["variant_classification"]["WEAK"].startswith("all 3")
 detail[key]={"manifest_sha256":sha(man),"config_sha256":sha(cfg),"source_sha256":m["source_build"]["sha256"]}
for k,p in files.items():
 tree,calls=run_calls(p)
 checks[k+"_compiles_ast"]=True
 checks[k+"_run_solver_count"]=(len(calls)==1 if k=="runner" else len(calls)==0)
 if k=="runner" and calls:
  call=calls[0]; in_loop=False
  for n in ast.walk(tree):
   if isinstance(n,(ast.For,ast.While)):
    for z in ast.walk(n):
     if z is call: in_loop=True
  checks["runner_run_solver_not_in_loop"]=not in_loop
checks["packet_v02"]='"schema_version":"runner-task-v0.2"' in files["packet"].read_text(encoding="utf-8")
checks["packet_live_solve_fail_closed"]="HOLD_M6_DIAG_LIVE_SOLVE_GRANT" in files["packet"].read_text(encoding="utf-8")
checks["presolve_named_inventory_no_index_scan"]="GetNameOfShapeFromIndex" not in files["presolve"].read_text(encoding="utf-8")
status="PASS_M6_D1D2_DIAGNOSTIC_SOLVE_STATIC_CONTRACT" if all(checks.values()) else "HOLD_M6_D1D2_DIAGNOSTIC_SOLVE_STATIC_CONTRACT"
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps({"status":status,"checks":checks,"detail":detail,"formal_solver_invocations":0,"BUILD_AUTHORIZED":False,"SOLVE_AUTHORIZED":False},indent=2)+"\n",encoding="utf-8")
print(status)
for k,v in checks.items():
 if not v: print("FAIL "+k)
sys.exit(0 if status.startswith("PASS_") else 4)
''',encoding="utf-8")

DOC.write_text("""# R4-A0-E2C-S0 M6 D1/D2 Diagnostic SOLVE Freeze V0.1

Status: FROZEN_READY_AWAIT_SOLVE_AUTH

This node freezes the diagnostic solve semantics only. No solver has been run.

## Common observer semantics

D1 and D2 use the exact E2A-S0L six-port observer network:

1. A_E_UP — source
2. A_P_IN — source/device-input plane
3. A_P_OUT — 50-ohm passive load only
4. B_E_UP — source
5. B_P_IN — source/device-input plane
6. B_P_OUT — 50-ohm passive load only

Ports 1,2,4,5 are the only selected sources. Ports 3,6 are never excited.

Frequency/solver fidelity is inherited from E2A-S0L: 1.0-1.8 GHz HF Frequency Domain, second-order tetrahedral adaptive mesh, MaxDeltaS 0.02, two consecutive checks, MaxPasses 16.

## Surface-current evidence

Three H-field monitors are frozen at:
- L2 1.2276 GHz
- mixed-mode diagnostic frequency 1.3384 GHz
- L1 1.57542 GHz

CST's high-frequency monitor workflow uses H-field monitor results for H-field/surface-current inspection on conducting surfaces. These field maps are supporting mechanism evidence; numerical convergence remains governed by the S-parameter hard gates.

For current-path review, compare source excitations 1 and 4 with identical display scale and inspect:
- observer radiator/feed;
- passive diagnostic entities;
- branch symmetry/antisymmetry;
- localization on signal metal versus ground/vias.

## Attribution metrics

Every variant is compared to the immutable isolated E2A baseline and normalized to the already-solved full-E2C Pol-A endpoint.

Metrics:
1. maximum complex delta of the 4x4 source-side S block;
2. E_UP differential-to-common peak degradation in dB;
3. E_UP plus/minus self-return imbalance in dB.

Effect fractions are defined against the full-E2C effect.

Variant classification:
- STRONG: at least two of three fractions >= 0.60;
- WEAK: all three fractions <= 0.30;
- INTERMEDIATE: otherwise.

Cross-variant interpretation:
- D1 STRONG / D2 WEAK -> pre-CIN signal path primary;
- D1 WEAK / D2 STRONG -> ground-return path primary;
- D1 WEAK / D2 WEAK while full E2C remains severe -> signal-ground interaction/composite mixed mode primary;
- D1 STRONG / D2 STRONG -> both classes independently strong;
- all other cases -> mixed/inconclusive and field-current review is required before geometry optimization.

## Execution order

Default future order is D1 solve first, close its grant and qualify it, then D2 under a separate SOLVE grant. There is no automatic continuation and no retry.

No geometry optimization, C1 promotion, or active-LNA integration is authorized by a diagnostic result.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
""",encoding="utf-8")

print("PREPARED_M6_D1D2_DIAGNOSTIC_SOLVE")
print("FULL_RAW_REF=%.9f"%full_raw)
print("BASE_MODE_DB=%.6f"%base_mode_peak)
print("FULL_MODE_DB=%.6f"%full_mode_peak)
print("FULL_MODE_DEGR_DB=%.6f"%full_mode_degr)
print("FULL_IMBALANCE_DB=%.6f"%full_imb)
print("D1_MANIFEST="+str(variants["D1"]["manifest"]))
print("D2_MANIFEST="+str(variants["D2"]["manifest"]))
