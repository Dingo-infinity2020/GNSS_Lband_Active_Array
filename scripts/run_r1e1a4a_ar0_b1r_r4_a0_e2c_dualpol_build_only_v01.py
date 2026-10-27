from __future__ import print_function
import argparse, hashlib, json, math, shutil, sys, traceback
from collections import Counter
from pathlib import Path

def _simops_emit(obj):
    print("SIMOPS_EVENT "+json.dumps(obj,separators=(",",":")),flush=True)

def simops_phase(phase,state,production_boundary,current=None,total=None,message=None):
    obj={"schema_version":"simops-project-event-v0.1","event":"PHASE",
         "phase":str(phase),"state":str(state),"production_boundary":str(production_boundary)}
    if current is not None: obj["current"]=int(current)
    if total is not None: obj["total"]=int(total)
    if message: obj["message"]=str(message)
    _simops_emit(obj)


# CST interpreter/environment is supplied by the runtime execution route.
# Project source intentionally contains no host-global CST installation path.
import cst.interface as ci
from cst.results import ProjectFile

# V02 recovery changes audit semantics only. Production geometry/macro/inventory are unchanged.
# The analytic pi*r^2*h drill-volume equality is diagnostic only; the hard gate compares
# against a CST/ACIS-native kernel reference generated from the same canonical parent.
PARENT_SHA="fbf375c605acff4f53e46fedefba7acf24ef871b427a579091144b7833dd149e"
HISTORY_LABEL="R4-A0-E2C dual-pol coexistence four-E1 V01"
REFERENCE_HISTORY_LABEL="R4-A0-E2C 16-via CST-native drill kernel reference V01"
S2=1.0/math.sqrt(2.0)
Z0=57.1428571428

PARENT_COMPONENT_COUNTS={
 "UnitCellGround":1,"Substrate":1,"TopCopper":1,"B0_Stalk":4,"B0_MSL":4,"B0_LNAEnvelope":4,
 "B1M_LowerStalk":2,"B1M_UpperRail":4,"B1M_TopTenon":4,"B1M_BottomTenon":4,
 "B1RT0_RFTenon":4,"B1RT0_TongueCu":4,"B1RT0_Solder":4,"B1RT1R1_BackGround":4
}

PORT_LOCAL={
 1:(3.0,4.650),2:(3.0,6.085),3:(3.0,7.915),4:(3.0,9.350),5:(4.45,9.800),6:(2.50,6.085),
 7:(-3.0,4.650),8:(-3.0,6.085),9:(-3.0,7.915),10:(-3.0,9.350),11:(-1.55,9.800),12:(-3.50,6.085),
 13:(3.0,4.650),14:(3.0,6.085),15:(3.0,7.915),16:(3.0,9.350),17:(4.45,9.800),18:(2.50,6.085),
 19:(-3.0,4.650),20:(-3.0,6.085),21:(-3.0,7.915),22:(-3.0,9.350),23:(-1.55,9.800),24:(-3.50,6.085)
}

MODIFIED_PARENT={"B0_Stalk:A_P_PRONG","B0_Stalk:A_N_PRONG","B0_Stalk:B_P_PRONG","B0_Stalk:B_N_PRONG"}

def sha(path):
    h=hashlib.sha256()
    with open(str(path),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def wrap(body):
    return "Sub Main()\n"+body+"\nEnd Sub"

def macro_body(path):
    lines=Path(path).read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    s=e=None
    for i,line in enumerate(lines):
        if line.strip()=="Sub Main()": s=i
        elif line.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("HOLD_E2C_MACRO_MARKERS")
    return "\n".join(lines[s+1:e])

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    srcdir=src.with_suffix(""); dstdir=dst.with_suffix("")
    if not srcdir.exists():
        raise RuntimeError("HOLD_E2C_SOURCE_COMPANION_MISSING:"+str(srcdir))
    if dstdir.exists():
        shutil.rmtree(str(dstdir),ignore_errors=True)
    shutil.copytree(str(srcdir),str(dstdir))

def inventory_vba(path):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Long, nm As String, mat As String",
      "f=FreeFile",
      'Open "'+p+'" For Output As #f',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+1200",
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

def named_inventory_vba(path,names,file_mode="Output"):
    p=str(path).replace("\\","/")
    if file_mode not in ("Output","Append"):
        raise RuntimeError("HOLD_E2C_INVENTORY_FILE_MODE")
    lines=[
      "On Error Resume Next",
      "Dim f As Integer, nm As String, mat As String, v As Double",
      "f=FreeFile",
      'Open "'+p+'" For '+file_mode+' As #f',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())'
    ]
    for name in names:
        q=str(name).replace('"','""')
        lines += [
          'nm="'+q+'"',
          "Err.Clear",
          "v=Solid.GetVolume(nm)",
          "If Err.Number <> 0 Then",
          ' Print #f, "MISSING|" & nm',
          " Err.Clear",
          "Else",
          " mat=Solid.GetMaterialNameForShape(nm)",
          ' Print #f, "SHAPE|" & nm & "|material=" & mat & "|volume=" & CStr(v)',
          "End If"
        ]
    lines += [
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f",
      "On Error GoTo 0"
    ]
    return "\n".join(lines)


