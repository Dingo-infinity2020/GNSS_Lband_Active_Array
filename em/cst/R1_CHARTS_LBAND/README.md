# R1 CHARTS-Inspired L-band CST Track

Current stage: **R1A1 scaled visible-aperture BUILD-ONLY**

Model:
`CHARTS_GNSS_R1A1_SCALED_APERTURE_V01`

Purpose:
- scale only the accepted R0 V0.3 visible topology by a single frozen factor,
- preserve 12 disconnected slot topology,
- establish a deterministic L-band geometry baseline,
- stop before feed, materials, ports, or solver.

Initial scale factor:
`s = 400 MHz / 1400 MHz = 0.285714285714`

Approximate source-band mapping:
- 300 MHz -> 1.05 GHz
- 500 MHz -> 1.75 GHz

Required project band:
- 1.15–1.65 GHz

The build-only ground is a 94 mm nominal future unit-cell reference footprint. It is not a scientific claim about the correct finite isolated-element ground plane.

Next stage after design review:
- R1A2 project-owned symmetric differential feed definition/build.
