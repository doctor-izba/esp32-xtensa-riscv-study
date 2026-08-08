# Decision 0001 — Two-mode experimental design

- Date: 2026-08-08
- Status: approved
- Approver: doctor-izba, by explicit research instruction
- Affected methodology: `0.2.0-two-mode-design`
- Affected schema family: `2.0.0-draft`

## Context

The foundation separated fair reproduction, CPU/ISA optimization, and full-SoC optimization as A, B1, and B2. That split added labels without improving the primary comparison and risked treating low-level analysis as another experiment family.

## Decision

There are exactly two experimental modes:

- **Mode A — fair/reproduction-oriented:** a reconstruction and ESP32-C6 extension of the recoverable Plauska workload contract. C/C++, Rust, and MicroPython share input, sizes, correctness, iteration, warm-up, preparation, and timing rules. Historical inconsistencies are limitations, not another mode. Mode A does not use architecture- or C6-specific optimization or hardware acceleration.
- **Mode B — optimized:** any predeclared compiler, placement, layout, RISC-V, intrinsic, assembly, peripheral, DMA, or hardware-accelerator optimization. Every enabled optimization is explicit in metadata and CSV. There are no B1/B2 submodes.

Generated-code and architectural evidence are analysis layers for Mode A and Mode B, not experimental modes.

The first-paper primary suite remains CRC-32, SHA-256, FFT, FIR, and IIR. AI/TinyML, Zig, mruby, WebAssembly, BlueScript, other runtimes/languages, and additional microbenchmark suites remain Future Work.

## Alternatives rejected

- A separate `A-Historical` mode to emulate inconsistent historical MicroPython boundaries.
- Separate B1 CPU/ISA and B2 full-SoC labels.
- A low-level architecture experimental mode.
- Expanding the first-paper suite before the five historical workloads are complete.

## Consequences and impact

- `benchmark_mode` changes incompatibly from `A|B1|B2` to `A|B`; the draft schema therefore advances from family 1 to family 2.
- Mode B profiles remain distinguishable through required `optimization_profile_id` and `optimization` fields rather than submode names.
- Research-question wording is unchanged; only applicable-mode labels and optimization evidence descriptions are updated.
- No local result rows or frozen raw evidence exist, so no migration or recollection is required.
- The change is prospective. Historical Plauska evidence remains separate baseline evidence.
- The CRC-32 implementation gate remains closed. This decision does not approve the proposed CRC protocol or any implementation.
