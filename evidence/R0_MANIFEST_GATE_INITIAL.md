# R0 Manifest Gate — Initial Check

Status: **HOLD_R0_PARAMETERS_UNRESOLVED**

The gate was replayed against the committed `parameters.csv` before any CST geometry generation.

Unresolved required parameters:

- `copper_thickness`
- `feed_center_gap`
- `ground_xy_size`
- `pcb_outer_size`
- `petal_geometry`
- `ring_outer_size`
- `ring_trace_width`
- `substrate_material`
- `substrate_thickness`

This HOLD is intentional.

It demonstrates that the repository does not permit R0 build-only geometry to proceed while critical reference dimensions remain unknown or unapproved.

Next action:
1. extract figure-derived dimensions at adequate resolution,
2. document reconstruction assumptions for parameters not published,
3. human-review the manifest,
4. rerun the gate.

No solver has been run and no electromagnetic performance claim is made.
