# Research Roadmap

This is the authoritative task sequence. Phases are gated by evidence, not dates.

## Phase 0 — Foundation

- [x] Initialize the Git repository on `main`.
- [x] Establish charter, research questions, methodology, reproducibility policy, and data schemas.
- [x] Create scoped repository structure.
- [x] Pin and preliminarily audit the Plauska paper/repository.
- [x] Start a primary-source verification ledger and literature database.
- [ ] Review this scaffold with the researcher.
- [ ] Make the initial user-controlled commit and record the approval decision.

**Exit evidence:** all links/schemas validate, no benchmark source or fabricated result exists, and explicit approval opens the CRC gate.

## Phase 1 — CRC-32 source and protocol freeze

- [ ] Confirm the pinned upstream snapshot and redistribution/license policy.
- [ ] Extract the canonical upstream byte vector and expected CRC values; record SHA-256.
- [ ] Independently verify the CRC variant and every expected value.
- [ ] Complete an exact/equivalent/deviation/unknown comparability matrix for C/C++, Rust, and MicroPython.
- [ ] Resolve or explicitly freeze the paper/repository iteration discrepancy and cross-language warm-up asymmetry.
- [ ] Pin feasible C6 C/C++, Rust, and MicroPython toolchains and capture all versions.
- [ ] Write and review `protocol-a-v1` with correctness and timing boundaries.

**Exit evidence:** signed-off protocol, vectors, oracle, toolchain plan, and unresolved fields visibly marked.

## Phase 2 — CRC-32 correctness-only implementations

- [ ] Implement equivalent C/C++, Rust, and MicroPython kernels with no performance tuning beyond Mode A.
- [ ] Run host/device correctness tests for every input size and negative test.
- [ ] Verify that Mode A does not call a hardware CRC/crypto path.
- [ ] Freeze implementation IDs and build profiles.

**Exit evidence:** all implementations produce the same expected 32-bit values; timing remains disabled until this gate passes.

## Phase 3 — CRC-32 acquisition pilot and Mode A collection

- [ ] Implement run capture, manifest hashing, and schema validation.
- [ ] Characterize timer resolution/overhead, frequency, scheduler/interrupt behavior, GC, and warm-up effects.
- [ ] Choose and freeze independent-run count after the pilot.
- [ ] Collect immutable C6 Mode A bundles, including a compatible 100-iteration dataset.
- [ ] Transcribe/import the historical baseline with double-review provenance.

**Exit evidence:** validated raw bundles and historical baseline remain separate and fully traceable.

## Phase 4 — CRC-32 analysis and first figures

- [ ] Implement `matlab/import_results.m` and `matlab/validate_results.m`.
- [ ] Implement statistics and CRC execution-time/normalized plots from CSV.
- [ ] Add build/code/RAM metrics where reproducible.
- [ ] Rebuild outputs from a clean checkout and record lineage.

**Exit evidence:** first end-to-end reproducible CRC result package.

## Phase 5 — Historical suite expansion

Add SHA-256, FFT, FIR, and IIR **one at a time**, repeating Phases 1–4 for each. Hardware SHA remains prohibited in Mode A.

## Phase 6 — Static architecture and assembly analysis

- [ ] Pin Xtensa and RISC-V C/C++ cross-toolchains.
- [ ] Preserve ELF/object/assembly/disassembly/link maps and hashes.
- [ ] Generate static instruction/byte/category metrics.
- [ ] Relate patterns to primary-source claims while separating static from runtime evidence.

## Phase 7 — Optimized modes

- [ ] Design and run B1 only after Mode A is frozen.
- [ ] Design and run B2 only after B1 is frozen.
- [ ] Keep sources, build IDs, datasets, plots, and claims mode-specific.

## Phase 8 — Deferred extensions

- [ ] Evaluate Set B microarchitectural kernels.
- [ ] Evaluate Set C modern compute/TinyML workloads.
- [ ] Conduct a feasibility review for mruby, Zig, WebAssembly runtimes, BlueScript, or other models without delaying the core paper.
- [ ] Design coarse USB-meter board-energy experiments and later high-resolution instrumentation work.

## Phase 9 — Paper and release

- [ ] Complete the English LaTeX manuscript, threats to validity, and reproducibility appendix.
- [ ] Produce archival manifests, licenses, citation metadata, dataset/code release, and PDF.
- [ ] Build the multi-paper GitHub Pages site.
- [ ] Create a versioned GitHub release and, when ready, a Zenodo DOI.
