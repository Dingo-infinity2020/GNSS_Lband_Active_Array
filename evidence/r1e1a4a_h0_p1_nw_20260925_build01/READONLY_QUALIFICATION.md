# R1E1A4A H0/P1 BUILD-ONLY Read-Only Qualification

Formal status: `HOLD_R1E1A4A_H0_P1_BUILD_AUDIT_VBA_RESERVED_WORD`.
Canonical status: `PASS_R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_READONLY_RECOVERY`.

The one authorized formal build invocation created and saved the target CST. Fresh-reopen audit then failed before qualification because the audit-only VBA used `imp` as a variable name; VBA treats `Imp` as a reserved logical operator. No solver was called.

No build rerun was performed. The persisted artifact was qualified using query-only VBA on fresh reopen, without `add_to_history`, model mutation, or save.

Qualified persisted geometry:
- shape count = 4;
- `UnitCellGround:UNITCELL_GROUND_REFERENCE` preserved;
- `Substrate:FR4_BOARD` preserved;
- `TopCopper:TOP_COPPER` preserved;
- `ActiveHub:H0_LOCAL_GROUND` added;
- H0 local-ground volume = 3.5 mm^3 = 10 x 10 x 0.035 mm.

Qualified P1 interface:
- port count = 2;
- both type = `SParameter`;
- both impedance = 50 ohm;
- P1A top endpoint = (+2.12132034356,+2.12132034356,58.1778571428) mm;
- P1A ground endpoint z = 57.1428571428 mm;
- P1B is the exact 180-degree partner;
- port length = 1.035 mm from top terminal plane to underside local-ground plane.

Periodic / execution invariants:
- UnitCellDs1 = UnitCellDs2 = 94 mm;
- theta = 0 deg broadside;
- no solver markers;
- no S-parameter / adaptive-meshing / power-excitation solver result items;
- parent P094 evidence snapshot was restored/verified; no parent evidence rewrite was detected in the final read-only qualification.

The first read-only checker itself also recorded a HOLD because it assumed the ground component was named `GroundReference` instead of the actual parent name `UnitCellGround`, and treated CST/VBA Boolean `-1` as failure rather than True. The raw values were already correct. Those checker assumptions were corrected, and the second read-only pass is the canonical qualification.

Solved/derived physics claims: NONE. This remains BUILD-ONLY.

Artifact:
`D:\GNSS_Lband_Active_Array\_r1e1a4a_h0_p1_build_work\R1E1A4A_H0_P1_MIXEDMODE_BUILD_ONLY_V01.cst`

SHA256:
`d1ebb6f4a6e8b48f3484cc5459790dd5c9bbd29482832c491076c84f783b3deb`

Artifact state: PROTECTED_IN_PLACE.
