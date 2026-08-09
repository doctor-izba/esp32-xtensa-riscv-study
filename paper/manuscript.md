---
title: "Workload-Dependent Performance Across ESP32 Generations: A Reproduction-Oriented Xtensa-to-RISC-V Study"
bibliography: references.bib
---

# Abstract

The transition from the classic ESP32's Xtensa LX6 processors to the ESP32-C6's RV32IMAC high-performance core invites simple claims about instruction-set performance, but the two systems also differ in microarchitecture, memory hierarchy, software generations, and peripherals. We present a historically anchored study of CRC-32, SHA-256, Q15 FFT, binary32 FIR, and binary32 IIR in C/C++, Rust, and MicroPython. Mode A reconstructs the recoverable methodology of Plauska et al. on one physical ESP32-C6 using common inputs, correctness rules, timing boundaries, warm-up, and 100 measurements at eight sizes. Mode B evaluates native performance-oriented compilation, the C6 SHA peripheral, and a precondition-audited Rust FFT variant. The new record contains 12,000 Mode A and 9,600 Mode B observations. Published classic-ESP32 results are retained as historical evidence rather than fabricated paired samples. Exact measured C6 binaries and matched, reconstructed Xtensa/RV32IMAC objects provide static generated-code evidence. Results are workload dependent: local native CRC-32, SHA-256, and FFT means are lower than the historical values, while FIR and IIR are substantially higher. Exact C6 FIR/IIR kernels call software-floating-point helpers, whereas matched Xtensa objects emit floating-point instructions; IIR feedback exposes a serialized helper chain. C++ versus Rust ordering crosses parity. Performance compilation helps, harms, or barely changes different kernels; hardware SHA provides the largest acceleration but is a SoC-peripheral result. Removing five surviving bounds-check failure paths accelerates only the audited FFT case. These findings reject a universal “RISC-V is faster” interpretation. Because no classic ESP32 was rerun under matched tools, reconstructed objects are not Plauska binaries, and only one C6 board was measured, the evidence supports workload/code-generation mechanisms and descriptive platform comparisons, not pure ISA causality.

# 1. Introduction

Microcontroller architecture comparisons are often compressed into an ISA label. That compression is especially risky for ESP32 generations. The classic ESP32 integrates Xtensa LX6 processors, while the ESP32-C6 integrates an Espressif RISC-V high-performance core configured as RV32IMAC [@espressifESP32Datasheet; @espressifESP32C6Datasheet]. A measured difference between them can reflect the ISA, core implementation, caches and flash, compiler backend, SDK, runtime, board, or experimental protocol. The central scientific problem is therefore not which label wins, but how verified low-level differences appear in particular workloads and how strongly the available evidence supports each explanation.

Plauska et al. measured C/C++, Rust, MicroPython, and TinyGo on a classic ESP32 using CRC-32, SHA-256, FFT, FIR, and IIR [@plauska2023performance]. Their work provides an unusually relevant historical anchor, but its published implementation contains recoverability and cross-language inconsistencies. This study reconstructs the comparable contract on ESP32-C6 without representing the result as an exact reproduction. It also adds correctness oracles, immutable raw evidence, exact C6 binaries, matched static reconstruction, and an explicitly separated optimization campaign.

The contribution is fourfold. First, it provides a correctness-gated, three-language physical ESP32-C6 dataset over five arithmetic classes. Second, it preserves published classic-ESP32 evidence separately and makes the limits of historical comparison explicit. Third, it connects timings to exact C6 and matched Xtensa generated code using an OBSERVED/DOCUMENTED/INFERRED evidence discipline. Fourth, it shows that compiler optimization, safety checks, and hardware acceleration answer different questions and must not be pooled as generic “RISC-V performance.”

# 2. Background

## 2.1 Classic ESP32 and Xtensa LX6

The classic ESP32 family uses configurable Xtensa LX6 processors. The vendor documentation describes the implemented processor, memory, cache, floating-point, and DSP-related facilities [@espressifESP32Datasheet; @espressifESP32TRM]. Xtensa's configurable nature matters: a generic ISA document establishes available forms, not the configuration of a particular chip [@cadenceXtensaISASummary]. Register-window behavior also affects calls and exception context, as explored in security and real-time work [@lehniger2023throughwindow; @lehniger2025shadowstacks]. This study does not infer ordinary kernel cost from that literature; it uses it as architectural context.

