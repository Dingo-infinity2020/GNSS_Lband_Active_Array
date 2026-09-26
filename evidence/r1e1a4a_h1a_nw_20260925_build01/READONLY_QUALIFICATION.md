# R1E1A4A-H1A OFFSET_GROUND BUILD-ONLY Read-Only Qualification

Formal status: `HOLD_R1E1A4A_H1A_BUILD_IN_SESSION_AUDIT_PERSISTENCE`.
Canonical status: `PASS_R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY_READONLY_RECOVERY`.

The one formal build invocation created and saved the intended H1A model. The in-session audit did not persist the enumerated shape lines and reported stale UnitCell Ds1/Ds2 = 4.242640687 mm. Fresh reopen reported the persisted model correctly. No build rerun was performed.

Fresh-reopen qualification:
- shape count = 4;
- parent ground/substrate/top-copper preserved;
- `ActiveHub:H1A_OFFSET_LOCAL_GROUND` present;
- ground volume = 3.5 mm^3 = 10 x 10 x 0.035 mm;
- ground top z = 55.1428571428 mm;
- radiator-substrate underside z = 57.1428571428 mm;
- exact air gap = 2.000 mm;
- exactly two SParameter ports, 50 ohm each;
- terminal x/y = +/-2.12132034356 mm;
- port lower endpoints lie on the offset ground top;
- port length = 3.035 mm;
- UnitCellDs1 = UnitCellDs2 = 94 mm;
- broadside theta = 0 deg, phi = 45 deg;
- no solver markers or solver result tree.

Artifact:
`D:\GNSS_Lband_Active_Array\_r1e1a4a_h1a_build_work\R1E1A4A_H1A_OFFSET_GROUND_BUILD_ONLY_V01.cst`

SHA256:
`b903d678a7039105ad4d91bea2f82e9c1e5e9f8bbf5a5977360c85e34ced3b94`

Artifact state: PROTECTED_IN_PLACE.

Per the user's conditional authorization, this canonical BUILD PASS enables exactly one H1A broadside production solve. No scan continuation is authorized.