def run_named_inventory(prj,path,names,phase=None,boundary="NOT_OBSERVED",batch_size=4):
    names=list(names)
    if not names:
        raise RuntimeError("HOLD_E2C_INVENTORY_EMPTY_NAMES")
    if batch_size < 1:
        raise RuntimeError("HOLD_E2C_INVENTORY_BAD_BATCH_SIZE")
    total=len(names)
    for start in range(0,total,batch_size):
        end=min(start+batch_size,total)
        chunk=names[start:end]
        body=named_inventory_vba(path,chunk,file_mode=("Output" if start==0 else "Append"))
        if not prj.schematic.execute_vba_code(wrap(body)):
            return False
        if phase:
            simops_phase(phase,"PROGRESS",boundary,current=end,total=total,
                         message="inventory batch complete")
    return True

def ports_vba(path):
    p=str(path).replace("\\","/")
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Integer, stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",
      'Open "'+p+'" For Output As #f',
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "For i=1 To 24",
      " Err.Clear",
      " pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P|" & CStr(i) & "|PROP_OK=" & CStr(pok) & "|ERR=" & CStr(Err.Number) & "|TYPE=" & stype & "|ZREF=" & CStr(zref)',
      " Err.Clear",
      " cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "C|" & CStr(i) & "|COORD_OK=" & CStr(cok) & "|ERR=" & CStr(Err.Number) & "|P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0) & "|P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i",
      "Close #f",
      "On Error GoTo 0"
    ])

def parse_inventory(path):
    rows=[]; kv={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("SHAPE|"):
            _,nm,mat,vol=line.split("|",3)
            rows.append({"name":nm,"component":nm.split(":",1)[0],
                         "material":mat.split("=",1)[1],
                         "volume":float(vol.split("=",1)[1])})
        elif "=" in line:
            k,v=line.split("=",1); kv[k]=v
    return rows,kv

def parse_ports(path):
    out={"count":None,"properties":{},"coordinates":{}}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("PORT_COUNT="):
            out["count"]=int(line.split("=",1)[1])
        elif line.startswith("P|"):
            parts=line.split("|"); idx=int(parts[1]); d={}
            for x in parts[2:]:
                k,v=x.split("=",1); d[k]=v
            out["properties"][idx]=d
        elif line.startswith("C|"):
            parts=line.split("|"); idx=int(parts[1]); d={}
            for x in parts[2:]:
                k,v=x.split("=",1); d[k]=v
            out["coordinates"][idx]=d
    return out

def xyz(s):
    return tuple(float(x) for x in s.split(","))

def expected_port(i):
    u,v=PORT_LOCAL[i]
    if i<=12:
        p1=(S2*u,S2*u,Z0-v)
        p2=(S2*(u+1.0),S2*(u-1.0),Z0-v)
    else:
        p1=(-S2*u,S2*u,Z0-v)
        p2=(S2*(1.0-u),S2*(u+1.0),Z0-v)
    return p1,p2

def ports_exact(data,tol=2e-8):
    if data["count"]!=24:
        return False
    for i in range(1,25):
        p=data["properties"].get(i,{})
        cc=data["coordinates"].get(i,{})
        if p.get("PROP_OK") not in ("True","TRUE","1","-1"): return False
        if cc.get("COORD_OK") not in ("True","TRUE","1","-1"): return False
        if p.get("TYPE")!="SParameter": return False
        if abs(float(p.get("ZREF","nan"))-50.0)>tol: return False
        a,b=expected_port(i)
        if any(abs(x-y)>tol for x,y in zip(xyz(cc["P1"]),a)): return False
        if any(abs(x-y)>tol for x,y in zip(xyz(cc["P2"]),b)): return False
    return True

def solver_tree(cst):
    try:
        p3=ProjectFile(str(cst),allow_interactive=True).get_3d()
        return [x for x in p3.get_tree_items()
                if ("S-Parameters" in x or "Convergence" in x or "Adaptive Meshing" in x or "Power\\Excitation" in x)]
    except Exception as ex:
        return ["RESULT_API_ERROR:"+str(ex)]

def signature(rows,names):
    return {r["name"]:(r["material"],round(r["volume"],12)) for r in rows if r["name"] in names}

def rowmap(rows):
    return {r["name"]:r for r in rows}

def whole_model_check(cst,out):
    p=str(out).replace("\\","/")
    body="\n".join([
      "On Error Resume Next",
      "Dim f As Integer",
      "f=FreeFile",
      'Open "'+p+'" For Output As #f',
      "Err.Clear",
      'RunCommand "CDCheckModelIntersections"',
      'Print #f, "COMMAND_ERR=" & CStr(Err.Number)',
      "Close #f",
      "On Error GoTo 0"
    ])
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(cst))
        ok=bool(prj.schematic.execute_vba_code(wrap(body)))
    finally:
        if prj is not None: prj.close()
        de.close()
    return ok

