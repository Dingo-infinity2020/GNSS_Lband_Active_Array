# R4-A0-E1 Prebuild Review Checklist V0.1

Status: PREBUILD CONTRACT NEAR-COMPLETE — NO BUILD AUTHORIZATION YET

Before first NW/CST call all items below must be PASS.

## Footprint

PASS:
- Rev-D package geometry transcribed
- Rev-D metal lands transcribed
- Rev-D solder-mask openings transcribed
- package pin numbering / RF-IN / RF-OUT orientation explicit
- one physical package rotation for both branches
- real package asymmetry retained

## Local ground

PASS:
- one-LNA baseline uses branch-local ground
- three local paddle vias
- no dependence on remote lower-stalk merge
- old half-lap exact slot geometry released if later twin-LNA ground requires local modification

## Bias / passive topology

PASS:
- input DC block mandatory
- output DC block mandatory
- pin 7 shared RF-OUT/VDD topology explicit
- 18-nH bias choke seed explicit
- VDD 100-pF + 1-uF decoupling topology explicit
- pin 6 FDD ground state explicit
- NC-pin ground choice explicit

## Circuit model seeds

PASS:
- QPL9547 G0 S/noise provenance retained
- Murata GRM1555C1H101JA01# selected as G0 100-pF C0G model family
- Coilcraft 0402CS-18NXGRW retained as G0 choke with real-model requirement

## E1 ports

PASS topology:
- E_UP
- P_IN
- P_OUT
- E_DN
- B_VDD
- all 50-ohm-normalized single-ended to finite local branch ground
- no differential port

PENDING:
- exact global/local coordinate table after the final E1 placement drawing is frozen

## Still required before BUILD_AUTHORIZED=true

1. final dimensioned E1 placement drawing:
   - package center
   - C_IN / C_OUT pad centers
   - L1 and decoupler pad centers
   - via centers
   - local-ground extents
   - short line extents

2. material contract:
   - FR4 epsilon_r / tan_delta authority for the selected board material
   - copper conductivity / roughness policy
   - solder-mask include/exclude decision
   - solder approximation

3. deterministic geometry predicates:
   - signal-to-via clearance
   - package-to-second-LNA keepout
   - component-to-slot/board-edge clearance
   - no positive-volume copper/FR4 embedding errors
   - no signal-ground shorts

4. build-only artifact names / hashes / fresh-reopen audit

Only after those four items:
BUILD_AUTHORIZED may be requested.
SOLVE remains separately gated.