## 2.2 ESP32-C6 and RV32IMAC

The ESP32-C6 vendor record identifies a single high-performance RISC-V CPU implementing RV32IMAC and a separate low-power core [@espressifESP32C6Datasheet; @espressifESP32C6TRM]. The `I` base provides integer computation, `M` multiplication/division, `A` atomics, and `C` compressed instructions [@riscvUnprivV22; @riscvCompressedV20]. The measured C6 target does not include the standard `F` extension. Its ABI and register roles follow the selected RISC-V toolchain rather than being inferred solely from a current generic ABI page [@riscvPsABI10].

## 2.3 Execution models

C++ and Rust compile to native RV32IMAC code but use different front ends, backends, libraries, safety semantics, and source structures. MicroPython executes through an interpreter with object and allocation costs; its own documentation treats allocation avoidance and native emitters as performance concerns [@micropythonSpeedV128]. Consequently, a MicroPython platform difference includes interpreter generation and implementation changes. Prior ESP32 work likewise reports substantial native/interpreted differences [@ionescu2020micropythonc; @tan2025scripting], while recent ESP32-C3 work demonstrates that runtime and event model remain important on Espressif RISC-V hardware [@tan2026eventdriven].

# 3. Related Work

Plauska et al. are the direct baseline [@plauska2023performance]. Their benchmark breadth and languages motivate the present suite, while their historical evidence remains distinct from our local observations. Ionescu and Enescu compared C and MicroPython CRC/SHA-related operations on ESP32 and STM32 [@ionescu2020micropythonc]. Tan et al. broadened ESP32 scripting-runtime comparisons [@tan2025scripting]. These works establish language/runtime benchmarking precedent but do not provide the present C6 physical reconstruction plus exact binary analysis.

Cross-platform embedded work emphasizes why heterogeneous boards do not isolate an ISA. Ariel OS evaluates Rust across Xtensa, RISC-V, and Arm devices [@frank2025ariel]. Femto-Containers evaluates portable isolation on heterogeneous microcontrollers [@zandberg2022femtocontainers]. Hubacz and Trybus study data alignment across many processors, including Espressif Xtensa and RISC-V devices [@hubacz2022alignment]. Molano Rodríguez includes classic ESP32 and ESP32-C6 in a broader undergraduate evaluation, but differing implementations and incomplete paired provenance limit direct use [@molano2025riscvfpga]. Our contribution is narrower: equivalent frozen kernels, three languages, accepted per-invocation C6 evidence, a pinned historical baseline, and generated-code mechanism analysis.

Energy and modern-runtime work are adjacent rather than evidentiary substitutes. Lima evaluates cryptographic configurations and module-rail measurement on C6 [@lima2025esp32c6signatures]. Has et al. examine WebAssembly on constrained devices including C6 [@has2025wasmiot]. We do not use either to infer the performance or energy of our kernels; precise chip energy and additional runtimes remain future work.

# 4. Research Questions

**RQ1.** How do fundamental low-level architectural differences between the Xtensa LX6 used in the original ESP32 and the RISC-V core of the ESP32-C6 manifest themselves in real computational workloads?

**RQ2.** How do C/C++, Rust, and MicroPython performance characteristics change from the published classic-ESP32 baseline to ESP32-C6?

The questions are explicitly not an ISA-only causal design. Mode B adds two exploratory questions: how each native toolchain's performance-oriented configuration changes C6 behavior, and what a dedicated C6 SHA peripheral changes relative to software.

# 5. Methodology

## 5.1 Evidence classes and historical baseline

We distinguish: (A) Plauska published/upstream historical timing, (B) new physical C6 observations, (C) exact measured C6 machine code, (D) reconstructed matched Xtensa/RV32IMAC code, (E) vendor/ISA documentation, and (F) inferred mechanisms. These classes are never silently collapsed. The historical source is DOI 10.3390/electronics12010143 and pinned repository commit `c42dba0d41d547960b73e63b3d4e09917d61e171`. Published aggregates are not expanded into invented samples.

## 5.2 Hardware and controls

