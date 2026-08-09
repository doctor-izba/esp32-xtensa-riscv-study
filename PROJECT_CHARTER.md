# Project Charter

## Mission

Build a serious, auditable, and extensible research project that relates workload behavior to documented architectural and software-platform differences between the original ESP32 and the ESP32-C6, while reproducing the historical benchmark design as closely as the available evidence permits.

## Primary research question

> How do the fundamental low-level architectural differences between the Xtensa LX6 used in the original ESP32 and the RISC-V core of the ESP32-C6 manifest themselves in real computational workloads?

## Secondary research question

> How have the performance characteristics of C/C++, Rust, and MicroPython changed when moving from the original Xtensa-based ESP32 platform to the modern RISC-V ESP32-C6 platform?

These questions do not define an ISA-only causal contrast. Any cross-chip difference may reflect ISA, microarchitecture, clock frequency, cache and memory behavior, compiler backend and version, SDK, runtime, core count, board configuration, or measurement protocol.

## Study scope

### In scope for the first paper

- New physical measurements on the user's ESP32-C6-N4, reported as a 4 MB flash device.
- Published classic-ESP32 measurements from Plauska et al. as historical evidence.
- C/C++, Rust, and MicroPython.
- Primary suite: CRC-32, SHA-256, FFT, FIR, and IIR, introduced one at a time after validation gates.
- Mode A fair, reproduction-oriented reconstruction/extension before any Mode B optimization work.
- Mode B optimized experiments with every compiler, architecture, placement, intrinsic, assembly, or hardware-accelerator choice recorded explicitly.
- Static C/C++ Xtensa and RISC-V machine-code comparison when reproducible cross-toolchains are available.
- Timing distributions, reliable cycle counts, build and memory metrics, static assembly metrics, and explicitly coarse board-level energy estimates.
- Primary-source architectural verification, a literature database, MATLAB analysis, a LaTeX paper, and release-ready provenance.

### Explicitly out of scope for the first paper

- Buying or physically testing an old ESP32.
- TinyGo implementations or new TinyGo measurements.
- AI/TinyML, Zig, mruby, WebAssembly, BlueScript, additional VM/runtime comparisons, and additional microbenchmark suites; these remain Future Work.
- Claiming pure ISA causality from a cross-chip comparison.
- Mixing Mode A and Mode B observations or distinct Mode B optimization profiles.
- Unsupported overclocking.
- Presenting USB power-meter readings as MCU-core energy.
- Implementing future targets such as ESP32-C5, ESP32-S31, ESP32-P4, or SBC systems in this study.

## Evidence hierarchy

1. Vendor manuals, ratified ISA specifications, ABI specifications, compiler documentation, and versioned source/toolchain artifacts.
2. Peer-reviewed publications and their archived supplementary material.
3. Reputable secondary technical sources, used only when their status is explicit.
4. Project constraints supplied by the researcher, which describe the intended experiment but do not verify technical claims.

AI answers, blogs, forums, and unsourced summaries are discovery aids only. An unsupported statement remains `UNVERIFIED`.

## Integrity commitments

- Correctness is established before timing.
- No measurement or citation is fabricated.
- Raw local evidence is append-only and never edited to improve a result.
- Published baselines are kept separate from local raw observations.
- Every run records protocol, vector, source, build, toolchain, hardware, and timer provenance.
- Fair Mode A does not receive an undocumented language-specific optimization.
- Architecture-specific explanations use qualified language and traceable sources.
- Generated statistics, figures, tables, and paper outputs are reproducible from CSV and scripts.
- Method changes are versioned and applied prospectively; prior data are not silently reinterpreted.

## Deliverables

- Versioned benchmark sources and correctness vectors.
- Immutable local run bundles and historical baseline transcriptions with provenance.
- Validation reports, processed CSV, and statistical outputs.
- Build manifests, code/RAM metrics, disassembly, and static assembly statistics.
- MATLAB analysis and publication figures.
- English-language LaTeX paper, reproduction guide, bibliography, and release manifest.
- A future GitHub Pages site that can host this and later papers without restructuring the research data.

## Milestone gates

1. **Foundation gate:** charter, questions, methodology, reproducibility policy, schemas, roadmap, source ledger, and repository structure reviewed.
2. **CRC source gate:** paper and repository pinned; CRC parameters, vectors, sizes, timing boundary, validation, iterations, and build assumptions classified as exact/equivalent/deviation/unknown.
3. **CRC correctness gate:** all three implementations match the same independent oracle for every frozen vector; no timing result is accepted before this passes.
4. **CRC acquisition gate:** run capture, schema validation, toolchain manifests, and raw-data immutability pass a pilot.
5. **CRC analysis gate:** Mode A dataset, MATLAB import/validation/statistics, and first figures reproduce from a clean checkout.
6. **Suite expansion gate:** add SHA-256, then FFT, FIR, and IIR one at a time through the same gates.
7. **Optimization gate:** Mode B begins only after Mode A is stable; each optimization combination has explicit metadata and a distinct build/profile identity.

## Current authorization state

CRC-32, SHA-256, FFT, FIR, and IIR Mode A are complete full vertical slices.
The minimal Mode B campaign is also complete under Decision 0013, including
COMPILER_PERF, HW_SHA, and the justified FFT RUST_UNCHECKED profile. The
experimental record is frozen; the project is in scientific synthesis and
manuscript preparation. Approval records are under `docs/decisions/`.

## Governance

- [METHODOLOGY.md](METHODOLOGY.md) is the normative experiment contract.
- [data/schemas/results_schema.md](data/schemas/results_schema.md) is the normative data interface.
- [docs/verification_ledger.md](docs/verification_ledger.md) is the claim-status register.
- [ROADMAP.md](ROADMAP.md) is the single authoritative task sequence.
- A protocol or schema change requires a version increment and a decision record stating rationale, affected data, and compatibility.
