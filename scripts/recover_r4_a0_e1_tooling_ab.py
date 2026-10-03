from __future__ import print_function
import argparse, hashlib, json, shutil, sys
from pathlib import Path

LIBS=r"D:\\Program Files (x86)\\CST Studio Suite 2022\\AMD64\\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)
import cst.interface as ci

def sha(p):
    h=hashlib.sha256()
    with open(str(p),"rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def wrap(body):
    return "Sub Main()\n"+body+"\nEnd Sub"

def copy_project(src,dst):
    src=Path(src); dst=Path(dst)
    shutil.copy2(str(src),str(dst))
    srcdir=src.with_suffix("")
    dstdir=dst.with_suffix("")
    if srcdir.exists():
        if dstdir.exists(): shutil.rmtree(str(dstdir),ignore_errors=True)
        shutil.copytree(str(srcdir),str(dstdir))

def probe_ports(cst,out):
    body="\n".join([
      "On Error Resume Next",
      "Dim f As Integer, i As Integer, stype As String, zref As Double, cur As Double, vol As Double, vimp As Double, rad As Double, mon As Boolean",
      "Dim x0 As Double, y0 As Double, z0 As Double, x1 As Double, y1 As Double, z1 As Double, pok As Boolean, cok As Boolean",
      "f=FreeFile",
      'Open "'+str(out).replace("\\","/")+'" For Output As #f',
      'Print #f, "SOLVER_PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "For i=1 To 10",
      " Err.Clear",
      " pok=DiscretePort.GetProperties(i,stype,zref,cur,vol,vimp,rad,mon)",
      ' Print #f, "P|" & CStr(i) & "|PROP_OK=" & CStr(pok) & "|ERR=" & CStr(Err.Number) & "|TYPE=" & stype & "|ZREF=" & CStr(zref)',
      " Err.Clear",
      " cok=DiscretePort.GetCoordinates(i,x0,y0,z0,x1,y1,z1)",
      ' Print #f, "C|" & CStr(i) & "|COORD_OK=" & CStr(cok) & "|ERR=" & CStr(Err.Number) & "|P1=" & CStr(x0) & "," & CStr(y0) & "," & CStr(z0) & "|P2=" & CStr(x1) & "," & CStr(y1) & "," & CStr(z1)',
      "Next i","Close #f","On Error GoTo 0"])
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(cst))
        ok=bool(p.schematic.execute_vba_code(wrap(body)))
    finally:
        if p is not None: p.close()
        de.close()
    return {"invoke_ok":ok,"text":out.read_text(encoding="utf-8") if out.exists() else ""}

def add_port(base,dst,mode,root):
    copy_project(base,dst)
    body="\n".join([
      "With DiscretePort",".Reset",
      '.PortNumber "99"','.Type "SParameter"','.Impedance "50.0"',
      '.Voltage "1.0"','.Current "1.0"',
      '.SetP1 "False", "0.0", "12.5", "0.0"',
      '.SetP2 "False", "0.0", "12.5", "-1.0"',
      '.InvertDirection "False"','.Monitor "False"','.Radius "0.0"','.Create',"End With"])
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    try:
        p=de.open_project(str(dst))
        if mode=="schematic":
            invoked=bool(p.schematic.execute_vba_code(wrap(body)))
        else:
            p.modeler.add_to_history("TOOLING_DIAG_ADD_PORT_99",body); invoked=True
        p.save()
    finally:
        if p is not None: p.close()
        de.close()
    return {"invoke_ok":invoked,"reopen":probe_ports(dst,root/(dst.stem+"_ports.txt"))}

