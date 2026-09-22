# Da Costa 2026 Differential-LNA Provenance

Source:
- Sophia Da Costa, Albert Wai Kit Lau, Keith Vanderlinde
- "Low-cost, ultra-wideband, differential low-noise amplifier for interferometric radio telescopes"
- arXiv:2607.21715
- preprint, July 2026

## Role

Circuit-level reference for a balanced antenna directly driving two commercial single-ended low-noise amplifiers, eliminating a passive pre-amplification balun.

## Reported results used as a reference

- commercial surface-mount implementation,
- approximately 20 USD reported unit cost,
- noise figure close to 0.3 dB across a broad band when matched to a constant 130-ohm source,
- feed-coupled system-noise temperatures as low as ~25 K with a Vivaldi feed over 300–1500 MHz.

## Project interpretation

This supports, but does not freeze, the concept:

```text
balanced terminal
  +        -
  |        |
 LNA      LNA
  |        |
 post-gain differential/single-ended conversion
```

R4 must reproduce the relevant QPL9547 noise/stability behavior from device data and our own measurements before the topology is trusted.

Because the source is a preprint, all performance claims must retain that status in project documentation.
