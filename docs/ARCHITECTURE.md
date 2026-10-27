# Architecture Notes

## Current Ver1.0 direction — 2026-10-27

Decision: [D0023](DECISIONS.md#d0023--define-ver10-as-a-chartsar0-b-dual-polarized-active-array-element). Full definition and evidence: [Ver1.0 project review](VER1_0_PRODUCT_DIRECTION_AND_PROJECT_REVIEW_20261027.md).

The MAINLINE remains a CHARTS-inspired balanced planar petal/ring radiator with two independent linear-polarization outputs and digital RHCP/LHCP synthesis. PUMA remains FIRST_BACKUP.

Current physical architecture is **AR0-B stalk-top twin-MSL/twin-LNA**, under its geometry/provenance manifests:

- one radiator PCB above a common backplane;
- two orthogonal approximately 1-mm PCB stalks provide mechanical support and carry the first-stage electronics close to the feed;
- two short input branches and two LNAs per polarization, four first-stage LNAs per element;
- differential-to-single-ended combining after first gain, followed by two RF/coax outputs with independently powered X/Y channels;
- radiator copper connects only to the intended signal tongues; no frontend ground/backing plane may overlap radiator copper or make galvanic contact to an arm;
- local paddle/decoupling returns are short and physically modeled; their eventual connections to the combiner, supply, connector shields and backplane remain a separate qualification question.

The 94-mm pitch, approximately 70.7-mm radiator span and 57.1-mm height are inherited engineering starting values. FR4 is the manufacturing/cost baseline and QPL9547 is a reference LNA. None is an assertion of final array/noise qualification.

## Model and acceptance boundaries

- Device physics, component/noise models and bias topology stay in the circuit domain; CST represents the passive conductors, dielectrics, launches, joints, grounds, vias and shields that need field modeling.
- Current E2C S0 partial networks and four finite branch-local grounds answer bounded sentinel questions. They do not close the assembled active receiver or permit an ideal common-ground substitution.
- Final antenna/LNA input matching waits for the integrated R1E2 scan-dependent source-impedance cloud. A 50-ohm post-gain output is compatible with this rule.
- Receiver/noise/stability budgets remain governed by the existing requirements and Gate R. Finite-array center/edge/corner and calibrated polarization validation are required before release.
- Current science remains HOLD_M7C_GUARD; the direct-sample diagnostic closes only its numerical-representation question. Product direction does not promote M7C or reopen BUILD/SOLVE.

Current geometry/lineage authorities:

- [AR0-B0](R1E1A4A_AR0_B0_STALK_TOP_TWIN_MSL_ARCHITECTURE_FREEZE_V01.md)
- [B1M mechanical stalk](R1E1A4A_AR0_B1M_FULL_MECHANICAL_STALK_FREEZE_V01.md)
- [E3C ground topology and open assembled returns](R1E1A4A_AR0_B1R_R4_A0_E3C_GROUND_RETURN_TOPOLOGY_FREEZE_V01.md)
- [E3F model lineage and supersession](R1E1A4A_AR0_B1R_R4_A0_E3F_CANONICAL_MODEL_LINEAGE_V01.md)

## Historical notes — superseded, retained for provenance

The notes below describe the earlier horizontal H0/hub and electronics-on-radiator direction. They do not control the current AR0-B placement or ground design. The old 10x10-mm local-ground baseline was rejected at its receiver gate; grounded T01 technology remains post-LNA only.

<details>
<summary>Earlier architecture text (historical; no current execution authority)</summary>

## Baseline signal concept

For one linear polarization:

```text
balanced radiator terminal
        +           -
        |           |
      LNA-A       LNA-B
        |           |
        +--- post-gain differential/single-ended network ---> RF output
```

A dual-polarized physical element therefore may use two active branches per polarization when a balanced active-balun topology is selected.

The alternative backup architecture is a direct unbalanced feed with one first-stage LNA per polarization.

## Mechanical concept

The preferred mainline geometry places the first-stage electronics in the weak-field central region of a planar radiator:

```text
               radiator / passive loading
                       |
                 feed terminals
                       |
            [small active-hub PCB]
          LNA / bias / local matching
               [RF shield]
                       |
             ground / backplane
                       |
                 RF+DC coax
```

The shield, local ground, and active PCB are electromagnetic objects and must enter full-wave simulation before hardware release.

## Co-design principle

Do not force an intermediate 50-ohm interface merely for convenience.

Later gates optimize the source impedance presented by the scanned array together with LNA noise and stability:

`Z_active,diff(f, theta, phi) -> LNA noise/stability model`.

The eventual figure of merit is receiver / array sensitivity, not isolated S11.

## R1E1A4A receiver-interface refinement

The active hub is now treated as a mandatory source-facing receiver interface H0, not as one candidate mechanical support among several.

H0 baseline:
- centered backside active-hub / local-ground region;
- 11 x 11 mm source-facing envelope;
- 10 x 10 mm initial local-ground island;
- exact-rotation feed symmetry;
- future passive P1A/P1B reference planes before the first-stage active devices.

Mechanical carrier families C0/C1/C2/C3 support the H0/radiator assembly to the main backplane and are evaluated separately.

The next passive EM interface uses two 50-ohm single-ended ports referenced to the same local ground for one polarization. Mixed-mode post-processing then provides the 100-ohm differential reference, common-mode response and mode conversion.

The active LNA transistor model stays outside CST. QPL9547 or a later device is connected in the circuit/noise domain to the extracted passive EM network.

Receiver acceptance is governed by Gate R in addition to the existing support-transparency Gate T.

Shield and ground-return geometry are part of the RF stability architecture. The shield must have a short local connection to H0 ground rather than relying on a remote output-coax ground path.

</details>
