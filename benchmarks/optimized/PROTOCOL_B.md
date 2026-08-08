# Minimal Mode B protocol v1.0.0

Mode B reads the accepted Mode A datasets without modifying them. All native
COMPILER_PERF runs use the same five frozen workload contracts, eight sizes,
one warm-up, existing kernel-only boundary, timer and correctness oracle.
There are 100 accepted observations per size and language.

Profiles:

- mode=B, optimization=COMPILER_PERF, profile=mode-b-compiler-perf-v1
- mode=B, optimization=HW_SHA, profile=mode-b-hw-sha-v1
- mode=B, optimization=RUST_UNCHECKED, profile=mode-b-rust-unchecked-v1

C/C++ uses ESP-IDF v5.5.5 CONFIG_COMPILER_OPTIMIZATION_PERF and must show -O2
in the kernel compile command. Rust uses rustc/cargo 1.97.1 with release
opt-level=3 and must show the effective profile in verbose build evidence.
No fast-math or semantic change is allowed.

The physical context remains ESP32-C6 revision 0.2, 160 MHz, 4 MB DIO flash at
80 MHz, radios off, sleep/dynamic scaling disabled. Exact flashed applications,
hashes, commands, disassemblies and logs are retained under artifacts/builds
and data/raw/esp32-c6/mode_b.

CRC IRAM is not executed: Mode A contains no instruction-fetch/cache
measurement or anomaly that could distinguish an IRAM mechanism.
The Rust FFT unchecked profile was activated only after its exact safe
COMPILER_PERF kernel retained five bounds-panic references. Its frozen
preconditions require a zero-or-power-of-two `n <= 1024`, `data.len() >= 2*n`,
and the generated twiddle table used by the frozen cases. Safe COMPILER_PERF
remains a separately measured profile and is never silently replaced.
