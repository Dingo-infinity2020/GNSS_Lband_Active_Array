"""R1A3 materialized FR4 BUILD-ONLY harness for NW/DC."""
import argparse, hashlib, json, os, sys

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(65536),b""):
            h.update(c)
    return h.hexdigest()

def body(path):
    lines=open(path,"r",encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=e=None
    for i,l in enumerate(lines):
        if l.strip()=="Sub Main()": s=i
        elif l.strip()=="End Sub": e=i
    if s is None or e is None or e<=s:
        raise RuntimeError("macro markers")
    return "\n".join(lines[s+1:e])

def inv(shape,param):
    return "\n".join([
      "On Error Resume Next","Dim f As Integer","Dim i As Long","Dim nm As String",
      "f=FreeFile", 'Open "%s" For Output As #f'%shape,
      'Print #f, "R1A3_SHAPE_INVENTORY"',
      'Print #f, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
      "For i=0 To Solid.GetNumberOfShapes()+10",
      " nm=Solid.GetNameOfShapeFromIndex(i)",
      " If Len(nm)>0 Then",
      '  Print #f, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm)) & "|area=" & CStr(Solid.GetArea(nm))',
      " End If","Next i","Close #f",
      "f=FreeFile", 'Open "%s" For Output As #f'%param,
      'Print #f, "R1A3_PARAMETER_INVENTORY"',
      'Print #f, "PARAM_COUNT=" & CStr(GetNumberOfParameters())',
      "For i=1 To GetNumberOfParameters()",
      ' Print #f, "PARAM|" & GetParameterName(i) & "|" & GetParameterSValue(i) & "|" & CStr(GetParameterNValue(i))',
      "Next i","Close #f","On Error GoTo 0"])

def shot(view,path):
    return 'Plot.RestoreView "%s"\nPlot.ZoomToStructure\nPlot.Update\nPlot.ExportImage "%s", 1800, 1400'%(view,path)

def parse_shapes(path):
    return [line for line in open(path,encoding="utf-8").read().splitlines() if line.startswith("SHAPE|")]

def run(repo,ev,work):
    os.makedirs(ev,exist_ok=True)
    os.makedirs(work,exist_ok=True)
    macro=os.path.join(repo,"source","cst","R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr")
    cst=os.path.join(work,"R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst")
    log=["MACRO_SHA256="+sha(macro)]

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.new_mws()
        prj.modeler.add_to_history("R1A3 materialized FR4 build-only",body(macro))
        prj.save(cst)
        log.append("BUILD_SAVE_PASS")
    finally:
        if prj is not None: prj.close()
        de.close()

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(cst)
        prj.modeler.add_to_history("inventory",inv(os.path.join(ev,"object_inventory.txt"),os.path.join(ev,"parameter_inventory.txt")))
        prj.modeler.add_to_history("top",shot("Front",os.path.join(ev,"top_view.png")))
        prj.modeler.add_to_history("persp",shot("Perspective",os.path.join(ev,"oblique_view.png")))
        log.append("EVIDENCE_PASS")
    finally:
        if prj is not None: prj.close()
        de.close()

    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.open_project(cst)
        prj.modeler.add_to_history("reopen inventory",inv(os.path.join(ev,"reopen_object_inventory.txt"),os.path.join(ev,"reopen_parameter_inventory.txt")))
        prj.modeler.add_to_history("reopen shot",shot("Perspective",os.path.join(ev,"view_after_reopen.png")))
        log.append("REOPEN_PASS")
    finally:
        if prj is not None: prj.close()
        de.close()

    shapes=parse_shapes(os.path.join(ev,"object_inventory.txt"))
    reopen=parse_shapes(os.path.join(ev,"reopen_object_inventory.txt"))
    residue=[x for x in shapes if "SlotTools:" in x or "CopperGapTools:" in x]
    checks={
      "ground": any("UnitCellGround:UNITCELL_GROUND_REFERENCE" in x for x in shapes),
      "substrate": any("Substrate:FR4_BOARD" in x for x in shapes),
      "top_copper": any("TopCopper:" in x for x in shapes),
      "no_tool_residue": len(residue)==0,
      "fresh_reopen_same": shapes==reopen,
    }
    checks["pass"]=all(checks.values())
    summary={
      "cst":cst,"cst_sha256":sha(cst),"cst_bytes":os.path.getsize(cst),
      "macro_sha256":sha(macro),"shape_count":len(shapes),"checks":checks,
      "tool_residue":residue,"log":log,"manual_review_required":True,
    }
    open(os.path.join(ev,"harness_summary.json"),"w").write(json.dumps(summary,indent=2))
    open(os.path.join(ev,"harness_log.txt"),"w").write("\n".join(log)+"\n")
    print("PASS_R1A3_BUILD_ONLY_AWAITING_HUMAN_REVIEW" if checks["pass"] else "HOLD_R1A3_RUNTIME_AUDIT")
    print("CST_PATH="+cst)
    print("CST_SHA256="+summary["cst_sha256"])
    print("CST_BYTES="+str(summary["cst_bytes"]))
    print("SHAPE_COUNT="+str(summary["shape_count"]))
    print(json.dumps(checks,sort_keys=True))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    a=ap.parse_args()
    run(a.repo,a.evidence,a.work)