def parse_kv(path):
    out={}
    if not Path(path).exists(): return out
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k]=v
    return out

def pair_one(source,tmp,out,a,b):
    copy_project(source,tmp)
    p=str(out).replace("\\","/")
    body="\n".join([
      "Dim f As Integer, v As Double",
      "f=FreeFile",
      'Open "'+p+'" For Output As #f',
      "On Error Resume Next",
      "Err.Clear",
      'Print #f, "A_BEFORE=" & CStr(Solid.GetVolume("'+a+'"))',
      'Print #f, "B_BEFORE=" & CStr(Solid.GetVolume("'+b+'"))',
      "Err.Clear",
      'Solid.Intersect "'+a+'", "'+b+'"',
      'Print #f, "INTERSECT_ERR=" & CStr(Err.Number)',
      "Err.Clear",
      'v=Solid.GetVolume("'+a+'")',
      "If Err.Number <> 0 Then",
      ' Print #f, "A_EXISTS_AFTER=0"',
      ' Print #f, "INTERSECTION_VOLUME=0"',
      " Err.Clear",
      "Else",
      ' Print #f, "A_EXISTS_AFTER=1"',
      ' Print #f, "INTERSECTION_VOLUME=" & CStr(v)',
      "End If",
      "On Error GoTo 0",
      "Close #f"
    ])
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(tmp))
        prj.schematic.execute_vba_code(wrap(body))
    finally:
        if prj is not None: prj.close()
        de.close()
    kv=parse_kv(out)
    err=int(kv.get("INTERSECT_ERR","999999"))
    vol=float(kv.get("INTERSECTION_VOLUME","nan"))
    return {"a":a,"b":b,"intersect_err":err,"intersection_volume_mm3":vol,
            "pass_zero_overlap":(err==0 and abs(vol)<=1e-12)}

def cleanup_project(p):
    p=Path(p)
    try: p.unlink()
    except Exception: pass
    d=p.with_suffix("")
    if d.exists(): shutil.rmtree(str(d),ignore_errors=True)

