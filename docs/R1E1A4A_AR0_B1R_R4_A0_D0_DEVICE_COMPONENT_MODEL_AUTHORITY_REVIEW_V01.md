# R4-A0-D0 Device and Component Model Authority Review V0.1

Status: PARTIAL PASS / HOLD FOR FORMAL FULL ACTIVE CO-SIM
Date: 2026-10-01
Execution: OFFLINE ONLY.

## QPL9547 device authority

QPL9547 remains the G0 reference device, not the frozen production LNA.

Frozen reference facts:
- bias 5 V / 65 mA
- 50-ohm Touchstone reference
- S/noise reference plane at device leads
- RF IN = pin 2
- RF OUT/VDD = pin 7
- backside paddle = RF/DC ground

The project records a traceable external raw S2P:
QPL9547_DEEMBEDDED_TRL_SN1_5V_65MA.S2P
SHA256 fad334a226acb9fbe1e4bd769f474afa14e2c23c18f31f4750c091f3d5d0424f
measurement header date 2024-10-04.

The raw S2P is intentionally not committed and is not currently present on NW.## Existing derived S-parameter authority

The repository contains seven sparse 1.15..1.65 GHz S-parameter anchors and a derived stability summary tied to the raw-file SHA256.

In-band derived minima:
- K_min = 1.2480
- mu_min = 1.3687
- mu_prime_min = 1.3873
- max |Delta| = 0.4437

Decision:
PASS as a traceable G0 science-band engineering reference.
NOT sufficient by itself to reproduce a dense 1.0..1.8 GHz formal co-simulation.

Before formal full co-sim, rehydrate the raw S2P or another production-authority device model and verify its hash/provenance.

## Noise authority

Rev-D anchors cover 1.1..1.7 GHz and include NFmin, GammaOpt magnitude/phase and Rn.

Decision:
PASS for explicit interpolation/shadow analysis over the 1.15..1.65 GHz science band.
The noise table is a separate provenance stream from the forum S2P and shall remain identified as such.## Passive component authority

Current frozen G0 topology/candidates:
- C_IN = 100 pF seed
- C_OUT = 100 pF seed
- 100 pF local RF decoupling
- Murata GRM1555C1H101JA01# family selected as the G0 100-pF C0G candidate
- L1 = Coilcraft 0402CS-18NXGRW, 18 nH
- R4 = 3.32 kOhm EVB reference
- 1 uF bulk/local decoupling remains topology-only

No broadband vendor model file for these passives is present in the repository.

A0-C0 may use ideal components for topology/math sanity.
A0-C1/formal assembled active authority shall use qualified broadband component models.

Decision:
HOLD_PASSIVE_BROADBAND_MODEL_AUTHORITY for formal full active co-sim.

## Stability scope

Standalone QPL9547 2-port stability in the science band is PASS for the G0 reference data.

This does not prove assembled active-antenna stability. Output routing, shield, bias return, package/ground feedback and antenna-source conditions remain outside the standalone device S2P.

## Overall decision

PASS_D0_G0_REFERENCE_DEVICE_AUTHORITY
HOLD_D0_FORMAL_FULL_ACTIVE_COSIM_MODEL_SET

No geometry change or BUILD_ONLY is implied.

Required before formal C1 active co-sim:
1. restore/verify dense raw QPL9547 S2P or qualified replacement;
2. freeze broadband C_IN/C_OUT/decoupling models;
3. freeze L1 broadband model;
4. select/model bulk decoupling as needed for the stability network;
5. retain separate noise-parameter provenance.

BUILD_AUTHORIZED = false
SOLVE_AUTHORIZED = false