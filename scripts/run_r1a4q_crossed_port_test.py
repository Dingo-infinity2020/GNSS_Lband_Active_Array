"""R1A4Q isolated crossed-discrete-port A/B qualification on NW."""
import os, sys, json, math, hashlib, argparse

LIBS=r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0,LIBS)

import cst.interface as ci
from cst.results import ProjectFile

def vba_geometry(lifted=False):
    lines = []
    lines += [
        'With Units',
        ' .Geometry "mm"',
        ' .Frequency "GHz"',
        ' .Time "ns"',
        ' .Voltage "V"',
        'End With',
        'Solver.FrequencyRange "0.5", "2.0"',
        'With Boundary',
        ' .Xmin "open"',
        ' .Xmax "open"',
        ' .Ymin "open"',
        ' .Ymax "open"',
        ' .Zmin "open"',
        ' .Zmax "open"',
        ' .Xsymmetry "none"',
        ' .Ysymmetry "none"',
        ' .Zsymmetry "none"',
        ' .ApplyInAllDirections "False"',
        'End With',
        'With Background',
        ' .ResetBackground',
        ' .XminSpace "30"',
        ' .XmaxSpace "30"',
        ' .YminSpace "30"',
        ' .YmaxSpace "30"',
        ' .ZminSpace "30"',
        ' .ZmaxSpace "30"',
        ' .ApplyInAllDirections "False"',
        'End With',
        'ChangeSolverType "HF Frequency Domain"',
        'FDSolver.OrderTet "First"',
        'FDSolver.MeshAdaptionTet "False"',
    ]
    pads=[
      ("NE","2","8","2","8"),
      ("NW","-8","-2","2","8"),
      ("SW","-8","-2","-8","-2"),
      ("SE","2","8","-8","-2"),
    ]
    for name,x1,x2,y1,y2 in pads:
        lines += [
          'With Brick',' .Reset',
          ' .Name "%s"'%name,' .Component "Pads"',' .Material "PEC"',
          ' .Xrange "%s", "%s"'%(x1,x2),
          ' .Yrange "%s", "%s"'%(y1,y2),
          ' .Zrange "0", "0.5"',' .Create','End With']
    if lifted:
        for name,x,y in [("NW_POST","-2.5","2.5"),("SE_POST","2.5","-2.5")]:
            lines += [
              'With Brick',' .Reset',
              ' .Name "%s"'%name,' .Component "Posts"',' .Material "PEC"',
              ' .Xrange "%s-0.25", "%s+0.25"'%(x,x),
              ' .Yrange "%s-0.25", "%s+0.25"'%(y,y),
              ' .Zrange "0.5", "3.0"',' .Create','End With']
    z2="3.0" if lifted else "0.5"
    lines += [
      'With DiscretePort',' .Reset',' .PortNumber "1"',' .Type "SParameter"',
      ' .Impedance "100"',' .Voltage "1.0"',' .Current "1.0"',
      ' .SetP1 "False", "2.5", "2.5", "0.5"',
      ' .SetP2 "False", "-2.5", "-2.5", "0.5"',
      ' .InvertDirection "False"',' .Monitor "True"',' .Radius "0.0"',' .Create','End With',
      'With DiscretePort',' .Reset',' .PortNumber "2"',' .Type "SParameter"',
      ' .Impedance "100"',' .Voltage "1.0"',' .Current "1.0"',
      ' .SetP1 "False", "-2.5", "2.5", "%s"'%z2,
      ' .SetP2 "False", "2.5", "-2.5", "%s"'%z2,
      ' .InvertDirection "False"',' .Monitor "True"',' .Radius "0.0"',' .Create','End With',
    ]
    return "\n".join(lines)

def get_s(cstfile):
    pf=ProjectFile(cstfile,allow_interactive=True)
    p3=pf.get_3d()
    tree=p3.get_tree_items()
    data={}
    for i,j in [(1,1),(1,2),(2,1),(2,2)]:
        item=r"1D Results\S-Parameters\S%d,%d"%(i,j)
        if item not in tree:
            data["tree_items"]=tree
            raise RuntimeError("missing result "+item)
        raw=p3.get_result_item(item).get_data()
        vals=[]
        for row in raw:
            x=row[0]
            c=complex(row[1])
            vals.append((float(x),float(abs(c)),float(20*math.log10(max(abs(c),1e-300)))))
        data["S%d%d"%(i,j)]=vals
    return data

