"""R1A1 CHARTS scaled-aperture BUILD-ONLY harness for NW/DC.

No ports, monitors or solver. Produces build/reopen evidence only.
"""

from __future__ import annotations
import argparse, hashlib, json, os, sys

LIBS = r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0, LIBS)
import cst.interface as ci

def sha256(path):
    if not os.path.exists(path): return "MISSING"
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(65536),b""): h.update(chunk)
    return h.hexdigest()

def read_body(path):
    txt=open(path,"r",encoding="utf-8").read().replace("\r\n","\n").split("\n")
    s=e=None
    for i,line in enumerate(txt):
        if line.strip()=="Sub Main()": s=i
        elif line.strip()=="End Sub": e=i
    if s is None or e is None or e<=s: raise RuntimeError("macro markers missing")
    return "\n".join(txt[s+1:e])

def inv_vba(shape_out,param_out):
    return "\n".join([
        "On Error Resume Next",
        "Dim fnum As Integer","Dim i As Long","Dim nm As String",
        "fnum = FreeFile",
        f'Open "{shape_out}" For Output As #fnum',
        'Print #fnum, "R1A1_SHAPE_INVENTORY"',
        'Print #fnum, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
        "For i = 0 To Solid.GetNumberOfShapes() + 1",
        "  nm = Solid.GetNameOfShapeFromIndex(i)",
        "  If Len(nm) > 0 Then",
        '    Print #fnum, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm)) & "|isSolid=" & CStr(Solid.IsSolidShape(nm))',
        "  End If","Next i","Close #fnum",
        "fnum = FreeFile",
        f'Open "{param_out}" For Output As #fnum',
        'Print #fnum, "R1A1_PARAMETER_INVENTORY"',
        'Print #fnum, "PARAM_COUNT=" & CStr(GetNumberOfParameters())',
        "For i = 1 To GetNumberOfParameters()",
        '  Print #fnum, "PARAM|" & GetParameterName(i) & "|" & GetParameterSValue(i) & "|" & CStr(GetParameterNValue(i))',
        "Next i","Close #fnum","On Error GoTo 0"])

def shot_vba(view,img):
    return f'Plot.RestoreView "{view}"\nPlot.ZoomToStructure\nPlot.Update\nPlot.ExportImage "{img}", 1600, 1200'

def add(prj,name,code):
    prj.modeler.add_to_history(name,code)

def session_build(macro,cstfile,log):
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.new_mws(); log.append("NEW_MWS_OK")
        body=read_body(macro); log.append(f"MACRO_BODY_LINES={len(body.splitlines())}")
        add(prj,"R1A1 scaled aperture build-only",body)
        prj.save(cstfile); log.append("SAVED="+cstfile)
    finally:
        if prj is not None: prj.close()
        de.close()

def session_evidence(cstfile,ev,reopen,log):
    de=ci.DesignEnvironment(); de.set_quiet_mode(True); prj=None
    try:
        prj=de.open_project(cstfile)
        prefix="reopen_" if reopen else ""
        add(prj,"inventory",inv_vba(
            os.path.join(ev,prefix+"object_inventory.txt"),
            os.path.join(ev,prefix+"parameter_inventory.txt")))
        img=os.path.join(ev,"view_after_reopen.png" if reopen else "top_view.png")
        add(prj,"shot",shot_vba("Perspective" if reopen else "Front",img))
        if not reopen:
            add(prj,"oblique shot",shot_vba("Perspective",os.path.join(ev,"oblique_view.png")))
        log.append(("REOPEN_OK" if reopen else "EVIDENCE_OK"))
    finally:
        if prj is not None: prj.close()
        de.close()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--work",required=True)
    args=ap.parse_args()
    os.makedirs(args.evidence,exist_ok=True); os.makedirs(args.work,exist_ok=True)
    macro=os.path.join(args.repo,"source","cst","R1A1_CHARTS_SCALED_APERTURE_BUILD_ONLY_V01.mcr")
    cstfile=os.path.join(args.work,"R1A1_CHARTS_SCALED_APERTURE_BUILD_ONLY_V01.cst")
    log=[f"DE_VERSION={ci.DesignEnvironment.version()}",f"MACRO_SHA256={sha256(macro)}"]
    session_build(macro,cstfile,log)
    session_evidence(cstfile,args.evidence,False,log)
    session_evidence(cstfile,args.evidence,True,log)
    summary={"macro":macro,"macro_sha256":sha256(macro),"cst_project":cstfile,
             "cst_project_sha256":sha256(cstfile),"log":log}
    open(os.path.join(args.evidence,"harness_summary.json"),"w").write(json.dumps(summary,indent=2))
    open(os.path.join(args.evidence,"harness_log.txt"),"w").write("\n".join(log)+"\n")
    print("PASS_R1A1_HARNESS_EXECUTED")
    print("CST_SHA256="+summary["cst_project_sha256"])

if __name__=="__main__":
    main()
