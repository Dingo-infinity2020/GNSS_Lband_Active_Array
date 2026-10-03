# H2A V0.1 — Human 3D Review Guide

Open:
`D:\GNSS_Lband_Active_Array\_r1e1a4a_h2a_build_work\R1E1A4A_H2A_UNIVERSAL_CENTER_BUILD_ONLY_V01.cst`

Review objective:
decide whether the universal passive/active center assembly is mechanically credible before any RF solve.

## Suggested visibility order

1. Show only `Substrate`, `TopCopper`, and `H2A_FeedModule`.
   Check that the same-board patterned ground leaves a clear center window around the four terminal projections.
2. Add `H2A_PopulationEnvelope`.
   Check whether four 2-mm package locations look serviceable and whether future traces could reasonably reach them.

3. Add `H2A_Shield`.
   Check package-to-shield clearance and whether an 18-mm square can looks practical.
4. Add `H2A_Carrier`.
   Check that the 21-mm inner opening clears the 18-mm shield and leaves a hollow service corridor.
5. Add `UnitCellGround`.
   Inspect the full support path from radiator PCB to the main backplane.

## Questions for human review
- Is a 30-mm square carrier too bulky relative to the 70.7-mm radiator board?
- Is the 18-mm shield too large or too small for realistic population and rework?
- Is the 8x8-mm center ground clearance mechanically/electrically plausible?
- Should the carrier be circular rather than square for fabrication?
- Where should RF output and DC bias leave the shield/carrier volume?

- Should passive test access be through temporary coax, probe pads, or a removable feed coupon?
- Do the four diagonal package locations create a routing or assembly conflict?

## Do not infer yet
Do not judge return loss, NF, stability or scan performance from this model. H2A has no RF ports and no solver result.

Any requested geometric change after review becomes H2A V0.2 or H2B design work; the current artifact remains immutable evidence.
