"""R0.1A TOPOLOGY BUILD-ONLY harness (H01).

Drives CST Studio Suite 2022 via the bundled CST Python API.

BUILD ONLY:
- no solver, no ports, no monitors, no substrate, no optimizer.

Session A: build the repository-controlled macro body from
  source/cst/R0_CHARTS_TOPOLOGY_BUILD_ONLY_V01.mcr inside a fresh MWS project,
  then save and close.
Session B: open the saved project fresh and capture view-controlled screenshots
  + object inventory.
Session C: open the saved project fresh again (fresh-reopen audit) and capture
  the reopen inventory + screenshot.

View commands use Plot.RestoreView with reserved names. In this CST build the
reserved name "Front" yields the view along the model Z axis (plan/top view),
"Bottom" yields the in-plane elevation exposing the 200 mm ground gap, and
"Perspective" the oblique view. Exact commands are logged in harness_log.txt.

The CST Python API only applies Plot.RestoreView reliably in a session that has
freshly opened a saved project, so all view-controlled screenshots are taken in
sessions B and C from the saved artifact.
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
EV = os.path.join(REPO, "evidence", "r0_1a_h01_20260922_2052")
WORK = r"D:\GNSS_Lband_Active_Array\_r0_1a_h01_work"
CSTFILE = os.path.join(WORK, "R0_1A_TOPOLOGY_BUILD_ONLY_H01.cst")
MACRO = os.path.join(REPO, "source", "cst", "R0_CHARTS_TOPOLOGY_BUILD_ONLY_V01.mcr")

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


OBJECTS = [
    ("ReferenceGround", "GROUND_REFERENCE"),
    ("Radiator", "PETAL_N"),
    ("Radiator", "PETAL_E"),
    ("Radiator", "PETAL_S"),
    ("Radiator", "PETAL_W"),
    ("PassiveRing", "RING_N"),
    ("PassiveRing", "RING_S"),
    ("PassiveRing", "RING_E"),
    ("PassiveRing", "RING_W"),
]


def inventory_vba(outfile):
    lines = [
        "On Error Resume Next",
        "Dim fnum As Integer",
        "Dim i As Long",
        "fnum = FreeFile",
        'Open "%s" For Output As #fnum' % outfile,
        'Print #fnum, "R0_1A_OBJECT_INVENTORY"',
    ]
    for comp, solid in OBJECTS:
        path = "Components\\%s\\%s" % (comp, solid)
        lines.append(
            'Print #fnum, "SELECT|%s\\%s=" & CStr(SelectTreeItem("%s"))'
            % (comp, solid, path)
        )
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
        err = try_vba(prj, "R0 topology build-only", body)
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
            ("Front", "top_view_radiator.png", True),
            ("Bottom", "side_view_ground_gap.png", False),
            ("Perspective", "oblique_view.png", False),
        ]
        for view_name, fname, hide in shots:
            img = os.path.join(EV, fname)
            code = shot_vba(view_name, img, hide)
            e = try_vba(prj, "shot %s" % fname, code)
            info("SHOT[%s] view=%r hide=%s err=%r sha=%s"
                 % (fname, view_name, hide, e, sha256(img)))
        inv = os.path.join(EV, "object_inventory.txt")
        e4 = try_vba(prj, "inventory", inventory_vba(inv))
        info("INVENTORY_ERR=%r" % e4)
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
        e = try_vba(prj, "reopen inventory", inventory_vba(inv))
        info("REOPEN_INVENTORY_ERR=%r" % e)
        img = os.path.join(EV, "view_after_reopen.png")
        code = shot_vba("Front", img, False)
        e2 = try_vba(prj, "reopen shot", code)
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
    build_session()
    evidence_session()
    reopen_session()

    summary = {
        "cst_project": CSTFILE,
        "cst_project_sha256": sha256(CSTFILE),
        "screenshots": {},
    }
    for name in ("top_view_full.png", "top_view_radiator.png",
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
