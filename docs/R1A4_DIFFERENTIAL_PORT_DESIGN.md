# R1A4 Differential Port Design

Status: DESIGN FROZEN FOR BUILD-ONLY QUALIFICATION

## Purpose

R1A4 adds an ideal balanced two-port excitation to the human-reviewed R1A3 geometry without modifying any solid geometry.

Immutable source:
D:\GNSS_Lband_Active_Array\_r1a3_materialized_fr4_work\R1A3_CHARTS_MATERIALIZED_FR4_BUILD_ONLY_V01.cst

Required source SHA256:
b921889aede44ff2b4ad476be4157c2c72053cc3c6f6de4a4bf358e607adc8fa

R1A4 copies this source into a fresh work directory. The reviewed R1A3 file is never overwritten.

## Differential basis

The four petal terminals are defined on the diagonal axes.

Port 1 / Pol-A:
- P1 = NE terminal
- P2 = SW terminal
- direction = NE -> SW

Port 2 / Pol-B:
- P1 = NW terminal
- P2 = SE terminal
- direction = NW -> SE

Port 2 is the exact +90 degree rotation of Port 1, including endpoint ordering.

## Terminal coordinates

Reuse the R1A2 metadata:
- terminal_r = 3.00 mm
- s2 = 1/sqrt(2)

Therefore terminal coordinate magnitude is:
terminal_xy = terminal_r * s2 = 2.12132034356 mm

All endpoints lie on the top surface of the R1A3 top conductor:
z = copper_top_z.

No local ground or main ground is used as a port terminal.

## Port model

CST object: DiscretePort
Type: SParameter
Differential reference impedance: 100 ohm
Monitor: false
Radius: 0
InvertDirection: false

The 100 ohm normalization is a project baseline anchored to the CHARTS near-center differential impedance region around 100 ohm. It is not claimed as a hidden published terminal geometry.

## Important crossing note

The two ideal port lines cross geometrically at the center. They are excitation objects, not conductive wires.

R1A4 exists specifically to test whether CST accepts and persists this crossed ideal differential-port representation without changing geometry.

If CST rejects it or the fresh-reopen audit is ambiguous:
- classify HOLD;
- do not create a fictitious ground reference;
- do not silently move endpoints;
- open a separate recovery/design ticket.

## Build-only acceptance

Required:
- immutable R1A3 source hash matches;
- pre-port copy hash equals R1A3 source hash;
- port-only macro contains no geometry creation or Boolean commands;
- CST creates exactly 2 ports;
- fresh reopen still reports exactly 2 ports;
- R1A4 shape inventory exactly matches R1A3 shape inventory;
- 0 solver starts.

PASS status:
PASS_R1A4_DIFFERENTIAL_PORT_BUILD_ONLY

This PASS does not authorize a smoke solve.


## R1A4Q solver-safety qualification addendum — 2026-09-24

The crossed diagonal discrete-edge-port representation has been qualified with an isolated toy-model A/B test.

Result:
- no direct galvanic short observed in CST 2022.5 HF Frequency Domain / tetrahedral mesh;
- CROSS S21 at 1.4 GHz = -59.40 dB;
- non-intersecting lifted reference S21 at 1.4 GHz = -78.09 dB;
- crossing adds about 18.69 dB of artificial inter-port coupling at 1.4 GHz;
- crossing penalty over 0.5–2.0 GHz is about 17.1–21.3 dB.

Therefore the R1A4 crossed ports are conditionally qualified only for:
- lightweight diagnostic smoke;
- HF Frequency Domain;
- tetrahedral mesh;
- qualitative resonance / gross S-parameter checks.

They are not the final production feed model and must not be used as the sole basis for high-dynamic-range polarization-isolation claims.

Transient/hexahedral use remains unqualified.

See:
`evidence/r1a4q_dc_nw_20260924_attempt3/RETURN_REPORT.md`