Measurements used one ESP32-C6 revision 0.2 module on an ESP32-C6 Relay X1 carrier with 4 MB DIO flash at 80 MHz. The high-performance CPU was fixed and read back at 160 MHz. Dynamic frequency scaling, sleep, Wi-Fi, BLE, and IEEE 802.15.4 were disabled. The timer was `esp_timer_get_time()` for native code and the frozen MicroPython equivalent. The available KWS-V20 meter cannot isolate the module or chip rail, so exact energy was not measured.

## 5.3 Mode A

Mode A is a fair, reproduction-oriented reconstruction. Each language uses the same recoverable algorithm, input vector, eight historical sizes, correctness requirements, one unmeasured warm-up, and 100 accepted samples per size. Allocation, slicing, vector preparation, garbage-collection preparation, table construction, validation, and output are outside the timed kernel boundary. A timer-resolution pilot selected frozen repeated-kernel batches where single calls were too short; raw data retain both batch duration and count.

CRC-32 is CRC-32/ISO-HDLC. SHA-256 is the frozen software implementation. FFT uses the recovered Q15 complex representation and scaling. FIR and IIR preserve binary32 coefficients, ordering, state initialization, and tolerances. No architecture-specific optimization or C6 accelerator is used in Mode A. Correctness against host/MATLAB oracles precedes timing.

The accepted Mode A record comprises 12,000 observations: five workloads × three languages × eight sizes × 100 repetitions. Repetitions within one acquisition are not claimed as independent physical replicates.

## 5.4 Mode B

Mode B preserves the computational contracts while changing declared profiles. `COMPILER_PERF` uses ESP-IDF v5.5.5's performance setting for C++; preserved commands show GCC 14.2.0 `-O2`. Rust uses rustc/cargo 1.97.1 release `opt-level=3`. These settings are native toolchain policies, not equivalent optimizer levels.

The separate `HW_SHA` profile invokes ESP-IDF's one-shot `mbedtls_sha256` path. Exact code contains ESP SHA arbitration, DMA, and HAL calls; setup/finalization are included in the timed call, while input preparation is excluded. The separate `RUST_UNCHECKED` FFT profile was activated only after exact safe code retained five bounds-panic references. Frozen preconditions prove all indexes for zero or power-of-two sizes through 1024 and the generated tables; correctness is unchanged. CRC IRAM was rejected because no existing fetch/cache observation provided an identifiable hypothesis. Mode B contains 9,600 accepted observations.

## 5.5 Toolchains, data, and statistics

C++ used ESP-IDF v5.5.5. Rust used rustc/cargo 1.97.1 and `esp-idf-sys` 0.37.2. Exact MicroPython firmware version and build provenance are recorded in workload run metadata. Every accepted native Mode B ELF is hashed; exact Mode A artifacts are retained except the original accepted Rust CRC ELF, for which only a labelled pinned-source reconstruction is available.

Processing validates correctness, size/iteration uniqueness, metadata, and reconstructability of normalized time from total batch duration and count. We report count, mean, median, and sample standard deviation. Historical/local ratios use published historical mean divided by local mean. C6 language ratios use medians. Ratios are descriptive; no null-hypothesis test treats within-run repetitions as independent boards.

## 5.6 Static binary analysis

Exact measured C6 ELF disassemblies are used for function size, static instructions, loads, stores, branches, calls, stack frames, helper calls, and panic references. Matched C++ source is compiled for Xtensa and RV32IMAC to inspect lowering under pinned toolchains. Reconstructed Xtensa objects were not run and are not the Plauska binaries. Static instructions are not dynamic traces, cycles, stalls, or cache misses.

# 6. Results

## 6.1 Cross-workload Mode A

Figure 1 reports published mean divided by local mean at the largest common input. Values greater than one mean the local C6 mean is lower. Native CRC-32, SHA-256, and FFT favor the local measurement direction; FIR and IIR strongly favor the historical direction. MicroPython local means are lower than historical means for all five workloads, but that observation is runtime-confounded.

![Historical/local mean ratio. Values above one indicate a lower local C6 mean. Sources: accepted Mode A processed datasets and Plauska historical aggregates; this is not an ISA treatment effect.](figures/fig1_historical_local_ratio.png)

