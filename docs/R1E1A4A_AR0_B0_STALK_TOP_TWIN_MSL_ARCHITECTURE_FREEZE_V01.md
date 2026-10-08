# AR0-B0 Stalk-Top Twin-MSL Active-Feed Architecture Freeze V0.1

Status: ARCHITECTURE FROZEN — BUILD NOT AUTHORIZED
SimulationOps: 0.2.8

## 1. Decision

The first active-feed architecture to pursue is **B0: stalk-top twin-microstrip / twin-LNA feed**.

The earlier H3B-C0 grounded-GCPW integration is not repaired in place. Its HOLD remains valid architecture evidence:
- four T01 vertical vias fell into the H3A top notch rather than through FR4;
- the grounded T01 topology imported a backing ground onto the radiator PCB;
- T01 ground pads collided with accepted mechanical lands;
- therefore a ground-referenced post-LNA coupon must not be promoted into the balanced radiator feed.

T01-A remains frozen and reusable only as a **post-LNA grounded-board interconnect technology**.

Architecture A (radiator-PCB electronics island) remains a deferred comparison candidate.

## 2. Hard electromagnetic ownership rules

These rules are architecture-level and may not be relaxed by a geometry optimizer.

### Radiator PCB
- The radiator PCB remains a balanced radiator, not a microstrip ground plane.
- No LNA ground plane, transmission-line backing ground, shield floor, or service ground may overlap the radiator copper on either face.
- No stalk ground may make galvanic contact with radiator copper.
- Each differential radiator terminal has exactly one intentional galvanic connection: to its corresponding signal tongue.
- Ground/shield metal near the feed is a separate EM object and must have explicit clearance.

### Stalk PCB
- The stalk is allowed to own a large ground conductor on its back face.
- Ground exists only on the vertical stalk, not on the radiator PCB.
- The first-stage LNA is on the stalk, close to the feed.
- Pre-LNA paths are kept short and symmetric.
- The pre-LNA feed remains two independent signal branches; no radiator arm is redefined as RF ground.

## 3. Coordinate system and polarization mapping

Reuse the qualified differential terminal authority:
- terminal radius along each polarization axis: 3.00 mm;
- Pol-A terminals: NE and SW;
- Pol-B terminals: NW and SE.

For each polarization stalk define:
- local u: along that polarization axis in the radiator plane;
- local v: downward from the radiator feed plane;
- local n: through stalk thickness.

Feed plane:
- v = 0.

Terminal centers:
- u = +3.00 mm;
- u = -3.00 mm.

Pol-A stalk plane follows the NE-SW axis.
Pol-B stalk plane is its exact 90-degree rotation and follows the NW-SE axis.

The two electrical feed heads must be exact rotational counterparts.

## 4. First-cut stalk stack

Nominal B0 carrier:
- dielectric: FR4_COST_BASELINE;
- thickness: 1.00 mm;
- copper engineering conductivity: 5.8e7 S/m;
- front face: two signal paths + LNA footprints/bias/output structures in later stages;
- back face: local MSL ground rails in the feed head, expanding to a broad common ground region below the sensitive feed head.

The 1-mm FR4 stack is a first-cut manufacturing baseline, not an optimized RF result.

## 5. Fork-head geometry

The upper stalk is not a solid slab.

From v = 0 through the active feed-head region it has:
- two RF prongs;
- a central longitudinal clearance slot around u = 0.

Purpose:
- keep both orthogonal polarization stalks out of each other's feed/LNA volume;
- avoid recreating the H3A large top notch;
- preserve solid FR4 beneath every RF via used later;
- separate mechanical crossing from the pre-LNA feed.

Nominal first-cut feed-head envelope:
- outer half-width: 5.0 mm (10.0-mm total width);
- central slot half-width: 1.00 mm (2.00-mm clear slot);
- feed-head depth: v = 0 to 12.0 mm.

Static pre-build orthogonal-prong analysis showed that the earlier +/-0.75-mm slot caused a positive-area A+/B- collision for a 1.0-mm one-sided stalk thickness. The nominal slot is therefore corrected to +/-1.00 mm before any CST build is consumed.

Thus each prong remains wide enough to carry the terminal at u=+-3 mm, a nominal 1.9-mm MSL, and an LNA package zone.

Below v = 12 mm the board may widen into the electronics/support body. The exact lower-body/interlock geometry is NOT frozen by B0 and must not force a change to the feed head.

## 6. Signal-only radiator-to-stalk launch

There is no three-conductor GCPW 90-degree launch at the antenna terminal.

Each terminal uses one signal-only board-edge/tongue connection:
- terminal + -> signal tongue +;
- terminal - -> signal tongue -.

No ground pad is permitted at the radiator/stalk joint.

The tongue is treated as a short unbacked transition because stalk backside ground is intentionally set back from the radiator plane.

The exact solder fillet/castellation geometry is deferred to the B0G build review, but the electrical rule is frozen:
**signal contact only; zero intentional ground contact at v=0.**

## 7. Ground setback

Nominal first-cut backside-ground onset:
- d_g = 3.0 mm below the radiator feed plane.

Therefore:
- 0 <= v < 3.0 mm: no backing ground behind either signal tongue;
- v >= 3.0 mm: each prong may carry backside ground under its MSL;
- no backside ground may extend above the frozen d_g plane.

d_g = 3.0 mm is an initial architecture-probe value, not an optimized value.
It must later be treated as an EM variable because it controls radiator loading, launch capacitance, and common-mode current.

Planned later sentinels, not authorized here:
- d_g = 2.0 mm;
- d_g = 4.0 mm.

## 8. Twin microstrip first-cut

