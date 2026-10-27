# R4-A0-E1 Local-Ground / Half-Lap Policy V0.1

Status: BASELINE SELECTED FOR A0-E1; TWIN-LNA COMMON-GROUND TOPOLOGY STILL OPEN

## Baseline G-L0

The first A0-E1 remote model is ONE LNA only.

Its ground is:
QPL9547 paddle
-> three local plated vias
-> finite backside branch-local RF ground.

This is a complete local single-ended RF reference for one LNA.

No long lower-stalk common-ground merge is required to make the one-LNA landing zone valid.

## Twin-LNA interpretation

For later A0-E2:
- each first-stage LNA gets its own valid local branch ground
- the two branch grounds are allowed to remain separate through the immediate first-stage region
- the EM model must retain their finite coupling/common-mode behavior

A low-inductance local common connection may be introduced as G-L1 only if it is mechanically real.

## Mechanical consequence

The exact old half-lap slot is no longer allowed to dictate first-stage RF grounding.

Frozen:
- two orthogonal stalk architecture
- radiator/stalk mechanical support concept
- stalk/reflector support concept

Released:
- local slot extent
- slot termination position
- local bridge/window geometry around the active electronics

However A0-E1 does not yet modify the half-lap because it is a one-LNA local coupon.

## G-L1 candidates for later twin-LNA study

Candidate 1:
local mechanically supported PCB bridge/window created by shortening or reshaping the half-lap slot.

Candidate 2:
short intentional RF ground interconnect / plated structural feature with explicit EM model.

Candidate 3:
grounded shield/metal feature that is simultaneously mechanical and RF ground.

No unsupported floating copper strap is allowed.

## G-R sentinel

The prior M0/M1 remote lower-stalk merge remains a sentinel only.

It shall not be used as the default first-stage LNA grounding topology.
