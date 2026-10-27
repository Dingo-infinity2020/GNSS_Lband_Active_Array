# R4-A0 Route Freeze After E2 A/B Passive Promotion V0.1

Status: ROUTE FROZEN — NO BUILD / SOLVE AUTHORIZED  
Date: 2026-09-29  
SimulationOps minimum: 0.2.12

## 1. First-principles reset

E2A and E2B established that the frozen twin-LNA landing-zone architecture is individually viable on both orthogonal stalks.

They did **not** establish that the final dual-polarization hardware is electromagnetically equivalent when all four LNA landing zones exist simultaneously.

Therefore the mainline is changed from:

`E2A/B -> immediate active co-sim`

to:

`E2C dual-pol coexistence -> component/device authority -> C1 active feasibility -> periodic/scan active-impedance co-design`

The project must not optimize isolated-element matching before scan-dependent active/embedded impedance becomes available.

## 2. Frozen route

### R4-A0-E2C-G0 — dual-pol coexistence geometry

Construct the final passive physical geometry with:
- both Pol-A E1 cells;
- both Pol-B E1 cells;
- all four local-ground systems;
- all sixteen plated vias;
- the proven Pol-B half-lap clearance notch;
- no transistor or discrete circuit component.

Purpose:
prove that the separately qualified Pol-A and Pol-B active-feed structures can physically coexist without hidden conductor/contact/interference changes.

### R4-A0-E2C-S0 — combined passive sentinel

Do **not** extract a full raw 24x24 network first.

Use a reduced loaded sentinel:
- four branches;
- per branch expose E_UP and P_IN as sources;
- retain P_OUT as a 50-ohm matched load-only port;
- remove E_DN/VDD/VBIAS audit ports from the solve copy;
- final solve network = 12 ports;
- source columns = 8;
- required response = 12 x 8 = 96 complex traces.

Purpose:
answer only whether installing the other polarization's complete landing zones materially perturbs the already-qualified isolated-polarization source-side behavior.

### R4-A0-D0 — device/component model authority

May proceed offline in parallel with E2C.

Before active claims:
- establish QPL9547 S2P provenance/reference planes/bias;
- determine whether qualified noise parameters exist;
- qualify C_IN/C_OUT/choke/decoupling models;
- distinguish vendor measured/model authority from ideal seed components.

No noise-temperature/NF claim is permitted from S2P alone if noise parameters are absent.

### R4-A0-C1-N0 — full passive network authority for active feasibility

Only after E2C PASS and D0 authority.

For reverse feedback and assembled stability, the four-source S0L partial matrix is insufficient.

Default first active pilot:
- Pol-A full raw passive 12-port network;
- no pre-active RF retune;
- chosen because Pol-A is already the slightly more conservative passive mode-conversion case.

Promote Pol-B or combined full network only if E2C/C1 evidence shows meaningful sensitivity.

### R4-A0-C1 — active feasibility anchor

Connect qualified circuit-domain models:
- C_IN;
- QPL9547;
- C_OUT;
- VDD choke/bias/decoupling network.

Primary questions:
- assembled stability;
- transducer gain;
- source/load sensitivity;
- passive-loss impact;
- NF/Te only when qualified noise data exists.

C1 is **not** final matching optimization.

### R4-R1 — periodic / scan-dependent active impedance

After active feasibility is established:
- periodic/unit-cell or equivalent array environment;
- scan angle / polarization dependence;
- active/embedded impedance atlas;
- only then release final source matching and LNA/antenna co-design.

## 3. Anti-drift rules

Before R4-R1:
- do not optimize isolated broadside S11 as the final objective;
- do not retune E2A/E2B geometry merely to improve combined sentinel numbers;
- do not assume 50-ohm source matching is equivalent to optimum receiver sensitivity;
- do not promote ideal C/L components to production authority;
- do not calculate final NF/Te without qualified device noise data;
- do not use the partial S0L matrix for unconditional active stability claims.

## 4. Current authority

E2 A/B passive promotion:
`PASS_R1E1A4A_AR0_B1R_R4_A0_E2AB_PASSIVE_PROMOTION`

Current next stage:
`R1E1A4A_AR0_B1R_R4_A0_E2C_DUALPOL_GEOMETRY_CONTRACT_FROZEN`

BUILD_AUTHORIZED = false  
SOLVE_AUTHORIZED = false  
LNA_INTEGRATION_AUTHORIZED = false
