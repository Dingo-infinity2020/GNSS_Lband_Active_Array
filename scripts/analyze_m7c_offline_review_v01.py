"""Read existing CSVs/native logs; never imports CST or changes a simulation.

Inputs are downloaded byte-for-byte from protected NW results.  The production
evaluator remains unchanged; supplemental diagnostics do not reclassify M7C.
"""
import argparse
import cmath
import csv
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import evaluate_m7c_modal_restoration_readonly_v01 as frozen

REPO = Path(__file__).resolve().parents[1]
WINDOW = (1.2088, 1.2584)
MODELS = ("full_E2C", "M7B", "M7C")


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save_json(p, value):
    p.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def save_csv(p, rows):
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def trace_stats(f, d, ij, idx):
    low = min(idx, key=lambda k: abs(d[ij][k]))
    high = max(idx, key=lambda k: abs(d[ij][k]))
    return {"min_db": frozen.db(d[ij][low]), "min_f_ghz": f[low],
            "max_db": frozen.db(d[ij][high]), "max_f_ghz": f[high],
            "excursion_db": frozen.db(d[ij][high]) - frozen.db(d[ij][low]),
            "max_abs_s": abs(d[ij][high])}


def guard_ranking(candidate, reference, f):
    idx = [k for k, x in enumerate(f) if 1.15 <= x <= 1.65]
    out = []
    for ij in candidate:
        if ij[0] == ij[1]:
            continue
        c = [frozen.db(candidate[ij][k]) for k in idx]
        r = [frozen.db(reference[ij][k]) for k in idx]
        best = None
        b = 0
        for a in range(len(idx)):
            b = max(a, b)
            while b + 1 < len(idx) and f[idx[b+1]] - f[idx[a]] <= .05 + 1e-12:
                b += 1
            if b <= a:
                continue
            gain = max(c[a:b+1]) - min(c[a:b+1]) - max(r[a:b+1]) + min(r[a:b+1])
            if best is None or gain > best["new_excursion_db"]:
                best = {"response_port": ij[0], "source_port": ij[1],
                        "new_excursion_db": gain, "start_ghz": f[idx[a]], "end_ghz": f[idx[b]]}
        out.append(best)
    return sorted(out, key=lambda x: -x["new_excursion_db"])


def macro_blocks(text, kind):
    for m in re.finditer(r"With " + kind + r"\b(.*?)End With", text, re.S):
        fields = {}
        for line in m.group(1).splitlines():
            match = re.match(r"\s*\.(\w+)\s+(.*)", line)
            if match:
                fields.setdefault(match[1], []).append(re.findall(r'"([^"\n]*)"', match[2]))
        yield fields


