#!/usr/bin/env python3
"""Static audit for the REF-CUI-R0B deterministic BUILD-ONLY CST macro.

This does not execute CST. It enforces the build-only contract before any
CST run.
"""

from __future__ import annotations

import argparse
from pathlib import Path

TWENTY_SIX = (
    "Lg", "H", "Lr", "Wr", "Ld", "Ws", "Ls", "Wg1", "Wg2", "Wp",
    "Lp1", "Lp2", "Lp3",
    "Lb1", "Lb2", "Lb3", "Lb4", "Lb5",
    "Wb1", "Wb2", "Wb3", "Wb4", "Wb5", "Wb6", "Wb7", "Wb8",
)

FORBIDDEN = (
    "StartSolver",
    ".Start",
    "Optimizer.",
    "ParameterSweep",
    "Sweep.",
    "AdaptiveMesh",
    "DiscretePort",
    "WaveguidePort",
    "FloquetPort",
    "LumpedElement",
    "Monitor.",
    "LNA",
    "QPL9547",
    "BiasTee",
    "Bias-Tee",
    "PETAL",
    "RING_",
    "CHARTS",
    "GNSS",
    "Lband",
    "L_band",
    "center_opening",
    "Optimize",
)

REQUIRED_MARKERS = (
    '.Name "Rogers_4350B"',
    '.Epsilon "er"',
    'StoreParameter "er", 3.48',
    'StoreParameter "sub_t", 0.76',
    '.Name "GROUND"',
    '.Name "LOOP"',
    '.Name "ARMS"',
    '.Name "BALUN1_SUB"',
    '.Name "BALUN2_SUB"',
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "macro",
        nargs="?",
        default="source/cst/REF_CUI_R0B_BUILD_ONLY_V01.mcr",
    )
    args = ap.parse_args()
    path = Path(args.macro)

    if not path.exists():
        print("HOLD_REF_CUI_R0B_MACRO_MISSING")
        return 2

    text = path.read_text(encoding="utf-8")
    failures: list[str] = []

    # Scan executable code only; ignore full-line VBA comments so documentation
    # may still name prohibited concepts.
    code_text = "\n".join(
        line for line in text.splitlines() if not line.strip().startswith("'")
    )

    for token in FORBIDDEN:
        if token in code_text:
            failures.append(f"forbidden_token:{token}")

    for symbol in TWENTY_SIX:
        if f'StoreParameter "{symbol}"' not in text:
            failures.append(f"missing_parameter:{symbol}")

    for marker in REQUIRED_MARKERS:
        if marker not in text:
            failures.append(f"missing_marker:{marker}")

    if "Sub Main()" not in text or "End Sub" not in text:
        failures.append("missing_flat_main")

    helper_lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip().lower().startswith(("sub ", "function "))
        and line.strip().lower() != "sub main()"
    ]
    if helper_lines:
        failures.append("helper_procedure_present:" + ",".join(helper_lines))

    if text.count("Sub Main()") != 1:
        failures.append("expected_exactly_one_sub_main")

    non_ascii = sorted({ch for ch in text if ord(ch) > 127})
    if non_ascii:
        failures.append("non_ascii_present:" + repr(non_ascii))

    if failures:
        print("HOLD_REF_CUI_R0B_MACRO_STATIC_AUDIT")
        for item in failures:
            print(f"- {item}")
        return 3

    print("PASS_REF_CUI_R0B_MACRO_STATIC_AUDIT")
    print("EXPECTED_SOURCE_PARAMETERS=26")
    print("EXPECTED_PORTS=0")
    print("EXPECTED_SOLVER_RUN=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
