# R0 CHARTS Topology BUILD-ONLY Runbook

Status: **READY FOR HUMAN/CST BUILD-ONLY REVIEW**

## Preconditions

Run:

```bash
python scripts/r0_manifest_gate.py --stage topology
python scripts/audit_r0_topology_macro.py
```

Expected:

```text
PASS_R0_TOPOLOGY_MANIFEST_READY_FOR_BUILD_ONLY
PASS_R0_TOPOLOGY_MACRO_STATIC_AUDIT
EXPECTED_SOLIDS=9
EXPECTED_PORTS=0
SOLVER_RUN=NO
```

## CST 2022 execution

Use a fresh, already-open Microwave Studio project.

Run:

`source/cst/R0_CHARTS_TOPOLOGY_BUILD_ONLY_V01.mcr`

through the CST macro/structure-macro workflow appropriate to CST 2022.

The `.bas` file is a source backup/reference copy.

## Expected model tree

Components / solids:

- ReferenceGround:GROUND_REFERENCE
- Radiator:PETAL_N
- Radiator:PETAL_E
- Radiator:PETAL_S
- Radiator:PETAL_W
- PassiveRing:RING_N
- PassiveRing:RING_S
- PassiveRing:RING_E
- PassiveRing:RING_W

Expected:
- 9 solids
- 0 ports
- 0 lumped elements
- no dielectric objects
- no solver result tree

## Human visual review

Check Candidate A (`candidate_swap=0`):

- fourfold rotational symmetry,
- central square opening visibly present,
- diagonal petal gaps remain open,
- passive ring surrounds petals without electrical contact,
- radiator plane is 200 mm above ground,
- no accidental overlap/short between petals,
- object naming matches runbook.

Do **not** judge S11, beamwidth, or gain. No solver is authorized.

## Candidate B check

After Candidate A is saved/audited, Candidate B may be checked by changing only:

```text
candidate_swap = 1
```

This is a visual semantic test only.

## Fresh-reopen audit

After a successful build:

1. save the project,
2. close CST,
3. reopen fresh,
4. verify the same 9 solids persist,
5. verify 0 ports,
6. verify no solver was started,
7. capture screenshots and object inventory.

## Stop condition

Return one of:

- `PASS_R0_TOPOLOGY_BUILD_ONLY`
- `HOLD_R0_TOPOLOGY_VISUAL_MISMATCH`
- `HOLD_R0_CST_RUNTIME_SYNTAX`
- `FAIL_R0_TOPOLOGY_REPLAY`

No solver may run after any of these outcomes.
