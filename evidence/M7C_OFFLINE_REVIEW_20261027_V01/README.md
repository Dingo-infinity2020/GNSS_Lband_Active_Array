# M7C offline review evidence — 2026-10-27

Science remains `HOLD_M7C_GUARD`. No simulator application or solver was invoked.

- `ANALYSIS.json`: frozen metric reproduction and supplemental diagnostics.
- `INPUT_RECEIPT.json`: five raw CSV locations and byte identities. Full CSVs remain protected on NW; temporary local caches are not authoritative storage.
- `REMOTE_READONLY_INTEGRITY.json`: independent NW/local byte comparison, including solved files and native auxiliary files.
- `GUARD_TRACE_RANKING.csv` / `ALL_FAILING_GUARD_TRACES.json`: all 88 off-diagonal trace maxima and the four >6-dB drivers, using the frozen evaluator's window convention.
- `GUARD_WINDOW_COMPLEX.csv`: real/imaginary, magnitude and wrapped phase for S2,5/S5,2 and the analogous Pol-B pair, all three models.
- `MODAL_ANCHORS.csv` / `MODAL_SPECTRUM.csv`: independent self/mutual/asymmetry decomposition; no changed production transform.
- `STATIC_GEOMETRY_AUDIT.json`: endpoint/rotation and source-primitive checks; not a new CST kernel qualification.
- `NATIVE_PROBLEMATIC_POSITIONS.csv`, original `*TetMesherError.axg/rex`, and `*_native_output.txt`: preserved position and frequency-sampling evidence. XML markers are not individual PEC edge IDs.
- `GUARD_REVIEW.svg` / `POLARIZATION_REVIEW.svg`: exported scientific plots, visually checked through PNG renderings.

Reproduce after copying each INPUT_RECEIPT remote CSV into a private raw directory as `full_E2C.csv`, `M7B.csv`, `M7C.csv`, `isolated_A.csv`, `isolated_B.csv`; include INPUT_RECEIPT as `TRANSFER_RECEIPT.json`. Add the three native output files as `<model>_output.txt` and the original `<model>__TetMesherError.axg` files. The script verifies the received CSV hashes and original modal/Guard metrics before writing a new output directory.

```sh
python3 scripts/analyze_m7c_offline_review_v01.py \
  --raw-dir /absolute/path/to/private/raw \
  --output /absolute/path/to/new/review-output
```

`--plots` additionally requires Matplotlib; its recorded version is in PLOT_TOOLCHAIN.json. The rest uses only Python stdlib and the unchanged local frozen evaluator. No CST libraries or applications are needed.

The scientific freeze in `execution/M7C_WEAK_RESPONSE_DIRECT_SAMPLE_SCIENTIFIC_FREEZE_V01.json` is a future proposal with false permissions and no entrypoint or packet.
