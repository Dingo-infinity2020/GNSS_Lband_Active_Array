#!/usr/bin/env python3
from pathlib import Path
import hashlib, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
PY=sys.executable

EXPECTED={
 ROOT/"source/cst/R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.mcr":"1e5bb3188c5d19146b673ec54372d0c35ae572abc775512529f71db71cfad5be",
 ROOT/"source/cst/R1A5F_POLA_SINGLE_PORT_BUILD_ONLY_V01.mcr":"f2b4555413005596f5fa8ceefacc64b7cadbba2cce1c430f0c9c713a6f7aead9",
 ROOT/"source/cst/R1E0A_PERIODIC_BROADSIDE_BUILD_ONLY_V01.mcr":"eaa9c714978c76381424747307d635397084078ddbf235103d54c3b51275f7ff",
 ROOT/"source/cst/R1E1A0R1_PITCH_READY_R1A3_GEOMETRY_V01.mcr":"6f54dc6b7e73160f48a974e214fa481773f0d342a80bdb1242d0316fa39be6b7",
 ROOT/"source/cst/R1E1A0R1_PARAMETER_READY_PERIODIC_BROADSIDE_V01.mcr":"b96469c62337f1dab9cb71a0bcdb7a7666e8ec558ee4f937c565d75a66e0de54",
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

fail=[]
for p,s in EXPECTED.items():
    if not p.exists(): fail.append("missing:"+str(p))
    elif sha(p)!=s: fail.append("hash_mismatch:"+str(p)+":"+sha(p))

# Deterministic generator must reproduce the checked-in derived macros exactly.
g=ROOT/"scripts/generate_r1e1a0r1_pitch_ready_macros.py"
if not g.exists():
    fail.append("missing_generator")
else:
    r=subprocess.call([PY,str(g),"--check"],cwd=str(ROOT))
    if r!=0: fail.append("generator_check_failed")

geom=(ROOT/"source/cst/R1E1A0R1_PITCH_READY_R1A3_GEOMETRY_V01.mcr").read_text(encoding="utf-8")
periodic=(ROOT/"source/cst/R1E1A0R1_PARAMETER_READY_PERIODIC_BROADSIDE_V01.mcr").read_text(encoding="utf-8")
harness=(ROOT/"scripts/run_r1e1a0r1_pitch_ready_source_build_only_dc.py").read_text(encoding="utf-8")
contract=(ROOT/"docs/R1E1A0R1_PITCH_READY_CANONICAL_SOURCE_CONTRACT.md").read_text(encoding="utf-8")
runbook=(ROOT/"em/cst/R1_CHARTS_LBAND/RUNBOOK_R1E1A0R1_PITCH_READY_SOURCE_BUILD_ONLY.md").read_text(encoding="utf-8")

for req in (
  'MakeSureParameterExists "unit_cell_pitch_nominal", "94.0"',
  'MakeSureParameterExists "ground_reference_span", "unit_cell_pitch_nominal"',
):
    if req not in geom: fail.append("geometry_missing:"+req)
for forbidden in (
  'StoreParameter "unit_cell_pitch_nominal"',
  'StoreParameter "ground_reference_span"',
):
    if forbidden in geom: fail.append("geometry_forbidden:"+forbidden)

for req in (
  'MakeSureParameterExists "R1E0_pitch_nominal_mm", "unit_cell_pitch_nominal"',
  'MakeSureParameterExists "R1E0_scan_theta_deg", "0.0"',
  'MakeSureParameterExists "R1E0_scan_phi_deg", "45.0"',
  '.SetPeriodicBoundaryAngles "R1E0_scan_theta_deg", "R1E0_scan_phi_deg"',
  '.UnitCellFitToBoundingBox "True"',
):
    if req not in periodic: fail.append("periodic_missing:"+req)
for forbidden in (
  'StoreParameter "R1E0_pitch_nominal_mm"',
  'StoreParameter "R1E0_scan_theta_deg"',
  'StoreParameter "R1E0_scan_phi_deg"',
):
    if forbidden in periodic: fail.append("periodic_forbidden:"+forbidden)

for req in (
  "de.new_mws()",
  'add_to_history("R1E1A0-R1 pitch-ready R1A3 geometry"',
  'add_to_history("R1E1A0-R1 frozen R1A5F Pol-A single port"',
  'add_to_history("R1E1A0-R1 parameter-ready periodic broadside"',
  "prj.schematic.execute_vba_code(audit_vba",
  "geometry_equals_historical_r1a3_build",
  "no_sweep_parameter_history_warning",
  "no_solver_result_items",
):
    if req not in harness: fail.append("harness_missing:"+req)

for forbidden in (
  ".run_solver(",
  ".start_solver(",
  "Solver.Start",
  "FDSolver.Start",
  "RebuildForParametricChange",
  "P088",
  "P100",
):
    if forbidden in harness: fail.append("harness_forbidden:"+forbidden)

for req in (
  "BUILD NOT AUTHORIZED",
  "PASS_R1E1A0R1_PITCH_READY_CANONICAL_SOURCE_BUILD_ONLY",
  "Do not perform 88/100 endpoint mutation in R1.",
):
    if req not in contract: fail.append("contract_missing:"+req)

for req in ("DESIGN ONLY","Exactly one formal build-only invocation after a separate authorization.","No solver."):
    if req not in runbook: fail.append("runbook_missing:"+req)

if fail:
    print("HOLD_R1E1A0R1_STATIC_AUDIT")
    for x in fail: print("- "+x)
    raise SystemExit(3)

print("PASS_R1E1A0R1_STATIC_AUDIT")
print("HISTORICAL_MACROS_UNCHANGED=YES")
print("DERIVED_MACROS_DETERMINISTIC=YES")
print("PITCH_DECLARATION=MakeSureParameterExists")
print("SCAN_DECLARATION=MakeSureParameterExists")
print("FRESH_MWS_BUILD=YES")
print("ENDPOINT_MUTATION=0")
print("SOLVER_COMMANDS=0")
