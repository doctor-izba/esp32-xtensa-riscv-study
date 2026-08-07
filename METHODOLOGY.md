# Methodology

Version: `0.1.0-foundation`  
Status: design contract; CRC implementation and measurement are not yet authorized.

## 1. Study design

This is a historically anchored, cross-platform observational comparison plus a within-ESP32-C6 language/runtime experiment. New measurements will be collected only on the ESP32-C6-N4. Classic ESP32 evidence will come from the Plauska et al. paper and its pinned repository snapshot.

The cross-platform contrast is not controlled for ISA alone. ISA, microarchitecture, clock, pipeline, core count, cache/memory system, compilers, SDKs, runtimes, and SoC peripherals all differ. Results must therefore use platform-scoped wording and discuss alternative mechanisms.

## 2. Evidence units and origins

| Unit | Grain | Location | Origin value |
|---|---|---|---|
| Local observation | One timed invocation | `data/raw/` | `local_measurement` |
| Local run context | One acquisition session | `data/raw/` | `local_measurement` |
| Historical row/aggregate | One reported external value | `data/baselines/` | `published_aggregate` or `upstream_recording` |
| Build metric | One build artifact | `artifacts/builds/` and derived CSV | `local_build` |
| Assembly metric | One object/function/configuration | `artifacts/assembly/` and derived CSV | `static_analysis` |
| Energy window | One long meter interval | Dedicated raw bundle/derived CSV | `board_level_measurement` |

Origins and grains are mandatory fields; directory names are not a substitute for metadata.

## 3. Benchmark sets

- **Set A — Historical reproduction:** CRC-32, SHA-256, FFT, FIR, and IIR. CRC-32 is the only initial workload.
- **Set B — Microarchitectural:** explanatory call, branch, register-pressure, arithmetic, memory, alignment, stack, and floating/fixed-point kernels. Deferred until Set A is stable.
- **Set C — Modern compute / TinyML:** int8 matrix/vector, dense-layer, activation, convolution, and inference workloads. Separate from historical results and deferred.

## 4. Experiment modes

| Mode | Purpose | Allowed | Prohibited |
|---|---|---|---|
| `A` | Fair/historical reproduction | Matched algorithm, frozen vectors, types, sizes, correctness, and comparable timing boundary | C6-only acceleration, hardware SHA when the historical kernel is software, handwritten RISC-V assembly, opportunistic IRAM placement, unsupported overclocking |
| `B1` | CPU/ISA optimized | Release tuning, justified compiler architecture options, data placement, loop work, intrinsics, architecture-specific code, scientifically useful inline assembly | Dedicated peripheral, DMA, or crypto offload; contamination of Mode A artifacts |
| `B2` | Full-SoC optimized | B1 plus SHA/crypto accelerators, DMA, and other dedicated units | Presentation as a CPU/ISA-only result; mixing with A or B1 data |

Each run records exactly one `benchmark_mode` and a versioned `protocol_id`. An implementation may participate in multiple modes only through distinct build and protocol identifiers.

## 5. Core language policy

C/C++, Rust, and MicroPython are the only new-measurement languages for the first paper. TinyGo is retained only when describing the historical study. Fair Mode A must match semantic work and timing scope across the three core languages as closely as each runtime permits; every deviation is documented before collection.

## 6. Protocol freeze and comparability

Before implementing a workload, create a versioned protocol that fixes:

- algorithm variant and parameters;
- input datatype, exact vector bytes, vector hash, and sizes;
- correctness oracle and expected outputs;
- initialization, allocation, setup, kernel, validation, and cleanup boundaries;
- timer source, resolution, wrap behavior, cycle-counter semantics, and overhead plan;
- warm-up policy, measured iterations, independent runs, reset/cache state, task/core placement, and background services;
- compiler/runtime profiles and allowed flags;
- output record fields and failure behavior.

For each Plauska property, the protocol audit records one of `exact`, `equivalent`, `deviation`, or `unknown`. An `unknown` is never silently treated as `exact`.

The preliminary CRC audit is at `references/original-study/CRC32_AUDIT.md`. It is not yet a frozen implementation protocol.

## 7. Correctness gate

1. Freeze one canonical test-vector file and SHA-256.
2. Generate expected CRC values with at least one independent, named host oracle.
3. Test all eight historical input lengths, including zero bytes.
4. Require every implementation to report an exact 32-bit result match outside the timed region.
5. Include negative tests that prove a changed byte causes the expected mismatch.
6. Do not accept, plot, or summarize timing from a build that fails correctness.

The oracle must not be the same implementation translated into another language without independent cross-checking.

## 8. Timing and run policy

