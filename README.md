# ESP32 Xtensa–RISC-V Workload Study

This repository is the reproducibility workspace for an academic comparison of the original Xtensa-based ESP32 historical results and new measurements on an ESP32-C6-N4 RISC-V platform.

**Status:** foundation phase. The research contracts and data schemas exist, but there is no benchmark implementation and there are no locally measured results. The CRC-32 implementation gate remains closed until explicit approval.

## Research focus

The study asks how low-level differences between the Xtensa LX6 used in the original ESP32 and the ESP32-C6 high-performance RISC-V CPU appear in real workloads, and how the observed behavior of C/C++, Rust, and MicroPython has changed across those platforms.

This is not an ISA-only experiment. The chips also differ in microarchitecture, frequency, core count, memory hierarchy, compiler generation, SDK, runtimes, and peripherals. Accordingly, the project will describe observations on a platform and possible consistency with architectural mechanisms; it will not report cross-chip timing ratios as pure ISA effects.

The exact questions and permitted interpretations are in [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md).

## Scope

- Physical measurement target: the user's ESP32-C6-N4 with 4 MB flash. Exact board model, board revision, chip revision, and board-instance identifier still need to be recorded.
- Historical comparator: published measurements and archived source material from Plauska, Liutkevičius, and Janavičiūtė (2023), not a locally tested classic ESP32.
- Core languages: C/C++, Rust, and MicroPython.
- TinyGo: historical context only; it is not part of the new study.
- First workload: CRC-32 only. SHA-256, FFT, FIR, and IIR remain gated until the CRC pipeline is validated.

## Experimental families

| Family | Purpose | Current state |
|---|---|---|
| Set A — Historical reproduction | Comparable software workloads and a published ESP32 baseline | CRC source audit started |
| Set B — Microarchitectural | Explanatory kernels for calls, branches, register pressure, memory, arithmetic, and alignment | Deferred |
| Set C — Modern compute / TinyML | Separate modern integer, vector, and inference workloads | Deferred |

Set A has three non-interchangeable modes: `A` (fair/historical reproduction), `B1` (CPU/ISA optimized), and `B2` (full-SoC optimized). Despite their names, B1 and B2 are optimization modes for a workload and are not Benchmark Sets B and C. Every dataset must carry an explicit `benchmark_mode` value.

## Evidence pipeline

```text
versioned protocol + test vectors
  -> build and correctness gate
  -> immutable raw run bundle
  -> non-mutating validation report
  -> derived CSV statistics
  -> MATLAB figures/tables
  -> LaTeX paper and release archive
```

Published historical aggregates live under `data/baselines/`; locally observed iteration data live under `data/raw/`. They must never be represented as the same evidence class.

## Repository map

| Path | Role |
|---|---|
| `benchmarks/` | Versioned benchmark sources, protocols, and test vectors |
| `literature/` | BibTeX, literature matrix, and source notes |
| `references/` | Provenance records and source audits |
| `data/raw/` | Immutable local acquisition bundles |
| `data/baselines/` | Published or externally acquired historical evidence |
| `data/validation/` | Validator output that never rewrites evidence |
| `data/processed/` | Reproducible derived CSV files |
| `data/schemas/` | Normative file-format contracts |
| `artifacts/assembly/` | Disassembly and static machine-code evidence |
| `matlab/` | CSV-driven validation, statistics, and plotting functions |
| `paper/` | LaTeX manuscript and generated inputs |
| `website/` | Future multi-paper research site |

The additions `data/baselines/`, `data/validation/`, and `artifacts/` deliberately separate different evidence grains and write stages. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## Start here

1. Read [PROJECT_CHARTER.md](PROJECT_CHARTER.md), [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md), and [METHODOLOGY.md](METHODOLOGY.md).
2. Review the preliminary [CRC-32 source audit](references/original-study/CRC32_AUDIT.md) and [verification ledger](docs/verification_ledger.md).
3. Review the [results schema](data/schemas/results_schema.md) and [ROADMAP.md](ROADMAP.md).
4. Do not run or implement CRC-32 yet; no reproduction command is claimed at this phase.

## Source status

The Plauska paper and upstream repository are pinned in the source audit. Two material issues are already visible: the paper and released results contain 100 iterations per CRC condition, while the checked-in MicroPython launcher requests 5; and the static random input bytes are present, but their generator seed is not documented. These are recorded as discrepancies, not resolved by assumption.

## Citation and license

The seed paper has a verified BibTeX record in `literature/references.bib`. A repository citation file, project license, dataset license, and third-party redistribution decision are still pending. Do not redistribute upstream source or PDFs until their licensing and provenance have been reviewed.
