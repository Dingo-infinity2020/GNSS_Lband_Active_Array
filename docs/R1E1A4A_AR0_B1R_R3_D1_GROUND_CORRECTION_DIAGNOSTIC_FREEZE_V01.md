# AR0-B1R-R3-D1 Ground Placement Correction and Return-Path Diagnosis Freeze V0.1

Status: BUILD AUTHORIZED; CONDITIONAL SOLVE AUTHORIZED
SimulationOps: 0.2.8

## 1. Root-cause correction

Boolean audit of the accepted T1 artifact proved that each backside ground taper was fully embedded in the corresponding FR4 prong:

- A_P ground volume = 1.134 mm^3
- A_P ground ∩ A_P prong = 1.134 mm^3
- A_N ground volume = 1.134 mm^3
- A_N ground ∩ A_N prong = 1.134 mm^3

Front-side MSL-to-FR4 destructive-intersection probe returned an empty intersection, so the defect is localized to backside-ground extrusion direction.

Temporary corrected probe changed only:
Extrude.Height +0.035 mm -> -0.035 mm

The corrected ground retained 1.134 mm^3 volume and had zero volumetric intersection with FR4.

## 2. Canonical correction: T1R1

Create:
R1E1A4A_AR0_B1R_T1R1_GROUND_PLACEMENT_CORRECTED_BUILD_ONLY

Parent:
T1 artifact SHA256
3144672323cbd4123d6413e7d9ae8f4842b78707d3a71b641748c7250ca2a8f6

T1R1 changes:
- delete all four B1RT1_BackGround solids;
- recreate the identical four taper outlines;
- base plane remains local n=-1.0 mm;
- copper thickness remains 0.035 mm;
- extrusion is outward to local n=-1.035 mm;
- all other geometry is unchanged.

Hard acceptance:
- four corrected grounds;
- each corrected ground volume = 1.134 mm^3;
- zero positive-volume intersection with its own FR4 prong;
- no cross-polarization ground/stalk collision;
- radiator, signal, RF-tenon, mechanics and LNA-surrogate solids unchanged;
- zero ports added to canonical T1R1;
- zero result tree;
- fresh reopen.

T1R1 supersedes original T1 as geometry authority for future stages.
Original T1 remains preserved as historical evidence.

## 3. D1-A differential control

Derive from corrected T1R1.

Retain exact Pol-A six-solid transition:
- two corrected FR4 prongs;
- two signal traces;
- two corrected backside ground tapers.

Ports:
- P1 = 100-ohm differential at v=0;
- P2 = 100-ohm differential at v=10 mm;
- ground rails remain passive and separate.

Purpose:
measure the corrected transition in pure differential/odd-mode form.

## 4. D1-B common-ground closure control

Derive from corrected T1R1.

Retain exact Pol-A six-solid transition plus diagnostic common-ground bridge:
- u=-1.2..+1.2 mm
- n=-1.035..-1.0 mm
- v=11..12 mm
- B0_COPPER
- bridge volume = 0.084 mm^3

Ports:
- P1 = 100-ohm differential at v=0;
- P2/P3 = 50-ohm signal-to-ground at v=10 mm;
- P2/P3 endpoints remain at signal n=0 and ground n=-1.0.

Purpose:
measure whether explicit downstream G+/G- closure removes the prior severe input mismatch.

The bridge is diagnostic only, not product geometry.

## 5. Build authority

User authorized model correction, build and solve.

Formal build stage may create:
- T1R1 corrected dual-pol canonical artifact;
- D1-A diagnostic fixture;
- D1-B diagnostic fixture.

No solver is allowed until all build/fresh-reopen/interference gates pass.

## 6. Conditional solve authority

If and only if the full D1 build stage PASSes:
- one formal NW solve for D1-A is authorized;
- one formal NW solve for D1-B is authorized;
- same frozen 1.0-1.8 GHz HF Frequency Domain adaptive solver configuration;
- no automatic retry;
- no parameter sweep.

Any build or solve HOLD stops that branch.

## 7. Scientific interpretation

Compare:
- prior flawed-geometry R2 baseline;
- corrected D1-A differential control;
- corrected D1-B common-ground closure.

Primary questions:
1. Was the severe capacitive mismatch materially caused by embedded backside copper?
2. With corrected copper placement, is differential-only behavior reasonably matched?
3. Does explicit common-ground closure materially change input match?
4. Are symmetry, common-mode suppression and mismatch-normalized loss preserved?

No product optimization is authorized in D1.
