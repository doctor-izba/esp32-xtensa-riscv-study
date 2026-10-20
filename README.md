# A Change of Core
## Revisiting ESP32 Benchmarks on ESP32-C6

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23493672.svg)](https://doi.org/10.5281/zenodo.23493672)

**Izbassar Yesbol** · [ORCID](https://orcid.org/0009-0002-1737-7982) · hello@izba.sarl

[Read the paper](https://zenodo.org/records/23493672/files/a-change-of-core-v1.0.1.pdf?download=1)
· [Supplement](https://zenodo.org/records/23493672/files/a-change-of-core-supplement-v1.0.1.pdf?download=1)
· [Data and analysis archive](https://zenodo.org/records/23493672)

How do familiar ESP32 workloads behave on ESP32-C6? I measured five kernels in
C/C++, Rust and MicroPython on one physical C6 board, then compared the results
with historical classic-ESP32 measurements. The ordering changes with the
workload. Equal clock frequency does not make the two experiments equivalent:
hardware, memory, compilers, runtimes and acquisition procedures also differ.

This is a technical report, revision **1.0.1**, published with its analysis
archive on **20 October 2026**. It has not undergone external peer review.

## The experiment

| | Scope |
|---|---|
| Hardware newly measured | One ESP32-C6 revision 0.2 board, 160 MHz |
| Workloads | CRC-32, SHA-256, Q15 FFT, binary32 FIR and IIR |
| Languages | C/C++, Rust, MicroPython |
| Mode A | 12,000 observations under a common correctness gate and timing boundary |
| Mode B | 9,600 observations under separately declared performance transformations |
| Historical context | Classic-ESP32 aggregates from [Plauska et al. (2023)](https://doi.org/10.3390/electronics12010143) |

The classic ESP32 was not newly timed. Matched Xtensa objects were reconstructed
for static inspection and were not executed. Historical aggregates remain
separate from local observations throughout the analysis.

## What the results show

At the largest shared input, native C6 CRC-32, SHA-256 and FFT means are below
the historical means; FIR and IIR means are above them. Within C6, Rust is faster
than C++ for CRC-32, slower for SHA-256 and FFT, and close for FIR and IIR.

![Historical classic-ESP32 mean divided by local ESP32-C6 mean, by workload and language](paper/figures/mode_a_historical_local.png)

*Historical/local ratios compare different experiments. A value above one
means a lower local C6 mean; it does not isolate an ISA effect.*

![Rust-to-C++ median time ratios on the measured ESP32-C6](paper/figures/mode_a_rust_cpp.png)

*Within-board Mode A ratios. Parity is not a statistical equivalence test.*

Exact C6 FIR/IIR binaries call software floating-point helpers, whereas matched
Xtensa objects emit floating-point instructions. This supports a mechanism to
investigate, but does not measure its share of the timing difference.

The Mode B Rust FFT transformation reduced its median by **22.7%** relative to
the safe performance build while changing the whole kernel. The C6 SHA
peripheral path was **8.70×** faster than Mode A software. These are distinct
source-transformation and peripheral results.

## Reproduce the analysis

The self-contained [`analysis-release/`](analysis-release/README.md) directory
matches the deposited package. Start there:

```sh
cd analysis-release
python verify_package.py
python analysis.py
```

Python 3's standard library reproduces **216 timing groups, 176 ratios and four
result tables**. To regenerate the four figures and build the report PDFs:

```sh
matlab -batch "addpath('matlab'); run_publication_analysis(string(pwd))"
python build_paper.py --sync-figures --tectonic /path/to/tectonic
```

The exercised environment used MATLAB R2024b, Tectonic, Poppler and DejaVu Sans.
See the [package guide](analysis-release/README.md) and
[actual reproduction log](analysis-release/validation/REPRODUCTION.txt).
The package reproduces analysis and presentation; it cannot rebuild firmware,
repeat correctness tests, rerun hardware or regenerate disassembly evidence.

## Read further

- [Report source](paper/manuscript.tex) and [local PDF](paper/review-manuscript.pdf)
- [Methodology](METHODOLOGY.md), [research questions](RESEARCH_QUESTIONS.md) and [reproducibility contract](REPRODUCIBILITY.md)
- [Included timing records](analysis-release/data/local_timings.csv) and [source lineage](analysis-release/source_lineage.csv)
- [Public history scope](PUBLIC_HISTORY.md) and [verified publication receipt](publication/ZENODO_DEPOSIT_V1_0_1.json)

## Archive, history and licensing

Version DOI: [10.5281/zenodo.23493672](https://doi.org/10.5281/zenodo.23493672).
For a reference that follows future versions, use the
[all-versions DOI](https://doi.org/10.5281/zenodo.23493671).

The retained history begins on **8 August 2026** and preserves 41 original
development milestones, followed by publication updates. It is a filtered
projection; hashes differ from the original private history. The full original
archive remains preserved privately.

Original analysis software uses **MIT**. Author-owned data, text and figures
use **CC BY 4.0**; see [license scope](analysis-release/LICENSING.md).
Input/reference arrays, benchmark implementations, native artifacts, full
disassemblies, complete console captures and private review conversations are
excluded from this distribution.

The Zenodo deposit is public. This existing GitHub repository remains private
while excluded old objects retained by GitHub are addressed. GitHub–Zenodo
automatic release preservation is not enabled. The DOI identifies the scoped
deposit, not the full private evidence archive.
