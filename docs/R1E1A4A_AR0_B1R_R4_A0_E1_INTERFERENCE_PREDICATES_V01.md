# R4-A0-E1 Geometry / Interference Predicates V0.1

Status: FROZEN FOR BUILD-ONLY GATE

## Allowed intentional contacts

Allowed:
- paddle-via barrel intersects FR4 by design
- paddle-via barrel joins top paddle copper
- paddle-via barrel joins backside local ground
- decoupling ground via joins its ground pad and backside ground
- RF taper touches its intended signal pad/land
- grounded NC/shutdown copper touches intended local-ground via/feature

All other positive-volume conductive overlaps require explicit ownership.

## Hard no-overlap predicates

Must be zero positive-volume:
- signal copper vs backside ground
- signal copper vs paddle via barrel
- signal copper vs decoupling ground via
- RF-IN node vs RF-OUT node
- C_IN two pad nodes
- C_OUT two pad nodes
- L1 two pad nodes
- C_RF VDD and ground pad nodes
- P_OUT fan vs local-ground top copper
- any RF/bias copper vs board edge/slot void as a solid collision
- package body envelope vs another component body envelope

## Clearance predicates

G0 minimums:

Signal copper to via-barrel OD:
>= 0.20 mm.

Via-barrel OD to coupon side edge:
>= 0.20 mm.

Component copper to coupon side edge:
>= 0.10 mm for build seed;
target >=0.20 mm for hardware DFM.

Unrelated top-copper node to unrelated top-copper node:
>= 0.20 mm unless a vendor land pattern forces a smaller package-internal spacing.

Package/body envelope to board edge:
>= 0.25 mm.

## FR4 embedding predicate

Top copper:
must lie on/outside front surface:
n >= 0.

Backside copper:
must lie on/outside backside:
n <= -1.0 mm.

No finite-thickness copper land/trace may be embedded inside -1<n<0 FR4, except plated via barrel walls which intentionally traverse the substrate.

This explicitly inherits the lesson from the T1 backside-ground sign error.

## Port validity predicates

Every discrete/conductor-interface port:
- signal endpoint at signal/FR4 interface n=0
- ground endpoint at backside-ground/FR4 interface n=-1.0
- line segment traverses FR4 only
- port line does not cross finite-thickness copper
- port endpoints lie inside their intended conductor footprint
- no two port segments intersect

## Build-only evidence

Must record:
- deterministic solid inventory
- node ownership table
- port endpoint table
- all via coordinates
- all component-pad rectangles
- fresh-reopen hash
- zero result tree
- solver invocation count = 0

Boolean/interference checks shall use pairwise temporary copies where destructive CST operations would consume solids.
