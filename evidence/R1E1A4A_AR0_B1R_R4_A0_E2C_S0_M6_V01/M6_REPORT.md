# E2C S0 M6 Static Geometry Attribution V0.1

Status: **PASS_M6_STATIC_GEOMETRY_ATTRIBUTION_READY**

No CST launch, BUILD, or SOLVE was used.

## Geometry inventory

- Pol-A: {'SIGNAL': 0, 'GROUND': 0, 'VIA': 0, 'OTHER': 0}
- Pol-B: {'SIGNAL': 0, 'GROUND': 0, 'VIA': 0, 'OTHER': 0}

## Closest cross-polarization classified pairs


## Minimum attribution variants

### M6-SIG
Test whether opposite-polarization pre-CIN signal copper is the dominant mixed-mode coupling path.

**Action:** In a disposable E2C copy, suppress only the opposite-pol active landing-zone SIGNAL extensions from upstream MSL/taper through E_UP-side C_IN pad while preserving radiator/feed parent geometry and all local-ground/via geometry.

**Prediction:** principal A/B modal coupling and same-pol diff/common degradation both improve strongly; ground-related branch imbalance may remain.

### M6-GND
Test whether branch-local ground/backside/via structures are the dominant mixed-mode coupling path.

**Action:** In a disposable E2C copy, retain all signal copper but remove only the added opposite-pol local-ground/paddle/spoke/backside-ground/via system that was absent in the isolated baseline comparison, using an electrically well-defined audit replacement only if required to keep ports valid.

**Prediction:** branch imbalance and diff/common conversion improve more than raw E_UP signal-to-signal coupling.

### M6-INT
Test signal-ground interaction if neither pure signal nor pure ground ablation explains the mixed eigenchannel.

**Action:** Retain both classes but selectively increase only the closest A/B signal-to-ground separation identified by the static geometry audit, without changing radiator dimensions or device-side geometry.

**Prediction:** modal coupling improves only when the nearest signal-ground adjacency is perturbed, while pure-class ablations are incomplete.

## Boundary

This is an attribution plan only. No BUILD or SOLVE authorization is created.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false
