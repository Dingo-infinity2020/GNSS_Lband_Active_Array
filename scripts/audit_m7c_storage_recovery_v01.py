"""Offline freeze audit, optionally plus read-only NW artifact/storage checks."""
from __future__ import print_function
import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path
from m7c_storage_recovery_preflight_v01 import artifact_checks, sha, storage_check

MANIFEST = "execution/M7C_STORAGE_RECOVERY_SOLVE_MANIFEST_V01.json"


def audit(root, host=False):
    root = Path(root).resolve()
    m = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    old = json.loads((root / m["recovery"]["original_manifest"]).read_text(encoding="utf-8"))
    c = json.loads((root / "execution/stage_contract.json").read_text(encoding="utf-8-sig"))
    checks = {}
    for key in ("solve_network", "raw_to_solve", "deleted_raw_ports", "isolated_baselines",
                "review_thresholds", "full_e2c_reference", "m7b_reference", "modal_gate"):
        checks["unchanged_" + key] = m[key] == old[key]
    checks["unchanged_reviewed_build"] = all(m["canonical_build"][k] == v for k, v in old["canonical_build"].items())
    checks["historical_manifest_immutable"] = sha(root / m["recovery"]["original_manifest"]) == m["recovery"]["original_manifest_sha256"]
    checks["permissions_closed"] = (c["authorization"]["BUILD_AUTHORIZED"] is False
                                     and c["authorization"]["SOLVE_AUTHORIZED"] is False
                                     and c["authorization"].get("active_grant") is None)
    checks["manifest_not_authority"] = m["authorization"] == {"BUILD_AUTHORIZED": False, "SOLVE_AUTHORIZED": False}
    checks["new_packet_identity"] = m["recovery"]["packet_id"] != m["recovery"]["original_consumed_packet_id"]
    checks["fresh_output_identity"] = m["execution"]["target_root"] != old["execution"]["target_root"]
    checks["single_invocation_no_retry"] = m["execution"]["formal_solver_budget"] == 1 and m["execution"]["automatic_retries"] == 0
    checks["storage_floor"] = m["storage_policy"]["output_min_free_bytes"] == 32 * 1024 ** 3 and m["storage_policy"]["temp_min_free_bytes"] == 8 * 1024 ** 3
    for path, expected in m["recovery"]["dependency_sha256"].items():
        checks["sha:" + path] = sha(root / path) == expected
    runner = root / m["execution"]["runner"]
    tree = ast.parse(runner.read_text(encoding="utf-8"))
    solves = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "run_solver"]
    guards = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "require_ready"]
    checks["exactly_one_solver_call"] = len(solves) == 1
    checks["solver_not_in_retry_loop"] = not any(isinstance(n, (ast.For, ast.While)) and any(s in list(ast.walk(n)) for s in solves) for n in ast.walk(tree))
    checks["guards_before_import_and_solve"] = len(guards) == 2 and guards[0].lineno < solves[0].lineno and guards[1].lineno < solves[0].lineno
    checks["no_module_scope_simulator_import"] = not any(isinstance(n, (ast.Import, ast.ImportFrom)) and "cst" in ast.get_source_segment(runner.read_text(), n) for n in tree.body)
    checks["help_without_simulator"] = subprocess.call([sys.executable, "-B", str(runner), "--help"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    pkt = (root / m["execution"]["packet_generator"]).read_text(encoding="utf-8")
    checks["packet_v02_and_native_disk_gate"] = '"schema_version":"runner-task-v0.2"' in pkt and '"type":"min_free_bytes"' in pkt
    checks["packet_requires_live_grant"] = "require_live_grant(c,m,root)" in pkt
    storage = None
    if host:
        checks["windows_host"] = sys.platform == "win32"
        checks.update({"host:" + k: v for k, v in artifact_checks(m, root).items()})
        checks["host_target_absent"] = not Path(m["execution"]["target_root"]).exists()
        storage = storage_check(m["storage_policy"], m["execution"]["target_root"])
        checks["host_storage"] = storage["status"] == "PASS_M7C_STORAGE_PREFLIGHT"
    ok = all(checks.values())
    return {"status": ("PASS" if ok else "HOLD") + "_M7C_RECOVERY_" + ("HOST_READONLY_QUALIFICATION" if host else "OFFLINE_FREEZE"),
            "checks": checks, "manifest_sha256": sha(root / MANIFEST),
            "entrypoint_sha256": sha(runner), "packet_generator_sha256": sha(root / m["execution"]["packet_generator"]),
            "storage": storage, "formal_build_invocations": 0, "formal_solver_invocations": 0,
            "simulator_application_launched": False, "formal_packet_generated": False,
            "live_grant": None, "next_boundary": "REVIEW_PREPARATION_THEN_FRESH_EXPLICIT_SOLVE_AUTHORIZATION"}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--host-readonly", action="store_true")
    ap.add_argument("--output", help="optional nonproduction evidence path; never the frozen formal output root")
    args = ap.parse_args()
    try:
        report = audit(args.project_root, args.host_readonly)
    except Exception as exc:
        report = {"status": "HOLD_M7C_RECOVERY_PREPARATION", "error": str(exc), "formal_solver_invocations": 0}
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        dst = Path(args.output).resolve()
        manifest = json.loads((Path(args.project_root) / MANIFEST).read_text(encoding="utf-8"))
        production = Path(manifest["execution"]["target_root"]).resolve()
        if dst == production or production in dst.parents or dst.exists():
            raise SystemExit("HOLD_M7C_PREPARATION_EVIDENCE_COLLISION")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
    print(text)
    sys.exit(0 if report["status"].startswith("PASS_") else 4)
