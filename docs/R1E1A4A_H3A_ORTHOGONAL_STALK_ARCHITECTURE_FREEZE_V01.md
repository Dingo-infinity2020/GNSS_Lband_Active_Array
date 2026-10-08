# H3A Orthogonal PCB Feed-Stalk / Support Architecture Freeze V0.1

Status: **ARCHITECTURE FROZEN — NO BUILD / NO SOLVE AUTHORIZATION**

Candidate ID: `H3A_ORTHOGONAL_STALK_ASSEMBLY_V01`

Purpose:
freeze one complete, manufacturable first-pass architecture in which two mutually perpendicular PCB stalks provide mechanical support, controlled post-LNA RF routing, bias-routing space and later network-integration space.

This document supersedes the open geometric choices in `R1E1A4A_H3_ORTHOGONAL_PCB_FEED_STALK_RESEARCH.md` for the first H3A build candidate.

H2A V0.2 remains retained reference evidence and is not modified or reused as a solve source.

## 1. Coordinate and immutable parent

Parent radiator source:
`R1E1A1_P094_PITCH_BUILD_ONLY_V01.cst`

Parent SHA256:
`fb4c6d39dafe7d9334c62528df3b7060f26b9501f6c7b1603157fcbd9bbaa32e`

Frozen parent coordinates:
- main backplane PEC: z = -0.50 ... 0.00 mm;
- radiator FR4 underside: z = 57.1428571428 mm;
- radiator FR4 top: z = 58.1428571428 mm;
- top copper: z = 58.1428571428 ... 58.1778571428 mm;
- radiator board span = 70.7142857142 mm;
- periodic cell = 94 mm.

## 2. Stalk orientation — FROZEN

The two vertical stalk PCBs are aligned to the global **X and Y axes**, not the +/-45-degree polarization axes.

Rationale:
- the accepted radiator already contains X/Y center-cross copper-isolation corridors;
- at radius >= 8.5714 mm the corridor width is about 2.5714 mm;
- a nominal 1.0-mm stalk / 1.25-mm substrate slot therefore fits inside existing copper-free space;
- this avoids cutting the accepted top-radiator copper for the mechanical mortises;
- it keeps mechanical insertion away from the four diagonal feed terminals.

Signal mapping is deliberately separate from mechanical orientation:
- Pol-A branch pair NE/SW -> X-stalk;
- Pol-B branch pair NW/SE -> Y-stalk.

## 3. Vertical stalk PCB construction

Both stalks use the same first-pass stack:
- substrate: FR4 cost-baseline class;
- nominal thickness = 1.00 mm;
- nominal copper = 0.035 mm where explicitly patterned;
- stalk in-plane half-width = 15.0 mm (30.0-mm overall);
- body extends from backplane top z=0 to radiator underside z=57.1428571428 mm;
- no continuous full-height copper plane is permitted in H3A V0.1.

The stalk dielectric itself is an RF object and is not assumed transparent.

Future 0.8-mm or low-loss stalk material is a later trade, not part of this freeze.

## 4. Central electronics cavity

To prevent the crossed stalks from occupying the LNA/shield volume, each stalk has a top-center U-notch:
- notch half-width along stalk axis = 8.50 mm;
- total clear width = 17.0 mm;
- notch depth below radiator underside = 7.0 mm;
- notch bottom z = 50.1428571428 mm.

Therefore the central 17 x 17 x 7 mm region immediately below the radiator is mechanically free of stalk dielectric.

Reserved active-hub envelope inside this cavity:
- shield outer envelope <= 16 x 16 mm;
- shield depth <= 5.5 mm;
- four dummy LNA packages remain within this envelope.

The shield dimensions are packaging envelopes only; RF shield metal is not yet qualified.

## 5. Stalk-to-stalk interlock

The two vertical PCBs use a deterministic half-depth cross-slot joint below the electronics cavity.

Common slot width = 1.25 mm for a nominal 1.00-mm PCB.

Available interlock height is z = 0 ... 50.1428571428 mm.
Mid-plane = 25.0714285714 mm.

X-stalk:
- center slot opens from its bottom edge;
- slot spans z = 0 ... 25.0714285714 mm.

Y-stalk:
- center slot opens from the top of the interlock body;
- slot spans z = 25.0714285714 ... 50.1428571428 mm.

The assembled boards must have clearance, not solid-solid overlap, at the cross joint.

## 6. Vertical insertion into the radiator PCB — FROZEN

Each stalk has **two dedicated top mechanical tenons**, one on each shoulder outside the central cavity.

Per stalk:
- tenon center positions = +/-12.0 mm along the stalk axis;
- tenon length along stalk axis = 3.0 mm;
- tenon thickness = stalk PCB thickness = 1.0 mm;
- tenon insertion height = radiator substrate thickness = 1.0 mm;
- tenon top ends flush with the radiator FR4 top surface; it does not intentionally protrude into top copper.

Radiator mortise slots:
- center positions match the +/-12.0-mm tenons;
- slot length = 3.30 mm;
- slot width normal to stalk = 1.25 mm;
- slot is cut through FR4 only;
- the slot must remain inside the existing X/Y copper-isolation corridor.

