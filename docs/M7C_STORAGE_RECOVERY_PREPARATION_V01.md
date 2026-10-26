# M7C same-geometry storage recovery preparation V0.1

Date: 2026-10-26 (Asia/Shanghai)
Status: PASS_M7C_RECOVERY_OFFLINE_FREEZE_AWAIT_REQUALIFICATION

## Scope and authority

The user authorized the proposed preparation package: storage preflight, a same-geometry recovery contract, entrypoint/hash qualification and current-state synchronization. No BUILD/SOLVE grant was given.

The user subsequently explicitly authorized Codex to use direct remote access to any host without Desktop Commander. Direct SSH is therefore permitted for this task; this is an execution-route exception to the SimulationOps DC preference, not a change to BUILD/SOLVE authority. The initial two read-only storage snapshots used DC before this instruction. Subsequent qualification uses direct SSH where available.

SimulationOps authority remains 0.2.26 at `c074982bce2ad1bc7c0914ad422244f2cba84d4a`. The scientific authority remains the original M7C diagnostic freeze and modal evaluator. This preparation does not change the antenna, local-return-island/moat geometry, material, ports, source/load mapping, solver fidelity, monitors or scientific thresholds.

## Original consumed attempt

`GNSS-M7C-DIAGNOSTIC-SOLVE-V01` remains consumed, with zero retries and storage HOLD. Adaptive convergence was reached, but only two standard S-parameter endpoints were materialized. It has no science classification. Original manifest, runner, logs, remaining result database, closeout and cleanup records are immutable history. Recovery starts from the reviewed BUILD complete project, not the failed solved project.

Reviewed `.cst` SHA256:
`ee25237bc5f70e457adadf3745faf3d64f1401bb47717da5322d7347ba50ce98`

Source companion identity, collected read-only on 2026-10-26:

- algorithm: `SIMOPS_TREE_ID_V1`
- tree SHA256: `76a988e78dcfa8b16967821e538039996ed51abce3f308b9047f231d4f463d52`
- 97 regular files; 6,557,288 bytes

Both `.cst` and companion identity are checked before copying/configuring and again immediately before solver launch. Original E2C and isolated PolA/PolB reference CSV hashes are also checked.

## Storage plan

Read-only NW snapshot at 2026-10-26 13:45:11 UTC:

| Volume | Filesystem | Free bytes | Disposition |
| --- | --- | ---: | --- |
| C: | NTFS | 139,732,905,984 | new temporary project recovery output |
| D: | NTFS | 14,859,431,936 | protected sources/history; below output budget |
| F: | exFAT | 1,290,932,322,304 | capacity observed; direct CST result storage unqualified |

Retained analog run sizes: M7B 6,073,255,844 bytes; full E2C 11,441,462,029 bytes. These are retained sizes, **not measured peak storage use**. The truncated M7C run is not used as a complete-run estimate.

Frozen engineering budget:

`output = ceil_GiB(max(32 GiB, 2 × max(retained analog sizes) + 8 GiB)) = 32 GiB`

Process TEMP adds an independent 8 GiB reservation. When output and TEMP share a filesystem, reservations sum to **40 GiB = 42,949,672,960 bytes**. Unknown volume, probe error, missing budget or insufficient capacity fails closed. No TEMP/environment redirection is introduced. NW TEMP was observed on C:.

The new output root is:
`C:\GNSS_Lband_Active_Array\runs\formal\solver_runs\M7C_STORAGE_RECOVERY_20261026_V01`

This is a project-owned temporary run root outside SimulationOps runtime. No existing D: artifact is relocated/deleted. C: is not declared long-term storage; later task-node closeout must classify the new complete project before any cleanup. No reservation guarantees that concurrent unrelated jobs cannot consume space; the immediate pre-solver check reduces that exposure. Storage HOLD remains a valid terminal outcome, with no automatic retry.

## Frozen recovery identity

- manifest: `execution/M7C_STORAGE_RECOVERY_SOLVE_MANIFEST_V01.json`
- proposed stage: `R1E1A4A_AR0_B1R_R4_A0_E2C_S0_M7C_STORAGE_RECOVERY_SOLVE_V01`
- proposed packet: `GNSS-M7C-STORAGE-RECOVERY-20261026-V01`
- entrypoint: `scripts/run_m7c_storage_recovery_solve_v01.py`
- packet generator: `scripts/make_m7c_storage_recovery_packet_v01.py`
- preflight helper: `scripts/m7c_storage_recovery_preflight_v01.py`
- audit: `scripts/audit_m7c_storage_recovery_v01.py`

The historical entrypoint is copied into a distinct recovery entrypoint, adding only pre-import and immediate pre-solver authorization/source/storage guards, runtime-relative project root, and truthful solver-invocation accounting. The presolve module, original config macro, qualifier and modal evaluator are reused byte-for-byte. All frozen scientific manifest sections are equality-checked against the historical manifest.

