# H3B-T01A Passive Baseline Solve Freeze V0.1

Status: FROZEN FOR ONE PASSIVE SOLVE — NO OPTIMIZATION SWEEP

Source artifact:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h3b_t01_build_work\R1E1A4A_H3B_T01_ORTHOGONAL_TRANSITION_BUILD_ONLY_V01.cst

Source SHA256:
f321b678d390470a2420df40fd6d0cf6553cc041f9219bfcd011c7e41fbadf3d

## Port fixture

Port 1 = RP1 at horizontal y=+12 mm:
- 50 ohm discrete S-parameter port;
- x=0, y=12 mm;
- P1 on horizontal signal lower surface z=-0.035 mm;
- P2 on horizontal backing-ground upper surface z=+1.035 mm.

Port 2 = RP2 at vertical z=-12 mm:
- 50 ohm discrete S-parameter port;
- x=0, z=-12 mm;
- P1 on vertical signal outer face y=+0.535 mm;
- P2 on vertical backing-ground outer face y=-0.535 mm.

No coupon geometry is modified for port fixture creation.

## Solver

- frequency range: 1.0–2.0 GHz;
- decision band: 1.15–1.65 GHz;
- solver: HF Frequency Domain;
- tetrahedral general-purpose mesh;
- second-order elements;
- adaptive mesh: enabled;
- minimum passes = 3;
- maximum passes = 8;
- MaxDeltaS = 0.02;
- DeltaS checks = 2;
- all six boundaries = open;
- background free-space margin = 30 mm each direction.

## Baseline interpretation frozen before results

Execution/numerical PASS requires:
- solver completes normally;
- both ports exist;
- S11, S21, S12, S22 are present;
- no missing/NaN result samples.

Scientific interpretation is diagnostic, not yet an optimization gate:
- preferred return loss: <= -15 dB across core band;
- acceptable first baseline: <= -10 dB across most core band;
- strong concern: return loss worse than -3 dB over substantial core-band region;
- preferred insertion loss magnitude: <0.20 dB across core band;
- concern: insertion loss >0.50 dB or any sharp S21 notch;
- topology concern: S21 notch below -3 dB inside 1.15–1.65 GHz;
- reciprocity check: S21 and S12 should agree within numerical tolerance for this passive reciprocal model.

Do not change Wsig/gap/pads/vias after seeing this solve. Any optimization becomes a new H3B-T01A iteration.