At 1024 units, Plauska/C6 mean ratios for C++ are 1.134 (CRC), 1.046 (SHA), 1.536 (FFT), 0.159 (FIR), and 0.066 (IIR). Rust ratios are 1.578, 1.403, 2.360, 0.130, and 0.076. The direction reversal aligns with arithmetic class (Figure 3) but does not alone establish its cause.

## 6.2 CRC-32

Mode A C6 medians at 1024 bytes are 104 us for C++ and 72 us for Rust, giving Rust/C++ = 0.692. Exact C++ and reconstructed Rust loops differ in addressing and termination. The matched C++ Xtensa loop is statically smaller than its RV32IMAC counterpart, illustrating that code density and cross-platform elapsed time need not point in the same direction.

`COMPILER_PERF` lowers the C++ median to 78 us (1.333× speedup) but raises Rust to 77.5 us (7.6% slower). CRC therefore supplies a counterexample to both “more optimization always helps” and “one language always wins.” The A-side Rust binary limitation prevents an exact measured-ELF A/B claim for Rust CRC; the reconstruction is explicitly labelled.

## 6.3 SHA-256

Mode A medians are 670 us for C++ and 711 us for Rust. The matched Xtensa transform uses `src` rotate idioms, whereas RV32IMAC expands rotations into shifts and combinations. The exact Rust transform has more control/storage structure than C++, yet the historical/local direction slightly favors C6. Static density is therefore explanatory evidence, not a timing oracle.

`COMPILER_PERF` produces 626 us for C++ and 628 us for Rust, improvements of 7.0% and 13.2%. `HW_SHA` produces 77 us at 1024 bytes: 8.70× faster than Mode A software and 8.13× faster than C++ `COMPILER_PERF`. Figure 5 keeps the three profiles distinct. The acceleration belongs to the C6 SHA peripheral and ESP-IDF path, not the RISC-V CPU ISA.

## 6.4 FFT

Mode A C++ and Rust medians are 1185.563 and 1493.750 us, so Rust/C++ = 1.260. Exact C6 code and matched objects use scalar fixed-point multiply/shift sequences; no Xtensa DSP/MAC or zero-overhead-loop instruction was observed in the matched kernel. Safe Rust contains five bounds-panic references and a larger control structure.

C++ `COMPILER_PERF` regresses 4.9% to 1243.438 us, while Rust improves 1.8% to 1467.688 us and retains all five panic references. The audited unchecked profile removes the references, reduces the extracted kernel from 125 to 83 static instructions, and reaches 1134.250 us. It is 22.7% faster than safe Rust `COMPILER_PERF`. This supports a safety-check cost for this frozen kernel and proven index domain, not a general Rust penalty.

## 6.5 FIR

At 1024 samples, local Mode A C++ and Rust medians are 188774 and 186340 us. Historical means are 30054.7 and 24219.2 us. The historical/local ratios, 0.159 and 0.130, are the first strong reversal in the suite. Exact C6 kernels contain two `__mulsf3` and two `__addsf3` call sites in the static loop body. The matched Xtensa object emits `madd.s` without helper calls.

`COMPILER_PERF` improves C++ by 7.1% but Rust by only 0.4%; helper calls persist. Optimization changes surrounding code but does not change the fundamental software-FP mechanism.

## 6.6 IIR

Mode A medians are 3268 us for C++ and 3277.5 us for Rust, nearly tied. Historical means are 214.32 and 248.93 us, yielding ratios 0.066 and 0.076. Each exact C6 kernel contains five `__mulsf3`, two `__addsf3`, and two `__subsf3` sites. The matched Xtensa object instead emits `mul.s`, `madd.s`, and `msub.s` operations.

The IIR recurrence carries state from one sample into the next. Under the frozen operation order, this dependency constrains cross-sample reordering and exposes the chain of software helper calls. `COMPILER_PERF` changes medians by only 1.2% for C++ and 0.2% for Rust, leaving the mechanism intact.

## 6.7 Language ratios

Figure 2 shows that Rust/C++ crosses parity rather than following a universal hierarchy. At the largest input it is 0.692 for CRC, 1.061 for SHA, 1.260 for FFT, 0.987 for FIR, and 1.003 for IIR. MicroPython/C++ ratios are approximately 241, 890, 204, 22, and 26. These are properties of the tested sources and toolchains, not language-wide constants.

