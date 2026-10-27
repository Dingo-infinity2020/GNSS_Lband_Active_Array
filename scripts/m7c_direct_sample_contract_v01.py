"""Stdlib-only guards and pre-registered direct-sample diagnostic logic."""
from __future__ import print_function
import datetime
import json
import math
import re
from pathlib import Path
from m7c_storage_recovery_preflight_v01 import (sha, artifact_checks, storage_check,
                                               require_source_ancestor)

FREQUENCIES = (1.152,1.1544,1.1728,1.1736,1.18,1.2016,1.204,1.2088,
               1.2096,1.2104,1.2112,1.2144,1.2328,1.2448,1.2584)
STAGE = "R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7C_DIRECT_SAMPLE_DIAGNOSTIC_V01"
QUALIFIED = "PASS_M7C_DIRECT_SAMPLE_NONPRODUCTION_HOST_QUALIFICATION"
SOURCES = (1,2,4,5,7,8,10,11)


def require_live_grant(contract, manifest, root):
    auth = contract["authorization"]
    g = auth.get("active_grant")
    q = contract["execution"].get("entrypoint_qualification", {})
    if (auth.get("BUILD_AUTHORIZED") is not False or auth.get("SOLVE_AUTHORIZED") is not True
            or not isinstance(g, dict)):
        raise RuntimeError("HOLD_M7C_DIRECT_NO_LIVE_SOLVE_GRANT")
    if (g.get("kind") != "SOLVE" or g.get("state") != "GRANTED"
            or g.get("stage") != STAGE or manifest["stage"] != STAGE
            or contract["execution"]["current_stage"] != STAGE
            or g.get("source_commit") != contract["project"]["source_commit"]
            or g.get("entrypoint_sha256") != sha(Path(root)/manifest["execution"]["runner"])
            or q.get("entrypoint_sha256") != g.get("entrypoint_sha256")
            or q.get("last_qualified_source_commit") != g.get("source_commit")
            or q.get("qualification_status") != QUALIFIED
            or g.get("grant_id") in {x["grant_id"] for x in contract.get("authorization_history", [])}):
        raise RuntimeError("HOLD_M7C_DIRECT_GRANT_IDENTITY")
    if g.get("expires_at") and datetime.datetime.strptime(g["expires_at"],"%Y-%m-%dT%H:%M:%SZ") <= datetime.datetime.utcnow():
        raise RuntimeError("HOLD_M7C_DIRECT_EXPIRED_GRANT")
    return g


def sample_intervals(text):
    return [(float(a),float(b),int(n),kind.lower(),adapt.lower()=="true")
            for a,b,n,kind,adapt in re.findall(
                r'\.AddSampleInterval\s+"([\d.]+)",\s*"([\d.]+)",\s*"(\d+)",\s*"([^"]+)",\s*"([^"]+)"',text)]


def require_direct_config(text):
    methods = re.findall(r'\.SetMethod\s+"([^"]+)",\s*"([^"]+)"',text)
    expected = [(1.8,1.8,1,"single",True)] + [(f,f,1,"single",False) for f in FREQUENCIES]
    if (methods != [("Tetrahedral","Discrete samples only")]
            or text.count('.ResetSampleIntervals "all"') != 1
            or sample_intervals(text) != expected):
        raise RuntimeError("HOLD_M7C_DIRECT_SAMPLING_CONFIG")
    if any(x in text for x in ('.AccuracyTet', '.Type "Direct"', '.Type "Iterative"',
                                'ForceRecalculateOldSamples', 'UpdateInterpolationSettings')):
        raise RuntimeError("HOLD_M7C_DIRECT_UNFROZEN_SOLVER_DELTA")
    return True