def summarize(data):
    out={}
    for key in ("S11","S12","S21","S22"):
        vals=data[key]
        # nearest samples to 0.75,1.0,1.4,1.8 GHz plus extrema
        samples={}
        for f0 in (0.75,1.0,1.4,1.8):
            row=min(vals,key=lambda r:abs(r[0]-f0))
            samples[str(f0)]={"f":row[0],"mag":row[1],"db":row[2]}
        out[key]={
          "samples":samples,
          "db_min":min(r[2] for r in vals),
          "db_max":max(r[2] for r in vals),
        }
    return out

def port_count_history(path):
    return "\n".join([
      "On Error Resume Next",
      "Dim f As Integer",
      "f=FreeFile",
      'Open "%s" For Output As #f'%path,
      'Print #f, "PORT_COUNT=" & CStr(Solver.GetNumberOfPorts())',
      "Close #f",
      "On Error GoTo 0"])

def read_port_count(path):
    for line in open(path,encoding="utf-8").read().splitlines():
        if line.startswith("PORT_COUNT="):
            return int(line.split("=",1)[1])
    raise RuntimeError("missing port count audit")

def run_model(outdir,name,lifted):
    os.makedirs(outdir)
    cstfile=os.path.join(outdir,name+".cst")
    portfile=os.path.join(outdir,"pre_solver_port_count.txt")
    de=ci.DesignEnvironment()
    de.set_quiet_mode(True)
    prj=None
    try:
        prj=de.new_mws()
        prj.modeler.add_to_history(name+" geometry and ports",vba_geometry(lifted))
        prj.save(cstfile)
        prj.modeler.add_to_history(name+" pre-solver port audit",port_count_history(portfile))
        pre_ports=read_port_count(portfile)
        if pre_ports != 2:
            raise RuntimeError("pre-solver port count is not 2")
        prj.modeler.run_solver()
        prj.save()
    finally:
        if prj is not None: prj.close()
        de.close()
    data=get_s(cstfile)
    summary=summarize(data)
    return {
      "name":name,"lifted":lifted,"cst":cstfile,
      "pre_solver_port_count":pre_ports,
      "summary":summary,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--work",required=True)
    ap.add_argument("--evidence",required=True)
    ap.add_argument("--only",choices=["both","cross","lifted"],default="both")
    a=ap.parse_args()
    if os.path.exists(a.work) or os.path.exists(a.evidence):
        raise RuntimeError("fresh work/evidence required")
    os.makedirs(a.work)
    os.makedirs(a.evidence)
    report={}
    if a.only in ("both","cross"):
        report["cross"]=run_model(os.path.join(a.work,"cross"),"CROSS",False)
    if a.only in ("both","lifted"):
        report["lifted"]=run_model(os.path.join(a.work,"lifted"),"LIFTED_REFERENCE",True)
    if a.only!="both":
        with open(os.path.join(a.evidence,"summary.json"),"w") as f:
            json.dump(report,f,indent=2)
        print(json.dumps(report,sort_keys=True))
        return
    cross=report["cross"]
    lifted=report["lifted"]
    c=cross["summary"]["S21"]["samples"]["1.4"]["db"]
    l=lifted["summary"]["S21"]["samples"]["1.4"]["db"]
    report["s21_1p4_cross_db"]=c
    report["s21_1p4_lifted_db"]=l
    report["cross_minus_lifted_db"]=c-l
    with open(os.path.join(a.evidence,"summary.json"),"w") as f:
        json.dump(report,f,indent=2)
    with open(os.path.join(a.evidence,"summary.txt"),"w") as f:
        f.write("CROSS_S21_1P4_DB=%.6f\n"%c)
        f.write("LIFTED_S21_1P4_DB=%.6f\n"%l)
        f.write("CROSS_MINUS_LIFTED_DB=%.6f\n"%(c-l))
        for model in ("cross","lifted"):
            f.write("\n[%s]\n"%model.upper())
            for key in ("S11","S21","S12","S22"):
                f.write("%s_DB_MIN=%.6f\n"%(key,report[model]["summary"][key]["db_min"]))
                f.write("%s_DB_MAX=%.6f\n"%(key,report[model]["summary"][key]["db_max"]))
    print(json.dumps({
      "CROSS_S21_1P4_DB":c,
      "LIFTED_S21_1P4_DB":l,
      "CROSS_MINUS_LIFTED_DB":c-l,
    },sort_keys=True))

if __name__=="__main__":
    main()
