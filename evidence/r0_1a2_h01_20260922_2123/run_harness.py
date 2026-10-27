"""R0.1A2 SLOTTED-PLATE BUILD-ONLY harness (H01).

Drives CST Studio Suite 2022 via the bundled CST Python API.

BUILD ONLY: no solver, no ports, no monitors, no dielectric, no optimizer.

Session A: execute the repository-controlled macro body from
  source/cst/R0_CHARTS_SLOTTED_PLATE_BUILD_ONLY_V02.mcr in a fresh MWS,
  then save and close.
Session B: fresh open; view-controlled screenshots + object inventory.
Session C: fresh open again (fresh-reopen audit); inventory + screenshot.

View control uses Plot.RestoreView reserved names. In this CST build "Front"
yields the model Z-axis (plan/top) view, "Bottom" the in-plane elevation
exposing the 200 mm ground gap, and "Perspective" the oblique view.
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
EV = os.path.join(REPO, "evidence", "r0_1a2_h01_20260922_2123")
WORK = r"D:\GNSS_Lband_Active_Array\_r0_1a2_h01_work"
CSTFILE = os.path.join(WORK, "R0_1A2_SLOTTED_PLATE_BUILD_ONLY_H01.cst")
MACRO = os.path.join(REPO, "source", "cst", "R0_CHARTS_SLOTTED_PLATE_BUILD_ONLY_V02.mcr")

LOG = []

EXPECT_PRESENT = [
    ("ReferenceGround", "GROUND_REFERENCE"),
    ("Radiator", "ANTENNA_PLATE"),
]
EXPECT_ABSENT = [
    ("SlotTools", "CUT_OUTER_N"),
    ("SlotTools", "CUT_OUTER_S"),
    ("SlotTools", "CUT_OUTER_E"),
    ("SlotTools", "CUT_OUTER_W"),
    ("SlotTools", "CUT_INNER_N"),
    ("SlotTools", "CUT_INNER_S"),
    ("SlotTools", "CUT_INNER_E"),
    ("SlotTools", "CUT_INNER_W"),
]


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


def inventory_vba(outfile):
    lines = [
        "On Error Resume Next",
        "Dim fnum As Integer",
        "Dim i As Long",
        "Dim nm As String",
        "fnum = FreeFile",
        'Open "%s" For Output As #fnum' % outfile,
        'Print #fnum, "R0_1A2_OBJECT_INVENTORY"',
    ]
    for comp, solid in EXPECT_PRESENT:
        path = "Components\\%s\\%s" % (comp, solid)
        lines.append(
            'Print #fnum, "EXPECT_PRESENT|%s\\%s=" & CStr(SelectTreeItem("%s"))'
            % (comp, solid, path)
        )
    for comp, solid in EXPECT_ABSENT:
        path = "Components\\%s\\%s" % (comp, solid)
        lines.append(
            'Print #fnum, "EXPECT_ABSENT|%s\\%s=" & CStr(SelectTreeItem("%s"))'
            % (comp, solid, path)
        )
    lines.append('Print #fnum, "COMPONENT_SLOTTOOLS=" & CStr(SelectTreeItem("Components\\SlotTools"))')
    lines.append('Print #fnum, "SHAPE_COUNT=" & CStr(Solid.GetNumberOfShapes())')
    lines.append("For i = 0 To Solid.GetNumberOfShapes() + 1")
    lines.append("  nm = Solid.GetNameOfShapeFromIndex(i)")
    lines.append("  If Len(nm) > 0 Then")
    lines.append(
        '    Print #fnum, "SHAPE|" & nm & "|volume=" & CStr(Solid.GetVolume(nm)) '
        '& "|isSolid=" & CStr(Solid.IsSolidShape(nm))'
    )
    lines.append("  End If")
    lines.append("Next i")
    lines.append('Print #fnum, "PARAM_COUNT=" & CStr(GetNumberOfParameters())')
    lines.append("For i = 1 To GetNumberOfParameters()")
    lines.append(
        'Print #fnum, "PARAM|" & GetParameterName(i) & "|" & '
        'GetParameterSValue(i) & "|" & CStr(GetParameterNValue(i))'
    )
    lines.append("Next i")
    lines.append("Close #fnum")
    lines.append("On Error GoTo 0")
    return "\n".join(lines)


def shot_vba(view_name, imgpath, hide_ground=False):
    code = ""
    if hide_ground:
        code += 'Component.HideComponent "ReferenceGround"\n'
    code += 'Plot.RestoreView "%s"\n' % view_name
    code += "Plot.ZoomToStructure\nPlot.Update\n"
    code += 'Plot.ExportImage "%s", 1600, 1200\n' % imgpath
    if hide_ground:
        code += 'Component.ShowComponent "ReferenceGround"\n'
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
        err = try_vba(prj, "R0.1A2 slotted plate build-only", body)
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
    info("=== SESSION B: SCREENSHOTS + INVENTORY (fresh open) ===")
    de = ci.DesignEnvironment()
    info("DE_PID=" + str(de.pid()))
    de.set_quiet_mode(True)
    prj = None
    try:
        prj = de.open_project(CSTFILE)
        info("OPEN_PROJECT_OK")
        shots = [
            ("Front", "top_view_full.png", False),
            ("Front", "top_view_plate.png", True),
            ("Bottom", "side_view_ground_gap.png", False),
            ("Perspective", "oblique_view.png", False),
        ]
        for view_name, fname, hide in shots:
            img = os.path.join(EV, fname)
            e = try_vba(prj, "shot %s" % fname, shot_vba(view_name, img, hide))
            info("SHOT[%s] view=%r hide=%s err=%r sha=%s"
                 % (fname, view_name, hide, e, sha256(img)))
        inv = os.path.join(EV, "object_inventory.txt")
        info("INVENTORY_ERR=%r" % try_vba(prj, "inventory", inventory_vba(inv)))
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
        inv = os.path.join(EV, "reopen_inventory.txt")
        info("REOPEN_INVENTORY_ERR=%r" % try_vba(prj, "reopen inventory", inventory_vba(inv)))
        img = os.path.join(EV, "view_after_reopen.png")
        e2 = try_vba(prj, "reopen shot", shot_vba("Front", img, False))
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
    for name in ("top_view_full.png", "top_view_plate.png",
                 "side_view_ground_gap.png", "oblique_view.png",
                 "view_after_reopen.png"):
        summary["screenshots"][name] = sha256(os.path.join(EV, name))
    with open(os.path.join(EV, "harness_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    with open(os.path.join(EV, "harness_log.txt"), "w") as fh:
        fh.write("\n".join(LOG) + "\n")
    info("HARNESS_DONE")


if __name__ == "__main__":
    main()
