# Research Questions

## Main questions

### RQ1 — Architecture and workloads

> How do the fundamental low-level architectural differences between the Xtensa LX6 used in the original ESP32 and the RISC-V core of the ESP32-C6 manifest themselves in real computational workloads?

### RQ2 — Language/runtime evolution

> How have the performance characteristics of C/C++, Rust, and MicroPython changed when moving from the original Xtensa-based ESP32 platform to the modern RISC-V ESP32-C6 platform?

## Operational subquestions

| ID | Question | Primary evidence | Metrics/observables | Applicable modes | Permitted inference |
|---|---|---|---|---|---|
| RQ1a | Which documented architectural, ABI, core, and memory-system features differ? | Primary manuals, ISA/ABI specifications, compiler target records | Registers, instruction forms, extensions, pipeline, caches, memory map, FPU/DSP, interrupts, counters/trace | Background; all modes | Factual comparison limited to verified configurations |
| RQ1b | How does equivalent C/C++ compile into Xtensa and RISC-V machine code? | Pinned compiler outputs, ELF files, disassembly, link maps | Instruction count/bytes, loads, stores, branches, calls, stack accesses, spills, helpers, loop structure | A first; B separately | Static code-generation differences, not measured runtime behavior |
| RQ1c | How does each Set A workload behave on the measured ESP32-C6? | Validated local iteration data | Time distribution, cycles when reliable, code/RAM size, memory metrics | A | Statements about the tested C6 configuration only |
| RQ1d | Are workload observations consistent with verified mechanisms? | Joint interpretation of RQ1a–c | Pattern-to-mechanism mapping with alternatives | A, then B | Qualified consistency claims; no single-cause attribution |
| RQ2a | How do C/C++, Rust, and MicroPython compare within the same C6 protocol? | Local builds and runs sharing vectors and boundaries | Timing distribution, sizes, memory, correctness, assembly where applicable | A | Within-C6 language/runtime comparison, with toolchain caveats |
| RQ2b | How do those within-platform patterns differ from the published Plauska study? | Local Mode A data plus explicitly published baseline evidence | Ratios/differences with uncertainty and provenance | A only | Historical cross-study comparison, not a controlled language-version effect |
| ERQ1 | What benefit is available from documented optimization? | Paired A and B implementations on C6, grouped by explicit optimization metadata | Time, cycles, code/RAM, assembly, and platform metrics where defined | B | Optimization effect on the tested C6 configuration; no cross-profile pooling |
| ERQ2 | What additional benefit is available from dedicated SoC facilities? | Paired A and B implementations using an explicitly recorded hardware-acceleration profile | Throughput, latency, board-level energy, setup cost | B | Full-platform result; not CPU/ISA performance |

## Units of analysis

- **Observation:** one recorded timed invocation for one input condition.
- **Run:** one acquisition session with one firmware/build/protocol/hardware context and many observations.
- **Independent replicate:** a separately initialized run, not merely another loop iteration in the same run.
- **Build:** one language/toolchain/configuration artifact set.
- **Function/object:** the unit for static assembly analysis.
- **Historical datum:** a published aggregate or an upstream recorded row with its own evidence origin.

The original 100 iterations are repeated observations within a run. They are not automatically 100 independent experimental replicates.

## Comparisons that are not valid

- `ESP32-C6 time / published ESP32 time` does not isolate RISC-V versus Xtensa.
- Static instruction count is not a cycle count.
- Nominal frequency multiplied by elapsed time is not a measured cycle counter.
- A Mode B hardware-accelerated SHA result is not comparable to a Mode A software SHA result.
- Historical published aggregates must not be expanded into invented per-iteration rows.
- MicroPython results cannot be interpreted without the exact firmware, interpreter configuration, garbage-collection policy, and timing primitive.

## Hypotheses

No directional hypotheses are preregistered in the foundation phase. Any confirmatory hypothesis must be written and versioned before viewing the corresponding local performance results. Exploratory findings will be labeled exploratory.
