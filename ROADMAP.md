# Research Roadmap

This is the authoritative task sequence. Phases are gated by evidence, not dates.

## Phase 0 — Foundation

- [x] Initialize the Git repository on `main`.
- [x] Establish charter, research questions, methodology, reproducibility policy, and data schemas.
- [x] Create scoped repository structure.
- [x] Pin and preliminarily audit the Plauska paper/repository.
- [x] Start a primary-source verification ledger and literature database.
- [x] Review this scaffold with the researcher.
- [x] Make the initial user-controlled commit and record the approval decision.

**Exit evidence:** all links/schemas validate, no benchmark source or fabricated result exists, and explicit approval opens the CRC gate.

## Phase 1 — CRC-32 source and protocol freeze

- [x] Confirm the pinned upstream snapshot and retain the vector without vendoring while redistribution remains unresolved.
- [x] Extract the canonical upstream byte vector and expected CRC values; record SHA-256.
- [x] Independently verify the CRC variant and every expected value.
- [x] Complete an exact/equivalent/deviation/unknown comparability matrix for C/C++, Rust, and MicroPython.
- [x] Resolve or explicitly freeze the paper/repository iteration discrepancy and cross-language warm-up asymmetry.
- [x] Pin feasible C6 C/C++, Rust, and MicroPython toolchains and capture all versions.
- [x] Review and approve `crc32-mode-a-v1` with correctness and timing boundaries.

**Exit evidence:** signed-off protocol, vectors, oracle, toolchain plan, and unresolved fields visibly marked.

## Phase 2 — CRC-32 correctness-only implementations

- [x] Implement equivalent C/C++, Rust, and MicroPython kernels with no performance tuning beyond Mode A.
- [x] Run host/device correctness tests for every input size and negative test.
- [x] Verify that Mode A does not call a hardware CRC/crypto path.
- [x] Freeze implementation IDs and build profiles.

**Exit evidence:** all implementations produce the same expected 32-bit values; timing remains disabled until this gate passes.

## Phase 3 — CRC-32 acquisition pilot and Mode A collection

- [x] Implement run capture, manifest hashing, and schema validation.
- [x] Characterize timer resolution/overhead, frequency, scheduler/interrupt behavior, GC, and warm-up effects.
- [x] Choose and freeze the first acquisition run plan after the pilot.
- [x] Collect immutable C6 Mode A bundles, including a compatible 100-iteration dataset.
- [x] Transcribe/import the historical baseline with provenance.

**Exit evidence:** validated raw bundles and historical baseline remain separate and fully traceable.

## Phase 4 — CRC-32 analysis and first figures

- [ ] Implement `matlab/import_results.m` and `matlab/validate_results.m`.
- [x] Implement statistics and CRC execution-time/normalized plots from CSV.
- [ ] Add build/code/RAM metrics where reproducible.
- [ ] Rebuild outputs from a clean checkout and record lineage.

**Exit evidence:** first end-to-end reproducible CRC result package.

## Phase 5 — Historical suite expansion

Add SHA-256, FFT, FIR, and IIR **one at a time**, repeating Phases 1–4 for each. Hardware SHA remains prohibited in Mode A.

- [x] SHA-256 software Mode A full vertical slice.
- [x] FFT Mode A complete.
- [x] FIR Mode A complete under Decision 0011.
- [x] IIR Mode A complete under Decision 0012; primary Mode A suite complete.

## Phase 6 — Static architecture and assembly analysis

- [x] Pin Xtensa and RISC-V C/C++ cross-toolchains.
- [x] Preserve available ELF/object/assembly/disassembly/link maps and hashes, with the missing accepted Rust ELF disclosed.
- [x] Generate static instruction/byte/category metrics.
- [x] Relate patterns to primary-source claims while separating static from runtime evidence.

## Phase 7 — Mode B optimization

- [x] Complete cross-workload Mode A synthesis and design the minimal Mode B question set without executing it.
- [x] Design and run the frozen minimal Mode B campaign after Mode A was frozen.
- [x] Record every enabled optimization and combination in run metadata and CSV.
- [x] Keep sources, build IDs, datasets, plots, and claims mode/profile-specific.

## Phase 8 — Deferred extensions

- [ ] Evaluate additional microarchitectural kernels.
- [ ] Evaluate modern compute/AI/TinyML workloads.
- [ ] Conduct a feasibility review for mruby, Zig, WebAssembly runtimes, BlueScript, or other models without delaying the core paper.
- [ ] Design coarse USB-meter board-energy experiments and later high-resolution instrumentation work.

## Phase 9 — Paper and release

- [ ] Complete the English LaTeX manuscript, threats to validity, and reproducibility appendix.
- [ ] Produce archival manifests, licenses, citation metadata, dataset/code release, and PDF.
- [ ] Build the multi-paper GitHub Pages site.
- [ ] Create a versioned GitHub release and, when ready, a Zenodo DOI.
