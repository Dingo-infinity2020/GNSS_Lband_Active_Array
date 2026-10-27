# H2A V0.2 — Human 3D Review Guide

Open:
`D:\GNSS_Lband_Active_Array\_r1e1a4a_h2av02_build_work\R1E1A4A_H2A_V02_SERVICE_ARCH_BUILD_ONLY_V01.cst`

Review objective:
verify that the universal active/passive center structure now has a credible RF-service path from future LNA outputs to the backplane without forcing a final connector or tube-bond choice.

Suggested visibility order:
1. `Substrate`, `TopCopper`, `H2A_FeedModule`, `H2A_PopulationEnvelope`.
2. Add `H2A_ServiceConnector` and `H2A_ServiceRouting`.
3. Add `H2A_Shield` and inspect the corner service egresses.
4. Add `H2A_ServiceTube` and `H2A_ServiceInterface`.
5. Add `UnitCellGround` and inspect the full cable path to the lower MMCX-class envelopes.

Questions to judge visually:
- Are the four MHF/U.FL-class envelopes too close to the LNA/package region?
- Do the horizontal cable bends look physically plausible?
- Is the 3x3-mm service-tube envelope too bulky?
- Is the 1.4-mm tube opening enough margin for a 0.81-mm micro-coax and assembly tolerance?
- Do the shield corner egresses look sufficiently open for cable bend radius and connector access?
- Are the four lower MMCX-class envelopes too crowded under the backplane?
- Should the service tubes eventually be round rather than square?
- Is it preferable to route bias through bias-tee on the coax, or later add a separate DC harness?

Do not infer RF performance from V0.2. The tube bond state remains deliberately unfrozen and the coax/connector objects are mechanical envelopes rather than validated transmission-line models.

Any requested geometry revision becomes a new build node. The current artifact remains immutable evidence.
