#!/usr/bin/env python3
"""Gate R0 geometry construction on explicit parameter provenance.

This script never runs CST. It validates the R0 parameter manifest and emits a
machine-readable status for either:

- topology: zero-thickness PEC topology build only
- materialized: dielectric/copper build preparation

A PASS from this script is not permission to run a solver.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ALLOWED_PROVENANCE = {
    "PAPER_EXPLICIT",
    "FIGURE_DERIVED_UNVERIFIED",
    "ASSUMPTION",
    "MEASURED",
    "OPTIMIZED",
}

TOPOLOGY_REQUIRED = {
    "height_ground",
    "feed_center_gap",
    "petal_span",
    "ring_outer_size",
    "petal_geometry",
    "petal_slit",
    "ring_trace_width",
    "ground_xy_size",
}

MATERIALIZED_EXTRA = {
    "pcb_outer_size",
    "substrate_material",
    "substrate_thickness",
    "copper_thickness",
}

UNRESOLVED_VALUES = {"", "UNKNOWN", "TBD"}
UNRESOLVED_STATUSES = {"OPEN"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "manifest",
        nargs="?",
        default="em/cst/R0_CHARTS_300_500/parameters.csv",
    )
    parser.add_argument(
        "--stage",
        choices=("topology", "materialized"),
        default="topology",
    )
    args = parser.parse_args()

    path = Path(args.manifest)
    if not path.exists():
        print("HOLD_R0_MANIFEST_MISSING")
        return 2

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    by_name = {row["parameter"]: row for row in rows}
    errors: list[str] = []

    for row in rows:
        prov = row.get("provenance", "")
        if prov not in ALLOWED_PROVENANCE:
            errors.append(f"{row.get('parameter')}:invalid_provenance={prov}")

    required = set(TOPOLOGY_REQUIRED)
    if args.stage == "materialized":
        required |= MATERIALIZED_EXTRA

    for name in sorted(required - set(by_name)):
        errors.append(f"{name}:missing_parameter")

    unresolved = []
    for name in sorted(required & set(by_name)):
        row = by_name[name]
        value = (row.get("value") or "").strip().upper()
        status = (row.get("status") or "").strip().upper()
        if value in UNRESOLVED_VALUES or status in UNRESOLVED_STATUSES:
            unresolved.append(name)

    if errors:
        print("HOLD_R0_MANIFEST_INVALID")
        for item in errors:
            print(f"- {item}")
        return 3

    if unresolved:
        print(f"HOLD_R0_{args.stage.upper()}_PARAMETERS_UNRESOLVED")
        for name in unresolved:
            row = by_name[name]
            print(
                f"- {name}: value={row.get('value')} "
                f"provenance={row.get('provenance')} status={row.get('status')}"
            )
        return 4

    optimized = [
        row["parameter"]
        for row in rows
        if row.get("provenance") == "OPTIMIZED"
        and row["parameter"] in required
    ]
    if optimized:
        print("HOLD_R0_OPTIMIZED_PARAMETERS_PRESENT")
        for name in optimized:
            print(f"- {name}")
        return 5

    if args.stage == "topology":
        print("PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY")
    else:
        print("PASS_R0_MATERIALIZED_MANIFEST_READY_FOR_BUILD_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
