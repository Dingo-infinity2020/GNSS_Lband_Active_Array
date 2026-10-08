# R4-A0-E2 A/B Passive Promotion Closure V0.1

Status: PASS  
Date: 2026-09-29

## Conclusion

Pol-B passes the mechanical/asymmetry sentinel without RF retuning.

The sole Pol-B geometry delta from the proven E2A cell is the 0.125 mm x 1 mm N-branch backside-ground half-lap clearance notch.

No frozen comparative review gate is triggered.

## Numerical authority

Pol-B formal solver invocation count: 1  
Automatic retries: 0  
Read-only recovery solver invocations: 0

Pol-B native final DeltaS:
- 0.00656218
- 0.00869598

24/24 loaded-source response traces are present on a common 1001-point 1.0..1.8 GHz grid.

Max source-side reciprocity residual:
2.199e-5

Max loaded column power:
0.9999873

## Mixed-mode A/B comparison

Peak decision-band conversion:

| Quantity | Pol-A | Pol-B | B-A |
|---|---:|---:|---:|
| E diff -> common | -30.711 dB | -32.433 dB | -1.722 dB |
| E common -> diff | -30.712 dB | -32.426 dB | -1.714 dB |
| E diff -> P_IN common | -67.615 dB | -69.181 dB | -1.566 dB |
| E common -> P_IN diff | -69.457 dB | -70.901 dB | -1.444 dB |
| P_IN diff -> common | -73.533 dB | -75.737 dB | -2.203 dB |
| P_IN common -> diff | -73.534 dB | -75.736 dB | -2.202 dB |

Positive degradation review was frozen at >6 dB. Pol-B does not degrade any of these conversion quantities; all are slightly lower than Pol-A.

Branch return-magnitude imbalance:
- Pol-A: 0.225 dB
- Pol-B: 0.186 dB
- review threshold: >1 dB

Largest <=50 MHz E-terminal mutual-coupling excursion:
- Pol-A: 1.009 dB
- Pol-B: 0.990 dB
- resonance review threshold: >=10 dB

## Mesh-warning classification

Pol-B TetMesherError problematic positions remain at:
- z approximately 57.143 mm: RF tongue contact edges;
- z approximately 58.143 / 58.428 mm: solder-bridge lower/upper seams.

No problematic position occurs in the lower-body half-lap region.

The known edge-contact warning remains a future loss/NF-modeling debt but is not a Pol-B half-lap failure.

## Decision

PASS_R1E1A4A_AR0_B1R_R4_A0_E2AB_PASSIVE_PROMOTION

- no Pol-B passive retune;
- no narrow mechanism probe;
- no additional passive solve required;
- E2 passive geometry mainline closes here.

Next:
R1E1A4A_AR0_B1R_R4_A0_C1_ACTIVE_COSIM_CONTRACT_FREEZE

C1 must be frozen from first principles before any additional solve. In particular, the minimum EM-network authority required for reverse feedback / active stability must be decided rather than automatically assuming that the S0L four-source partial matrix is sufficient.