- Serial output, allocation, test-vector copying, table construction, validation, and cleanup are outside the kernel timing boundary unless a frozen Mode A compatibility decision states otherwise.
- Timing boundaries must represent equivalent semantic work in all languages.
- Warm-ups are explicit and either recorded as `phase=warmup` or documented as unrecorded by the acquisition protocol. Warm-ups never masquerade as measured iterations.
- A 100-iteration dataset compatible with the Plauska study will be retained for Mode A.
- The number of independent runs will be chosen after timer-resolution and variance pilots, then frozen before the main collection; 100 loop iterations alone are not treated as independent replicates.
- CPU frequency is configured where supported and read back. The recorded value is not inferred from a board default.
- Core affinity, scheduler state, radio/background-service state, power management, cache/reset sequence, garbage collection, and interrupt policy are recorded.
- A timer-overhead experiment is separate from the workload and is never subtracted without a predeclared rule.
- Cycle counts are stored only when read from a documented counter with understood frequency, width, privilege, wrap, and interrupt semantics. They are never synthesized as `elapsed time × nominal frequency`.

## 9. Acquisition and data flow

Each local run will be captured as an immutable bundle:

```text
data/raw/<target>/<benchmark>/<run_id>/
  run.csv
  observations.csv
  manifest.csv
  console.log        # optional but preferred
```

`run.csv` holds one context row; `observations.csv` holds one row per invocation; `manifest.csv` hashes every file. This normalized interface avoids repeating build/hardware metadata on every timing row and prevents build-, energy-, and iteration-level quantities from sharing an ambiguous row grain.

Validation writes a separate report under `data/validation/`. Processing consumes an explicit manifest of validated run hashes and writes `data/processed/`. No stage edits an upstream file. The normative columns and invariants are in `data/schemas/results_schema.md`.

## 10. Statistical plan

Raw observations are retained in full. For each predeclared group, analysis may report count, mean, median, standard deviation, minimum, maximum, p95/p99 when sample size supports them, and confidence intervals chosen for the sampling design. Distribution plots accompany summaries when space permits.

Outlier handling is predeclared. Suspect observations remain in raw data; exclusions are represented in validation/analysis metadata with a reason. Analyses distinguish within-run variation from between-run variation. Multiple comparisons, timer censoring/quantization, zero-length overhead, and non-normal distributions are addressed explicitly.

## 11. Historical comparison

- Plauska data retain their original evidence origin, statistic type, units, reported sample count, source locator, and transcription status.
- Only Mode A may appear in direct historical-comparability plots.
- Local C6 measurements and published ESP32 values are visually and textually distinguished.
- No per-iteration historical samples are fabricated from a mean and standard deviation.
- Comparisons state the hardware, frequency, toolchain/runtime eras, and protocol mismatches.

## 12. Static machine-code analysis

For equivalent kernels and pinned compilers, preserve source, compiler invocation, target triple/configuration, ELF/object, assembly listing, disassembly, link map, compiler version, and hashes. Metrics include function bytes, static instruction count, instruction-width distribution, loads, stores, branches, calls, stack-pointer accesses, likely spill traffic, integer/floating instructions, helper calls, and loop structure.

Static counts are properties of a particular artifact. They do not establish dynamic instruction counts, cache misses, branch outcomes, or execution cycles.

## 13. Resource metrics

Binary/file size, section sizes, static RAM, heap, peak heap, and stack high-water marks are separate metric families with exact definitions and collection tools. A file size is not reported as code size; `.data` and `.bss` are not conflated; runtime heap and build-time static RAM are not placed in the same observation row.

## 14. Power and energy

The current USB meter supports coarse board-level estimates only. Workloads will be repeated for a stable, sufficiently long interval; raw voltage/current/power readings, duration, operation count, idle/control window, meter model, sampling behavior, and board configuration will be recorded. Energy per operation is derived downstream.

Limitations include meter sampling rate and precision, regulator loss, USB interface and LEDs, peripherals, background tasks, and the distinction between board input energy and MCU-core energy. Higher-resolution equipment is future work.

## 15. Architecture and literature verification

Every technical claim receives an atomic claim ID, evidence class, verification status, source key, and exact locator in `docs/verification_ledger.md`. Primary sources are preferred. If a core-specific detail cannot be found in an accessible primary source, it remains unverified even if a generic ISA manual describes an optional feature.

## 16. Threats to validity

- **Internal:** scheduler/interrupt interference, thermal/power variation, timer quantization, cache state, GC, build drift, and inconsistent timing boundaries.
- **Construct:** execution time may not capture throughput, energy, memory pressure, determinism, development cost, or real application behavior.
- **External:** one C6 device/board, five historical kernels, and particular toolchains do not generalize to all Espressif or RISC-V/Xtensa systems.
- **Conclusion:** dependent iterations, small independent-run counts, multiple comparisons, censoring, and inappropriate distributions can overstate certainty.
- **Historical:** original raw provenance, warm-up behavior, environment details, and some toolchain configuration may be incomplete or internally inconsistent.

## 17. Methodology change control

A material change requires a decision record and a new protocol/schema/implementation version before new data are collected. The record states rationale, affected evidence, compatibility, and whether recollection is required. Existing raw and baseline files are never rewritten. A corrected historical algorithm is a distinct protocol, not a silent replacement for Mode A.
