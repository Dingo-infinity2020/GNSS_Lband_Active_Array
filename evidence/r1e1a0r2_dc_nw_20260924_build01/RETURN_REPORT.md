# R1E1A0-R2 Endpoint Proof — Final Report

**FINAL_STATUS = PASS_R1E1A0R2_PITCH_PARAMETERIZATION_BUILD_ONLY**

Formal source commit: `063d3b467c5b149e1a818daf0a0e585a1ea1b5c9`
Formal invocation count: 1
Runtime: 91.57 s
Solver: NOT RUN

P088 SHA256: `089fdcfd7a2339a3504b8fb3b9542a586265549773e7c13ac4b20ef483e37b3a`
P100 SHA256: `8ffd74b176ad2f139770afbb5aa2201ae60e1a4f0e1fb38cf05a2254966e5a03`

Both endpoint models:
- persist target pitch after fresh reopen;
- preserve non-ground geometry and one-port feed;
- preserve broadside periodic boundary metadata;
- have matching UnitCellDs1/Ds2 and structure spans;
- emit no protected-parameter history warning;
- contain no solver markers/results.

Conclusion:
`PASS_R1E1A0_PITCH_PARAMETERIZATION_MECHANISM`

Next stage:
R1E1A1 six-pitch FR4 immutable source set.
