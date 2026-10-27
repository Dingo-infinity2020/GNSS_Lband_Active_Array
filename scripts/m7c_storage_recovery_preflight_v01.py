"""Read-only M7C recovery guards; stdlib only, no simulator imports."""
from __future__ import print_function

import datetime
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path

GIB = 1024 ** 3
OUTPUT_FLOOR = 32 * GIB
TEMP_FLOOR = 8 * GIB


def sha(path):
    h = hashlib.sha256()
    with open(str(path), "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def existing_parent(path):
    path = Path(path).resolve()
    while not path.exists():
        if path == path.parent:
            raise RuntimeError("HOLD_M7C_STORAGE_VOLUME_MISSING")
        path = path.parent
    return path


def storage_check(policy, output, temp=None, disk_usage=None, volume_identity=None):
    """Sum reservations when output and TEMP share a filesystem."""
    try:
        output_bytes = policy["output_min_free_bytes"]
        temp_bytes = policy["temp_min_free_bytes"]
        if (type(output_bytes) is not int or type(temp_bytes) is not int
                or output_bytes < OUTPUT_FLOOR or temp_bytes < TEMP_FLOOR):
            raise ValueError("invalid or weakened storage budget")
        usage = disk_usage or shutil.disk_usage
        identity = volume_identity or (lambda p: os.stat(str(p)).st_dev)
        groups = {}
        for role, path, reserve in (("output", output, output_bytes),
                                    ("temp", temp or tempfile.gettempdir(), temp_bytes)):
            ancestor = existing_parent(path)
            key = str(identity(ancestor))
            group = groups.setdefault(key, {"roles": [], "probe_path": str(ancestor),
                                            "required_free_bytes": 0})
            group["roles"].append(role)
            group["required_free_bytes"] += reserve
        for group in groups.values():
            group["free_bytes"] = int(usage(group["probe_path"]).free)
            group["pass"] = group["free_bytes"] >= group["required_free_bytes"]
        ok = all(group["pass"] for group in groups.values())
        return {"status": "PASS_M7C_STORAGE_PREFLIGHT" if ok else "HOLD_M7C_STORAGE_PREFLIGHT",
                "volumes": list(groups.values()), "new_build": False, "new_solve": False}
    except Exception as exc:
        return {"status": "HOLD_M7C_STORAGE_PREFLIGHT", "error": str(exc),
                "new_build": False, "new_solve": False}


def tree_identity(root):
    """SIMOPS_TREE_ID_V1; reject links/reparse/special files, globally sort paths."""
    root = Path(root)
    records = []
    info = root.lstat()
    if not root.is_dir() or root.is_symlink() or getattr(info, "st_file_attributes", 0) & 0x400:
        raise RuntimeError("HOLD_M7C_SOURCE_TREE_MISSING_OR_REPARSE")
    for directory, dirs, files in os.walk(str(root), followlinks=False):
        for name in dirs + files:
            item = Path(directory) / name
            info = item.lstat()
            if (item.is_symlink() or getattr(info, "st_file_attributes", 0) & 0x400
                    or not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode))):
                raise RuntimeError("HOLD_M7C_SOURCE_TREE_SPECIAL_FILE")
            if stat.S_ISREG(info.st_mode):
                records.append((item.relative_to(root).as_posix(), info.st_size, sha(item)))
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError("HOLD_M7C_SOURCE_TREE_MISSING")
    digest = hashlib.sha256()
    for name, size, file_sha in sorted(records):
        digest.update((name + "\0" + str(size) + "\0" + file_sha + "\n").encode("utf-8"))
    return {"algorithm": "SIMOPS_TREE_ID_V1", "tree_sha256": digest.hexdigest(),
            "files": len(records), "bytes": sum(row[1] for row in records)}


