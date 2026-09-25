# H3 Orthogonal-PCB Feed-Stalk / Support Architecture Research

Status: DESIGN / RESEARCH ONLY — NO BUILD OR SOLVE AUTHORIZATION

## Why H3 exists

H2A V0.2 proved useful as a service-routing thought experiment, but human review found geometry interference and exposed a deeper packaging issue: separate shield, coax, connector and support objects create many coupled mechanical constraints.

H3 asks whether the support itself can become a controlled PCB RF structure.

The candidate uses two mutually perpendicular vertical PCBs below the horizontal radiator PCB. They form a rigid cross-shaped feed-stalk/support frame and can carry post-LNA RF, bias and later combining/balun functions.

## External precedents reviewed

1. PCB feed arms soldered orthogonally into a feed hub have been used to create three-dimensional antenna feed structures.
2. IPC board-in-board assembly practice explicitly covers daughterboards mounted perpendicular to a parent PCB and soldered through board-in-board joints.
3. Antenna/feed structures exist in which substrate tabs enter cutouts in an orthogonal PCB and multiple solder fillets provide both mechanical and electrical connections.
4. RF board-to-board transitions are not electrically transparent: published vertical-connector work uses GCPW, ground shaping and full-wave optimization to control parasitics.
5. Edge plating / plated board edges are established techniques for RF grounding, shielding and controlled edge transitions.

These precedents support the manufacturability of the concept, but no external dimensions are copied into H3.

## Proposed mechanical topology

- horizontal radiator PCB remains the primary radiating board;
- two vertical support/feed-stalk PCBs are mutually perpendicular;
- preferred orientation is along the two linear-polarization axes rather than arbitrary X/Y axes;
- the two stalk PCBs interlock with a half-depth cross-slot below the feed region;
- each stalk uses dedicated mechanical tabs/tenons into slots in the radiator PCB and later into the lower backplane;
- mechanical tabs should be separated from the sensitive RF transition pads whenever possible;
- solder fillets lock the board-in-board joints after deterministic slot/tab registration.

The interlocking slots are mechanical geometry and must be included in CST, not represented as ideal alignment constraints.

## RF transition philosophy

A naked microstrip ending in an uncontrolled solder blob at a 90-degree PCB junction is NOT the preferred baseline.

Preferred transition family:
- short GCPW or locally ground-referenced signal tongue;
- plated/castellated board edge where fabrication permits;
- signal solder pad plus nearby symmetric ground solder pads;
- local ground clearances designed as part of the transition;
- transition geometry measured from the manufactured board edge, not an abstract centerline;
- full-wave EM model of solder fillet / edge plating / pad discontinuity before RF qualification.

Mechanical tabs and RF tabs should not be forced to be the same feature if that creates a poor RF launch or fragile solder joint.

## LNA placement variants

### H3-L1 — Recommended first architecture
LNA stays on the radiator backside, immediately adjacent to the four feed terminals.

Then:
antenna terminal -> very short input pad/transition -> first-stage LNA -> short post-gain 90-degree transition -> vertical support PCB.

Advantages:
- minimizes pre-LNA passive path and preserves receiver-noise margin;
- makes the mechanically difficult cross-PCB transition occur after first-stage gain;
- lets the vertical stalk carry output RF, bias and later combining functions with relaxed loss requirements.

This is the current preferred H3 baseline.

### H3-L2 — LNA at the top of each vertical stalk
The LNA is mounted very near the stalk top edge and its input is solder-transitioned directly to the radiator terminal region.

Advantages:
- fewer components on the radiator backside;
- potentially clean modular feed-stalk replacement.

Risks:
- the orthogonal-board solder transition becomes pre-LNA and therefore directly affects NF and source impedance;
- edge-ground and package reference plane become harder to separate from antenna loading.

H3-L2 remains a comparison candidate, not the baseline.

## Where differential-to-single-ended conversion belongs

Do not freeze a passive pre-LNA balun merely because the support PCB has space.

Preferred order for the first H3 study:
1. preserve the balanced radiator terminals;
2. place the first low-noise devices as close to the terminals as practical;
3. carry the amplified branch signals onto the vertical stalks;
4. only then consider 180-degree combining, active-balun, transformer/hybrid, filtering or output conversion on the stalk PCB.

Post-gain conversion loss is much less damaging to receiver NF than an equivalent passive loss before the first LNA.

## Why the vertical stalk may be better than the copper-tube/coax candidate

Potential benefits:
- removes long loose micro-coax from the antenna near field;
- RF route becomes lithographically controlled GCPW/stripline rather than cable placement;
- support, ground return, bias routing and RF routing share one deterministic object;
- easier fourfold / two-polarization symmetry;
- fewer separate parts and connector interfaces;
- bottom service connector can be placed on an accessible backplane rather than near the feed.

Risks:
- two dielectric/copper fins are strong EM objects and may significantly move active impedance;
- stalk copper/ground rails can support common-mode or resonant currents;
- cross-slot and solder joints introduce manufacturing tolerance;
- the orthogonal transition must be modeled rather than treated as ideal.

## Proposed next design node (not yet authorized)

`H3A_ORTHOGONAL_STALK_ASSEMBLY_BUILD_ONLY_V01`

Build-only scope should contain:
- radiator PCB;
- two orthogonal interlocking vertical PCB stalks;
- top mechanical tabs and radiator-board slots;
- bottom mechanical tabs/backplane slots;
- representative copper ground rails and post-LNA route envelopes;
- four dummy LNA envelopes on the radiator backside (H3-L1);
- explicit solder-fillet envelopes at mechanical and RF joints;
- no transistor, no RF port, no solver.

Mandatory acceptance includes fresh-reopen CST Geometry Intersection Check under SimulationOps >=0.2.5.
