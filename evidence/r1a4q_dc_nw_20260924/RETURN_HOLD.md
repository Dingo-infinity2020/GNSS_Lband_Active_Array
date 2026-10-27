# R1A4Q Attempt-1 Return

**FINAL_STATUS = HOLD_R1A4Q_HARNESS_RUNTIME_BEFORE_SOLVER**

Source HEAD:
cc76c1c3d18b3e54df9267e6bdddb6f3269fe9ea

Script SHA256:
166f05e60bed8000037bdb893ffb43943df2b9fe2f12d3e9f4494caebae24f28

Formal invocation count:
1

Exit code:
1

Runtime:
17.10 s

Failure:
`AttributeError: object has no attribute 'evaluate'`

Location:
`pre_ports=prj.modeler.evaluate("Solver.GetNumberOfPorts()")`

Important classification:
- CROSS toy geometry/ports were created and saved;
- the harness failed before `prj.modeler.run_solver()`;
- no EM solver was started;
- no S-parameter result exists;
- this is not evidence for or against crossed-port shorting.

Attempt-1 work is retained at:
D:\GNSS_Lband_Active_Array\_r1a4q_crossed_port_test

No silent retry is allowed.

Recovery:
replace the unsupported Python `modeler.evaluate()` call with a CST VBA file audit using `Solver.GetNumberOfPorts()`, then authorize a fresh attempt-2 with new work/evidence paths.
