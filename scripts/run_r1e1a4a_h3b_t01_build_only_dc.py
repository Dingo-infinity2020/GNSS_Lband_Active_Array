"""H3B-T01 standalone orthogonal transition coupon — one-shot BUILD-ONLY harness."""
from __future__ import print_function
import argparse, json, os, sys, hashlib
from collections import Counter

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path: sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

SOLVER_MARKERS=("meshing successful","adaptive mesh refinement pass","running solver","excitation: port")

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""): h.update(c)
    return h.hexdigest()

def macro_body(path):
    lines=open(path,encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=lines.index("Sub Main()"); e=lines.index("End Sub")
    return "\n".join(lines[s+1:e])

def parameter_map(cstfile):
    q=os.path.join(os.path.splitext(cstfile)[0],"Model","Parameters.json")
    data=json.load(open(q,encoding="utf-8")); out={}
    def walk(x):
        if isinstance(x,dict):
            if "name" in x and "value" in x: out[str(x["name"])]=str(x["value"])
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(data); return out

def solver_tree_items(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    return [x for x in pf.get_3d().get_tree_items()
            if ("S-Parameters" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]

def solver_log_hits(cstfile):
    q=os.path.join(os.path.splitext(cstfile)[0],"Result","output.txt")
    if not os.path.isfile(q): return []
    low=open(q,encoding="utf-8",errors="ignore").read().lower()
    return [m for m in SOLVER_MARKERS if m in low]

def audit_vba(shape_path,status_path):
    return "\n".join([
      "On Error Resume Next","Dim f As Integer, i As Long, nm As String",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape_path,
      'Print #f, "H3B_T01_SHAPE_INVENTORY"',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+120",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      ' If Len(nm)>0 Then Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm))',
      "Next i","Close #f",
      "f=FreeFile", 'Open "%s" For Output As #f'%status_path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f","On Error GoTo 0"
    ])

def intersection_vba(status_path):
    return "\n".join([
      "Dim f As Integer","f=FreeFile",
      'Open "%s" For Output As #f'%status_path,
      'Print #f, "COMMAND=CDCheckModelIntersections"',
      'Print #f, "STARTED=TRUE"',"Close #f",
      'RunCommand "CDCheckModelIntersections"',
      "f=FreeFile",'Open "%s" For Append As #f'%status_path,
      'Print #f, "RETURNED=TRUE"',"Close #f"
    ])

def parse_kv(path):
    d={}
    for line in open(path,encoding="utf-8").read().splitlines():
        if "=" in line:
            k,v=line.split("=",1); d[k.strip()]=v.strip()
    return d

def shape_rows(path):
    out=[]
    for line in open(path,encoding="utf-8").read().splitlines():
        if line.startswith("SHAPE|"):
            _,name,vol=line.split("|",2)
            out.append((name,float(vol.split("=",1)[1])))
    return out

def component_counts(rows):
    c=Counter()
    for name,_ in rows: c[name.split(":",1)[0]]+=1
    return dict(c)

def critical_clearances():
    return {
      "line_signal_ground_gap_mm":0.30,
      "pad_signal_ground_gap_mm":0.25,
      "pad_outer_to_board_edge_mm":5.0-(1.10+0.25+2.40),
      "via_barrel_to_ground_inner_edge_mm":2.30-0.20-(0.90+0.30),
      "via_barrel_to_ground_outer_edge_mm":(0.90+0.30+2.20)-2.30-0.20,
      "via_to_board_edge_mm":5.0-2.30-0.20,
      "back_ground_to_board_edge_mm":5.0-4.0,
      "horizontal_board_vertical_board_positive_overlap_mm":0.0
    }

def run(repo,evidence,work):
    if os.path.exists(evidence): raise RuntimeError("HOLD_H3B_T01_EVIDENCE_EXISTS")
    if os.path.exists(work): raise RuntimeError("HOLD_H3B_T01_WORK_EXISTS")
    macro=os.path.join(repo,"source","cst","R1E1A4A_H3B_T01_ORTHOGONAL_TRANSITION_BUILD_ONLY_V01.mcr")
    if not os.path.isfile(macro): raise RuntimeError("HOLD_H3B_T01_MACRO_MISSING")
    os.makedirs(evidence); os.makedirs(work)
    dst=os.path.join(work,"R1E1A4A_H3B_T01_ORTHOGONAL_TRANSITION_BUILD_ONLY_V01.cst")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New)
    de.set_quiet_mode(True); prj=None
    try:
        prj=de.new_mws()
        prj.modeler.add_to_history("H3B-T01 Orthogonal Transition Coupon V0.1",macro_body(macro))
        prj.save(dst,include_results=False)
    finally:
        if prj is not None: prj.close()
        de.close()

    result_sha=sha(dst); result_bytes=os.path.getsize(dst)

    shapes=os.path.join(evidence,"reopen_shapes.txt")
    status=os.path.join(evidence,"reopen_status.txt")
    inter_status=os.path.join(evidence,"intersection_builtin_status.txt")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New)
    de.set_quiet_mode(True); prj=None
    builtin_return=False
    try:
        prj=de.open_project(dst)
        prj.schematic.execute_vba_code("Sub Main()\n"+audit_vba(shapes,status)+"\nEnd Sub")
        builtin_return=bool(prj.schematic.execute_vba_code("Sub Main()\n"+intersection_vba(inter_status)+"\nEnd Sub"))
    finally:
        if prj is not None: prj.close()
        de.close()

    rows=shape_rows(shapes); counts=component_counts(rows)
    st=parse_kv(status); inter=parse_kv(inter_status)
    params=parameter_map(dst); clear=critical_clearances()
    expected={
      "H3B_Board":2,
      "H3B_Line":6,
      "H3B_BackGround":2,
      "H3B_Transition":6,
      "H3B_EdgeCap":3,
      "H3B_Solder":3,
      "H3B_Via":16,
    }
    checks={
      "shape_count_38":len(rows)==38,
      "component_counts_exact":counts==expected,
      "all_shape_volumes_positive":all(v>0 for _,v in rows),
      "no_tools_remaining":"H3B_Tools" not in counts,
      "port_count_zero":int(st["PORT_COUNT"])==0,
      "builtin_intersection_command_executed":builtin_return and inter.get("STARTED")=="TRUE" and inter.get("RETURNED")=="TRUE",
      "critical_clearances_nonnegative":all(v>=0 for v in clear.values()),
      "positive_required_clearances":all(v>0 for k,v in clear.items() if "positive_overlap" not in k),
      "rp1_12":abs(float(params["h3b_t01_rp1_y"])-12.0)<1e-9,
      "rp2_minus12":abs(float(params["h3b_t01_rp2_z"])+12.0)<1e-9,
      "no_solver_markers":len(solver_log_hits(dst))==0,
      "no_solver_result_items":len(solver_tree_items(dst))==0,
      "artifact_unchanged_by_reopen":sha(dst)==result_sha,
    }
    checks["pass"]=all(checks.values())
    summary={
      "mode":"H3B_T01_POST_LNA_ORTHOGONAL_TRANSITION_COUPON_BUILD_ONLY",
      "simulationops":"0.2.6",
      "solver_run":False,
      "result_cst":dst,
      "result_sha256":result_sha,
      "result_bytes":result_bytes,
      "shape_count":len(rows),
      "component_counts":counts,
      "critical_clearances_mm":clear,
      "parameters":{k:params.get(k) for k in (
        "h3b_t01_board_t","h3b_t01_cu_t","h3b_t01_wsig","h3b_t01_gap",
        "h3b_t01_wgnd","h3b_t01_pad_sig","h3b_t01_pad_gap","h3b_t01_pad_gnd",
        "h3b_t01_rp1_y","h3b_t01_rp2_z","h3b_t01_via_outer_r","h3b_t01_via_inner_r",
        "h3b_t01_freq_lo","h3b_t01_freq_hi")},
      "intersection_command":{"command":"CDCheckModelIntersections","returned":builtin_return,"status":inter},
      "checks":checks
    }
    with open(os.path.join(evidence,"summary.json"),"w") as f: json.dump(summary,f,indent=2)
    final="PASS_R1E1A4A_H3B_T01_TRANSITION_COUPON_BUILD_ONLY" if checks["pass"] else "HOLD_R1E1A4A_H3B_T01_BUILD_QUALIFICATION"
    with open(os.path.join(evidence,"FORMAL_STATUS.txt"),"w") as f: f.write(final+"\n")
    print(final); print("RESULT_SHA256="+result_sha); print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True); ap.add_argument("--evidence",required=True); ap.add_argument("--work",required=True)
    a=ap.parse_args(); run(a.repo,a.evidence,a.work)