def artifact_checks(manifest, root):
    root = Path(root)
    checks = {}
    source = manifest["canonical_build"]
    checks["reviewed_source_sha256"] = sha(source["path"]) == source["sha256"]
    checks["complete_source_companion"] = tree_identity(Path(source["path"]).with_suffix("")) == source["companion_identity"]
    gate = json.loads((root / manifest["execution"]["human_review_gate"]).read_text(encoding="utf-8-sig"))
    checks["human_review"] = (gate["status"] == "PASS_M7C_HUMAN_GEOMETRY_REVIEW"
                               and gate["artifact_sha256"] == source["sha256"])
    refs = [manifest["full_e2c_reference"]]
    checks["full_e2c_reference"] = sha(refs[0]["response_csv"]) == refs[0]["response_csv_sha256"]
    for pol, meta in manifest["isolated_baselines"].items():
        checks["isolated_" + pol] = sha(meta["csv_path"]) == meta["csv_sha256"]
    for path, expected in manifest["recovery"]["dependency_sha256"].items():
        checks[path] = sha(root / path) == expected
    return checks


def require_live_grant(contract, manifest, root):
    auth = contract["authorization"]
    grant = auth.get("active_grant")
    if (auth.get("BUILD_AUTHORIZED") is not False or auth.get("SOLVE_AUTHORIZED") is not True
            or not isinstance(grant, dict)):
        raise RuntimeError("HOLD_M7C_RECOVERY_NO_LIVE_SOLVE_GRANT")
    expected_sha = sha(Path(root) / manifest["execution"]["runner"])
    qualified = contract["execution"].get("entrypoint_qualification", {})
    if (grant.get("kind") != "SOLVE" or grant.get("state") != "GRANTED"
            or grant.get("stage") != manifest["stage"]
            or contract["execution"]["current_stage"] != manifest["stage"]
            or grant.get("source_commit") != contract["project"]["source_commit"]
            or grant.get("entrypoint_sha256") != expected_sha
            or qualified.get("entrypoint_sha256") != expected_sha
            or qualified.get("last_qualified_source_commit") != grant.get("source_commit")
            or qualified.get("qualification_status") != "PASS_M7C_RECOVERY_NONPRODUCTION_HOST_QUALIFICATION"
            or grant.get("grant_id") in {g["grant_id"] for g in contract.get("authorization_history", [])}):
        raise RuntimeError("HOLD_M7C_RECOVERY_GRANT_IDENTITY")
    if grant.get("expires_at"):
        expiry = datetime.datetime.strptime(grant["expires_at"], "%Y-%m-%dT%H:%M:%SZ")
        if expiry <= datetime.datetime.utcnow():
            raise RuntimeError("HOLD_M7C_RECOVERY_GRANT_EXPIRED")
    return grant


def require_source_ancestor(contract, root):
    # The later authorization commit changes the contract itself. Bind the
    # qualified source as an ancestor; native packet preflight binds exact HEAD.
    result = subprocess.call(["git", "-C", str(root), "merge-base", "--is-ancestor",
                              contract["project"]["source_commit"], "HEAD"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result != 0:
        raise RuntimeError("HOLD_M7C_RECOVERY_SOURCE_COMMIT")


def require_ready(manifest, root, out, evidence, fresh):
    """Called before any simulator import/copy and again before the single solve."""
    root = Path(root)
    contract = json.loads((root / "execution/stage_contract.json").read_text(encoding="utf-8-sig"))
    require_live_grant(contract, manifest, root)
    require_source_ancestor(contract, root)
    target = Path(manifest["execution"]["target_root"])
    if (Path(out).resolve() != (target / manifest["execution"]["artifact_name"]).resolve()
            or Path(evidence).resolve() != (target / "evidence").resolve()):
        raise RuntimeError("HOLD_M7C_RECOVERY_OUTPUT_IDENTITY")
    if fresh and target.exists():
        raise RuntimeError("HOLD_M7C_RECOVERY_TARGET_EXISTS")
    checks = artifact_checks(manifest, root)
    if not all(checks.values()):
        raise RuntimeError("HOLD_M7C_RECOVERY_DEPENDENCY_IDENTITY:" + ",".join(k for k, v in checks.items() if not v))
    report = storage_check(manifest["storage_policy"], target)
    if report["status"] != "PASS_M7C_STORAGE_PREFLIGHT":
        raise RuntimeError(json.dumps(report, sort_keys=True))
    return report
