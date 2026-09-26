# GNSS L-band Active Array — Requirements v0.1

Status: **FROZEN FOR R0/R1 PLANNING**  
Scope: research prototype, not a production specification.

## 1. Mission

Develop a low-cost, room-temperature, low-noise, dual-polarized active antenna element that can scale into a digitally beamformed array for full L-band GNSS reception.

The design must balance:

1. receiver noise temperature,
2. wide-field / scan behavior,
3. polarization fidelity,
4. manufacturability and cost,
5. stability and calibration repeatability.

No single paper, antenna family, or LNA part is frozen as the final architecture.

## 2. RF envelope

- Required continuous design band: **1.15–1.65 GHz**
- Two independent linear-polarization outputs per physical element
- No analog 90-degree hybrid in generation 1
- RHCP/LHCP formation is performed digitally from calibrated X/Y complex voltages
- Core scan region: **0–60 deg from zenith**
- Extended target: **60–75 deg from zenith**
- Below 15 deg elevation is not a generation-1 optimization target

## 3. Array-aware requirements

The isolated-element return loss is not the system objective.

Required quantities for later gates:

- differential active impedance versus frequency and scan,
- common-mode impedance and mode conversion,
- embedded element pattern,
- finite-array edge effects,
- X/Y phase-center behavior,
- digital RHCP/LHCP realized gain / axial ratio,
- receiver noise under the actual active source-impedance locus.

Initial lattice search window for the L-band array:

- nominal pitch: **90–95 mm**
- exploratory range: **88–100 mm**

This range is a design search space, not a frozen dimension.

## 4. Low-noise frontend requirements

Architecture preference:

- balanced radiator terminal,
- first gain stage located at the feed point / central active hub,
- no intentionally lossy passive balun before first gain,
- differential-to-single-ended conversion may occur after first-stage gain.

QPL9547 is the **reference G0 device**, not a frozen production component.

A second cost-down candidate shall be evaluated after the QPL9547 reference model is validated.

Desired receiver targets for the GNSS band:

- reference target: NF <= 0.5 dB under relevant source impedances
- stretch target: NF <= 0.4 dB
- pre-LNA passive loss: minimize; do not accept a long cable or lossy input balun merely to obtain a nominal 50-ohm interface
- stability must be checked over differential mode, common mode, source-impedance variation, and out-of-band frequencies

## 5. Power and interface

Generation-1 element:

- X and Y remain independent
- two RF output coaxial connections per element
- Bias-Tee powering is the preferred field interface
- local filtering/regulation may be used at the active hub if needed
- independent X/Y powering is preferred for bring-up and fault isolation

No exact feed voltage is frozen at R0.

## 6. Manufacturability

Priority is a low-cost repeatable array element, not maximum electromagnetic sophistication.

Preferred:

- standard PCB processes,
- commercial SMT parts,
- compact clip-on / stamped RF shields,
- simple ground/backplane,
- minimal manual micro-coax assembly,
- no precision-machined RF cavity unless measurements prove it is necessary.

The preferred product direction is no more complicated than:

1. radiator PCB / conductive sheet,
2. small active-hub PCB,
3. ground/backplane and simple mechanical support.

More complex C-ORA / TCDA / PUMA structures remain references or fallback architectures.

## 7. Current architecture hierarchy

### Main investigation
CHARTS-inspired planar petal/ring radiator plus a feed-point differential active frontend.

### Performance references
- Cui 2023 square-loop compact dual-polarized radiator
- ASKAP-style active balun concepts
- C-ORA active-array / coincident-phase-center concepts
- ASTRON / Vivaldi low-noise-array methodology

### First backup
PUMA / unbalanced tightly-coupled architecture with LNA behind the ground plane.

## 8. Gate discipline

R0 is **passive reconstruction only**.

Forbidden during R0:

- claiming an exact CHARTS replica,
- L-band optimization,
- QPL9547 integration,
- array optimization,
- solver-derived performance claims before geometry provenance review,
- silently fitting figure-derived dimensions to make results look better.

Any parameter changed from a reference must have provenance:
`PAPER_EXPLICIT`, `FIGURE_DERIVED_UNVERIFIED`, `ASSUMPTION`, or later `OPTIMIZED`.
