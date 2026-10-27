# R4-A0-E2C Combined Passive Sentinel Contract V0.1

Status: SOLVE CONTRACT FROZEN — INACTIVE UNTIL E2C BUILD + HUMAN PASS  
Date: 2026-09-29

## 1. Purpose

The first combined dual-pol solve is a **coexistence sentinel**, not a complete network extraction.

Question:

**Does installing all four frozen landing zones simultaneously materially perturb the already-qualified isolated Pol-A and Pol-B source-side behavior?**

Do not compute a full raw 24x24 network unless this sentinel shows evidence that requires it.

## 2. Solve-copy reduction

Raw build network: 24 ports.

For each of four branches retain:
- E_UP;
- P_IN;
- P_OUT as a passive 50-ohm matched load.

Remove from the solve copy:
- E_DN;
- B_VDD;
- B_VBIAS.

Physical pads remain unchanged/open where circuit-domain parts are absent.

Final combined sentinel network: 12 ports.

## 3. Frozen 12-port semantic map

1 A_P_E_UP — source  
2 A_P_P_IN — source  
3 A_P_P_OUT_LOAD50 — load-only

4 A_N_E_UP — source  
5 A_N_P_IN — source  
6 A_N_P_OUT_LOAD50 — load-only

7 B_P_E_UP — source  
8 B_P_P_IN — source  
9 B_P_P_OUT_LOAD50 — load-only

10 B_N_E_UP — source  
11 B_N_P_IN — source  
12 B_N_P_OUT_LOAD50 — load-only

Source excitation set:

`{1,2,4,5,7,8,10,11}`

Matched-load-only set:

`{3,6,9,12}`

No load-only port may be excited.

## 4. Required response

Required common-run response:

12 rows x 8 source columns = **96 complex traces**.

No output-load source columns are required.

No full 24x24 or 12x12 source-complete matrix is required in this first sentinel.

## 5. Solver fidelity

Same fidelity as the qualified isolated S0L baselines:

- frequency: 1.0..1.8 GHz;
- decision band: 1.15..1.65 GHz;
- reference L5/L2/L1;
- CST HF Frequency Domain;
- second-order tetrahedral mesh;
- adaptive mesh;
- MaxDeltaS = 0.02;
- two consecutive native DeltaS <=0.02;
- MaxPasses = 16;
- open radiation boundaries;
- one formal solver invocation;
- automatic retry = 0.

Native solver log is convergence authority.

## 6. Hard numerical gates

1. exact qualified E2C build SHA;
2. solve-copy geometry identity unchanged;
3. exactly 12 reduced ports with exact semantic map;
4. exact eight-source excitation list;
5. four P_OUT ports are passive 50-ohm load-only;
6. result tree empty before solve;
7. final two native DeltaS <=0.02;
8. all 96 required traces exist on one common run/grid;
9. source-side reciprocity among the eight excited source ports:
   `max |Sij-Sji| <= 0.02`;
10. for every source column, power sum over all 12 response rows <=1.02;
11. no fatal solver error;
12. no mesh corruption.

## 7. Coexistence comparison authority

Existing isolated baselines are fixed references:

Pol-A solved SHA:
`811a31eabcd193bcf5f9cbecdf05f8aab1b1ab945bad4bda51a94d21d57b04b3`

Pol-B solved SHA:
`2abafb4435a6f1dc7bfcadec029ee1c81436cf91f27fefe99ca64337820eba02`

For each polarization, extract from E2C the same four source-side nodes:

`E_P, E_N, P_IN_P, P_IN_N`

and transform to:
- E differential/common;
- P_IN differential/common.

Compare combined vs isolated on the same frequency grid.

## 8. Frozen scientific review triggers

These are pre-frozen mechanism/promotion triggers, not optimization targets.

### 8.1 Own-pol source-network perturbation

For the corresponding own-pol source-side 4x4 complex S block:

- max pointwise complex `|S_combined - S_isolated| > 0.10` => REVIEW;
- >0.20 => SEVERE REVIEW.

### 8.2 Differential/common conversion degradation

For:
- E diff->common;
- E common->diff;
- E diff->P_IN common;
- E common->P_IN diff;
- P_IN diff->common;
- P_IN common->diff;

if the combined peak decision-band magnitude is stronger than the isolated baseline by:
- >3 dB => REVIEW;
- >6 dB => SEVERE REVIEW.

### 8.3 Branch imbalance

Within either polarization:

single-ended E_UP return-magnitude imbalance >1 dB => REVIEW.

### 8.4 New narrow mechanism

Any unintended coupling/conversion trace with:
- >=10 dB excursion over <=50 MHz

=> resonance/mechanism REVIEW.

### 8.5 Cross-pol device-side coupling

Cross-pol P_IN / P_OUT-load coupling:
- > -20 dB => REVIEW;
- > -10 dB => SEVERE REVIEW.

These are sentinels, not final polarization-isolation specifications.

## 9. Promotion rule

### Direct E2C PASS

Allowed only if:
- all hard numerical gates PASS;
- no SEVERE trigger;
- own-pol max complex perturbation <=0.10;
- no >3 dB own-pol mode-conversion degradation;
- no branch-imbalance review;
- no resonance review.

Then:
- no combined full 24x24 network is required before active-model authority work;
- E2C establishes that the other polarization's complete active-feed hardware is a small perturbation at the passive source-side level.

### REVIEW

If a non-severe trigger occurs:
- classify the mechanism offline first;
- do not retune geometry;
- promote to a targeted full-network/mechanism extraction only if attribution requires it.

### SEVERE / hard failure

HOLD:
- no C1 promotion;
- no geometry retune without a newly frozen mechanism hypothesis.

## 10. Active-co-sim boundary

Even an E2C PASS does **not** make this 12-port/8-source partial network sufficient for unconditional active stability analysis.

Reverse feedback / arbitrary output and bias terminations still require a separately frozen full passive network authority for C1.

## 11. Authorization

This contract is frozen now but inactive.

BUILD_AUTHORIZED = false  
SOLVE_AUTHORIZED = false

Activation sequence:

`E2C source/static audit -> BUILD authorization -> build PASS -> human review PASS -> SOLVE authorization -> combined sentinel`
