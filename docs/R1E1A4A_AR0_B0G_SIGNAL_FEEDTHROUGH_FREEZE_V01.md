# AR0-B0G Signal-Only Feedthrough Implementation Freeze V0.1

Status: FROZEN FOR AUTHORIZED B0G BUILD-ONLY

## Why this addendum exists

The radiator terminals are on the top copper while the stalk approaches from below the 1.0-mm radiator substrate. A literal edge tongue cannot contact the top terminal without either a board slot or a signal feedthrough.

For the first B0G geometry probe, use a **signal-only plated feedthrough** at each of the four qualified terminal centers.

This is an implementation detail of the already frozen B0 rule:
terminal -> signal path only; no ground contact at the radiator/stalk joint.

## Geometry

For each terminal:
- center = existing qualified terminal coordinate;
- substrate hole radius = 0.20 mm;
- plated barrel outer radius = 0.20 mm;
- plated barrel inner radius = 0.10 mm;
- barrel spans from radiator substrate bottom to top-copper bottom;
- top end contacts the existing radiator copper by face contact;
- bottom end contacts the stalk-front signal trace by face contact.

The radiator top-copper solid is not cut, enlarged or re-shaped.
Only a small substrate feedthrough hole is added at the terminal point.

No bottom ground pad.
No ground via.
No backing ground on the radiator PCB.

## Stalk reference plane

For each polarization, the stalk is offset so its **front signal face passes through the two terminal/feedthrough centers**.
The 1.0-mm stalk dielectric extends entirely behind that signal face.

This lets the feedthrough barrel meet the top edge of the microstrip signal without an artificial conductive bridge through stalk FR4.

## Status

The feedthrough dimensions are first-cut build geometry, not an optimized RF via.
Any later change requires a separate EM/tolerance stage.

No solver is authorized by this addendum.
