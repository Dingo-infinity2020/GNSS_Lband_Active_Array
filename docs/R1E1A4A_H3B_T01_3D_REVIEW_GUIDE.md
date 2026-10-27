# H3B-T01 V0.1 — Human 3D Review Guide

Open:
D:\GNSS_Lband_Active_Array\_r1e1a4a_h3b_t01_build_work\R1E1A4A_H3B_T01_ORTHOGONAL_TRANSITION_BUILD_ONLY_V01.cst

Review objective: judge whether the standalone 90-degree post-LNA PCB transition is physically credible before adding RF ports or running a passive solve.

Suggested visibility order:

1. Show H3B_Board only.
   - verify true 90-degree board contact;
   - verify the vertical board butts against the horizontal underside without positive-volume overlap.

2. Add H3B_Line + H3B_BackGround + H3B_Via.
   - inspect the symmetric G-S-G lines on both boards;
   - inspect the local opposite-face backing grounds;
   - verify the plated via fences are centered inside the ground rails and look manufacturable.

3. Add H3B_Transition + H3B_EdgeCap.
   - inspect the signal and two ground transition pads independently;
   - inspect the plated/castellated top-edge caps;
   - verify signal and grounds retain visible separation through the 90-degree turn.

4. Add H3B_Solder last.
   - inspect whether the three solder envelopes can realistically be formed and inspected;
   - verify the signal solder cannot bridge to either ground solder;
   - judge whether the box-envelope fillet is too large for a realistic prototype and should be reduced before solve.

Key dimensions to review:
- Wsig 1.80 mm;
- line gap 0.30 mm;
- ground rail width 2.20 mm;
- transition signal pad width 2.20 mm;
- transition gap 0.25 mm;
- transition ground pad width 2.40 mm;
- plated via OD/ID = 0.40 / 0.30 mm;
- RP1 y=+12 mm; RP2 z=-12 mm.

Do not judge insertion loss, return loss or impedance from this build-only artifact. It has zero RF ports and no solver results.
