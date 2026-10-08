from __future__ import print_function
import argparse, hashlib, json, shutil, sys, traceback
from collections import Counter
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

HISTORY_LABEL="R4-A0-E1 persistent V03 build"

EXPECTED_NAMES=set([
"E1_Substrate:FR4_COUPON",
"E1_BackGround:LOCAL_BACK_GROUND",
"E1_Signal:UPSTREAM_MSL","E1_Signal:UPSTREAM_TAPER",
"E1_Signal:CIN_UP_PAD","E1_Signal:CIN_DN_PAD","E1_Signal:CIN_TO_RFIN_TAPER",
"E1_PackageLands:PIN1_VBIAS","E1_PackageLands:PIN2_RFIN",
"E1_PackageLands:PIN3_GND","E1_PackageLands:PIN4_GND",
"E1_PackageLands:PIN8_GND","E1_PackageLands:PIN7_RFOUT_VDD",
"E1_PackageLands:PIN6_GND_FDD","E1_PackageLands:PIN5_GND",
"E1_LocalGroundTop:EXPOSED_PADDLE",
"E1_LocalGroundTop:PIN3_SPOKE","E1_LocalGroundTop:PIN4_SPOKE",
"E1_LocalGroundTop:PIN8_SPOKE","E1_LocalGroundTop:PIN6_SPOKE","E1_LocalGroundTop:PIN5_SPOKE",
"E1_Vias:PADDLE_VIA_M","E1_Vias:PADDLE_VIA_C","E1_Vias:PADDLE_VIA_P",
"E1_Signal:RFOUT_TO_COUT_TAPER",
"E1_Signal:COUT_DEV_PAD","E1_Signal:COUT_DN_PAD",
"E1_Bias:L1_RF_PAD","E1_Bias:L1_VDD_PAD","E1_Bias:POUT_TO_L1_FAN",
"E1_Bias:VDD_TRACE","E1_Bias:CRF_VDD_PAD",
"E1_LocalGroundTop:CRF_GND_PAD","E1_Vias:CRF_GROUND_VIA",
"E1_Signal:DOWNSTREAM_TAPER","E1_Signal:DOWNSTREAM_MSL"
])

EXPECTED_COMPONENT_COUNTS={
"E1_Substrate":1,"E1_BackGround":1,"E1_Signal":10,
"E1_PackageLands":8,"E1_LocalGroundTop":7,"E1_Vias":4,"E1_Bias":5
}

EXPECTED_PORTS={
1:(0.0,4.650,0.0,0.0,4.650,-1.0,50.0),
2:(0.0,6.085,0.0,0.0,6.085,-1.0,50.0),
3:(0.0,7.915,0.0,0.0,7.915,-1.0,50.0),
4:(0.0,9.350,0.0,0.0,9.350,-1.0,50.0),
5:(1.45,9.800,0.0,1.45,9.800,-1.0,50.0),
6:(-0.50,6.085,0.0,-0.50,6.085,-1.0,50.0)
}

PAIR_TESTS=[
("VIA_M_vs_FR4","E1_Vias:PADDLE_VIA_M","E1_Substrate:FR4_COUPON"),
("VIA_C_vs_FR4","E1_Vias:PADDLE_VIA_C","E1_Substrate:FR4_COUPON"),
("VIA_P_vs_FR4","E1_Vias:PADDLE_VIA_P","E1_Substrate:FR4_COUPON"),
("CRF_VIA_vs_FR4","E1_Vias:CRF_GROUND_VIA","E1_Substrate:FR4_COUPON"),
("PIN1_vs_PADDLE","E1_PackageLands:PIN1_VBIAS","E1_LocalGroundTop:EXPOSED_PADDLE"),
("PIN2_vs_PADDLE","E1_PackageLands:PIN2_RFIN","E1_LocalGroundTop:EXPOSED_PADDLE"),
("PIN7_vs_PADDLE","E1_PackageLands:PIN7_RFOUT_VDD","E1_LocalGroundTop:EXPOSED_PADDLE"),
("DN_TAPER_vs_CRF_VDD","E1_Signal:DOWNSTREAM_TAPER","E1_Bias:CRF_VDD_PAD"),
("DN_MSL_vs_CRF_GND","E1_Signal:DOWNSTREAM_MSL","E1_LocalGroundTop:CRF_GND_PAD"),
("COUT_DN_vs_L1_VDD","E1_Signal:COUT_DN_PAD","E1_Bias:L1_VDD_PAD")
]

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def wrap(body):
    return "Sub Main()\n"+body+"\nEnd Sub"

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    starts=[i for i,x in enumerate(lines) if x.strip()=="Sub Main()"]
    ends=[i for i,x in enumerate(lines) if x.strip()=="End Sub"]
    if len(starts)!=1 or len(ends)!=1 or ends[0]<=starts[0]:
        raise RuntimeError("HOLD_E1_V03_MACRO_NOT_FLAT_MAIN")
    return "\n".join(lines[starts[0]+1:ends[0]])

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    srcdir=src.with_suffix(""); dstdir=dst.with_suffix("")
    if not srcdir.exists():
        raise RuntimeError("HOLD_E1_SOURCE_COMPANION_MISSING:"+str(srcdir))
    if dstdir.exists(): shutil.rmtree(str(dstdir),ignore_errors=True)
    shutil.copytree(str(srcdir),str(dstdir))