![Within-C6 Mode A Rust/C++ median ratios across sizes. The parity line is descriptive; values below one favor Rust.](figures/fig2_rust_cpp_ratio.png)

![Largest-input arithmetic-class contrast. Historical/local direction changes between integer/fixed-point and binary32 native workloads.](figures/fig3_arithmetic_class.png)

## 6.8 Integrated Mode B response

Figure 4 shows nonuniform compiler response. C++ CRC is compiler-sensitive; C++ FFT regresses; SHA improves modestly in both languages; FIR/IIR move little, especially in Rust. FIR changes language ordering from a slight Rust advantage to a C++ advantage, while CRC becomes nearly tied.

![Largest-input COMPILER_PERF/Mode A median ratio. Below one is faster; above one is slower.](figures/fig4_compiler_perf.png)

![SHA-256 1024-byte medians for software Mode A, software COMPILER_PERF, and HW_SHA. Logarithmic time axis; HW_SHA is a SoC-peripheral profile.](figures/fig5_sha_profiles.png)

![FIR/IIR COMPILER_PERF response. Exact optimized binaries retain software-FP helper calls.](figures/fig6_software_fp.png)

# 7. Discussion

## 7.1 Central thesis and RQ1

The strongest defensible thesis is interaction: architectural facilities matter through workload-specific compiler lowering, arithmetic representation, control dependencies, runtime behavior, and SoC context. RQ1 is answered by heterogeneous manifestations. CRC exposes loop/address formation; SHA exposes rotate lowering; Q15 FFT exposes scalar multiply/shift and surviving safety control; FIR/IIR expose hardware-instruction versus software-helper strategies. IIR feedback makes the helper chain particularly difficult to hide. These mechanisms are observed in exact or explicitly reconstructed artifacts. They do not establish that an ISA label alone caused the historical timing ratios.

## 7.2 RQ2

RQ2 also has no single direction. Relative to published classic-ESP32 means, local C6 native CRC, SHA, and FFT are lower, while FIR/IIR are much higher. Within C6, C++ and Rust ordering changes by workload. MicroPython is much slower than native code locally, although its local results improve relative to the historical study. Interpreter, numeric-object, SDK, and implementation-generation changes make that improvement unsuitable as an ISA comparison.

## 7.3 Floating-point case study

FIR/IIR provide the strongest code-supported architectural contrast. **Observed:** exact RV32IMAC binaries call software FP helpers; matched Xtensa objects emit FP instructions. **Documented:** the C6 target is RV32IMAC without `F`. **Inferred:** the different execution strategies are consistent with software FP being a major contributor to the large historical/local native gap, with IIR dependency increasing exposure. The experiment does not quantify a pure FP-unit causal effect because the historical binaries and matched physical controls are unavailable.

## 7.4 What Mode B adds

Mode B does not overturn Mode A; it makes its interaction story stronger. Performance-oriented compilation improves, degrades, or barely changes different kernels. Persistent FIR/IIR helpers show a limit to compiler-only compensation. FFT demonstrates a measurable cost for checks that survive optimization in one audited kernel. HW SHA demonstrates that a dedicated peripheral can dominate software compiler gains. The negative result—no uniform benefit—is scientifically useful because it prevents an optimization flag from being treated as a platform-independent capability measure.

# 8. Threats to Validity

**Historical/internal validity.** No physical classic ESP32 was rerun. Plauska is a historical baseline, not a controlled paired experiment, and its source/paper contain warm-up, slicing, launcher, and iteration inconsistencies. Compiler, SDK, Rust ecosystem, and MicroPython generations differ. Both reported platforms used 160 MHz, but equal nominal frequency does not equal matched microarchitecture or measured cycles.

**Construct validity.** Elapsed kernel time does not measure IPC, cache misses, dynamic instructions, energy, memory pressure, development cost, or application throughput. Static instruction counts are not dynamic traces. The KWS-V20 and unmodified carrier cannot isolate exact chip energy, so no energy result is claimed.

**External validity.** One C6 board and five compact kernels cannot represent all ESP32 devices, RISC-V/Xtensa cores, toolchains, languages, or applications. Binary32 FIR/IIR emphasize a C6 configuration without standard hardware FP; other workloads and chips may behave differently.

