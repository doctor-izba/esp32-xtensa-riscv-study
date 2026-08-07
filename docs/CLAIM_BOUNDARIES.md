# Claim Boundaries

- Status: mandatory guardrails derived from the related-work and novelty audit
- Effective date: 2026-08-08

This document constrains future interpretation and writing. It does not change the approved research questions or methodology, and it does not open the CRC-32 or Protocol A gates.

## Core rule

The study compares **platform configurations and evidence classes**, not isolated ISAs. Classic ESP32 and ESP32-C6 differ in core implementation, ISA, SoC, clock, memory system, peripherals, toolchains, runtimes, board design, and publication era. No statistical treatment can turn that cross-chip design into a pure Xtensa-versus-RISC-V causal experiment.

## Claim vocabulary

| Evidence available | Safe language | Language to avoid |
|---|---|---|
| Direct local observation | “On the tested board/configuration, we observed …” | “ESP32-C6 always …”; “RISC-V inherently …” |
| Published historical statistic | “Plauska et al. reported …” | “We observed …”; fabricated historical rows or confidence intervals |
| Static disassembly/artifact | “The captured build contains/emits …” | “The processor executed … times”; “this cost … cycles” |
| Primary architecture documentation | “The documented implementation provides/implements …” | Generalizing the feature to all Xtensa or all RISC-V cores |
| Observation plus plausible mechanism | “The pattern is consistent with …”; “a candidate explanation is …” | “The mechanism caused …” without an identifying experiment |
| Focused literature audit | “We did not identify a study in the audited corpus that combines …” | “No prior work exists”; “first ever”; “the only study” |

## Platform and architecture claims

Allowed:

- Name the exact board, SoC, CPU core, documented ISA extensions, clock, core selection, memory placement, build, and runtime.
- Compare observed platform-level results after stating the mismatches that remain.
- Use vendor TRMs/datasheets for chip-specific implementation facts and ISA/ABI specifications for generic rules.
- Describe a mechanism as a candidate interpretation when the implementation fact and artifact evidence are both verified.

Not allowed:

- Attribute a cross-board result solely to Xtensa or RISC-V.
- Treat the optional features of an ISA family as features of the tested core.
- Infer an undocumented pipeline, issue width, latency, predictor, cache policy, or performance counter.
- Use the Xtensa security papers to assert that register-window overflow/underflow occurred in a benchmark unless the build ABI and dynamic event are established.
- Treat ESP32-S3/LX7 or ESP32-C3 evidence as direct evidence for classic ESP32/LX6 or ESP32-C6, respectively.

## Programming-language claims

Every language comparison must name:

- workload and input size;
- source implementation and validation oracle;
- language implementation/runtime and version;
- compiler/interpreter configuration and mode;
- board/SoC, clock, core affinity, and execution environment;
- timed boundary and included/excluded setup work; and
- reported statistic and observation count.

Allowed:

> For the audited CRC-32 kernel and stated timing boundary on the tested ESP32-C6 configuration, implementation X had a lower median elapsed time than implementation Y.

Not allowed:

> Rust is faster than C.

Do not interpret a runtime library call, native extension, interpreter bytecode loop, and compiled source kernel as equivalent implementation work without documenting those differences. A matched native-disassembly comparison applies to compiled C/C++ and Rust artifacts. For MicroPython, identify bytecode, interpreter firmware, and native helper/library calls separately; do not claim an equivalent per-kernel native compilation unless such an artifact actually exists. TinyGo may be discussed as historical Plauska evidence but is out of scope for new implementations and measurements.

## Historical baseline and replication claims

- Historical rows remain published or versioned-source evidence and must never be presented as local observations.
- The Plauska paper reports 100 iterations, while the pinned MicroPython launcher requests five. The production path for the 100-row MicroPython data is unavailable.
- C/C++ and Rust exclude setup/allocation/copy from the timed CRC call; the pinned MicroPython path includes prefix slicing inside its timed call.
- C/C++ and Rust discard one warm-up per size; the pinned MicroPython runner does not.
- Historical “cycle” fields do not share one cross-language hardware-counter semantic.
- The exact Plauska source revision, flashed build configuration, toolchain, ELF, and binary are unavailable. Any locally rebuilt classic-Xtensa ELF/disassembly is a reconstruction under the declared toolchain and configuration, not Plauska's original binary.

Therefore use “reproduction-oriented reconstruction” or “partial replication of the recoverable protocol,” not “exact replication” or “bit-for-bit reproduction.” A Mode A deviation must be recorded before collection and cannot be hidden in analysis.

## Time and cycles

- Elapsed time and cycles are separate metrics.
- Cycles may be reported only from a verified direct counter with documented scope, width, wrap behavior, privilege/access method, and read overhead.
- Never derive cycles from elapsed time multiplied by nominal frequency.
- Record timer overhead, resolution, quantization, warm-up, interruptions, core migration, frequency management, and invalid-observation rules.
- A low or zero sample standard deviation does not by itself prove determinism, jitter-free execution, absence of an OS, or hard real-time behavior.

## Scheduling, interrupts, and multicore