def kernel_reference(parent,reference_macro,parent_rows,evidence):
    ref=evidence/"kernel_reference_preflight.cst"
    inv=evidence/"kernel_reference_inventory.txt"
    if ref.exists() or ref.with_suffix("").exists():
        raise RuntimeError("HOLD_E2C_KERNEL_REFERENCE_EXISTS")
    copy_project(parent,ref)
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(ref))
        prj.modeler.add_to_history(REFERENCE_HISTORY_LABEL,macro_body(reference_macro))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()

    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(ref))
        if not run_named_inventory(prj,inv,sorted(parent_rows),phase="kernel_reference",boundary="NOT_OBSERVED"):
            raise RuntimeError("HOLD_E2C_KERNEL_REFERENCE_INVENTORY")
    finally:
        if prj is not None: prj.close()
        de.close()

    rows,kv=parse_inventory(inv)
    rm=rowmap(rows)
    hist=ref.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=hist.read_text(encoding="utf-8",errors="replace") if hist.exists() else ""
    losses={n:parent_rows[n]["volume"]-rm[n]["volume"] for n in sorted(MODIFIED_PARENT)}
    checks={
      "shape_count_45":len(rows)==45,
      "port_count_zero":int(kv.get("PORT_COUNT","-1"))==0,
      "tool_components_consumed":not any("E2C_REF_" in r["component"] for r in rows),
      "history_persistent":REFERENCE_HISTORY_LABEL in htext,
      "result_tree_empty":len(solver_tree(ref))==0,
      "polA_branch_losses_symmetric":abs(losses["B0_Stalk:A_P_PRONG"]-losses["B0_Stalk:A_N_PRONG"])<=1e-9,
      "polB_branch_losses_symmetric":abs(losses["B0_Stalk:B_P_PRONG"]-losses["B0_Stalk:B_N_PRONG"])<=1e-9,
      "four_prong_losses_present":len(losses)==4,
      "positive_drill_loss":all(v>0 for v in losses.values())
    }
    result={
      "classification":"CST_ACIS_KERNEL_REFERENCE_ON_DISPOSABLE_COMPLETE_PROJECT_COPY",
      "formal_build_invocations":0,
      "solver_invocations":0,
      "reference_macro":str(reference_macro),
      "reference_macro_sha256":sha(reference_macro),
      "prong_loss_mm3":losses,
      "checks":checks
    }
    (evidence/"kernel_reference_summary.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    cleanup_project(ref)
    if not all(checks.values()):
        raise RuntimeError("HOLD_E2C_KERNEL_REFERENCE_GATE")
    return losses

def coexistence_contract(contract):
    bp=contract["interference"]["source_broadphase"]
    return {
      "a_solid_count":72,
      "b_solid_count":72,
      "all_cross_pairs":72*72,
      "broadphase_candidate_count":len(bp["candidate_pairs"]),
      "registered_pairwise_count":len(contract["interference"]["registered_pairs"]),
      "positive_volume_crosspol_contact_allowed":False,
      "polB_half_lap_notch_frozen":bool(contract["coexistence"]["polB_half_lap_notch_frozen"])
    }

def main(parent,macro,reference_macro,inventory_contract,out,review_copy,evidence):
    parent=Path(parent); macro=Path(macro); reference_macro=Path(reference_macro); inventory_contract=Path(inventory_contract)
    out=Path(out); review_copy=Path(review_copy); evidence=Path(evidence)

    if not parent.exists() or sha(parent)!=PARENT_SHA:
        raise RuntimeError("HOLD_E2C_PARENT_HASH")
    if not parent.with_suffix("").exists():
        raise RuntimeError("HOLD_E2C_PARENT_COMPANION_MISSING")
    if out.exists() or out.with_suffix("").exists():
        raise RuntimeError("HOLD_E2C_DEST_EXISTS")
    if evidence.exists():
        raise RuntimeError("HOLD_E2C_EVIDENCE_EXISTS")
    if not macro.exists() or not reference_macro.exists() or not inventory_contract.exists():
        raise RuntimeError("HOLD_E2C_SOURCE_MISSING")

    contract=json.loads(inventory_contract.read_text(encoding="utf-8"))
    expected_final=set(contract["expected_final_names"])
    expected_removed=set(contract["removed_parent_objects"])
    expected_preserved=set(contract["preserved_parent_objects"])
    expected_counts=contract["expected_final_component_counts"]

    simops_phase("parent_inventory","START","NOT_OBSERVED",message="copy/open/inventory canonical parent")
    evidence.mkdir(parents=True)
    copy_project(parent,out)
    if sha(out)!=PARENT_SHA:
        raise RuntimeError("HOLD_E2C_PARENT_COPY_HASH")

    pinv=evidence/"parent_inventory.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not run_named_inventory(prj,pinv,sorted(expected_removed|expected_preserved),phase="parent_inventory",boundary="NOT_OBSERVED"):
            raise RuntimeError("HOLD_E2C_PARENT_INVENTORY")
    finally:
        if prj is not None: prj.close()
        de.close()

    prows,pkv=parse_inventory(pinv)
    pnames=set(r["name"] for r in prows)
    pcounts=Counter(r["component"] for r in prows)
    parent_checks={
      "shape_count_45":len(prows)==45,
      "component_counts_exact":dict(pcounts)==PARENT_COMPONENT_COUNTS,
      "removed_objects_all_present":expected_removed.issubset(pnames),
      "preserved_objects_all_present":expected_preserved.issubset(pnames),
      "port_count_zero":int(pkv.get("PORT_COUNT","-1"))==0,
      "result_tree_empty":len(solver_tree(out))==0,
    }
    if not all(parent_checks.values()):
        (evidence/"parent_gate.json").write_text(json.dumps(parent_checks,indent=2)+"\n",encoding="utf-8")
        simops_phase("parent_inventory","HOLD","NOT_OBSERVED",message="parent gate failed")
        raise RuntimeError("HOLD_E2C_PARENT_GATE")
    simops_phase("parent_inventory","PASS","NOT_OBSERVED")

    parent_rows=rowmap(prows)
    preserve_exact_names=expected_preserved-MODIFIED_PARENT
    parent_sig=signature(prows,preserve_exact_names)

    # Tooling preflight only: measure CST/ACIS-native loss for the exact eight drill primitives
    # on a disposable complete-project copy of the canonical parent. This is not a formal
    # production build and occurs before the frozen E2C production History is executed.
    simops_phase("kernel_reference","START","NOT_OBSERVED",message="CST-native 16-via drill reference")
    kernel_ref_loss=kernel_reference(parent,reference_macro,parent_rows,evidence)
    simops_phase("kernel_reference","PASS","NOT_OBSERVED")

    simops_phase("production_open","START","NOT_OBSERVED")
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        simops_phase("production_open","PASS","NOT_OBSERVED")
        simops_phase("production_build","START","OBSERVED",message="frozen E2C History insertion boundary")
        prj.modeler.add_to_history(HISTORY_LABEL,macro_body(macro))
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()
    simops_phase("production_build","PASS","OBSERVED")

    build_sha=sha(out)
    simops_phase("fresh_reopen","START","OBSERVED")
    rinv=evidence/"reopen_inventory.txt"; rports=evidence/"reopen_ports.txt"
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(str(out))
        if not run_named_inventory(prj,rinv,sorted(expected_final),phase="fresh_reopen",boundary="OBSERVED"):
            raise RuntimeError("HOLD_E2C_REOPEN_INVENTORY")
        if not prj.schematic.execute_vba_code(wrap(ports_vba(rports))):
            raise RuntimeError("HOLD_E2C_REOPEN_PORTS")
    finally:
        if prj is not None: prj.close()
        de.close()

    rows,kv=parse_inventory(rinv); pdata=parse_ports(rports)
    simops_phase("fresh_reopen","PASS","OBSERVED")
    names=set(r["name"] for r in rows)
    counts=Counter(r["component"] for r in rows)
    rm=rowmap(rows)
    post_sig=signature(rows,preserve_exact_names)

    via_names=[n for n in names if (
        n.startswith("E2C_A_P_Vias:") or n.startswith("E2C_A_N_Vias:") or
        n.startswith("E2C_B_P_Vias:") or n.startswith("E2C_B_N_Vias:")
    )]
    via_target=math.pi*(0.175**2-0.125**2)*1.07
    via_volumes=[rm[n]["volume"] for n in via_names]

    analytic_drill_loss=16.0*math.pi*(0.175**2)*1.0
    prong_loss={}
    for n in sorted(MODIFIED_PARENT):
        prong_loss[n]=parent_rows[n]["volume"]-rm[n]["volume"]

    hist=out.with_suffix("")/"Model"/"3D"/"Model.mod"
    htext=hist.read_text(encoding="utf-8",errors="replace") if hist.exists() else ""

    tree=solver_tree(out)
    basic_checks={
      "shape_count_177":len(rows)==177,
      "exact_shape_name_set":names==expected_final,
      "component_counts_exact":dict(counts)==expected_counts,
      "preserved_parent_signature_exact":parent_sig==post_sig,
      "removed_parent_objects_absent":len(names.intersection(expected_removed))==0,
      "tool_components_consumed":not any("ViaHoleTools" in r["component"] for r in rows),
      "sixteen_vias":len(via_names)==16,
      "via_volumes_exact":len(via_volumes)==16 and max(abs(v-via_target) for v in via_volumes)<=1e-7,
      "four_prong_drill_loss_matches_cst_kernel_reference":all(abs(prong_loss[n]-kernel_ref_loss[n])<=1e-7 for n in prong_loss),
      "ports_exact_24":ports_exact(pdata),
      "history_persistent":HISTORY_LABEL in htext and all(('.PortNumber "%d"'%i) in htext for i in range(1,25)),
      "result_tree_empty":len(tree)==0,
      "fresh_reopen_hash_stable":sha(out)==build_sha,
      "all_positive_volume":all(r["volume"]>0 for r in rows),
    }

    simops_phase("whole_model_intersection","START","OBSERVED")
    whole=evidence/"whole_model_intersection.txt"
    whole_ok=whole_model_check(out,whole)
    whole_kv=parse_kv(whole)
    basic_checks["builtin_intersection_command_returned"]=whole_ok and int(whole_kv.get("COMMAND_ERR","999999"))==0
    basic_checks["artifact_hash_stable_after_builtin_check"]=sha(out)==build_sha
    simops_phase("whole_model_intersection","PASS","OBSERVED")

    simops_phase("pairwise","START","OBSERVED",current=0,total=len(contract["interference"]["registered_pairs"]))
    pair_root=evidence/"pair_work"; pair_root.mkdir()
    pair_results=[]
    for idx,(a,b) in enumerate(contract["interference"]["registered_pairs"],start=1):
        tmp=pair_root/("pair_%02d.cst"%idx)
        txt=evidence/("pair_%02d.txt"%idx)
        try:
            pair_results.append(pair_one(out,tmp,txt,a,b))
        except Exception as ex:
            pair_results.append({"a":a,"b":b,"error":repr(ex),"pass_zero_overlap":False})
        finally:
            cleanup_project(tmp)
        simops_phase("pairwise","PROGRESS","OBSERVED",current=idx,total=len(contract["interference"]["registered_pairs"]))
    pair_pass=all(x.get("pass_zero_overlap",False) for x in pair_results)
    basic_checks["registered_pairwise_zero_overlap"]=pair_pass
    basic_checks["artifact_hash_stable_after_pairwise"]=sha(out)==build_sha
    simops_phase("pairwise","PASS","OBSERVED",current=len(pair_results),total=len(contract["interference"]["registered_pairs"]))

    coexist=coexistence_contract(contract)
    basic_checks["broadphase_candidate_count_exact"]=coexist["broadphase_candidate_count"]==1
    basic_checks["registered_pair_count_29"]=coexist["registered_pairwise_count"]==29
    basic_checks["a_b_positive_volume_contact_forbidden"]=not coexist["positive_volume_crosspol_contact_allowed"]
    basic_checks["polB_half_lap_notch_frozen"]=coexist["polB_half_lap_notch_frozen"]

    status=("PASS_R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_ONLY"
            if all(basic_checks.values())
            else "HOLD_R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_ONLY")

    summary={
      "status":status,
      "simulationops":"0.2.17",
      "formal_build_invocations":1,
      "solver_invocations":0,
      "parent":{"path":str(parent),"sha256":PARENT_SHA,"checks":parent_checks},
      "sources":{
        "macro":str(macro),"macro_sha256":sha(macro),
        "inventory_contract":str(inventory_contract),"inventory_contract_sha256":sha(inventory_contract)
      },
      "artifact":{"path":str(out),"sha256":sha(out),"build_sha256":build_sha},
      "shape_count":len(rows),
      "component_counts":dict(counts),
      "port_count":pdata["count"],
      "device_plane_ports":[2,3,8,9,14,15,20,21],
      "via_volumes_mm3":via_volumes,
      "expected_via_volume_mm3":via_target,
      "four_prong_volume_loss_mm3":prong_loss,
      "cst_kernel_reference_prong_loss_mm3":kernel_ref_loss,
      "analytic_prong_drill_loss_mm3_diagnostic_only":analytic_drill_loss,
      "prong_loss_minus_kernel_reference_mm3":{n:prong_loss[n]-kernel_ref_loss[n] for n in prong_loss},
      "whole_model_intersection":whole_kv,
      "pairwise_results":pair_results,
      "coexistence_contract":coexist,
      "checks":basic_checks,
      "human_review_required":True,
      "interpretation":"BUILD-only geometry/persistence qualification; no RF-layout or solve qualification."
    }
    (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    (evidence/"FINAL_STATUS.txt").write_text(status+"\n",encoding="utf-8")
    review=[
      "# R4-A0-E2C Dual-Pol Coexistence Build Human Review","",
      "Automated status: "+status,"",
      "Inspect a review copy; do not save over the protected canonical artifact.",
      "1. Verify all four frozen E1 landing zones are simultaneously present.",
      "2. Verify Pol-A geometry matches E2A and Pol-B geometry matches E2B; no RF retune.",
      "3. Verify all 16 vias pass through their intended A_P/A_N/B_P/B_N FR4 prongs.",
      "4. Verify the frozen Pol-B N-backside-ground half-lap notch is present.",
      "5. Verify no A/B local-ground, package-land, signal or via conductor has an unplanned galvanic bridge.",
      "6. Inspect the one source-AABB broadphase candidate: A_P backside ground vs B_N backside ground.",
      "7. Verify old B0 full-length MSL/LNA-envelope and T1R1 ground-taper objects are absent.",
      "8. Verify 24 raw ports are on intended E_UP/P_IN/P_OUT/E_DN/B_VDD/B_VBIAS planes.",
      "9. No D2 remote common-ground structure may appear.","",
      "Human PASS is geometry/assembly sanity only; it is not active-circuit or solve authorization.",
      "No solver is authorized by this build stage."
    ]
    (evidence/"HUMAN_3D_REVIEW.md").write_text("\n".join(review)+"\n",encoding="utf-8")

    review_copy=Path(review_copy)
    review_record=None
    if status.startswith("PASS_"):
        simops_phase("review_copy","START","OBSERVED")
        if review_copy.exists() or review_copy.with_suffix("").exists():
            raise RuntimeError("HOLD_E2C_REVIEW_COPY_TARGET_EXISTS:"+str(review_copy))
        copy_project(out,review_copy)
        review_sha=sha(review_copy)
        if review_sha!=sha(out):
            raise RuntimeError("HOLD_E2C_REVIEW_COPY_SHA_MISMATCH")
        if not review_copy.with_suffix("").exists():
            raise RuntimeError("HOLD_E2C_REVIEW_COPY_COMPANION_MISSING")
        review_record={
          "path":str(review_copy),
          "sha256":review_sha,
          "companion_path":str(review_copy.with_suffix("")),
          "complete_project_copy":True
        }
        summary["review_copy"]=review_record
        (evidence/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
        simops_phase("review_copy","PASS","OBSERVED")
    simops_phase("complete","PASS" if status.startswith("PASS_") else "HOLD","OBSERVED",message=status)

    print(status)
    print("ARTIFACT_SHA256="+sha(out))
    if review_record:
        print("REVIEW_COPY_SHA256="+review_record["sha256"])
    print("PAIRWISE_PASS=%s"%pair_pass)
    return 0 if status.startswith("PASS_") else 4

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--parent-cst",required=True)
    ap.add_argument("--macro",required=True)
    ap.add_argument("--kernel-reference-macro",required=True)
    ap.add_argument("--inventory-contract",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--review-copy",required=True)
    ap.add_argument("--evidence",required=True)
    a=ap.parse_args()
    try:
        sys.exit(main(a.parent_cst,a.macro,a.kernel_reference_macro,a.inventory_contract,a.out,a.review_copy,a.evidence))
    except Exception:
        Path(a.evidence).mkdir(parents=True,exist_ok=True)
        Path(a.evidence,"EXCEPTION.txt").write_text(traceback.format_exc(),encoding="utf-8")
        Path(a.evidence,"FINAL_STATUS.txt").write_text("HOLD_R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_EXECUTION\n",encoding="utf-8")
        traceback.print_exc()
        sys.exit(9)
