# E2C S0 M1/M2 Offline Mechanism Analysis V0.1

M1 status: **PASS_M1_SEMANTIC_INTEGRITY**
M2 status: **PASS_M2_COUPLING_DECOMPOSITION_EVIDENCE_READY**

No CST launch, BUILD, or SOLVE was used.

## M1 semantic integrity

- combined_csv_sha256: 63efb3b3c046ffa633d04092d0190afc4d01ea03f4fd6316ffa1d87170af8a46
- combined_1001_points: True
- combined_grid_1p0_1p8: True
- combined_grid_step_0p0008: True
- required_96_columns: True
- manifest_12_ports: True
- manifest_names_exact: True
- source_ports_exact: True
- load_ports_exact: True
- transform_orthonormal: True
- transform_orthonormal_error: 2.220446049250313e-16
- qualifier_hard_checks_all_pass: True
- formal_solver_invocations_one: True
- automatic_retries_zero: True
- PolA_baseline_hash_exact: True
- PolA_grid_exact: True
- PolA_16_columns: True
- PolA_modal_selftest_zero: True
- PolB_baseline_hash_exact: True
- PolB_grid_exact: True
- PolB_16_columns: True
- PolB_modal_selftest_zero: True

## M2 key observables

### PolA
- max same-pol complex delta: 0.703793 at 1.3432 GHz, ['A_P_E_UP', 'A_P_E_UP']
- E_UP branch return imbalance: 11.374 dB at 1.2984 GHz
- E diff->common peak: -8.915 dB at 1.3584 GHz
- isolated E diff->common peak: -30.711 dB

### PolB
- max same-pol complex delta: 0.700675 at 1.3400 GHz, ['B_N_E_UP', 'B_N_E_UP']
- E_UP branch return imbalance: 11.237 dB at 1.2984 GHz
- E diff->common peak: -8.972 dB at 1.3544 GHz
- isolated E diff->common peak: -32.433 dB

### Cross-pol/coupling
- cross-pol E_UP<->E_UP peak: -3.071 dB at 1.3160 GHz (A_P_E_UP -> B_N_E_UP)
- cross-pol E_UP->P_IN peak: -42.323 dB
- cross-pol device-side peak: -73.565 dB
- 50 MHz resonance excursion: 6.441 dB

## Evidence-ranked mechanism classes

- **HIGH — REAL_DUALPOL_EUP_ELECTROMAGNETIC_COUPLING**: cross-pol E_UP<->E_UP peak > -20 dB
- **HIGH — PLUS_MINUS_BRANCH_REFERENCE_OR_RETURN_ASYMMETRY**: E_UP branch self-return imbalance > 6 dB
- **HIGH — DIRECT_DEVICE_SIDE_CROSSPOL_COUPLING_NOT_DOMINANT**: cross-pol P_IN/device-side coupling remains below -40 dB
- **MEDIUM — NARROW_RESONANCE_NOT_PRIMARY_TRIGGER**: 50 MHz excursion below frozen 10 dB gate

## Boundary

No rerun or geometry mutation is authorized. M3/M4 must use the existing solution.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
