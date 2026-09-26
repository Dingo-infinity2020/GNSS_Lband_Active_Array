# R1E1A4A Reference Plane + Passive-EM / LNA Co-Simulation Spec

Status: DESIGN DRAFT — NO CST BUILD OR SOLVER AUTHORIZATION

## Core decision

Do not put the active transistor model directly into the periodic CST model as the next step.

Instead separate the problem at physically meaningful reference planes:
- CST / full-wave EM owns the passive antenna + periodic environment + support + active-hub PCB geometry + local ground/shield geometry + passive package/launch geometry as needed;
- circuit/noise analysis owns the active QPL9547 or later LNA device model;
- the two domains meet at two single-ended LNA input planes P1A/P1B per polarization.

This permits scan-dependent EM extraction and LNA noise/stability analysis without forcing a 50-ohm pre-LNA interface.

## Present P0 model

The current P094 periodic model uses one ideal differential port between the Pol-A terminal regions.

This is sufficient for differential Z_active screening but insufficient to prove what two physical single-ended LNAs referenced to a finite local ground will see.

The current model does not independently expose common-mode impedance, mode conversion, branch imbalance, local-ground current, shield/hub coupling, or the feed transition from radiator contact to device package.

## Required next passive-EM interface

Future support/hub-inclusive CST models should expose two symmetric single-ended ports for one polarization:
- P1A: terminal-A / LNA-A input to the defined local RF ground;
- P1B: terminal-B / LNA-B input to the same defined local RF ground.

From the 2-port single-ended S/Z matrix, derive mixed-mode quantities:
- Sdd / Zdd differential mode;
- Scc / Zcc common mode;
- Sdc and Scd mode conversion;
- per-branch source impedance under the intended odd-mode excitation.

Only after this model demonstrates the intended symmetry / virtual-ground condition may the simpler relation `Z_branch = Z_diff / 2` be used as a qualified approximation.

## Passive hub content

The first mixed-mode model should include enough passive geometry to make P1 physically meaningful:
- source-facing radiator contact / pad geometry;
- small local ground used by both LNA branches;
- candidate structural PCB / support geometry where applicable;
- passive feed traces from antenna terminals to LNA package input pads;
- RF shield envelope or grounded wall if mechanically credible;
- via / return-current structures that exist before first gain.

Do not include arbitrary downstream circuitry that is shielded behind the first gain stage and cannot materially change the antenna-side source condition.

The active QPL9547 device itself remains outside CST.

## Circuit co-simulation

For each frequency / scan state:
1. obtain the passive EM multiport seen at P1A/P1B;
2. connect identical QPL9547 G0 device models in the circuit/noise domain;
3. apply the intended odd-mode / correlated antenna excitation representation;
4. compute source-conditioned noise factor / noise temperature, gain and stability;
5. retain common-mode and imbalance diagnostics.

Later ADS implementation may replace the initial Python receiver shadow, but it must reproduce the frozen analytic/noise-parameter checks first.

## Mechanical prioritization

For the next geometry design:
- H0 backside active-hub / local-ground interface is mandatory in the mainline because the final antenna requires feed-point electronics and CHARTS explicitly places active electronics at the feed region;
- C1 central dielectric tube / serviceable standoff is the conventional mechanical comparator;
- C0 bonded Rohacell foam remains the low-epsilon reference / attribution case;
- C2 PCB / printed frame is a structural alternative beneath H0;
- C3 metal carrier is deferred unless intentionally integrated into local ground/shield/common-mode control.

This ordering is a design priority, not a final winner declaration.

## Immediate next work within R1E1A4A

1. Freeze a dimensioned local-ground / active-hub skeleton compatible with the existing four terminal contact zones and exact 90-degree polarization symmetry.
2. Freeze P1A/P1B package-plane coordinates and the two-port port definition.
3. Freeze H0 and the C1/C2 mechanical envelope drawings/parameters; retain the historical S1 bonded-foam geometry as the C0 reference.
4. Complete the QPL9547 receiver-shadow calculation and define Gate R from the receiver requirements.
5. Only then prepare a separate BUILD-ONLY contract for the mixed-mode passive P094 model.

No CST execution is authorized by this document.