The radiator slot is NOT allowed to cut accepted top-radiator copper.

The stalk main-body shoulder seats against the radiator underside; the tenon provides deterministic XY registration and shear resistance.

Mechanical solder is applied on the radiator **backside**, not across the radiating top copper.

Mechanical solder lands are electrically separate from the sensitive RF-transition pads in H3A V0.1.

Nominal solder-fillet envelope per tenon:
- maximum lateral leg = 0.60 mm;
- fillet is modeled explicitly in the build candidate;
- its contact with the dedicated mechanical copper land is an allowlisted `INTENTIONAL_CONTACT`;
- solder/dielectric or solder/radiator-copper volume overlap is not allowlisted.

## 7. Lower backplane insertion

The existing 0.50-mm PEC backplane remains the geometric authority for H3A V0.1.

Each stalk receives two bottom tenons aligned with the top tenons:
- center positions = +/-12.0 mm along stalk axis;
- tenon length = 3.0 mm;
- tenon depth = 0.50 mm through the backplane thickness.

Backplane mortises:
- length = 3.30 mm;
- width = 1.25 mm;
- cut completely through the 0.50-mm ground sheet.

Prototype interpretation:
the backplane is assumed to be a solderable conductive sheet or equivalent metallized interface for this first mechanical architecture.

A future aluminium-specific fastening solution is a later manufacturing variant and is not silently substituted into V0.1.

Bottom mechanical tab copper is treated as a dedicated mechanical/ground island.

The vertical stalk RF-ground rails are **not hard-wired to this bottom mechanical island** in H3A V0.1. A reserved jumper/bridge gap is kept between them so later passive qualification can compare bottom-ground bond states without redesigning the mechanical PCB.

Thus:
- mechanical bottom solder joint may contact the conductive backplane;
- RF-route ground can remain electrically separable;
- bottom RF-ground bonding becomes a controlled later variable rather than an accidental consequence of assembly.

## 8. Radiator-backside LNA topology — H3-L1 FROZEN FOR H3A

H3A uses the H3-L1 arrangement:
- four first-stage LNA package envelopes remain on the radiator backside;
- package centers remain on the four diagonal feed axes;
- nominal package envelope = 2.0 x 2.0 x 0.6 mm;
- nominal package-center radius = 6.2 mm.

The pre-LNA path stays on the radiator PCB and is intentionally kept as short as practical.

H3A does NOT place the first-stage LNA on the vertical stalk.

H3-L2 (LNA at stalk top) remains a later comparison candidate only.

## 9. Post-LNA branch mapping to stalks

The difficult 90-degree PCB transition is deliberately placed **after first-stage gain**.

Frozen branch assignment:
- NE LNA output -> +X transition -> X-stalk route 1;
- SW LNA output -> -X transition -> X-stalk route 2;
- NW LNA output -> +Y transition -> Y-stalk route 1;
- SE LNA output -> -Y transition -> Y-stalk route 2.

This keeps each linear-polarization pair on one stalk while preserving 180-degree symmetry.

No differential-to-single-ended conversion is performed at the radiator board in H3A V0.1.

## 10. Orthogonal RF transition reference planes

Each post-LNA branch reaches one dedicated top-edge transition on its assigned stalk.

Transition-center positions:
- +/-9.4 mm along the relevant X or Y stalk axis;
- located on the stalk shoulder, inside the +/-15-mm stalk width but outside the +/-8.5-mm electronics notch.

Topology:
- horizontal radiator-side output route approaches the stalk edge;
- signal uses a dedicated edge/castellated pad;
- two nearby ground pads provide a symmetric local return;
- vertical stalk continues as a GCPW-class route envelope.

Mechanical tenons at +/-12.0 mm are physically separated from the RF transition centers at +/-9.4 mm.

The RF transition and the mechanical joint are therefore different features.

H3A build-only may model:
- signal pad envelope;
- paired ground-pad envelopes;
- solder-fillet envelopes;
- plated/castellated edge envelope.

It must NOT claim 50-ohm performance yet.

Exact line width, GCPW gap, via fence, edge-plating stack and solder impedance are deferred to the passive RF interconnect gate after mechanical BUILD qualification.

## 11. Backside local-ground / shield concept

H3A retains the **topological** lesson from H2 but does not copy H2 V0.2 geometry blindly.

Frozen packaging envelope:
- backside local-ground/shield zone <= 20 x 20 mm;
- central RF-sensitive clearance >= 8 x 8 mm before later EM optimization;
- shield outer envelope <= 16 x 16 mm;
- shield depth <= 5.5 mm;
- four side egress windows align with the +/-X and +/-Y post-LNA transition directions.

The 17 x 17 x 7-mm stalk cavity is deliberately larger than the shield envelope so there is nominal assembly clearance.

Actual local-ground copper pattern remains an RF design object; H3A build-only will show the frozen first-pass pattern but no performance claim is made.

## 12. Vertical-stalk routing zones

Each stalk reserves two independent post-LNA RF route corridors, one for each branch of its polarization pair.

