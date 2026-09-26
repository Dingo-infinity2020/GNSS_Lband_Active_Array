"""REF-CUI-R0B BUILD-ONLY harness (H01).

Drives CST Studio Suite 2022 via the bundled CST Python API.

BUILD ONLY: no ports, no monitors, no solver, no optimizer.

Session A: execute the repository macro body in a fresh MWS, save, close.
Session B: fresh open; enumerate shapes, dump parameters, take screenshots.
Session C: fresh open again; enumerate shapes, screenshot (reopen audit).

View control: Plot.RestoreView reserved names ("Front" = model Z plan view,
"Bottom" = in-plane elevation, "Perspective" = oblique).
"""

import os
import sys
import json
import hashlib

LIBS = r"D:\Program Files (x86)\CST Studio Suite 2022\AMD64\python_cst_libraries"
if LIBS not in sys.path:
    sys.path.insert(0, LIBS)

import cst.interface as ci

REPO = r"D:\GNSS_Lband_Active_Array\GNSS_Lband_Active_Array-project-r0-charts-scaffold"
EV = os.path.join(REPO, "evidence", "ref_cui_r0b_h01_20260923_1341")
WORK = r"D:\GNSS_Lband_Active_Array\_ref_cui_r0b_work"
CSTFILE = os.path.join(WORK, "REF_CUI_R0B_BUILD_ONLY_V01.cst")
MACRO = os.path.join(REPO, "source", "cst", "REF_CUI_R0B_BUILD_ONLY_V01.mcr")

LOG = []


def info(msg):
    print(msg)
    LOG.append(str(msg))


def sha256(path):
    if not os.path.exists(path):
        return "MISSING"
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_macro_body(path):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    lines = text.replace("\r\n", "\n").split("\n")
    start = None
    end = None
    for i, line in enumerate(lines):
        s = line.strip()
        if s == "Sub Main()":
            start = i
        elif s == "End Sub":
            end = i
    if start is None or end is None or end <= start:
        raise RuntimeError("Sub Main/End Sub markers not found in macro")
    return "\n".join(lines[start + 1:end])


def inventory_vba(shape_out, param_out):
    lines = [
        "On Error Resume Next",
        "Dim fnum As Integer",
        "Dim i As Long",
        "Dim nm As String",
        "fnum = FreeFile",
        'Open "%s" For Output As #fnum' % shape_out,
        'Print #fnum, "REF_CUI_R0B_SHAPE_INVENTORY"',
        'Print #fnum, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())',
        "For i = 0 To Solid.GetNumberOfShapes() + 1",
        "  nm = Solid.GetNameOfShapeFromIndex(i)",
        "  If Len(nm) > 0 Then",
        '    Print #fnum, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm)) '
        '& "|isSolid=" & CStr(Solid.IsSolidShape(nm))',
        "  End If",
        "Next i",
        "Close #fnum",
        "fnum = FreeFile",
        'Open "%s" For Output As #fnum' % param_out,
        'Print #fnum, "REF_CUI_R0B_PARAMETER_INVENTORY"',
        'Print #fnum, "PARAM_COUNT=" & CStr(GetNumberOfParameters())',
        "For i = 1 To GetNumberOfParameters()",
        'Print #fnum, "PARAM|" & GetParameterName(i) & "|" & '
        'GetParameterSValue(i) & "|" & CStr(GetParameterNValue(i))',
        "Next i",
        "Close #fnum",
        "On Error GoTo 0",
    ]
    return "\n".join(lines)


def shot_vba(view_name, imgpath, hide=None):
    code = ""
    if hide:
        code += 'Component.HideComponent "%s"\n' % hide
    code += 'Plot.RestoreView "%s"\n' % view_name
    code += "Plot.ZoomToStructure\nPlot.Update\n"
    code += 'Plot.ExportImage "%s", 1600, 1200\n' % imgpath
    if hide:
        code += 'Component.ShowComponent "%s"\n' % hide
    return code


def try_vba(prj, header, code):
    try:
        prj.modeler.add_to_history(header, code)
        return None
    except Exception as exc:  # noqa
        return "%s: %s" % (type(exc).__name__, exc)


