# R1E1A2 Read-Only Qualification

Original formal status: `HOLD_R1E1A2_SUPPORT_BUILD_ONLY`.

Classification: `IN_SESSION_AUDIT_PERSISTENCE`, not geometry/material/physics failure.

Observed in-session artifact:
- correct shape-count header (S1=15, S4=7), but shape-name enumeration was incomplete;
- transient UnitCellDs1/Ds2 was not authoritative before reopen.

No build rerun was performed.

Fresh-reopen qualification for all four artifacts:
- S1 shapes = 15; S4 shapes = 7;
- S1 foam/body/bond volumes persist;
- port count = 1;
- scan metadata exactly matches B0 / C60P45 / C60P135;
- UnitCellDs1 = UnitCellDs2 = 94 mm;
- S1 epsilon/tan-delta parameters match the frozen contract;
- no solver markers;
- no solver result-tree items.

Canonical closeout: `PASS_R1E1A2_SUPPORT_BUILD_ONLY_READONLY_RECOVERY`.

Immutable solve-source hashes:
- S1_BONDED_B0 `addcd7a30fabdac49227b9f8ab8f05a6832266f0e00b58d288982abec13bae95`
- S1_BONDED_C60P45 `9c66bad44df42761aa09bacca835704dbc9d0e9eea458cd5088bb674d6ce8105`
- S1_BONDED_C60P135 `05ef5bb2ff7094072bae01895b2aa066d16abbf2213ef68e42202479745af789`
- S4_PEC_B0 `3962a20eb07c3db0f920304a9f3fc90d33e6946c03c753a9f43e99f4ede3223c`