- FreeRTOS, interrupts, task migration, core affinity, and competing work are plausible sources of timing interference.
- Pinning to one core reduces one confounder but does not remove interrupts, RTOS activity, shared-memory/cache effects, timer quantization, or frequency changes.
- Do not generalize the unusually large cross-core values reported by Arm et al. to a different ESP-IDF/FreeRTOS version or benchmark. Use that study to justify control and recording of affinity, task state, and interference.
- Report distributions and invalid observations; do not equate a mean with worst-case execution time.

## Assembly and generated code

Static analysis may report, for a captured artifact:

- code/section size;
- disassembled instruction and compressed-instruction counts;
- calls, branches, loads/stores, and selected instruction classes;
- symbol boundaries and compiler/ABI metadata; and
- visible helper/library calls and stack-frame structure.

Static analysis may not by itself report:

- dynamic instruction count;
- instruction retirement, cycles per instruction, stalls, branch misses, or cache misses;
- register pressure over time;
- executed call depth or register-window spill count; or
- the causal contribution of an instruction class to elapsed time.

Hand interpretation must remain traceable to the exact ELF/disassembly hash. Generated tables must come from scripts and cannot be hand-tuned. Keep native C/C++ and Rust machine-code evidence separate from MicroPython bytecode/interpreter/helper evidence, and label any rebuilt classic-Xtensa artifact as a reconstruction rather than a recovered historical binary.

## Registers and calling conventions

- The Xtensa LX windowed-register mechanism and the RISC-V psABI register convention are architectural/ABI facts, not measured performance effects.
- Verify the actual compiler ABI and ELF before asserting that the historical or new artifact uses a particular convention.
- A static register name occurrence is not a dynamic register-use count.
- Security-countermeasure overheads from register-window papers are workload-specific and cannot be transferred numerically to CRC-32 or other kernels.

## Alignment, cache, and memory

- Hubacz and Trybus establish that access method, width, alignment, compiler, VM, and CPU implementation can change behavior. Their heterogeneous CPDev results are not direct predictions for the proposed native kernels.
- Describe alignment and placement explicitly for every buffer and table whose behavior is interpreted.
- Do not claim a cache effect without a protocol that controls or measures relevant cache state/events.
- A flash-mapped load and an internal-RAM load are different conditions; do not mix them silently.
- RAM and flash figures require named definitions and tools. Static sections, heap high-water marks, stack high-water marks, interpreter firmware, runtime heap, and board partition usage are not interchangeable.

## Energy and power

- Unless a validated setup isolates the CPU rail, supply-side measurements are board-level energy/current/power.
- Report sensor, shunt, calibration, averaging/conversion settings, sample rate, trigger/alignment method, voltage location, idle/background treatment, and uncertainty.
- Do not label board-level energy as ISA energy or CPU energy.
- Very short kernels may be below a monitor’s useful time resolution; batching changes the measured unit and must be defined prospectively.
- Energy results from Lima or Has et al. inform method selection but are not measurements of this project.

## RAM and flash

- Report exactly what the tool counts and whether firmware/runtime/library/shared code is included.
- Compare like with like only. A MicroPython firmware image plus script, an ESP-IDF application image, and a Rust binary have different ownership boundaries.
- Do not convert static linker totals into peak RAM use.
- Preserve raw size-tool output and the exact binary/map hashes.

## Optimization modes

- Mode A is reproduction-oriented and is analyzed only against Mode A/historical evidence.
- B1 CPU/ISA optimization and B2 SoC-specific optimization are separate experimental groups.
- Never merge modes, select the best mode post hoc as the language result, or describe a B1/B2 result as a Plauska reproduction.
- Any optimization must be symmetric where the mode requires symmetry, versioned, and justified before collection.

## Novelty claims

Defensible, once the artifacts and results exist:

> In the focused corpus audited through 8 August 2026, we did not identify a study combining the audited Plauska baseline for C/C++, Rust, and MicroPython, matched ESP32-C6 measurements, versioned compiled C/C++/Rust generated-code evidence and separately bounded MicroPython execution-path evidence, primary-document architectural interpretation, and predeclared reproduction and optimization modes.

Not defensible:

- first Xtensa-versus-RISC-V ESP32 comparison;
- first ESP32-C6 benchmark;
- first ESP32 language comparison;
- first CRC-32 comparison on ESP32;
- first analysis of Xtensa registers, register windows, or alignment; or
- proof that one ISA, architecture family, or language is universally superior.

## Required qualification checklist

Before an empirical claim enters a paper table, abstract, conclusion, or website, verify:

1. Is the evidence local, historical, source-derived, static, or documentary?
2. Are hardware, software, mode, timing boundary, and statistic named?
3. Does the cited source directly support the statement and exact scope?
4. Is a platform observation being mistaken for ISA causality?
5. Is a static property being mistaken for a dynamic metric?
6. Are unlike RAM, flash, cycle, or energy definitions being compared?
7. Are Mode A, B1, and B2 kept separate?
8. Is uncertainty, missing evidence, or a conflict disclosed?
9. Would “consistent with” be more accurate than “caused by”?
10. Does the claim survive the strongest prior-work overlap in `literature/RELATED_WORK_DEEP_REVIEW.md`?
