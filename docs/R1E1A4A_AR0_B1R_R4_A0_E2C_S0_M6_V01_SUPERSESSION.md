# M6 V0.1 Supersession

M6 V0.1 is non-authoritative for geometry attribution.

Reason: its static parser handled only Brick/Cylinder primitives. The E2C landing-zone copper is primarily created with CST Extrude, so V0.1 incorrectly reported zero classified A/B entities while still labeling the result PASS.

No CST, BUILD, or SOLVE occurred in V0.1.

M6 V0.2 replaces V0.1 using:
- expected_final_names from the frozen E2C final inventory as entity authority;
- Extrude geometry reconstruction;
- Cylinder plus immediate z-rotation reconstruction;
- explicit fail-closed geometry coverage.

Do not use V0.1 geometry counts or distances.
