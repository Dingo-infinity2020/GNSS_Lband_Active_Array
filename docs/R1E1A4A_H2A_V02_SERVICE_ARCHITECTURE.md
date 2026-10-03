# R1E1A4A-H2A V0.2 Service Architecture

Status: BUILD-ONLY AUTHORIZED; NO SOLVE AUTHORIZATION

Purpose:
extend the accepted H2A V0.1 universal center structure so RF outputs have a mechanically credible route from the future LNA region to maintainable backplane interfaces.

H2A V0.2 remains an assembly/interface model. It does not claim RF-optimal cable, connector, tube, shield-window or ground-bond dimensions.

## Lineage

- immutable EM parent remains the qualified bare P094 source;
- H2A V0.1 remains protected review evidence and is not modified;
- V0.2 reproduces the accepted V0.1 feed-module topology and adds service-routing geometry;
- H1A/H1R remain diagnostic/deferred and are not reopened.

## Retained V0.1 topology

- 20 x 20 mm same-board patterned backside ground;
- 8 x 8 mm central RF clearance;
- four signal pad/pin proxies at the terminal centers;
- four 2 x 2 x 0.6 mm dummy LNA package envelopes;
- 18 x 18 mm shield outer envelope;
- no real LNA device, matching network, bias network or RF port.

The old 30 x 30 mm PEEK square carrier is removed from the V0.2 product concept.

## Board-side RF-output service interface

Future LNA orientation rule:
- input faces inward toward the antenna terminal;
- output faces radially outward.

Board-side connector class:
- MHF4 / U.FL-class micro-RF interface;
- V0.2 mechanical envelope = 2.4 x 2.4 x 1.2 mm;
- connector center radius = 9.0 mm on each diagonal;
- exact vendor part and land pattern are NOT frozen.

A visual PCB-route envelope connects each dummy LNA output side to its connector envelope. This route is not an impedance-controlled RF trace and is not conductive authority.

## Cable and shield egress

Internal cable class:
- nominal 0.81 mm micro-coax service envelope;
- exact cable construction is deferred to H2B.

The shield retains four walls and a lid, but each corner is intentionally open as a diagonal RF-service window. The four cable routes leave the LNA/connector region through these windows rather than crossing laterally across the radiator aperture.

Generation-0 bias strategy remains bias-tee over the RF coax. No separate DC harness is added to H2A V0.2; this avoids creating an unplanned fifth service path through the shield/cage.

## Hollow copper service tubes

Four identical hollow copper-tube proxies are placed on the same four diagonal axes:
- tube-center radius = 13.5 mm;
- square outer envelope = 3.0 x 3.0 mm;
- square inner opening = 1.4 x 1.4 mm;
- one nominal 0.81-mm micro-coax envelope runs inside each tube;
- each tube is PEC because the metal structure is expected to be RF-relevant.

Square tubes are used in V0.2 only as a deterministic CST/fabrication envelope proxy. Circular brass/copper tube remains a later manufacturable option.

## Electrical-bond strategy is intentionally NOT frozen

The tube geometry is shared by later T0/T1/T2 passive studies. V0.2 inserts insulating interface spacers so the build does not silently choose a grounding state:
- top PEEK spacer thickness = 0.50 mm between tube and local-ground plane;
- bottom PEEK spacer thickness = 0.50 mm between tube and main backplane;
- both spacers have a central cable clearance hole.

Later passive RF states may replace the relevant spacer/interface with a conductive bridge:
- T0: no conductive tube bond;
- T1: top bonded only;
- T2: top and bottom bonded.

No one of these states is selected or solved in H2A V0.2.

## Backplane service interface

Four cable feedthrough clearances are added to the parent main backplane at the tube axes.

Backplane connector class:
- MMCX-class service connector;
- V0.2 envelope = 5 x 5 x 5.5 mm below the backplane;
- exact connector part, mounting style and launch are NOT frozen.

The intent is a two-level connector system:
internal micro-RF connector + micro-coax above, maintainable MMCX-class service interface below.

## Build-only acceptance

Fresh reopen must verify:
- exact P094 radiator/periodic metadata retained;
- zero RF ports;
- no old PEEK carrier solids;
- patterned ground/pads/pins and four LNA envelopes retained;
- four MHF4/U.FL-class connector envelopes;
- four outward route envelopes and four diagonal micro-coax route envelopes;
- four hollow PEC service tubes;
- four top and four bottom insulating interface spacers;
- four vertical cable envelopes through the tubes;
- four main-backplane feedthrough clearances;
- four MMCX-class lower connector envelopes;
- no solver-generated results.

## Stop boundary

BUILD ONLY. Stop after fresh-reopen qualification for human 3D review.
No H2A V0.2 solve, no H2B/T0/T1/T2 solve, no active LNA integration and no H1R recovery.
