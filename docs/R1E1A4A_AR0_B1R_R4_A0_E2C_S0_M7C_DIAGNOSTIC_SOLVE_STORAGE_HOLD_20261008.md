# M7C Diagnostic SOLVE Storage HOLD — 2026-10-08

Status: **HOLD_M7C_RESULT_STORAGE_DISK_EXHAUSTION_NO_SCIENCE_CLASSIFICATION**

The one authorized M7C SOLVE was consumed. The adaptive electromagnetic solve converged, but broadband result storage failed because NW D: was effectively full.

## What passed

- one-shot runner preflight PASS;
- solver launch occurred exactly once;
- no retry;
- adaptive Delta-S: 0.0726795 -> 0.0154014 -> 0.0149362;
- desired accuracy reached;
- solved project persisted.

## What failed

During later frequency samples / result materialization CST reported:
- could not write E/H/D/B field data;
- error accessing 1D result storage;
- not all S-parameters calculated.

The standard S-parameter tree contains only two samples: 1.0 and 1.8 GHz. This is insufficient for any frozen M7C modal gate.

## Root cause

Read-only forensic storage state immediately after HOLD:
- D: used ~132.08 GB;
- D: free ~0.16 GB;
- M7C run footprint ~3459 MB.

The failure is therefore classified as storage-resource exhaustion, not a geometry rejection.

## Scientific boundary

Do **not** classify M7C as PASS, PARTIAL or REJECT from this run.

Do **not** interpolate the two endpoint samples to 1.2056/1.2984/1.3432/1.5752/1.6496 GHz.

## Process lesson

A future SimulationOps hardening should include a stage-specific minimum-free-space preflight before production BUILD/SOLVE launch. For this model class the threshold should be comfortably above the observed ~3.46 GB run footprint and include working margin.

No recovery SOLVE is authorized by this closeout.