The inventory JSON is bound to its unchanged Git/LF bytes in the isolated checkout (`core.autocrlf=false`). Its new byte hash is recorded separately in `recovery.byte_binding_rebaseline`; no inventory content is edited. The original manifest is untouched.

## Preparation qualification

Run only stdlib/static tests, read-only artifact/hash/tree/storage probes and safe `--help`. Do not open a CST project or launch a simulator application in this stage. Use the qualified SimulationOps control Python and separately check safe help under the CST bundled Python from `SimulationOps/infrastructure/HOSTS.md`.

```text
python -B scripts/test_m7c_storage_recovery_v01.py
python -B scripts/audit_m7c_storage_recovery_v01.py --host-readonly
<CST_BUNDLED_PYTHON> -B scripts/run_m7c_storage_recovery_solve_v01.py --help
```

The host checkout is task-private, clean and configured with `core.autocrlf=false`; the old NW checkout is not updated because it still contains the historical pre-consumption grant. Current Git/handoff/contract, not that stale checkout, controls preparation.

Actual production packet generation, validate/dry-run and formal launch remain deferred. Both direct entrypoint and generator reject absent/consumed/mismatched/expired grants before simulator imports/output creation. A future grant binds the qualified source commit and new entrypoint hash. That source commit must be an ancestor of the checkout containing the later authorization update; the packet separately binds exact checkout HEAD and stage-contract bytes. This avoids a self-reference in which a commit would have to contain its own SHA. The formal packet uses `runner-task-v0.2`, native `min_free_bytes`, source/dependency/contract hashes, fresh result paths and global one-shot lock. Never replay the original packet.

## Scientific acceptance and stop

Exactly one invocation only if later explicitly authorized; automatic retries = 0. Preserve the proven 12-port / 8-source network, 1.0–1.8 GHz modeled range, 1.15–1.65 GHz decision band, second-order adaptive tetra mesh, DeltaS ≤0.02 for two consecutive checks, max 16 passes, no H-field monitor.

Require all 96 responses on the complete native 1001-point grid, native convergence, reciprocity, loaded-power and fatal/mesh-error hard checks. Then apply unchanged M7C symmetry (10 checks), differential restoration (6 checks), secondary raw metric and >6-dB/≤50-MHz guard. Preserve the original PASS/REVIEW/REJECT/HOLD classification semantics.

Stop after qualification and modal classification. No automatic next stage, geometry sweep, LNA integration, material A/B, CST251 execution, cleanup or retry is authorized.

## Evidence and current boundary

Evidence root: `evidence/M7C_STORAGE_RECOVERY_PREP_20261026/`.

BUILD_AUTHORIZED=false; SOLVE_AUTHORIZED=false; active_grant=null.

The preparation package is reviewable independently of later production authorization. Host qualification status must be read from its evidence, not inferred from offline tests or free-space snapshots.

## 2026-10-26 qualification closeout

Direct SSH qualification of source commit `18f13b127a0635551edc0fa83fe6a3855e08918a` completed at 14:00:05 UTC. The checkout is clean and `core.autocrlf=false`. The entrypoint, helper, generator, frozen manifest and reused scientific source bytes are unchanged by this documentation/evidence closeout.

- Offline regression: 8/8 PASS.
- NW regression: 7 PASS; one link-creation test skipped because Windows symlink privilege is not assumed.
- All host artifact/source/reference/tree/storage checks PASS. C: free bytes at qualification: 139,754,782,720; combined requirement: 42,949,672,960.
- SimulationOps native contract-check PASS, no errors/warnings.
- Historical inventory byte SHA is `e4f4157bf4248bd94c0d33b18c0a8dad4a8831ae46204d6a8fae4ecba86a8095`; isolated Git/LF byte SHA is `d8246dd39640825a95a4525b9c0fac113e00bf8adde3cd6efca59ccb8227c6c9`. Parsed JSON equality PASS.
- Actual CST bundled Python is 3.6.0. Safe help and import-only checks PASS. A targeted subsequent read-only compatibility probe also passed artifact/tree/reference/storage checks and confirmed ungranted launch refusal under Python 3.6. This additional small probe was needed after discovering the actual runtime version; its exact source is preserved as `RUNTIME_PREFLIGHT_PROBE.py`.
- Build invocations=0; solver invocations=0; CST application instantiations=0; actual formal packets generated=0.
- Production output root was not created. Original NW checkout and all science baselines remain unchanged.

The task-private host checkout/control evidence is CHECKPOINTED for authorization review. Retain it until that decision or explicit abandonment; no cleanup is part of this preparation. A future formal grant must bind a clean reviewed Git HEAD and current contract; validate/dry-run must then precede the single run.

### Source-binding review

Final review separated the qualified source commit from the later authorization-contract commit. The recovery helper and generator were updated to require qualification/source agreement and source ancestry; exact checkout HEAD remains a native packet preflight. This changes authorization bookkeeping only. A second nonproduction qualification is required for these updated helper/generator bytes; the original 18f13b1 receipts above remain historical preparation evidence.
