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

## Experimental scope

| Family | Purpose | Current state |
|---|---|---|
| Historical suite | CRC-32, SHA-256, FFT, FIR, and IIR with a published ESP32 baseline | CRC protocol proposed |
| Low-level analysis | Generated code, ABI, registers, loads/stores, branches, calls, spills, floating-point behavior, and code size | Analysis layer; not an experimental mode |
| Future work | Additional microbenchmarks, AI/TinyML, languages, and VMs | Deferred beyond the first paper |

There are exactly two non-interchangeable modes: `A` (fair, reproduction-oriented reconstruction/extension) and `B` (optimized). Mode B records every enabled optimization explicitly; it has no B1/B2 submodes. Published Plauska results remain historical baseline evidence rather than a local experimental mode.

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
2. Review the [related-work deep review](literature/RELATED_WORK_DEEP_REVIEW.md), [novelty-gap analysis](docs/NOVELTY_GAP_ANALYSIS.md), and [claim boundaries](docs/CLAIM_BOUNDARIES.md).
3. Review the preliminary [CRC-32 source audit](references/original-study/CRC32_AUDIT.md) and [verification ledger](docs/verification_ledger.md).
4. Review the [results schema](data/schemas/results_schema.md) and [ROADMAP.md](ROADMAP.md).
5. Review the proposed CRC-32 Mode A protocol. Do not implement CRC-32 until its approval is recorded.

## Source status

The Plauska paper and upstream repository are pinned in the source audit. Two material issues are already visible: the paper and released results contain 100 iterations per CRC condition, while the checked-in MicroPython launcher requests 5; and the static random input bytes are present, but their generator seed is not documented. These are recorded as discrepancies, not resolved by assumption.

## Citation and license

The seed paper has a verified BibTeX record in `literature/references.bib`. A repository citation file, project license, dataset license, and third-party redistribution decision are still pending. Do not redistribute upstream source or PDFs until their licensing and provenance have been reviewed.