H3A V0.1 uses route **envelopes**, not impedance-qualified copper:
- each RF corridor envelope width = 3.0 mm;
- corridor descends from the +/-9.4-mm top transition region toward the lower service zone;
- no continuous full-board ground sheet is added;
- local GCPW ground rails may be shown only within the route envelope.

A separate central low-current corridor is reserved for DC/bias routing.

The support PCB may later host filtering, gain, 180-degree combining or active-balun functions, but none is instantiated in H3A V0.1.

## 13. Differential-to-single-ended policy

Generation-1 H3A preserves the four first-stage branch outputs.

Do not insert a lossy passive balun before the first LNA merely because the stalk offers board area.

Preferred later sequence:
antenna terminal -> first-stage LNA -> post-gain stalk route -> optional combine/balun/filter -> service output.

The exact differential-to-single-ended implementation is explicitly deferred.

The first H3A build must remain valid whether later conversion is implemented by:
- active combining;
- transformer/balun;
- 180-degree hybrid;
- digital/receiver-side recombination;
- no local conversion at all.

## 14. Lower service interface

H3A V0.1 does not freeze a specific MMCX/MHF/U.FL part.

Instead each stalk reserves two connector/service zones near its lower region:
- one zone per amplified branch;
- nominal reserved rectangle per branch = 6 x 8 mm;
- recommended center-height range = z 8 ... 18 mm above the backplane;
- connector body may face outward for assembly/service access.

The physical connector class will be frozen only after the stalk RF-route geometry and access clearance have been reviewed in 3D.

This avoids repeating the H2 mistake of defining a connector before verifying the surrounding mechanical architecture.

## 15. Assembly sequence — FROZEN FOR PROTOTYPE REVIEW

1. Fabricate X-stalk and Y-stalk with cross slots, top/bottom tenons and RF/mechanical copper features.
2. Interlock the two stalks using the half-depth center slots.
3. Insert both stalks' bottom tenons through the four backplane mortises.
4. Tack-solder / fixture the lower mechanical joints while maintaining orthogonality.
5. Lower the radiator PCB onto the assembled cross so all four top tenons enter the radiator mortises simultaneously.
6. Seat the stalk shoulders against the radiator underside.
7. Solder the dedicated top mechanical lands on the backside.
8. Solder the separate post-LNA RF transition pads/ground pads.
9. Populate/attach the active-hub hardware only after mechanical geometry is qualified.
10. Install the shield last so transitions and solder joints remain inspectable during assembly.

## 16. Mandatory H3A build-only acceptance

A future H3A build is not allowed to pass on shape-count alone.

Required fresh-reopen checks:
- P094 parent radiator and 94-mm periodic metadata preserved;
- X/Y stalk orientations exact;
- all eight radiator/backplane mortises and all eight tenons present;
- X/Y half-depth interlock slots present with nominal 0.25-mm thickness clearance;
- central 17 x 17 x 7-mm electronics cavity clear;
- four dummy LNA envelopes inside the cavity/shield envelope;
- mechanical tenons and RF transitions spatially separate;
- no solver-generated results;
- RF port count = 0.

### CST Geometry Intersection Check — HARD GATE

After fresh reopen, execute CST `Intersection Check / Check Model Intersections` under SimulationOps >=0.2.5.

Expected result:
**zero unresolved geometric interference.**

Allowed contacts must be explicitly listed in the build evidence, for example:
- stalk shoulder touching radiator underside;
- solder fillet touching its dedicated copper land / plated stalk edge;
- shield flange touching its intended ground land, if shield metal is instantiated.

Not allowed:
- stalk dielectric penetrating radiator dielectric outside mortise slots;
- stalks overlapping each other at the cross joint;
- solder penetrating radiator top copper or unrelated dielectric;
- LNA/shield envelopes intersecting stalk dielectric;
- RF transition pads intersecting mechanical tabs;
- connector/service envelopes intersecting backplane or neighboring stalk.

Any unexpected or unclassified intersection => `HOLD_H3A_GEOMETRY_INTERFERENCE`.

The future build evidence must retain the intersection-check report/log/screenshot or equivalent auditable output.

## 17. What H3A V0.1 does NOT freeze

Not frozen yet:
- final stalk material;
- exact impedance-qualified GCPW dimensions;
- actual QPL9547 or alternate LNA package launch;
- bottom connector part number;
- bottom RF-ground jumper state;
- differential-to-single-ended network;
- final shield material/details;
- bias topology;
- RF performance thresholds for the stalk transition.

These are downstream gates, not missing pieces of the H3A mechanical architecture.

## 18. Next authorized boundary

The architecture is now frozen sufficiently for a deterministic build-only source bundle.

Proposed next node:
`H3A_ORTHOGONAL_STALK_ASSEMBLY_BUILD_ONLY_V01`

Current permissions remain:
- BUILD: NO;
- SOLVE: NO;
- ACTIVE DEVICE: NO.

A new explicit BUILD authorization is required before generating or executing the formal H3A CST build.

No solver authorization is implied by this freeze.
