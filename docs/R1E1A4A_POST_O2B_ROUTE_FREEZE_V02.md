# Post-O2B Route Freeze V0.2

Status: FROZEN — O3/O4 BUILD+SOLVE AUTHORIZED

This document supersedes the old automatic continuation from O2B into O2C nominal tuning.

## Decision

The qualified O2B winner P20_G30_E30 is accepted as the nominal transition geometry for physical-fidelity verification.

O2C ground/via/solder optimization is DEFERRED_CONTINGENCY_ONLY. It may be reopened only if O3 physical-fidelity or O4 manufacturing sentinels fail an acceptable gate and the failure is attributable to return-path / via / solder behavior.

No further nominal signal-pad tuning is authorized.

## O3 — physical-fidelity qualification

Nominal geometry is frozen:
- Wsig = 1.50 mm
- Gcpw = 0.40 mm
- signal pad width = 2.00 mm
- pad gap = 0.30 mm
- transition extension = 0.30 mm
- all via, ground-pad, board, RP1/RP2 and mechanical coordinates from P20_G30_E30

O3 adds physical conductor models without changing geometry:
- copper conductors: finite conductivity, sigma = 5.8e7 S/m engineering model
- solder blocks: explicit finite-conductivity solder proxy, sigma = 7.0e6 S/m
- FR4 model remains the already frozen cost-baseline dielectric

O3 requires two matched fresh-run models:
1. transition winner with finite-conductivity copper + solder
2. W15_G40 straight reference with identical copper model and identical discrete-port convention

Solver fidelity:
- 1.0–2.0 GHz
- second-order tetrahedral
- MaxDeltaS = 0.02
- two consecutive checks
- MaxPasses = 16
- no silent retry

Acceptance across 1.15–1.65 GHz:
- acceptable worst-case return loss >= 12 dB
- preferred >= 15 dB is informative, not mandatory for project continuation
- junction excess loss versus paired copper straight reference <= 0.15 dB acceptable, <= 0.10 dB preferred
- no S21 notch below -3 dB
- reciprocity difference <= 0.05 dB

The paired straight reference is the required port-model/de-embedding sentinel for this stage.

## O4 — minimal deterministic manufacturing sentinels

O4 is validation, not optimization. Nominal O3 is the baseline.

Exactly six sentinel cases are frozen:
1. FAB_LOWZ: Wsig +0.10 mm and Gcpw -0.05 mm
2. FAB_HIGHZ: Wsig -0.10 mm and Gcpw +0.05 mm
3. ALIGN_P020: vertical-board lateral x offset +0.20 mm
4. ALIGN_M020: vertical-board lateral x offset -0.20 mm
5. SOLDER_SMALL: preserve both PCB contact faces; reduce only the free solder protrusion in +y and -z by 25% from nominal
6. SOLDER_LARGE: preserve both PCB contact faces; increase only the free solder protrusion in +y and -z by 25% from nominal

All other geometry is frozen. No candidate selection and no winner promotion are permitted.

Each sentinel uses the same finite-conductivity material assumptions and full O3 solver fidelity.

O4 PASS condition:
- every sentinel remains numerically converged
- every sentinel keeps worst-case core-band return loss >= 12 dB
- no S21 notch below -3 dB
- reciprocity difference <= 0.05 dB
- no gross topology/intersection failure

O4 is allowed to miss the 15 dB preferred return target.

## T01-A FREEZE

If O3 and O4 PASS:
- freeze P20_G30_E30-derived physical geometry
- freeze RP1/RP2
- freeze finite-conductivity nominal Touchstone/N-port
- freeze paired straight-reference result
- freeze O3 junction-excess report
- freeze O4 sentinel report
- mark O2C contingency closed but recoverable

Then move immediately to H3B Complete Passive Unit / H3B-I01. The active-antenna route remains:

T01-A FREEZE
→ H3B Complete Passive Unit
→ H3B-I01 passive integrated pilot
→ LNA-on-stalk A0 engineering prototype
→ realistic periodic unit cell
→ R1E2 active-impedance atlas
→ A1 final antenna/LNA co-design
→ 2x2 then 4x4 finite active-array validation.

T01-C remains deferred.
