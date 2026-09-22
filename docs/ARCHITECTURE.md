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