def inventory_vba(shape_path,port_path):
    sp=str(shape_path).replace("\\","/")
    pp=str(port_path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "Dim stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",'Open "%s" For Output As #f'%sp,
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+300",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      "  mat=Solid.GetMaterialNameForShape(nm)",
      '  Print #f, "SHAPE|" & nm & "|material=" & mat & "|volume=" & CStr(Solid.GetVolume(nm))',
      " End If","Next i","Close #f",
      "f=FreeFile",'Open "%s" For Output As #f'%pp,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "For i=1 To 6",
      " Err.Clear",
      " pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P|" & CStr(i) & "|PROP_OK=" & CStr(pok) & "|ERR=" & CStr(Err.Number) & "|TYPE=" & stype & "|ZREF=" & CStr(zref)',
      " Err.Clear",
      " cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "C|" & CStr(i) & "|COORD_OK=" & CStr(cok) & "|ERR=" & CStr(Err.Number) & "|P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0) & "|P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i","Close #f","On Error GoTo 0"])

def intersection_vba(status_path):
    p=str(status_path).replace("\\","/")
    return "\n".join([
      "Dim f As Integer","f=FreeFile",
      'Open "%s" For Output As #f'%p,
      'Print #f, "COMMAND=CDCheckModelIntersections"',
      'Print #f, "STARTED=TRUE"',"Close #f",
      'RunCommand "CDCheckModelIntersections"',
      "f=FreeFile",'Open "%s" For Append As #f'%p,
      'Print #f, "RETURNED=TRUE"',"Close #f"])

