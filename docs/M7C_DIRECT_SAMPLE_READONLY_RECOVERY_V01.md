# M7C direct-sample result-reader recovery V0.1

The one formal SOLVE completed; no solver retry is allowed. Its runner outcome remains HOLD_ENTRYPOINT. The post-solve exception was `ValueError: too many values to unpack (expected 2)`.

Native read-only inspection identifies the representation difference: the eight reflection curves return `(frequency, complex S, complex Zref)` records, while transmission curves return pairs. All 96 curves expose separate `get_xdata()` and `get_ydata()` arrays with 16 points. Sampled diagonal auxiliary Zref values are 50 ohm; the frozen presolve gate separately verified all 12 port impedances.

Recovery uses the documented separate x/y accessors, checks equal lengths, and retains all existing finite-value, grid, native direct-frequency, residual, convergence, reciprocity, power-upper-bound and hash checks. No scientific threshold or classification rule is changed.

- locked solved SHA256: `c21fa9f047d83f4f3776d5e6ef5718e8924aaf8e54f0ad8cbb7cb6a7c6681851`
- standalone script: `scripts/recover_m7c_direct_sample_readonly_v01.py`
- fresh output: `C:\GNSS_Lband_Active_Array\runs\formal\solver_runs\M7C_DIRECT_SAMPLE_20261027_V01\evidence\qualification_recovery_v01`
- library-level `cst.results.ProjectFile(..., allow_interactive=False)` only; no `cst.interface`, application or solver launch.
- original formal qualifier, result packet, exception, production source and solved artifact remain unchanged.
- before/after production SHA required; only the single locked artifact is accepted.
- fixture with a three-item reflection record passes using separate x/y accessors; source compilation/help pass before remote extraction.

The user explicitly delegated completion of this stage. Its formal SOLVE grant is now CONSUMED; current BUILD/SOLVE=false and active_grant=null. This remaining work is zero-solver read-only qualification, not a new execution grant. The original M7C science remains HOLD_M7C_GUARD independently of the diagnostic result.
