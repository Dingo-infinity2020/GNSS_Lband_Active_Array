# R1A5 Isolated-Element Diagnostic Smoke Solve Contract

Status: FROZEN FOR STATIC AUDIT / NW SMOKE AUTHORIZATION

## Purpose

R1A5 is the first electromagnetic solve of the actual GNSS CHARTS-inspired passive element.

It answers only:
1. does the hash-locked two-port model solve stably;
2. where are the dominant input-match features over a deliberately broad L-band window;
3. are Pol-A and Pol-B still electromagnetically symmetric;
4. is the result reciprocal and free of gross feed/model failure.

R1A5 is diagnostic qualification, not production science and not geometry optimization.

## Immutable input

R1A4 CST:
D:\GNSS_Lband_Active_Array\_r1a4_differential_ports_work\R1A4_DIFFERENTIAL_PORTS_BUILD_ONLY_V01.cst

Required SHA256:
4875ce8bf9e3af0a17db2bd98ded7524ea7cfa042c0203113b8e4c3493dd2364

The harness must make a byte-identical copy before changing solver/boundary settings.

No geometry or port changes are permitted.

## Solver

- CST Studio Suite 2022.5
- HF Frequency Domain
- tetrahedral mesh
- first-order basis
- mesh adaptation OFF
- standard two-port solve
- no optimization
- no parameter sweep
- no far-field monitors in this smoke gate

## Boundary

All six boundaries:
open

Background distance:
50 mm in Xmin/Xmax/Ymin/Ymax/Zmin/Zmax.

Reason:
provide a simple reproducible radiation boundary for first diagnostic solve while keeping NW workload modest.

## Frequency

1.0–1.8 GHz.

The science target remains approximately 1.15–1.65 GHz.
The broader smoke window is intentional so that resonance migration is visible rather than hidden by a narrow band.

## Port model

Reuse R1A4 exactly:
- Port 1 / Pol-A = NE -> SW
- Port 2 / Pol-B = NW -> SE
- 100 ohm S-parameter reference
- crossed ideal discrete edge ports

R1A4Q limitation:
the crossed representation produced an artificial S21 floor around -69 to -55 dB over 0.5–2.0 GHz compared with a lifted non-intersecting reference.

Therefore:
- S11/S22 and gross resonance diagnostics are permitted;
- Pol-A/B symmetry is permitted;
- S21/S12 are qualitative only;
- isolation near/below approximately -50 dB is tagged PORT_MODEL_LIMITED;
- no high-dynamic-range polarization-isolation claim is permitted.

## Required outputs

- S11, S22, S21, S12 complex curves
- CSV over all returned frequencies
- best-match frequency and value for S11 and S22
- matched-load input impedance derived from each self S-parameter using Z0=100 ohm
- anchor-frequency samples:
  - 1.17645 GHz
  - 1.22760 GHz
  - 1.27875 GHz
  - 1.40000 GHz
  - 1.56110 GHz
  - 1.57542 GHz
  - 1.60200 GHz
- max S11/S22 dB asymmetry
- max complex reciprocity error |S21-S12|
- solver-result existence
- source/copy/config/output hashes
- solver/mesh warning capture where available

## PASS/HOLD logic

PASS_R1A5_DIAGNOSTIC_SMOKE if:
- immutable source hash matches;
- fresh copied CST hash matches before configuration;
- solver finishes;
- all four S-parameter curves exist and have equal nonzero length;
- no NaN/Inf values;
- reciprocity error <= 1e-3 in complex linear S;
- max absolute S11/S22 dB difference <= 1.0 dB.

These are model-integrity gates, not performance targets.

Report but do not fail solely because:
- return loss is weak;
- resonance is outside 1.15–1.65 GHz;
- efficiency/gain are not available;
- S21 is port-model-limited.

HOLD if:
- solver/runtime fails;
- results are incomplete;
- reciprocity or polarization symmetry is grossly broken;
- source/hash/geometry/port provenance changes.

## Stop boundary

After diagnostic S-parameter/impedance interpretation:
- return baton to DESIGN;
- no automatic geometry optimization;
- no material A/B;
- no production solve;
- no CST251 staging.