def parse_shapes(path):
    rows=[]; meta={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            _,nm,mat,vol=line.split("|",3)
            rows.append({"name":nm,"component":nm.split(":",1)[0],
                         "material":mat.split("=",1)[1],
                         "volume":float(vol.split("=",1)[1])})
        elif "=" in line:
            k,v=line.split("=",1); meta[k]=v
    return rows,meta

def parse_ports(path):
    out={"properties":{},"coordinates":{},"count":None}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("PORT_COUNT="):
            out["count"]=int(line.split("=",1)[1])
        elif line.startswith("P|"):
            p=line.split("|"); idx=int(p[1]); d={}
            for x in p[2:]:
                k,v=x.split("=",1); d[k]=v
            out["properties"][idx]=d
        elif line.startswith("C|"):
            p=line.split("|"); idx=int(p[1]); d={}
            for x in p[2:]:
                k,v=x.split("=",1); d[k]=v
            out["coordinates"][idx]=d
    return out

def parse_xyz(s):
    return tuple(float(x) for x in s.split(","))

def ports_ok(data):
    if data["count"]!=6: return False
    tol=1e-9
    for i,e in EXPECTED_PORTS.items():
        p=data["properties"].get(i,{})
        c=data["coordinates"].get(i,{})
        if p.get("PROP_OK") not in ("True","TRUE","1","-1"): return False
        if c.get("COORD_OK") not in ("True","TRUE","1","-1"): return False
        if abs(float(p.get("ZREF","nan"))-e[6])>tol: return False
        p1=parse_xyz(c["P1"]); p2=parse_xyz(c["P2"])
        if any(abs(a-b)>tol for a,b in zip(p1,e[:3])): return False
        if any(abs(a-b)>tol for a,b in zip(p2,e[3:6])): return False
    return True

def result_tree(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return [x for x in p3.get_tree_items()
                if ("S-Parameters" in x or "Adaptive Meshing" in x or
                    "Convergence" in x or "Power\\Excitation" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+str(ex)]

def pair_zero(source,work,evidence,label,a,b):
    tmp=work/("pair_"+label+".cst")
    out=evidence/("pair_"+label+".txt")
    copy_project(source,tmp)
    body="\n".join([
      "Dim f As Integer, vb As Double, va As Double",
      "f=FreeFile",'Open "%s" For Output As #f'%str(out).replace("\\","/"),
      "On Error Resume Next","Err.Clear",
      'vb=Solid.GetVolume("%s")'%a,
      'Print #f, "BEFORE_A_ERR=" & CStr(Err.Number)',
      'Print #f, "BEFORE_A=" & CStr(vb)',
      "Err.Clear",'Solid.Intersect "%s", "%s"'%(a,b),
      'Print #f, "INTERSECT_ERR=" & CStr(Err.Number)',
      "Err.Clear",'va=Solid.GetVolume("%s")'%a,
      'Print #f, "AFTER_A_ERR=" & CStr(Err.Number)',
      "If Err.Number <> 0 Then",
      ' Print #f, "INTERSECTION_VOLUME=0"',
      " Err.Clear","Else",
      ' Print #f, "INTERSECTION_VOLUME=" & CStr(va)',
      "End If","On Error GoTo 0","Close #f"])
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    err=None
    try:
        p=de.open_project(str(tmp))
        ok=bool(p.schematic.execute_vba_code(wrap(body)))
    except Exception as ex:
        ok=False; err=repr(ex)
    finally:
        if p is not None: p.close()
        de.close()
    kv={}
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if "=" in line:
                k,v=line.split("=",1); kv[k]=v
    ierr=int(kv.get("INTERSECT_ERR","999999"))
    berr=int(kv.get("BEFORE_A_ERR","999999"))
    try: before=float(kv.get("BEFORE_A","nan"))
    except Exception: before=float("nan")
    try: vol=float(kv.get("INTERSECTION_VOLUME","nan"))
    except Exception: vol=float("nan")
    passed=(ok and err is None and berr==0 and before>0 and ierr==0 and abs(vol)<=1e-12)
    try: tmp.unlink()
    except Exception: pass
    td=tmp.with_suffix("")
    if td.exists(): shutil.rmtree(str(td),ignore_errors=True)
    return {"label":label,"a":a,"b":b,"execution_error":err,
            "before_volume_mm3":before,"intersect_err":ierr,
            "intersection_volume_mm3":vol,"pass_zero_overlap":passed}

def main(macro_path,out_path,evidence):
    macro_path=Path(macro_path); out_path=Path(out_path); evidence=Path(evidence)
    work=evidence/"pair_work"
    if not macro_path.exists(): raise RuntimeError("HOLD_E1_V03_MACRO_MISSING")
    if out_path.exists() or out_path.with_suffix("").exists(): raise RuntimeError("HOLD_E1_V03_ARTIFACT_EXISTS")
    if evidence.exists(): raise RuntimeError("HOLD_E1_V03_EVIDENCE_EXISTS")
    evidence.mkdir(parents=True); work.mkdir(parents=True)
    (evidence/"source_macro_sha256.txt").write_text(sha(macro_path)+"\n",encoding="utf-8")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.new_mws()
        p.modeler.add_to_history(HISTORY_LABEL,macro_body(macro_path))
        p.save(str(out_path))
    finally:
        if p is not None: p.close()
        de.close()

    build_sha=sha(out_path)
    shapes=evidence/"reopen_inventory.txt"
    ports=evidence/"reopen_ports.txt"
    inter=evidence/"intersection_builtin_status.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    builtin=False
    try:
        p=de.open_project(str(out_path))
        if not p.schematic.execute_vba_code(wrap(inventory_vba(shapes,ports))):
            raise RuntimeError("HOLD_E1_V03_REOPEN_AUDIT")
        builtin=bool(p.schematic.execute_vba_code(wrap(intersection_vba(inter))))
    finally:
        if p is not None: p.close()
        de.close()

    reopen_sha=sha(out_path)
    rows,_=parse_shapes(shapes)
    pdata=parse_ports(ports)
    names=set(x["name"] for x in rows)
    counts=Counter(x["component"] for x in rows)
    material_ok=all(
      (x["component"]=="E1_Substrate" and x["material"]=="FR4_COST_BASELINE") or
      (x["component"]!="E1_Substrate" and x["material"]=="E1_COPPER")
      for x in rows)
    hist=out_path.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=hist.read_text(encoding="utf-8",errors="replace") if hist.exists() else ""
    history_ok=(HISTORY_LABEL in htext and
                all(('.PortNumber "%d"'%i) in htext for i in range(1,7)) and
                "DiscretePort" in htext and "FR4_COUPON" in htext)

    pairs=[pair_zero(out_path,work,evidence,*x) for x in PAIR_TESTS]
    itext=inter.read_text(encoding="utf-8") if inter.exists() else ""
    checks={
      "history_persistent":history_ok,
      "shape_count_36":len(rows)==36,
      "exact_shape_name_set":names==EXPECTED_NAMES,
      "component_counts_exact":dict(counts)==EXPECTED_COMPONENT_COUNTS,
      "materials_exact":material_ok,
      "ports_exact_6_with_properties_coordinates":ports_ok(pdata),
      "drill_tools_consumed":counts.get("E1_ViaHoleTools",0)==0,
      "result_tree_empty":len(result_tree(out_path))==0,
      "artifact_hash_stable_fresh_reopen":build_sha==reopen_sha,
      "builtin_intersection_command_returned":builtin and "STARTED=TRUE" in itext and "RETURNED=TRUE" in itext,
      "critical_pairwise_zero_overlap":all(x["pass_zero_overlap"] for x in pairs)
    }
    status="PASS_R1E1A4A_AR0_B1R_R4_A0_E1_V03_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_R4_A0_E1_V03_BUILD_ONLY"
    summary={
      "status":status,"simulationops":"0.2.10","formal_builds":1,"solver_invocations":0,
      "macro_path":str(macro_path),"macro_sha256":sha(macro_path),
      "artifact_path":str(out_path),"artifact_sha256":reopen_sha,
      "shape_count":len(rows),"component_counts":dict(counts),
      "port_count":pdata["count"],"port_audit":pdata,
      "history_file":str(hist),"history_persistent":history_ok,
      "critical_pairwise":pairs,"checks":checks}
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    print(status); print("ARTIFACT_SHA256="+reopen_sha)
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--macro",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.macro,a.out,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R4_A0_E1_V03_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
