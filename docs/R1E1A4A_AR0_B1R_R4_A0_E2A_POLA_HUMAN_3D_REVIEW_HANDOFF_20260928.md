# R4-A0-E2A Pol-A Human 3D Review Handoff — 2026-09-28

Status: `BUILD PASS — HUMAN REVIEW REQUIRED`

Canonical artifact (do not open/save in GUI):

`D:\GNSS_R4A0E2A_20260928_BUILD_R2\R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_INTEGRATED_BUILD_ONLY_V02_RECOVERY.cst`

Canonical SHA256:

`78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804`

Human-review copy:

`D:\GNSS_R4A0E2A_20260928_BUILD_R2\R1E1A4A_AR0_B1R_R4_A0_E2A_POLA_HUMAN_REVIEW_COPY.cst`

At creation, review-copy SHA256 was identical to canonical:

`78c9d38e186e38b1d0398e7771758af34345fc5e8f780fdc8c7fade4a8705804`

The review copy includes the complete same-stem companion project directory.

## What to inspect

1. Full radiator + both orthogonal stalks remain present and mechanically coherent.
2. Pol-A has two active branches from radiator/tenon/tongue through v=0..3 mm stubs into the twin E1 landing zones.
3. Pol-B electrical feed stops after the intended v=0..3 mm open stubs; no Pol-B E1 landing zone is present.
4. Old full-length B0 MSL geometry and old T1R1 feed-head backside grounds are absent.
5. Both QPL9547 footprints use the same package rotation; pinout is not mirrored.
6. Eight plated vias visibly pass through real Pol-A stalk FR4 at intended positions.
7. Branch-local backside grounds do not penetrate the orthogonal Pol-B stalk or lower body.
8. No ground touches radiator copper.
9. No historical D2 remote-ground rail/common bridge is present.
10. Twelve discrete ports are located on the intended E_UP / P_IN / P_OUT / E_DN / B_VDD / B_VBIAS planes.

Human review is geometry/assembly sanity only, not RF-layout or solve qualification.

Current authorization:

- BUILD_AUTHORIZED = false
- SOLVE_AUTHORIZED = false

After human PASS, the next allowed work is offline E2A passive-solve contract freeze. No solve may start without a new explicit authorization.