def main(raw, out, plots):
    out.mkdir(parents=True, exist_ok=False)
    transfer = json.loads((raw / "TRANSFER_RECEIPT.json").read_text())
    for n, item in transfer.items():
        assert digest(raw / (n + ".csv")) == item["sha256"], n
        if item["expected_sha256"]:
            assert item["sha256"] == item["expected_sha256"], n
    data = {n: frozen.read96(raw / (n + ".csv")) for n in MODELS}
    assert all(len(d) == 96 and all(math.isfinite(z.real) and math.isfinite(z.imag)
                                   for curve in d.values() for z in curve)
               for _, d in data.values())
    f = data["M7C"][0]
    assert len(f) == 1001 and all(f == x[0] for x in data.values())
    bases = {}
    for pol in ("A", "B"):
        bf, bd = frozen.read16(raw / ("isolated_" + pol + ".csv"))
        assert bf == f
        bases[pol] = bd
    manifest = json.loads((REPO / "execution/M7C_STORAGE_RECOVERY_SOLVE_MANIFEST_V01.json").read_text())
    prior = json.loads((REPO / "evidence/M7C_STORAGE_RECOVERY_SOLVE_20261026/evidence__modal__modal_evaluation.json").read_text())
    gd = frozen.guard(data["M7C"][1], data["full_E2C"][1], f, 6, .05)
    assert gd == prior["guard"]
    old_guard = frozen.guard(data["M7B"][1], data["full_E2C"][1], f, 6, .05)
    assert abs(old_guard["new_excursion_db"] - 1.9112812691476933) < 1e-10
    ranking = guard_ranking(data["M7C"][1], data["full_E2C"][1], f)
    assert abs(ranking[0]["new_excursion_db"] - gd["new_excursion_db"]) < 1e-12
    idx = [k for k, x in enumerate(f) if WINDOW[0]-1e-12 <= x <= WINDOW[1]+1e-12]
    window, curve_rows = {}, []
    traces = ((2, 5), (5, 2), (8, 11), (11, 8))
    for n in MODELS:
        d = data[n][1]
        window[n] = {"S%d_%d" % ij: trace_stats(f, d, ij, idx) for ij in traces}
        k = max(idx, key=lambda k: abs(d[(2, 5)][k] - d[(5, 2)][k]))
        window[n]["pair_2_5_reciprocity"] = {
            "max_abs_complex_difference": abs(d[(2, 5)][k] - d[(5, 2)][k]),
            "frequency_ghz": f[k],
            "db_forward": frozen.db(d[(2, 5)][k]), "db_reverse": frozen.db(d[(5, 2)][k])}
        for k in idx:
            row = {"model": n, "f_ghz": f[k]}
            for ij in traces:
                z = d[ij][k]
                key = "S%d_%d" % ij
                row.update({key+"_real": z.real, key+"_imag": z.imag,
                            key+"_db": frozen.db(z), key+"_phase_deg": math.degrees(cmath.phase(z))})
            curve_rows.append(row)
    save_csv(out / "GUARD_WINDOW_COMPLEX.csv", curve_rows)
    save_csv(out / "GUARD_TRACE_RANKING.csv", ranking)
    failing_windows = []
    for item in ranking:
        if item["new_excursion_db"] <= 6:
            continue
        ij = item["response_port"], item["source_port"]
        ii = [k for k, x in enumerate(f) if item["start_ghz"]-1e-12 <= x <= item["end_ghz"]+1e-12]
        failing_windows.append({**item, "model_window_stats": {
            n: trace_stats(f, data[n][1], ij, ii) for n in MODELS}})
    save_json(out / "ALL_FAILING_GUARD_TRACES.json", failing_windows)

    # Independent two-terminal identities cross-check the frozen 4x4 transform.
    modal, spectrum = [], []
    decomposition_error = 0.0
    for pol, cp in (("A", (1, 2, 4, 5)), ("B", (7, 8, 10, 11))):
        ep, _, en, _ = cp
        base = bases[pol]
        for n in MODELS:
            d = data[n][1]
            for k, x in enumerate(f):
                dd = frozen.mode_dd(d, k, cp) - frozen.mode_dd(base, k, (1, 2, 4, 5))
                dc = frozen.mode_dc(d, k, cp) - frozen.mode_dc(base, k, (1, 2, 4, 5))
                a = ((d[(ep,ep)][k]-base[(1,1)][k]) + (d[(en,en)][k]-base[(4,4)][k])) / 2
                mutual = ((d[(ep,en)][k]-base[(1,4)][k]) + (d[(en,ep)][k]-base[(4,1)][k])) / 2
                asym = ((d[(ep,ep)][k]-base[(1,1)][k]) - (d[(en,en)][k]-base[(4,4)][k])) / 2
                nonrec = ((d[(en,ep)][k]-base[(4,1)][k]) - (d[(ep,en)][k]-base[(1,4)][k])) / 2
                decomposition_error = max(decomposition_error, abs(dd-(a-mutual)), abs(dc-(asym+nonrec)))
                if 1.15 <= x <= 1.65:
                    spectrum.append({"model": n, "pol": pol, "f_ghz": x, "delta_sdc_abs": abs(dc),
                                     "delta_sdd_abs": abs(dd), "self_average_abs": abs(a),
                                     "mutual_average_abs": abs(mutual), "self_asymmetry_abs": abs(asym),
                                     "nonreciprocal_term_abs": abs(nonrec)})
                if any(abs(x-y) < 1e-9 for y in manifest["modal_gate"]["symmetry"]["anchors_ghz"]):
                    modal.append({"model": n, "pol": pol, "f_ghz": x,
                                  "delta_sdc_abs": abs(dc), "delta_sdd_abs": abs(dd),
                                  "self_average_abs": abs(a), "mutual_average_abs": abs(mutual),
                                  "self_asymmetry_abs": abs(asym), "nonreciprocal_term_abs": abs(nonrec)})
    assert decomposition_error < 1e-14
    for item in prior["symmetry"]:
        row = next(x for x in modal if x["model"] == "M7C" and x["pol"] == item["polarization"][-1]
                   and abs(x["f_ghz"]-item["frequency_ghz"]) < 1e-9)
        assert abs(row["delta_sdc_abs"]-item["candidate_delta_sdc"]) < 1e-12
    for item in prior["differential_restoration"]:
        pol, x = item["polarization"][-1], item["frequency_ghz"]
        row = next(r for r in modal if r["model"] == "M7B" and r["pol"] == pol and abs(r["f_ghz"]-x) < 1e-9)
        assert abs(row["delta_sdd_abs"]-item["m7b_delta_sdd"]) < 1e-12
    save_csv(out / "MODAL_ANCHORS.csv", modal)
    save_csv(out / "MODAL_SPECTRUM.csv", spectrum)

    # Compare actual raw port coordinates to the frozen raw->solve manifest.
    macro = (REPO / "source/cst/R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_BUILD_ONLY_V01.mcr").read_text()
    ports = {int(b["PortNumber"][0][0]): b for b in macro_blocks(macro, "DiscretePort")}
    errors = []
    rotation = []
    for item in manifest["raw_to_solve"]:
        b = ports[item["raw"]]
        for field, label in (("SetP1", "p1"), ("SetP2", "p2")):
            errors.extend(abs(float(a)-z) for a, z in zip(b[field][0][-3:], item[label]))
        assert b["InvertDirection"][0] == ["False"]
    for a, b in zip(manifest["raw_to_solve"][:6], manifest["raw_to_solve"][6:]):
        for key in ("p1", "p2"):
            x, y, z = a[key]
            rotation.extend(abs(u-v) for u, v in zip((-y, x, z), b[key]))
    assert max(errors) < 1e-12 and max(rotation) < 1e-12
    extrudes = {b["Component"][0][0]+":"+b["Name"][0][0]: b for b in macro_blocks(macro, "Extrude")}
    local_differences, pairs = [], 0
    for name, a in extrudes.items():
        if not name.startswith("E2C_A_"):
            continue
        bname = name.replace("E2C_A_", "E2C_B_", 1)
        b = extrudes[bname]
        pairs += 1
        for key in ("Material", "Height", "Point", "LineTo", "Vvector"):
            if a.get(key) != b.get(key):
                local_differences.append({"a": name, "b": bname, "field": key})
        for key in ("Origin", "Uvector"):
            x, y, z = map(float, a[key][0])
            assert max(abs(u-float(v)) for u, v in zip((-y, x, z), b[key][0])) < 1e-12
    assert {x["b"] for x in local_differences} == {"E2C_B_N_BackGround:LOCAL_BACK_GROUND"}
    moat_text = (REPO / "source/cst/R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7C_LOCAL_RETURN_ISLAND_BUILD_ONLY_V01.mcr").read_text()
    moat = {b["Name"][0][0]: b for b in macro_blocks(moat_text, "Extrude")}
    for name, a in moat.items():
        if "_A_" not in name:
            continue
        b = moat[name.replace("_A_", "_B_")]
        for key in ("Height", "Point", "LineTo", "Vvector"):
            assert a[key] == b[key]
        for key in ("Origin", "Uvector"):
            x, y, z = map(float, a[key][0])
            assert max(abs(u-float(v)) for u, v in zip((-y, x, z), b[key][0])) < 1e-12
    geometry = {"paired_landing_zone_extrudes": pairs,
                "local_A_B_differences": local_differences,
                "difference_authority": "frozen B_N half-lap notch, v=12..13, u=-1..-1.125 mm",
                "M7C_moat_tools": len(moat), "M7C_A_B_local_cutters_identical": True,
                "limits": "static source audit; no new kernel geometry or current distribution claim"}
    save_json(out / "STATIC_GEOMETRY_AUDIT.json", geometry)

    # Native Problematic Positions are auxiliary geometry, read without CST.
    positions, warnings, samples = [], {}, {}
    for n in MODELS:
        text = (raw / (n+"_output.txt")).read_text(errors="replace")
        warnings[n] = {"thin_pec_edge_warning": "infinitely thin PEC wires" in text,
                       "partial_excitation_yz_warning": "No calculation of YZ Matrices possible" in text}
        # Earlier mesh passes may repeat samples; retain the final broadband block.
        tail = text[text.rfind("Mesh adaptation terminated"):]
        samples[n] = [1.8] + [float(x) for x in re.findall(r"Sample \d+ \(([\d.]+) GHz\)", tail)]
        for node in ET.parse(raw / (n+"__TetMesherError.axg")).findall(".//Sphere"):
            x, y, z = map(float, node.attrib["position"].split())
            positions.append({"model": n, "x_mm": x, "y_mm": y, "z_mm": z,
                              "v_from_radiator_mm": 57.1428571428-z,
                              "in_moat_z_span": 57.1428571428-7.65-1e-5 <= z <= 57.1428571428-3.9+1e-5})
    assert not any(p["in_moat_z_span"] for p in positions)
    save_csv(out / "NATIVE_PROBLEMATIC_POSITIONS.csv", positions)
    summary = {
        "schema_version": "gnss-m7c-offline-review-v0.1", "science_status_unchanged": "HOLD_M7C_GUARD",
        "build_authorized": False, "solve_authorized": False, "simulator_applications_launched": 0,
        "solver_invocations": 0, "input_csvs": transfer,
        "native_grid_identical": True, "native_points": len(f), "frozen_guard_reproduced": gd,
        "M7B_previous_guard_reproduced": old_guard,
        "guard_window": window, "guard_ranking_top10": ranking[:10],
        "failing_guard_trace_count": len(failing_windows), "static_geometry_audit": geometry,
        "modal_identity_max_complex_error": decomposition_error,
        "port_endpoint_max_error_mm": max(errors), "port_A_to_B_rotation_max_error_mm": max(rotation),
        "native_warnings": warnings, "native_direct_sample_frequencies_ghz": samples,
        "problematic_positions": {n: {"count": sum(p["model"] == n for p in positions),
                                        "inside_moat_z_span": 0,
                                        "z_values_mm": sorted({p["z_mm"] for p in positions if p["model"] == n})}
                                  for n in MODELS},
        "limits": ["weak-curve reciprocity is a diagnostic, not a replacement for the frozen absolute gate",
                   "1001 native output points are not 1001 directly solved frequency samples",
                   "Problematic Positions do not provide individual PEC edge IDs or prove causality",
                   "source geometry records do not establish RF current distributions"]}
    save_json(out / "ANALYSIS.json", summary)
    save_json(out / "INPUT_RECEIPT.json", transfer)
    if plots:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        matplotlib.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "m7c-review-v01", "font.size": 10})
        fig, ax = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
        for n in MODELS:
            d = data[n][1]
            for a, ij in zip(ax[0], ((2,5), (5,2))):
                a.plot([f[k] for k in idx], [frozen.db(d[ij][k]) for k in idx], label=n)
                a.set(title="S%d,%d native broadband output" % ij, ylabel="20 log10 |S| (dB)", xlabel="Frequency (GHz)")
            for a, ij in zip(ax[1], ((2,5), (5,2))):
                a.plot([f[k] for k in idx], [math.degrees(cmath.phase(d[ij][k])) for k in idx], label=n)
                a.set(title="S%d,%d phase (wrapped)" % ij, ylabel="Phase (degrees)", xlabel="Frequency (GHz)")
        for a in ax.flat:
            a.grid(alpha=.25)
            a.legend(fontsize=8)
        fig.suptitle("M7C Guard review: weak coupling and directional inconsistency; original HOLD retained")
        fig.savefig(out / "GUARD_REVIEW.svg", metadata={"Date": None})
        fig.savefig(raw / "GUARD_REVIEW.png", dpi=140)
        plt.close(fig)
        fig, ax = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
        for pol, a in zip(("A", "B"), ax):
            for n in MODELS:
                rows = [r for r in spectrum if r["pol"] == pol and r["model"] == n]
                a.plot([r["f_ghz"] for r in rows], [r["delta_sdc_abs"] for r in rows], label=n)
            a.set(title="Pol-"+pol, xlabel="Frequency (GHz)", ylabel="|Delta Sdc| vs isolated baseline")
            a.grid(alpha=.25)
            a.legend()
        fig.suptitle("M7C symmetry failure remains independent of the weak S2,5 Guard feature")
        fig.savefig(out / "POLARIZATION_REVIEW.svg", metadata={"Date": None})
        fig.savefig(raw / "POLARIZATION_REVIEW.png", dpi=140)
        plt.close(fig)
        save_json(out / "PLOT_TOOLCHAIN.json", {"python": sys.version, "matplotlib": matplotlib.__version__})
    print(json.dumps({"guard": gd, "window": window["M7C"], "output": str(out)}, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--plots", action="store_true")
    args = ap.parse_args()
    main(args.raw_dir, args.output, args.plots)