def build_session():
    info("=== SESSION A: BUILD ===")
    de = ci.DesignEnvironment()
    info("DE_PID=" + str(de.pid()))
    de.set_quiet_mode(True)
    prj = None
    try:
        prj = de.new_mws()
        info("NEW_MWS_OK")
        body = read_macro_body(MACRO)
        info("MACRO_BODY_LINES=%d" % len(body.split("\n")))
        err = try_vba(prj, "REF-CUI-R0B build-only", body)
        info("BUILD_ADD_TO_HISTORY_ERR=%r" % err)
        if err is not None:
            return
        prj.save(CSTFILE)
        info("SAVED=%s exists=%s" % (CSTFILE, os.path.exists(CSTFILE)))
    finally:
        try:
            if prj is not None:
                prj.close()
        except Exception as exc:  # noqa
            info("A_CLOSE_PROJECT_ERR=%r" % exc)
        try:
            de.close()
        except Exception as exc:  # noqa
            info("A_CLOSE_DE_ERR=%r" % exc)


def evidence_session():
    info("=== SESSION B: INVENTORY + SCREENSHOTS ===")
    de = ci.DesignEnvironment()
    info("DE_PID=" + str(de.pid()))
    de.set_quiet_mode(True)
    prj = None
    try:
        prj = de.open_project(CSTFILE)
        info("OPEN_PROJECT_OK")
        shape_out = os.path.join(EV, "object_inventory.txt")
        param_out = os.path.join(EV, "parameter_inventory.txt")
        info("INVENTORY_ERR=%r" % try_vba(prj, "inventory",
                                          inventory_vba(shape_out, param_out)))
        shots = [
            ("Front", "top_view.png", None),
            ("Perspective", "oblique_view.png", None),
            ("Perspective", "underside_balun.png", "RadiatorBoard"),
            ("Bottom", "side_view.png", None),
        ]
        for view_name, fname, hide in shots:
            img = os.path.join(EV, fname)
            e = try_vba(prj, "shot %s" % fname, shot_vba(view_name, img, hide))
            info("SHOT[%s] view=%r hide=%r err=%r sha=%s"
                 % (fname, view_name, hide, e, sha256(img)))
    finally:
        try:
            if prj is not None:
                prj.close()
        except Exception as exc:  # noqa
            info("B_CLOSE_PROJECT_ERR=%r" % exc)
        try:
            de.close()
        except Exception as exc:  # noqa
            info("B_CLOSE_DE_ERR=%r" % exc)


def reopen_session():
    info("=== SESSION C: FRESH-REOPEN AUDIT ===")
    de = ci.DesignEnvironment()
    info("DE_PID=" + str(de.pid()))
    de.set_quiet_mode(True)
    prj = None
    try:
        prj = de.open_project(CSTFILE)
        info("OPEN_PROJECT_OK")
        shape_out = os.path.join(EV, "reopen_inventory.txt")
        param_out = os.path.join(EV, "reopen_parameter_inventory.txt")
        info("REOPEN_INVENTORY_ERR=%r" % try_vba(prj, "reopen inventory",
                                                 inventory_vba(shape_out, param_out)))
        img = os.path.join(EV, "view_after_reopen.png")
        e2 = try_vba(prj, "reopen shot", shot_vba("Perspective", img, None))
        info("REOPEN_SHOT_ERR=%r sha=%s" % (e2, sha256(img)))
    finally:
        try:
            if prj is not None:
                prj.close()
        except Exception as exc:  # noqa
            info("C_CLOSE_PROJECT_ERR=%r" % exc)
        try:
            de.close()
        except Exception as exc:  # noqa
            info("C_CLOSE_DE_ERR=%r" % exc)


def main():
    if not os.path.isdir(EV):
        os.makedirs(EV)
    if not os.path.isdir(WORK):
        os.makedirs(WORK)
    info("DE_VERSION=" + ci.DesignEnvironment.version())
    info("MACRO_SHA256=" + sha256(MACRO))
    build_session()
    evidence_session()
    reopen_session()

    summary = {
        "cst_project": CSTFILE,
        "cst_project_sha256": sha256(CSTFILE),
        "macro": MACRO,
        "macro_sha256": sha256(MACRO),
        "screenshots": {},
    }
    for name in ("top_view.png", "oblique_view.png", "underside_balun.png",
                 "side_view.png", "view_after_reopen.png"):
        summary["screenshots"][name] = sha256(os.path.join(EV, name))
    with open(os.path.join(EV, "harness_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    with open(os.path.join(EV, "harness_log.txt"), "w") as fh:
        fh.write("\n".join(LOG) + "\n")
    info("HARNESS_DONE")


if __name__ == "__main__":
    main()
