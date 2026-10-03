# R4-A0-E3E R1E2 Array-Interface Freeze V0.1

Status: OFFLINE INTERFACE FREEZE — NO BUILD / NO SOLVE AUTHORIZATION
Date: 2026-10-01

## Purpose

Ensure the accepted E2C R7 active-interface geometry can later enter the authoritative periodic/finite-array source-environment workflow without redefining the LNA reference planes or pretending that a broadside isolated impedance is final.

The old R1E0 94-mm periodic workflow is numerical/method infrastructure, not the final physical source model.

R1E0 already proved that scan-plane dependence is large. At theta=60 deg the C60P45 versus C60P135 active-impedance difference reaches about 209 ohm in the science band. Therefore a single broadside match is not an acceptable LNA-source authority.

## Physical model promoted to R1E2

R1E2 must use the accepted real integrated architecture, not a stripped radiator-only legacy cell.

The periodic unit-cell geometry shall include the then-current accepted:
- dual-polarization radiator
- orthogonal stalk/support mechanics
- RF tenon/tongue/solder launch
- E2C-class active landing-zone passive geometry
- local ground/via structures
- any support/hub/backplane geometry that has been promoted before R1E2

Mechanics that materially alter active impedance are part of the antenna, not removable clutter.## Two source-environment layers

### Layer A — antenna-side array authority

For each polarization, form the balanced differential/common-mode environment from its two E_UP branch nodes:

Pol-A:
A_P_E_UP, A_N_E_UP

Pol-B:
B_P_E_UP, B_N_E_UP

The periodic EM model must preserve all four E_UP single-ended nodes long enough to quantify:
- differential active source environment
- common-mode conversion
- Pol-A/Pol-B cross coupling
- branch asymmetry

A historical single 100-ohm differential port may be used only as a validated numerical sentinel. It is not the final raw interface.

### Layer B — LNA device-source authority

The authoritative QPL9547 source condition is at each P_IN device-lead plane, not at E_UP.

Because C_IN remains a circuit-domain component, P_IN source impedance must be derived only after the qualified passive component model is connected between E_UP and P_IN.

Therefore:
periodic EM network + C_IN model -> scan-dependent P_IN source cloud.

CST alone with an open C_IN gap must not be reported as final LNA source impedance.## Array-state coordinates and outputs

Core scan grid:
theta = 0, 15, 30, 45, 60 deg
phi = 0, 45, 90 deg where symmetry does not make a state redundant.

Extended investigation:
theta = 65, 70, 75 deg only after the core grid is qualified.

For every state, retain exact:
- geometry SHA / source lineage
- pitch and periodic-cell dimensions
- theta / phi and polarization excitation
- frequency grid
- port/reference-plane map
- solver convergence provenance

Required Layer-A outputs:
- complex active S / Z at E_UP differential and common modes
- Pol-A/Pol-B coupling and symmetry metrics
- common-mode conversion
- embedded element pattern
- co/cross-pol pattern
- radiation efficiency and realized gain
- scan-blindness/resonance indicators

Required Layer-B outputs after circuit reconnection:
- complex source impedance at every P_IN device plane
- differential/common-mode source cloud per polarization
- branch-to-branch source imbalance
- source conditions exported in a circuit-consumable table tied to scan/frequency/geometry metadata.## Active impedance definition

For a periodic/multiport representation, active reflection at a retained port must include the scan-dependent coherent excitation of coupled ports rather than using isolated S11 alone.

Conceptually:

Gamma_active,m = (sum_n S_mn a_n) / a_m

with the excitation vector a_n carrying the lattice scan phase and the intended polarization/mode excitation.

Any conversion to Z_active must state the reference impedance and mode basis used.

For the balanced polarization source environment, single-ended branch waves shall be transformed into differential/common modes explicitly. Do not infer a 100-ohm target from the transform.

## Finite-array closure

Infinite periodic R1E2 is the primary source-cloud generator, not final hardware release authority by itself.

A later finite passive array, nominally 5x5 or 7x7 as resources permit, must inspect:
- center element
- edge element
- corner element

If finite-array source loci extend beyond the periodic cloud, the union/envelope becomes the LNA robustness domain.

The finite-array comparison must use the same physical reference-plane semantics as R1E2; it may not silently fall back to a different legacy feed port.## Promotion sequence

Current order remains:

E2C coexistence sentinel
-> device/passive component authority restoration
-> full passive-network authority as required for active feedback/stability
-> R1E2 integrated periodic active-impedance / embedded-pattern atlas
-> circuit co-design against the resulting source cloud
-> finite-array center/edge/corner expansion
-> final active-array validation

Circuit-only QPL9547 research may continue in parallel, but no final input match may be frozen before the R1E2/finite-array source domain exists.

## Decision

PASS_E3E_R1E2_ARRAY_INTERFACE_COMPATIBLE

The E2C R7 branch/device reference-plane architecture is compatible with the later active-array workflow.

No geometry rebuild is required merely to preserve future array compatibility.

Future R1E2 must promote the integrated physical element and preserve a four-E_UP single-ended raw interface before mode transformation.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false

Next offline node:
E3F_CANONICAL_MODEL_LINEAGE_AND_SUPERSESSION_MAP