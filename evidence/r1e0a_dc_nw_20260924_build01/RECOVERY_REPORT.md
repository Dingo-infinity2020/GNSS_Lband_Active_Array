# R1E0A Read-Only Recovery Qualification

**RECOVERY_STATUS = PASS_R1E0A_PERIODIC_CONFIG_BUILD_ONLY_READONLY_RECOVERY**

Recovery source HEAD:
76b875e397f05fdea607ca069c74bbdd4b8fe8ea

CST rerun:
NO

Artifact modified:
NO

Original formal invocation remains:
HOLD_R1E0A_PERIODIC_CONFIG_AUDIT

Original HOLD classification:
AUDIT_BOOLEAN_ENCODING_MISMATCH

## Read-only evidence

Artifact:
D:\GNSS_Lband_Active_Array\_r1e0a_periodic_build_only_work\R1E0A_POLA_PERIODIC_BROADSIDE_BUILD_ONLY_V01.cst

SHA256:
48dfee8146575cae657b9fcb2e52b27920aec7253809c185c435db2d80191223

Source:
D:\GNSS_Lband_Active_Array\_r1a5f_split_single_port_work\R1A5F_POLA_SINGLE_PORT_V01.cst

Source SHA256:
74497f112b79b0f75548209bb3f3d8a9037644803c9efc808e6e0a74796bb1ce

Build and fresh-reopen status files are identical.

Fresh-reopen periodic metadata:
- Xmin/Xmax = unit cell
- Ymin/Ymax = unit cell
- Zmin/Zmax = expanded open
- structure X span = 94 mm
- structure Y span = 94 mm
- UnitCellDs1 = 94 mm
- UnitCellDs2 = 94 mm
- UnitCellAngle = 90 deg
- SCAN_QUERY_ERR = 0
- SCAN_VALID raw = -1
- SCAN_VALID interpreted = True
- theta = 0 deg
- phi = 45 deg
- direction = 1 / outward
- port count = 1
- no solver output exists

Geometry inventories at build and reopen are identical to the clean R1A5F Pol-A source.

## Conclusion

The R1E0A CST artifact correctly persists the intended 94-mm periodic/unit-cell broadside configuration.

The original formal HOLD was caused solely by treating the COM/VBA Boolean value -1 as invalid instead of True.

No rebuild was required and no solver was run.

The corrected future harness accepts True, 1 or -1 as Boolean true.

## Canonical stage conclusion

R1E0A periodic configuration qualification is accepted as PASS through read-only recovery.

Next stage:
R1E0B broadside periodic smoke DESIGN ONLY.
