from __future__ import print_function
import argparse, hashlib, json, shutil, sys, traceback
from collections import Counter
from pathlib import Path

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci
from cst.results import ProjectFile

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
"E1_Substrate":1,
"E1_BackGround":1,
"E1_Signal":10,
"E1_PackageLands":8,
"E1_LocalGroundTop":7,
"E1_Vias":4,
"E1_Bias":5
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
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def wrap(body):
    return "Sub Main()\n"+body+"\nEnd Sub"

def inventory_vba(path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(path).replace("\\","/"),
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+300",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      "  mat=Solid.GetMaterialNameForShape(nm)",
      '  Print #f, "SHAPE|" & nm & "|material=" & mat & "|volume=" & CStr(Solid.GetVolume(nm))',
      " End If",
      "Next i",
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f",
      "On Error GoTo 0"
    ])

def parse_inventory(path):
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

def solver_tree(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return [x for x in p3.get_tree_items()
                if ("S-Parameters" in x or "Adaptive Meshing" in x or
                    "Convergence" in x or "Power\\Excitation" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+str(ex)]

def cleanup_project_copy(p):
    try:
        p.unlink()
    except Exception:
        pass
    d=p.with_suffix("")
    if d.exists():
        shutil.rmtree(str(d),ignore_errors=True)

def pair_zero(source,work,evidence,label,a,b):
    tmp=work/("pair_"+label+".cst")
    out=evidence/("pair_"+label+".txt")
    shutil.copy2(str(source),str(tmp))
    body="\n".join([
      "Dim f As Integer, v As Double",
      "f=FreeFile",
      'Open "%s" For Output As #f'%str(out).replace("\\","/"),
      "On Error Resume Next",
      "Err.Clear",
      'Solid.Intersect "%s", "%s"'%(a,b),
      'Print #f, "INTERSECT_ERR=" & CStr(Err.Number)',
      "Err.Clear",
      'v=Solid.GetVolume("%s")'%a,
      "If Err.Number <> 0 Then",
      ' Print #f, "INTERSECTION_VOLUME=0"',
      " Err.Clear",
      "Else",
      ' Print #f, "INTERSECTION_VOLUME=" & CStr(v)',
      "End If",
      "On Error GoTo 0",
      "Close #f"
    ])
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    err=None
    try:
        prj=de.open_project(str(tmp))
        prj.schematic.execute_vba_code(wrap(body))
    except Exception as ex:
        err=str(ex)
    finally:
        if prj is not None: prj.close()
        de.close()
    kv={}
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if "=" in line:
                k,v=line.split("=",1); kv[k]=v
    ierr=int(kv.get("INTERSECT_ERR","999999"))
    try: vol=float(kv.get("INTERSECTION_VOLUME","nan"))
    except Exception: vol=float("nan")
    ok=(err is None and ierr==0 and abs(vol)<=1e-12)
    cleanup_project_copy(tmp)
    return {"label":label,"a":a,"b":b,"execution_error":err,
            "intersect_err":ierr,"intersection_volume_mm3":vol,
            "pass_zero_overlap":ok}

def main(macro_path,out_path,evidence):
    macro_path=Path(macro_path); out_path=Path(out_path); evidence=Path(evidence)
    work=evidence/"pair_work"
    if not macro_path.exists(): raise RuntimeError("HOLD_E1_MACRO_MISSING")
    if out_path.exists(): raise RuntimeError("HOLD_E1_ARTIFACT_EXISTS")
    if evidence.exists(): raise RuntimeError("HOLD_E1_EVIDENCE_EXISTS")
    evidence.mkdir(parents=True); work.mkdir(parents=True)

    macro_text=macro_path.read_text(encoding="utf-8")
    (evidence/"source_macro_sha256.txt").write_text(sha(macro_path)+"\n",encoding="utf-8")

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.new_mws()
        ok=prj.schematic.execute_vba_code(macro_text)
        if not ok: raise RuntimeError("HOLD_E1_MACRO_EXECUTION")
        prj.save(str(out_path))
    finally:
        if prj is not None: prj.close()
        de.close()

    build_sha=sha(out_path)
    rinv=evidence/"reopen_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out_path))
        if not prj.schematic.execute_vba_code(wrap(inventory_vba(rinv))):
            raise RuntimeError("HOLD_E1_REOPEN_INVENTORY")
    finally:
        if prj is not None: prj.close()
        de.close()

    reopen_sha=sha(out_path)
    rows,meta=parse_inventory(rinv)
    names=set(r["name"] for r in rows)
    counts=Counter(r["component"] for r in rows)
    tree=solver_tree(out_path)
    material_ok=all(
      (r["component"]=="E1_Substrate" and r["material"]=="FR4_COST_BASELINE") or
      (r["component"]!="E1_Substrate" and r["material"]=="E1_COPPER")
      for r in rows
    )

    pairs=[pair_zero(out_path,work,evidence,*x) for x in PAIR_TESTS]

    checks={
      "shape_count_36":len(rows)==36,
      "exact_shape_name_set":names==EXPECTED_NAMES,
      "component_counts_exact":dict(counts)==EXPECTED_COMPONENT_COUNTS,
      "materials_exact":material_ok,
      "port_count_6":int(meta.get("PORT_COUNT","-1"))==6,
      "drill_tool_component_consumed":counts.get("E1_ViaHoleTools",0)==0,
      "result_tree_empty":len(tree)==0,
      "artifact_hash_stable_fresh_reopen":build_sha==reopen_sha,
      "critical_pairwise_zero_overlap":all(x["pass_zero_overlap"] for x in pairs)
    }
    status="PASS_R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_ONLY" if all(checks.values()) else "HOLD_R1E1A4A_AR0_B1R_R4_A0_E1_BUILD_ONLY"

    summary={
      "status":status,
      "simulationops":"0.2.8",
      "formal_builds":1,
      "solver_invocations":0,
      "macro_path":str(macro_path),
      "macro_sha256":sha(macro_path),
      "artifact_path":str(out_path),
      "artifact_sha256":reopen_sha,
      "shape_count":len(rows),
      "component_counts":dict(counts),
      "port_count":int(meta.get("PORT_COUNT","-1")),
      "critical_pairwise":pairs,
      "checks":checks
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    (evidence/"HUMAN_3D_REVIEW.md").write_text(
      "# R4-A0-E1 Human 3D Review\n\n"
      "Inspect before any solve authorization:\n"
      "1. top full 4-mm x 10-mm coupon;\n"
      "2. pin lands + exposed paddle + 3 plated vias;\n"
      "3. input DC-block launch;\n"
      "4. pin7 / C_OUT / L1 fan;\n"
      "5. C_RF and dedicated ground via;\n"
      "6. bottom local ground;\n"
      "7. cross-section through all via barrels and drilled FR4;\n"
      "8. six port segments through FR4 only.\n\n"
      "If the 4-mm active-region width looks mechanically/electrically cramped, HOLD and widen it; do not shrink vendor lands.\n",
      encoding="utf-8")
    print(status)
    print("ARTIFACT_SHA256="+reopen_sha)
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
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R4_A0_E1_EXECUTION_EXCEPTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
