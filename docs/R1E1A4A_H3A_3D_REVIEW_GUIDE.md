# H3A V0.1 — Human 3D Review Guide

Open:
`D:\GNSS_Lband_Active_Array\_r1e1a4a_h3a_build_work\R1E1A4A_H3A_ORTHOGONAL_STALK_BUILD_ONLY_V01.cst`

Review objective:
judge whether the orthogonal PCB stalk concept is mechanically credible before any RF solve.

## Suggested visibility order

1. Show `Substrate`, `TopCopper`, `H3A_Stalk` only.
   - inspect the X/Y stalk orientation;
   - inspect the half-depth cross interlock;
   - inspect all four top tenons entering the radiator mortises;
   - inspect the four bottom tenons entering the backplane mortises.

2. Add `H3A_MechLand` and `H3A_MechSolder`.
   - verify that mechanical solder features are physically separate from the RF transition region;
   - inspect whether the solder access looks realistic for hand/prototype assembly.

3. Add `H3A_LNAEnvelope`, `H3A_HubGround`, `H3A_Shield`, and `H3A_RouteEnvelope`.
   - inspect the 17 x 17 x 7-mm electronics cavity;
   - verify that the 16-mm shield envelope is visibly clear of both stalks;
   - verify that the four post-LNA route envelopes leave through the +/-X,+/-Y shield egresses.

4. Add `H3A_RFTransition` and `H3A_RFSolder`.
   - inspect the separate +/-9.4-mm RF transition locations versus +/-12-mm mechanical tenons;
   - check whether the 90-degree transition has realistic solder access.

5. Add `H3A_StalkRF` and `H3A_ServiceEnvelope`.
   - inspect whether two RF branches per polarization fit comfortably on one stalk;
   - inspect the lower service zones and whether future connectors/bias networks have usable access.

## Specific questions for human review

- Is the 30-mm stalk width too large or too small relative to the 70.7-mm radiator board?
- Does the 17-mm central notch leave enough mechanical stiffness in the two shoulders?
- Are the +/-12-mm top tenons positioned far enough from the active hub while still giving useful leverage?
- Is a 1.25-mm mortise for a nominal 1.0-mm PCB realistic for the intended PCB fabrication tolerance?
- Should the top tenons be 3.0 mm long, or should the next revision use shorter/wider paired tabs?
- Does the half-depth cross-slot look mechanically stiff enough without an extra fastener?
- Is backside-only top soldering practical after both stalks are interlocked?
- Should the lower backplane joint remain soldered in the prototype, or move to a mechanical clamp/slot in a later version?
- Are the post-LNA routes and service zones sufficiently separated from the mechanical joints?

Do not judge S-parameters, NF, stability, scan response or G/T from H3A V0.1. This artifact has zero RF ports and no solver results.
