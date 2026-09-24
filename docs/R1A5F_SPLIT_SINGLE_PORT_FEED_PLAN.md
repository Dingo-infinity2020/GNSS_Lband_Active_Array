# R1A5F Split Single-Port Differential Feed Plan

Status: DESIGN BASELINE — NO BUILD/SOLVER AUTHORIZATION YET

## Motivation

R1A4Q proved that the simultaneous crossed two-port discrete-edge representation does not hard-short in HF Frequency Domain / tetrahedral mesh, but it adds artificial inter-port coupling.

R1A5M2 then established a numerically converged passive-matching baseline using that diagnostic model.

For production passive characterization, we should remove the crossed-port ambiguity rather than carry it into material, efficiency, gain and far-field studies.

## Proposed production passive strategy

Use two separate, hash-locked single-port models.

### Model A — Pol-A only

- immutable geometry source: human-reviewed R1A3 CST;
- exactly one 100 ohm differential discrete port;
- NE -> SW;
- no Pol-B port exists.

### Model B — Pol-B only

- same immutable R1A3 geometry;
- exactly one 100 ohm differential discrete port;
- NW -> SE;
- exact +90 degree rotational counterpart of Model A;
- no Pol-A port exists.

Because only one diagonal discrete port exists in each model, there is no central port-port crossing.

## Immutable geometry source

R1A3 human-reviewed CST:
D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst

SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

This is preferred over deleting a port from R1A4 because R1A3 contains no feed objects and preserves clean geometry provenance.

## Port definition

Reuse the frozen R1A4 terminal coordinates:
- terminal_r = 3.00 mm
- terminal_xy = 2.12132034356 mm
- terminal_z = copper_top_z
- reference impedance = 100 ohm
- type = SParameter

Model A:
P1 = NE
P2 = SW

Model B:
P1 = NW
P2 = SE

The B endpoint ordering is the exact +90 degree rotation of A.

## R1A5F build-only gate

Before any solver:
- create A and B from byte-identical copies of the R1A3 source;
- add exactly one port to each;
- no geometry/material changes;
- save/close/fresh reopen;
- verify port count = 1 for each;
- verify shape inventory exactly matches R1A3;
- verify A/B port definitions are exact rotational counterparts;
- hash both CST artifacts.

No solver is part of the R1A5F build-only gate.

## Why this is useful

These two single-port models can later support:
- converged S11 / input impedance for each linear polarization;
- radiation efficiency;
- total efficiency;
- realized gain;
- co-pol / cross-pol far-field patterns;
- material A/B comparison;
- exact Pol-A versus Pol-B symmetry checks.

They do NOT directly provide:
- simultaneous two-port S21/S12 isolation.

That quantity is intentionally deferred until a physically meaningful multi-conductor feed / active front-end model exists.

## Future solver reuse

After R1A5F build-only qualification, future single-port passive solves should start from the numerically converged R1A5M2 solver baseline:
- HF Frequency Domain
- tetrahedral second order
- curvature order 3
- General purpose
- HighFrequencyTet adaptive mesh
- MaxDeltaS 0.02
- two consecutive checks
- sufficient MaxPasses

Far-field monitors and efficiency outputs would be added only in a separate explicitly authorized production-passive stage.

## Stop boundary

R1A5F currently remains DESIGN only.

No build and no solver are authorized by this document.
