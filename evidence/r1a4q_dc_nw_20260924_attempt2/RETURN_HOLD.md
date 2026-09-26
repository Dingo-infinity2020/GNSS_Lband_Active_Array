# R1A4Q Attempt-2 Return

**FINAL_STATUS = HOLD_R1A4Q_POSTPROCESS_RUNTIME_AFTER_CROSS_SOLVE**

Source HEAD:
002119337b5502bdbc97224609d899c4b2a92459

Formal invocation:
1

Exit code:
1

Runtime:
21.46 s

CROSS solver:
COMPLETED

LIFTED_REFERENCE solver:
NOT STARTED

Failure:
`ValueError: too many values to unpack (expected 2)`

Cause:
CST S-parameter self terms such as S11 return rows containing frequency, complex S value, and reference impedance. The harness assumed every row contained only frequency and complex S value.

This is a post-processing bug, not a solver/model failure.

## Read-only recovery of existing CROSS result

No solver rerun was used.

CROSS S21:
- 0.5 GHz: -69.089 dB
- 0.75 GHz: -65.429 dB
- 1.0 GHz: -62.747 dB
- 1.4 GHz: -59.402 dB
- 1.8 GHz: -56.662 dB
- 2.0 GHz: -55.434 dB

CROSS S12 is reciprocal to within a few millidecibels.

CROSS S11/S22 remain close to 0 dB, expected for the deliberately unloaded isolated-pad toy geometry.

Interpretation:
the crossed-port configuration does not show the strong direct transmission expected from a simple galvanic short in the tested HF Frequency Domain / tetrahedral configuration.

However the frozen A/B qualification remains incomplete because LIFTED_REFERENCE has not yet been solved.

Solver log:
- discrete port 1 added;
- discrete port 2 added;
- no port-overlap/intersection error reported;
- only generic mesh-size warnings were observed.

Attempt-2 work is preserved:
D:\GNSS_Lband_Active_Array\_r1a4q_crossed_port_test_attempt2
