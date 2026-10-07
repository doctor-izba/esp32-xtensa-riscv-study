# Analysis archive v1.0.0 — prepared, not publicly deposited

Researcher: Izbassar Yesbol, https://orcid.org/0009-0002-1737-7982.
The report is a technical report, not an externally peer-reviewed publication.

This is a bounded analysis package, not the complete private research repository.
It is prepared for a future Zenodo dataset deposit with the report and analysis
as associated files. The owner explicitly withheld publication on 2026-10-07:
no record URL, DOI, public GitHub repository, or journal acceptance is claimed.

## Reproduce

1. `python verify_package.py` — validate the archive's byte manifest.
2. `python analysis.py` — recompute 216 timing groups, 176 ratios and four
   generated result tables using only Python 3's standard library.
3. From this directory, run MATLAB R2024b:
   `matlab -batch "addpath('matlab'); run_publication_analysis(string(pwd))"`.
   This is the existing publication script, not a redesigned plotting workflow.
4. `python build_paper.py --sync-figures` — copy the regenerated four PDF/PNG
   figures into the paper, then compile both PDFs using an existing `tectonic`
   executable. Supply `--tectonic /path/to/tectonic` if it is not on PATH.

Generated timing results are under `results/` and `data/processed/`; MATLAB
outputs are under `artifacts/matlab/publication/`; rebuilt PDFs are under
`results/pdf/`. Source tables and publication figures are derived outputs.
Byte hashes of regenerated PDFs/figures can differ because of tool versions
and metadata. Numerical reproduction is tested separately from byte identity.
Run the manifest check **before** reproduction; after regeneration it still
checks the deposited snapshot, not a promise of identical PDF serialization.

Python 3.14, MATLAB R2024b, Tectonic, and Poppler were used for the local
reproduction/preflight. Exact exercised version outputs and results are
included under `validation/`. No toolchain binary is distributed here.
MATLAB needs DejaVu Sans available for the existing archival-safe figure export.

## Data and boundaries

`data/local_timings.csv` has 21,600 accepted records (12,000 Mode A and 9,600
Mode B), projected by column name from the validated local datasets. It keeps
iteration, workload units, language/profile, whole-batch microseconds,
batch count, recorded normalized time, correctness status, and source row/hash.
These are **not** the original complete raw run bundles or console logs.
Zero-size rows remain available although the main ratio figure uses 16–1024.

MicroPython FFT/FIR/IIR stored normalized values retain their original printed
precision; the existing validators allow a difference of <0.001 us from
total/batch. The analysis uses those recorded values rather than silently
substituting higher-precision division. Empty metadata mean absent from the
source table, not an inferred default. The board's controls and limitations
are described in the paper; retained metadata are not a new hardware readback.

`data/historical_means.csv` contains cited historical aggregates, kept separate
from local records. CRC/SHA/IIR means were derived from the pinned upstream
recording; FFT/FIR means were transcribed from publication Table 5. The
external-source locator manifest accompanies them. No third-party source
recording or full publication is bundled. Recomputing ratios does **not**
independently verify those external aggregates.

The two codegen-metric CSVs contain imported numeric counts used by the FFT
table. They are facts derived from retained artifacts, not disassembly or a
means of re-auditing the compiler output. `source_lineage.csv` records exact
private source-file hashes and projection rules; `manifest.csv` hashes every
included file except itself. Private source hashes are provenance references,
not files that can be checked without access to that archive.

Excluded: input/coefficient/twiddle/reference arrays; benchmark kernels/ports;
ELF/BIN/object/firmware; full disassembly artifacts; complete console captures; upstream
source/PDF/CSV bytes; Git history; private review chats and internal reports.
CRC/SHA result values are omitted; their accepted correctness flags remain.
The package does not independently repeat correctness tests, rebuild firmware,
rerun hardware, or regenerate the static-code evidence. It does reproduce
timing statistics/ratios, four publication figures, result tables, and both
PDFs from supplied authored manuscript sources.
The unchanged report retains its short, attributed generated-instruction
excerpts as scientific evidence; these are not full disassemblies or executable
benchmark implementations. Excerpt source paths refer to the private archive.

The full private evidence archive is preserved, including exact measured
artifacts except the disclosed accepted Rust CRC ELF omission. Its unresolved
distribution items are not granted a license here or promised upon request.
Upstream clarification remains at:
https://github.com/ignasp/ProgLangComp_onESP32/issues/2 .

## Licenses and eventual deposit

Original author software: MIT (`LICENSE-MIT.txt`). Author-owned timing records,
derived presentations, manuscript, and authored documentation: CC BY 4.0
(`LICENSING.md`). These grants cover only the author's rights, not ownership
of otherwise unprotected facts or external source documents. Historical
sources remain cited with their provenance. No upstream code is included.

`ZENODO_METADATA.json` is a preparation worksheet, **not** an API-created
record. It deliberately has no invented affiliation, funding, publication
date, URL or DOI. Before a separately authorized deposit, set the actual
publication date and add the permanent archive locator to the paper's
availability statement; rebuild and revalidate the deposited version.