def require_ready(m, root, out, evidence, fresh):
    root = Path(root)
    c = json.loads((root/"execution/stage_contract.json").read_text(encoding="utf-8-sig"))
    require_live_grant(c,m,root)
    require_source_ancestor(c,root)
    target = Path(m["execution"]["target_root"])
    if (Path(out).resolve() != (target/m["execution"]["artifact_name"]).resolve()
            or Path(evidence).resolve() != (target/"evidence").resolve()
            or (fresh and target.exists())):
        raise RuntimeError("HOLD_M7C_DIRECT_OUTPUT_IDENTITY_OR_EXISTS")
    if tuple(m["direct_sample_diagnostic"]["frequencies_ghz"]) != FREQUENCIES:
        raise RuntimeError("HOLD_M7C_DIRECT_FREQUENCY_FREEZE")
    checks = artifact_checks(m,root)
    ref = m["direct_sample_diagnostic"]["comparison_csv"]
    checks["comparison_csv"] = sha(ref["path"]) == ref["sha256"]
    if not all(checks.values()):
        raise RuntimeError("HOLD_M7C_DIRECT_INPUT_HASH:"+str([k for k,v in checks.items() if not v]))
    require_direct_config((root/m["execution"]["config_macro"]).read_text(encoding="utf-8"))
    report = storage_check(m["storage_policy"],target)
    if report["status"] != "PASS_M7C_STORAGE_PREFLIGHT":
        raise RuntimeError(json.dumps(report))
    return report


def native_frequencies(text):
    values = re.findall(r'(?:Mesh adaptation sample \d+ of \d+|Sample \d+)\s*\(([\d.eE+-]+) GHz\)',text,re.I)
    return sorted(set(float(x) for x in values))


def native_deltas(text):
    return [float(x) for x in re.findall(r'All\s+S-Parameters\s*=\s*([\d.eE+-]+)',text,re.I)]


def exact_index(frequencies, target):
    idx = [k for k,x in enumerate(frequencies) if abs(x-target) <= 1e-9]
    if len(idx) != 1:
        raise RuntimeError("HOLD_MISSING_OR_DUPLICATE_DIRECT_SAMPLE:"+str(target))
    return idx[0]


def classify(frequencies, direct, old_f, old, numerical_pass):
    idx = [exact_index(frequencies,x) for x in FREQUENCIES]
    max_recip = max(abs(direct[(2,5)][k]-direct[(5,2)][k]) for k in idx)
    k = exact_index(frequencies,1.2096)
    oldk = exact_index(old_f,1.2096)
    peak = 7.867156165947698e-5
    changes = [abs(direct[ij][k]-old[ij][oldk]) for ij in ((2,5),(5,2))]
    nearby = [exact_index(frequencies,x) for x in (1.2088,1.2096,1.2104,1.2112)]
    suppressed = all(abs(direct[ij][j]) <= .5*peak for ij in ((2,5),(5,2)) for j in nearby)
    reproduced = all(abs(direct[ij][k]) >= .8*peak for ij in ((2,5),(5,2)))
    if not numerical_pass:
        status = "HOLD_M7C_DIRECT_NUMERICAL_OR_PROVENANCE"
    elif max_recip <= 1e-6 and max(changes) >= 1e-5 and suppressed:
        status = "H_NUM_SUPPORTED_M7C_DIRECT_SAMPLE"
    elif max_recip <= 1e-6 and reproduced:
        status = "FEATURE_REPRODUCED_M7C_DIRECT_SAMPLE"
    else:
        status = "INCONCLUSIVE_HOLD_M7C_DIRECT_SAMPLE"
    return {"status":status,"numerical_pass":numerical_pass,"max_primary_pair_reciprocity_abs":max_recip,
            "budget_abs":1e-6,"at_peak_change_vs_old_abs":changes,
            "near_peak_both_directions_lte_half_old_peak":suppressed,
            "at_peak_both_directions_gte_0p8_old_peak":reproduced,
            "at_peak_direct_abs":[abs(direct[ij][k]) for ij in ((2,5),(5,2))],
            "science_status_unchanged":"HOLD_M7C_GUARD",
            "boundary":"No geometry change, full-band reclassification, retry or automatic next stage."}
