# M7C Diagnostic SOLVE Freeze V0.1

M7C `LOCAL_RETURN_ISLAND_MOAT` passed user manual CST 3D geometry review.

The protected reviewed artifact is the only source allowed for a future diagnostic solve:

`D:\GNSS_Lband_Active_Array\runs\formal\build_only\M7C_LOCAL_RETURN_ISLAND_V01\R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7C_LOCAL_RETURN_ISLAND_BUILD_ONLY_V01.cst`

SHA256:

`ee25237bc5f70e457adadf3745faf3d64f1401bb47717da5322d7347ba50ce98`

## Solver semantics

Reuse the proven full-E2C / M7A / M7B 12-port coexistence network:

- source ports: 1, 2, 4, 5, 7, 8, 10, 11;
- matched load-only ports: 3, 6, 9, 12;
- modeled band: 1.0–1.8 GHz;
- decision band: 1.15–1.65 GHz;
- CST HF Frequency Domain;
- second-order tetrahedral adaptive mesh;
- MaxDeltaS = 0.02;
- two consecutive convergence checks;
- maximum 16 passes;
- no H-field monitor;
- automatic retries = 0;
- formal solver budget = 1.

## First-principles M7C test

M7B showed that removing local backside ground does two things at once:

1. it suppresses branch asymmetry / differential-to-common conversion;
2. it worsens the symmetric differential input environment.

M7C is successful only if it keeps the first benefit while reversing the second penalty.

### Primary family A — symmetry preservation

At 1.2056, 1.2984, 1.3432, 1.5752 and 1.6496 GHz, for **both polarizations**:

[
|\Delta S_{dc}|_{M7C}
\le 0.25
|\Delta S_{dc}|_{full\ E2C}.
]

All ten checks must pass.

### Primary family B — differential restoration

At 1.3432, 1.5752 and 1.6496 GHz, for **both polarizations**:

[
|\Delta S_{dd}|_{M7C}
\le 0.70
|\Delta S_{dd}|_{M7B}.
]

All six checks must pass.

The frozen M7B (|\Delta S_{dd}|) references are embedded in the manifest before M7C solve.

### Secondary raw check

Worst own-pol source-side complex deviation over 1.15–1.65 GHz:

[
\le 0.6567025281.
]

This is 0.80 times the frozen M7B worst value 0.8208781602.

### Guard

No off-diagonal response may gain a new >6 dB excursion in any <=50 MHz window relative to full E2C.

## Classification

- `PASS_M7C_LOCAL_RETURN_ISLAND`: numerical PASS + all symmetry primary checks + all differential-restoration checks + guard PASS.
- `REVIEW_M7C_PARTIAL`: numerical/guard PASS and exactly one primary family passes, or at least one failed primary item improves by >=10% in the predicted direction.
- `REJECT_M7C_LOCAL_RETURN_TOPOLOGY`: numerical/guard PASS and neither family nor any primary item improves by >=10%.
- `HOLD_M7C_GUARD`: numerical PASS but guard fails.
- `HOLD_M7C_NUMERICAL`: numerical hard gate fails.

The secondary raw check is reported but does not substitute for either primary family.

## Authorization boundary

BUILD_AUTHORIZED = false.

SOLVE_AUTHORIZED = false.

Before any SOLVE grant is activated, the frozen host static audit must return exactly:

`PASS_M7C_DIAGNOSTIC_SOLVE_STATIC_CONTRACT`

No retry, sweep, geometry mutation or automatic next stage is authorized by this contract.
