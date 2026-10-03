# AR0-B1R-T1 Build-Only Plan V0.1

Status: BUILD AUTHORIZED; SOLVE FORBIDDEN

Parent:
R1E1A4A_AR0_B1R_T0_RF_TENON_BUILD_ONLY_V01.cst
SHA256 f4c51b603fc01e8c3cec095de0ca641a3a671dc1e2449a95a123af6a8b902bb9

Frozen nominal geometry:
- stalk FR4 = 1.00 mm;
- signal width = 1.90 mm, unchanged;
- balanced throat L_bal = 1.50 mm;
- linear ground-acquisition taper L_taper = 3.00 mm;
- full local ground begins at v = 4.50 mm;
- ground width = 3.60 mm centered below each signal;
- local full-ground region continues to v = 12.00 mm.

Actions:
1. verify exact T0 parent hash;
2. inventory parent;
3. delete four old B0_BackGround solids only;
4. create four continuous triangular-flare + rectangular-tail backside-ground solids;
5. preserve every other geometry object;
6. fresh reopen;
7. verify component/volume preservation;
8. deterministic C4/mirror/collision audit;
9. verify zero ports and zero solver tree;
10. stop for human 3D review.

No RF solve.
No parameter sweep.
No silent retry.