def intersect(base,dst,mode,root):
    copy_project(base,dst)
    out=root/(dst.stem+"_intersect.txt")
    a="E1_PackageLands:PIN2_RFIN"; b="E1_LocalGroundTop:EXPOSED_PADDLE"
    body="\n".join([
      "On Error Resume Next","Dim f As Integer, vb As Double, va As Double",
      "f=FreeFile",'Open "'+str(out).replace("\\","/")+'" For Output As #f',
      'vb=Solid.GetVolume("'+a+'")','Print #f, "BEFORE_A=" & CStr(vb)',
      "Err.Clear",'Solid.Intersect "'+a+'", "'+b+'"',
      'Print #f, "INTERSECT_ERR=" & CStr(Err.Number)',"Err.Clear",
      'va=Solid.GetVolume("'+a+'")','Print #f, "AFTER_ERR=" & CStr(Err.Number)',
      'Print #f, "AFTER_A=" & CStr(va)',"Close #f","On Error GoTo 0"])
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    err=None
    try:
        p=de.open_project(str(dst))
        if mode=="schematic":
            invoked=bool(p.schematic.execute_vba_code(wrap(body)))
        else:
            p.modeler.add_to_history("TOOLING_DIAG_INTERSECT",body); invoked=True
    except Exception as ex:
        invoked=False; err=repr(ex)
    finally:
        if p is not None: p.close()
        de.close()
    return {"invoke_ok":invoked,"exception":err,"text":out.read_text(encoding="utf-8") if out.exists() else ""}

def nondestructive_query(base,root):
    out=root/"nondestructive_intersection_query.txt"
    pairs=[
      ("PIN2_PADDLE","E1_PackageLands:PIN2_RFIN","E1_LocalGroundTop:EXPOSED_PADDLE"),
      ("DN_MSL_CRF_GND","E1_Signal:DOWNSTREAM_MSL","E1_LocalGroundTop:CRF_GND_PAD"),
      ("VIA_C_FR4","E1_Vias:PADDLE_VIA_C","E1_Substrate:FR4_COUPON")]
    lines=["On Error Resume Next","Dim f As Integer, q As Boolean","f=FreeFile",
           'Open "'+str(out).replace("\\\\","/")+'" For Output As #f']
    for tag,a,b in pairs:
        lines += [
          "Err.Clear",
          'q=Solid.DoTheseGeometricallyIntersect("'+a+'","'+b+'")',
          'Print #f, "Q|'+tag+'|ERR=" & CStr(Err.Number) & "|INTERSECT=" & CStr(q)']
    lines += ["Close #f","On Error GoTo 0"]
    de=ci.DesignEnvironment(ci.DesignEnvironment.StartMode.New); de.set_quiet_mode(True); p=None
    ok=False; err=None
    try:
        p=de.open_project(str(base))
        ok=bool(p.schematic.execute_vba_code(wrap("\n".join(lines))))
    except Exception as ex:
        err=repr(ex)
    finally:
        if p is not None: p.close()
        de.close()
    return {"invoke_ok":ok,"supported":err is None,"exception":err,
            "text":out.read_text(encoding="utf-8") if out.exists() else ""}

def main(source,outdir):
    source=Path(source); root=Path(outdir)
    if root.exists(): raise RuntimeError("HOLD_TOOLING_DIAG_DIR_EXISTS")
    root.mkdir(parents=True)
    base=root/"base_copy.cst"; copy_project(source,base)
    before=sha(base)
    result={
      "mode":"READ_ONLY_RECOVERY_TOOLING_AB_ON_TEMP_COPIES",
      "formal_build":False,"solver_invocations":0,
      "source_sha256":sha(source),
      "base_probe":probe_ports(base,root/"base_ports.txt"),
      "nondestructive_query":nondestructive_query(base,root),
      "port_schematic":add_port(base,root/"port_schematic.cst","schematic",root),
      "port_history":add_port(base,root/"port_history.cst","history",root),
      "intersect_schematic":intersect(base,root/"intersect_schematic.cst","schematic",root),
      "intersect_history":intersect(base,root/"intersect_history.cst","history",root)}
    result["base_integrity"]=sha(base)==before
    (root/"result.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True); ap.add_argument("--outdir",required=True)
    a=ap.parse_args()
    main(a.source,a.outdir)
