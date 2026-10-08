# Architecture Notes

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
