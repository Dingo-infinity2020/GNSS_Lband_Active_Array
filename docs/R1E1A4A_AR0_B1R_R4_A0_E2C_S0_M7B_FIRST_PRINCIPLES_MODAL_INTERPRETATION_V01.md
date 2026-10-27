# M7B First-Principles Modal Interpretation V0.1

## Conclusion

M7B is not simply a partial version of the desired solution. It performs two different electrical actions at once:

1. it removes the mechanism that makes the + and - branches electrically unequal;
2. it also removes too much of the local CIN return reference, creating a large symmetric differential-mode impedance discontinuity.

The first action is beneficial; the second is harmful.

## Minimal two-branch model

For one polarization, write the source-side pair as

[
A=rac{S_{++}+S_{--}}{2},qquad
M=rac{S_{+-}+S_{-+}}{2}.
]

Then approximately

[
S_{dd}=A-M,
]

while, for a reciprocal pair, differential-to-common conversion is dominated by the branch asymmetry

[
S_{dc}simrac{S_{++}-S_{--}}{2}.
]

This separates three physically different questions:
- are the two branches unequal;
- are the branches strongly coupled to one another;
- or are both branches being shifted together by the same local environment?

## What M7B actually did

Across 1.2056, 1.2984, 1.3432, 1.5752 and 1.6496 GHz:

- branch asymmetry / Sdc falls to about 4–8% of the full-E2C deviation;
- the branch mutual-average term remains roughly 0.76–1.06 times the full-E2C deviation;
- the self-average term grows to roughly 1.7–2.4 times full E2C;
- the differential Sdd deviation grows to roughly 2.25–3.60 times full E2C.

Therefore the large M7B residual is not primarily a remaining asymmetry or direct branch-to-branch coupling. It is dominated by symmetric self-loading.

The penalty grows toward the upper band rather than appearing as a narrow new resonance. This is consistent with removing a local pad-to-ground RF reference / capacitance: the local discontinuity becomes more important as frequency rises.

## Physical interpretation

The full-E2C state is best represented as:

[
	ext{CIN signal pad}
ightarrow C_mathrm{local}
ightarrow 	ext{non-ideal local/shared return network}.
]

If the effective return seen by + and - branches is unequal, the same pad-to-return coupling creates branch imbalance and differential/common-mode conversion.

M7B makes (C_mathrm{local}) much smaller by deleting the ground directly under the pad. That decouples the signal from the unequal return environment, which is why branch imbalance and Sdc collapse.

But the same action also removes the intended local RF reference. Hence both branches are shifted together and Sdd becomes worse.

This explains why M7B can simultaneously be spectacularly good for branch balance and bad for source-side differential impedance.

## Relation to M6 and M7A

- M6-D1: opposite-pol pre-CIN signal metal alone is weak, so direct signal-signal overlap is not the primary mechanism.
- M6-D2: ground/backside/via metal is important, especially for mode conversion, but its frequency shape is not a scaled copy of full E2C.
- M7A: moving the upstream center-facing ground edge does not help.
- M7B: changing only the ground directly under CIN removes the asymmetry mechanism, proving that the terminal-local signal/return coupling is real.

After the modal decomposition, the remaining uncertainty is narrower than before: a larger shared-return contribution may still exist in full E2C, but the present M7B result is dominated by the self-loading penalty created by the full under-pad aperture. That penalty must be removed before another large-scale ground hypothesis can be tested cleanly.

## Next geometry principle

Do not enlarge the M7B hole.

The next topology should try to satisfy two conditions simultaneously:

1. **keep a local RF reference directly under/near the CIN pad**, preserving the average self impedance;
2. **prevent that local return from freely participating in the shared/global backside-current path**, preserving the M7B symmetry benefit.

The most physically motivated family is therefore a **local return island/tongue with a surrounding moat**, galvanically tied to the branch-local package/via return rather than left floating.

A second, weaker fallback is a **partial under-pad aperture** that retains continuous ground but reduces coupling more gently.

Exact dimensions are intentionally not frozen yet. The next valid action is offline topology definition and geometry-feasibility review only.

BUILD_AUTHORIZED = false.
SOLVE_AUTHORIZED = false.
