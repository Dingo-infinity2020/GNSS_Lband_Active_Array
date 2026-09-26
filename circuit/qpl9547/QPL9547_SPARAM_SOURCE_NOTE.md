# QPL9547 S-Parameter Reference Note

Status: TRACEABLE G0 REFERENCE — NOT A FINAL DEVICE MODEL

Source context:
- Qorvo Tech Forum thread: `QPL9547 25 MHz operation`;
- attachment filename: `QPL9547_DEEMBEDDED_TRL_SN1_5V_65MA.S2P`;
- forum attachment URL recorded in the derived stability JSON;
- measurement header date: 2024-10-04;
- bias: 5 V, 65 mA;
- Touchstone reference impedance: 50 ohm;
- file SHA256: `fad334a226acb9fbe1e4bd769f474afa14e2c23c18f31f4750c091f3d5d0424f`.

The forum source states that the extended very-low-frequency data are less reliable because the TRL calibration kit was designed for roughly 600 MHz and above. The present project uses only the 1.15–1.65 GHz band from this file for the main G0 S-parameter reference.

Derived project artifacts:
- `QPL9547_SPARAM_REFERENCE_1P15_1P65.csv` — sparse in-band anchors;
- `analysis/QPL9547_SPARAM_STABILITY_SUMMARY.json` — source hash and stability summary.

In-band derived bounds from the downloaded file:
- K_min = 1.2480;
- mu_min = 1.3687;
- mu-prime_min = 1.3873;
- max |Delta| = 0.4437.

Therefore the standalone 2-port is unconditionally stable by the usual K/Delta and mu criteria over the project science band in this reference measurement.

This does NOT prove assembled active-antenna stability. Packaging, shield, output routing and ground-return feedback paths are outside the standalone device S2P model.

The raw external S2P file is intentionally not committed to the repository; only derived project data, source metadata and hash are retained.
