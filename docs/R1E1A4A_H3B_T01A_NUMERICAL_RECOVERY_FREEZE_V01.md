# H3B-T01A Numerical Recovery Freeze V0.1

Status: FROZEN FOR ONE RECOVERY SOLVE — NO GEOMETRY OR RF OPTIMIZATION

Reason:
T01-A baseline solve returned complete reciprocal 2-port S-parameters but reached adaptive pass 8 with final All-S DeltaS = 0.03094547, above the frozen 0.02 threshold.

## Immutable source
Protected BUILD artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h3b_t01_build_work\R1E1A4A_H3B_T01_ORTHOGONAL_TRANSITION_BUILD_ONLY_V01.cst

SHA256:
f321b678d390470a2420df40fd6d0cf6553cc041f9219bfcd011c7e41fbadf3d

## Recovery delta
The ONLY numerical change relative to T01-A baseline is:
- adaptive maximum passes: 8 -> 16.

Everything else remains frozen:
- same two 50-ohm discrete ports at RP1/RP2;
- same 1.0–2.0 GHz solve range;
- same 1.15–1.65 GHz decision band;
- same HF Frequency Domain solver;
- same tetrahedral general-purpose formulation;
- same second-order elements;
- same curvature order 3;
- same minimum passes = 3;
- same MaxDeltaS = 0.02;
- same two consecutive checks;
- same linear-growth limit 40;
- same open boundaries and 30-mm background margin;
- no geometry changes;
- no material changes;
- no optimization sweep.

## Qualification
Native convergence evidence is read from CST result tree:
1D Results\Adaptive Meshing\f=2\S-Parameters\Delta\All S-Parameters

Numerical PASS requires:
- complete S11/S12/S21/S22 result curves;
- finite samples;
- final two available All-S DeltaS values <= 0.02;
- reciprocal passive response remains consistent;
- no geometry/source provenance change.

If pass 16 is reached without two final values <=0.02, canonical status is HOLD. No further retry is implied.

## Comparison
Recovered S-parameters are compared against the maxpass-8 baseline over 1.15–1.65 GHz. This comparison is diagnostic; numerical convergence is determined by the native adaptive DeltaS sequence.

## Stop boundary
Stop after one recovery solve and read-only qualification.
No line-width/gap/pad/via tuning, no T01-C, no H3B-I01 and no active-device work.
