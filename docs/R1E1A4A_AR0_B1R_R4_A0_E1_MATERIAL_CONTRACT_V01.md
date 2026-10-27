# R4-A0-E1 Material / Conductor Contract V0.1

Status: FROZEN FOR E1 BASELINE + LATER SENSITIVITY

## FR4 baseline

Reuse project-owned low-cost laminate baseline:
- epsilon_r = 4.2
- tan_delta = 0.018
- thickness = 1.00 mm

Provenance:
existing FR4_COST_BASELINE project design baseline.

This remains a generic low-cost FR4 surrogate, not a named laminate guarantee.

## Copper

Physical thickness:
- 0.035 mm, 1 oz class

Solve conductivity baseline:
- sigma = 5.8e7 S/m

Build-only shall use the same physical thickness.

PEC may be used only for isolated geometry-debug sentinel models, not the final E1 qualification solve.

## Copper roughness

E1 baseline:
- smooth copper

Reason:
roughness authority is unavailable for a named board stack.

Later sensitivity:
- add a documented roughness sentinel if E1 loss is close to budget.

## Solder mask

E1 baseline:
- no solder mask over the RF landing-zone coupon.

Interpretation:
explicit local solder-mask keepout over the critical RF traces/package launch region.

Why:
- avoids introducing an uncontrolled generic mask epsilon/tan-delta into the first landing-zone mechanism model;
- keeps reference-plane/launch extraction deterministic.

Rev-D solder-mask opening geometry remains stored for later production-layout checks.

## Solder

E1 baseline EM:
- no volumetric solder fillet model.

Use direct ideal metal continuity between PCB land and device-lead reference plane / component terminal reference.

Solder-volume sensitivity is deferred until the landing-zone topology is electrically sane.

## Package body

QPL9547 body envelope:
- visual/interference object only in build-only
- do not assign it an invented RF dielectric in E1

The active device is represented by external S2P/noise data.

## Boundary between baseline and hardware authority

E1 can qualify topology/launch behavior on this generic material contract.

Hardware release still requires:
- selected FR4 vendor/grade
- measured/manufacturer Dk/Df context
- copper roughness class
- actual solder-mask material
- final ENIG/HASL finish and assembly process.
