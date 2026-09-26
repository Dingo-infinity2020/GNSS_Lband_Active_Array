# R1A4Q Crossed Discrete-Port Qualification — Final Report

**FINAL_STATUS = PASS_R1A4Q_NO_HARD_SHORT_WITH_PARASITIC_COUPLING**

## Question

Do the two diagonal CST discrete edge ports in R1A4 create a direct electrical short when they cross at the center?

## Documentation finding

CST 2022.5 local Help states that a discrete edge port consists of:
- a perfect-conducting wire between its start/end points;
- a central lumped/source element.

Its mesh representation is metallic wire except for the central source element.

Therefore the user's concern was physically/numerically justified and required qualification.

## Test

A — CROSS:
- four isolated PEC pads;
- two diagonal 100 ohm S-parameter discrete ports crossing at the center.

B — LIFTED_REFERENCE:
- same four isolated pads;
- same diagonal pairing;
- second port lifted in z using two short PEC posts so the port wires do not intersect in 3D.

Both:
- CST 2022.5;
- HF Frequency Domain;
- tetrahedral first-order mesh;
- no adaptation;
- 0.5–2.0 GHz.

No GNSS antenna model was solved.

## Result

CROSS S21:
-69.09 dB at 0.5 GHz
-62.75 dB at 1.0 GHz
-59.40 dB at 1.4 GHz
-55.43 dB at 2.0 GHz

LIFTED_REFERENCE S21:
-86.21 dB at 0.5 GHz
-80.53 dB at 1.0 GHz
-78.09 dB at 1.4 GHz
-76.76 dB at 2.0 GHz

Crossing penalty:
approximately +17.1 to +21.3 dB coupling over 0.5–2.0 GHz.

## Interpretation

1. No direct galvanic short was observed in HF Frequency Domain / tetrahedral mesh.
2. The crossed edge-port representation is not electrically invisible; it creates a measurable artificial inter-port coupling path.
3. At 1.4 GHz the artificial coupling floor is about -59.4 dB in the toy problem.
4. This level is small enough for a first diagnostic antenna smoke run whose expected physical polarization coupling is much larger than -59 dB.
5. It is not acceptable as an unqualified high-dynamic-range isolation reference.
6. The result does not authorize transient/hexahedral use because CST represents discrete elements on the calculation mesh and diagonal elements can have solver/mesh-specific behavior.

## Engineering decision

Current R1A4 crossed ports may be used only for:
- R1A5 lightweight diagnostic smoke;
- HF Frequency Domain;
- tetrahedral mesh;
- qualitative resonance / gross S-parameter sanity.

They are NOT the final production feed model.

Before production-quality polarization-isolation claims, replace or cross-check with a non-intersecting feed representation such as:
- a local discrete face-port construction if geometry supports it;
- a physically realized feed transition;
- a multipin/waveguide or circuit-domain differential formulation.

No R1A5 solver is authorized by this report itself.