**Generated-code validity.** Reconstructed Xtensa artifacts are not Plauska binaries and were not executed. Matched builds reduce source differences but retain compiler/backend differences. The accepted Mode A Rust CRC ELF was not retained. Exact C6 artifacts establish what was emitted for measured builds, except that disclosed case, but do not identify dynamic path frequencies.

**Mode B validity.** `COMPILER_PERF` is language-specific: C++ `-O2` and Rust opt-level 3 are not equivalent knobs. HW SHA and unchecked FFT answer separate mechanistic questions and are not historically equivalent profiles. The unchecked result depends on proven frozen preconditions and must not be generalized to arbitrary Rust code.

**Sampling validity.** One hundred iterations within a run are repeated observations, not 100 independent device replicates. Thermal, supply, board-unit, and day-to-day variation are not estimated. A retained C++ CRC watchdog diagnostic occurred between timed samples; all unique records and timing boundaries remained valid, but it documents scheduler-system activity outside the kernel interval.

# 9. Reproducibility

The frozen experimental input anchor is commit `933363b342ac960c0d364b4c6379b1ac884dec9f`; the manuscript commit reported with this paper adds only downstream synthesis and paper artifacts. Analysis-only reproduction starts with `data/processed/`, validates hashes in `paper/tables/experimental_inventory.csv`, and runs the workload MATLAB scripts plus `matlab/run_mode_a_cross_workload_analysis.m` and `matlab/run_mode_b_analysis.m` in MATLAB R2024b. `paper/FIGURE_MANIFEST.csv` maps each selected figure to its generated source and SHA-256.

Firmware rebuilding uses ESP-IDF v5.5.5 for C++, rustc/cargo 1.97.1 with `esp-idf-sys` 0.37.2 for Rust, and the firmware/toolchain metadata recorded in each MicroPython bundle. The target is ESP32-C6 revision 0.2, 160 MHz, 4 MB DIO/80 MHz flash, with radios, sleep, and dynamic scaling disabled. Frozen vectors and workload protocols reside under `benchmarks/historical/<workload>/`; Mode B is under `benchmarks/optimized/`.

Physical reruns must execute correctness first, retain one warm-up and 100 measurements for each of eight sizes, preserve batch count plus total time, and create new raw evidence rather than overwriting accepted data. Exact build artifacts and disassemblies are under `artifacts/builds/` and `artifacts/assembly/`. Historical provenance is under `references/original-study/` and `data/baselines/`. Detailed steps are in `paper/REPRODUCIBILITY_CHECKLIST.md`.

# 10. Future Work

The most valuable extension is a physical classic-ESP32 rerun using matched contemporary toolchains, identical vectors, and the same timing/correctness harness. Additional Xtensa and RISC-V Espressif families could separate family-specific from recurring effects. Precise module-rail or chip-rail instrumentation is required for energy per operation. Hardware counters or traces could test dynamic instruction, stall, cache, and branch hypotheses.

Numerical reformulation should be a new declared experiment: binary32 versus fixed point or reduced precision, and fast-math with an explicit numerical-semantics contract. Multicore throughput belongs to a separate design. Additional languages and runtimes—including WebAssembly, Zig, mruby, and embedded Rust OS configurations—remain useful but should not be mixed into the present conclusions [@wallentowitz2022wasm; @moron2023wasmjit].

# 11. Conclusion

Across five workloads, three languages, 21,600 accepted local observations, and exact/reconstructed code analysis, the ESP32 generation change has no universal performance direction. Integer checksum, cryptographic, fixed-point transform, feed-forward floating-point, and feedback floating-point kernels expose different lowering and execution mechanisms. C++ and Rust cross parity. Compiler-performance settings are not uniformly beneficial. Hardware SHA is powerful but peripheral-specific. The strongest architectural contrast is the observed software-FP helper strategy on C6 versus FP instructions in matched Xtensa FIR/IIR objects, especially under IIR feedback. The scientifically supported conclusion is workload-dependent architecture–compiler–runtime interaction, not ISA supremacy.

# References

References are resolved from `paper/references.bib`. Only verified repository bibliography entries cited above are included by the document processor.