Each polarization uses two symmetric single-ended microstrip branches.

Nominal geometry:
- trace center positions: u = +-3.0 mm;
- W_MSL = 1.90 mm;
- substrate thickness = 1.00 mm;
- FR4 epsilon_r baseline = 4.3;
- copper thickness inherited from the project physical stack.

W_MSL = 1.90 mm is only a nominal near-50-ohm starting point for 1-mm FR4.
It is NOT an antenna matching decision and it is NOT the final LNA noise match.

The two branches must later be characterized as a coupled two-line structure:
- odd mode;
- even mode;
- differential/common-mode conversion.

No passive pre-LNA balun is included in B0.

## 9. First-stage LNA architecture

Per polarization:
- two QPL9547 devices are reserved;
- one device receives the + terminal branch;
- one device receives the - terminal branch.

Per dual-polarization element:
- four first-stage QPL9547 devices total.

QPL9547 architecture facts used here:
- single-ended device;
- nominally internally matched RF LNA family;
- 0.1-6 GHz published frequency range;
- 2 x 2 mm DFN package;
- published 0.3 dB NF at 2 GHz.

The B0 geometry freeze uses **package/ground-via keepout envelopes only**.
Actual pad map, RF pad launch, bias network, decoupling and thermal/ground-via array require a later QPL9547 package-layout freeze.

Nominal package center locations for the first geometry probe:
- u = +3.0 mm, v = 7.0 mm;
- u = -3.0 mm, v = 7.0 mm.

This keeps the first active device close to the antenna while placing it well inside a region with real FR4 and stalk ground beneath it.

## 10. Ground-via rule

The old T01 vertical via fence is deleted from the antenna-feed architecture.

B0 hard rule:
- every LNA ground via and every future stitching via must pass through positive-volume stalk FR4;
- a via center inside a slot/notch/air region is an automatic geometry HOLD.

The first B0 build uses only via-reserve predicates around the LNA envelopes.
No fake via is inserted merely for visual completeness.

## 11. Ground topology on the fork head

Because the central slot divides the upper stalk:
- each RF prong initially has its own backside ground rail below d_g;
- the two rails are allowed to merge into a broad common stalk ground only below the sensitive feed/LNA head.

The exact merge/interlock height is deferred to lower-body mechanical design.
It must not require a ground bridge across the radiator feed region.

This avoids forcing an RF-ground conductor through the center of the balanced radiator.

## 12. Mechanical rules

The previous H3A top notch / top mechanical-land pattern is not inherited.

Reusable concepts:
- vertical PCB support;
- tab/slot assembly;
- lower board-to-board mechanical interlock;
- separate mechanical and RF functions.

New hard rules:
- no mechanical copper or solder land inside the signal-tongue launch zone;
- no mechanical tab may touch radiator copper unless explicitly designed as a radiator conductor;
- mechanical registration features must remain outside the two terminal paths;
- the orthogonal-stalk crossing/interlock shall be below the pre-LNA feed head or use explicit central clearances;
- mechanical changes below the feed head must not move the frozen terminal/twin-MSL/LNA coordinates.

## 13. Post-LNA boundary

B0 freezes only the first-stage topology.

After each QPL9547:
- two amplified single-ended branch outputs remain available;
- differential-to-single-ended combining is deferred;
- filtering is deferred;
- output connector/backplane routing is deferred;
- T01-A may be reconsidered here because loss is now post-gain.

This explicitly separates:
PRE-LNA = balanced two-terminal -> twin signal paths -> twin LNAs
from
POST-LNA = grounded RF routing / combining / service.

## 14. What B0 does not claim

B0 does not claim:
- W_MSL = 1.90 mm is the final impedance/noise match;
- d_g = 3.0 mm is optimal;
- QPL9547 is proven as the final first-stage device;
- the lower stalk outline/interlock is final;
- a four-LNA implementation has been noise/stability optimized;
- the architecture is superior to Architecture A before EM evidence.

It only freezes a physically coherent first candidate.

## 15. B0G next build-only node

Next proposed node:
R1E1A4A_AR0_B0G_FEED_HEAD_BUILD_ONLY

Build-only scope:
- qualified P094 radiator geometry;
- no new ground on radiator PCB;
- two orthogonal fork-head stalks;
- two signal tongues per stalk;
- nominal twin MSL traces;
- backside ground setback and ground rails;
- four non-conductive QPL9547 package envelopes;
- non-conductive ground-via reserve zones;
- no active transistor model;
- no matching network;
- no RF port;
- no solver.

Build-only acceptance:
- radiator copper unchanged;
- zero radiator/backside-ground overlap;
- zero galvanic radiator-to-ground contact;
- exact Pol-A/Pol-B rotation at the feed heads;
- all four terminal-to-tongue contacts intentional and unique;
- d_g exactly 3.0 mm;
- no ground metal above d_g;
- MSL center/width symmetry;
- QPL9547 envelopes entirely on real stalk FR4;
- via-reserve zones entirely on real stalk FR4;
- orthogonal stalk feed-heads do not geometrically collide;
- no unexplained positive-volume overlap;
- fresh reopen;
- zero port;
- zero solver result.

Human 3D review is mandatory before any passive EM solve.

## 16. Architecture-A status

Architecture A is not rejected.

It is deferred as:
AR0-A-DEFERRED_SENTINEL

Its future hard rule remains:
LNA/electronics local-ground island and shield may not overlap radiator copper on either side of the radiator PCB.

No A build is authorized by this freeze.

## 17. Stop boundary

This document does not authorize BUILD or SOLVE.

Current stop:
AWAIT B0G BUILD-ONLY AUTHORIZATION.
