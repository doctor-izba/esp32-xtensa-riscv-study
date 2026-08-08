# Decision 0003 — CRC-32 feasibility and batching freeze

- Date: 2026-08-08
- Status: approved implementation of Decision 0002 conditions
- Approver: doctor-izba, by the explicit feasibility-and-pilot instruction
- Affected protocol: `crc32-mode-a-v1.1.0`
- Existing performance evidence affected: none

## Context

Decision 0002 opened correctness implementation and required exact physical feasibility plus a timer-resolution pilot before performance acquisition. The approver subsequently requested ESP-IDF v5.5.5 as the mature stable branch where compatible, while retaining all three languages.

## Decision

- C++ uses ESP-IDF v5.5.5 commit `b774170ff46c393eeb5e495ea37936038d3f4f4f` and bundled RISC-V GCC 14.2.0 (`esp-14.2.0_20260121`).
- Rust uses Rust 1.97.1, `rust-src`, explicit `RUSTC_BOOTSTRAP=1` target-standard-library construction, `esp-idf-sys` 0.37.2, `embuild` 0.33.3, `ldproxy` 0.3.5, LLVM/libclang 22.1.8, and ESP-IDF v5.5.5 at the same commit. `Cargo.lock` is normative.
- MicroPython uses the official ESP32_GENERIC_C6 v1.28.0 merged firmware built on ESP-IDF v5.5.1. The merged image SHA-256 is `d338042d2dd87a00dad2163071f44bf67da1401e1d1d0686f2bb2e336e78f0e6`; image inspection reports DIO, 80 MHz, 4 MiB and application compile time 2026-04-06 13:46:37.
- The operations-per-observation values in `benchmarks/historical/crc32/TIMING_PILOT.md` are frozen for the first main acquisition.

The distinct MicroPython IDF patch level is an explicit runtime/toolchain difference. It does not create another experimental mode. ESP-IDF v6.0.2 remains excluded from this protocol because the selected MicroPython release does not support it.

## Alternatives rejected

- Pretending Rust nightly-2026-08-08 succeeded after its `std` failure.
- Retaining `embuild` 0.33.1 after it failed to parse the exact IDF tools manifest.
- Selecting batch counts manually or forcing one count across very different language/runtime durations.
- Treating diagnostic pilot elapsed values as main performance measurements.

## Consequences

- Correctness and timing-resolution gates have passed for all three languages.
- Performance acquisition is permitted prospectively but has not started.
- Batch elapsed time and `operations_per_observation` are raw; normalization is downstream.
- Rust flashing provenance must be corrected from the convenience `espflash` bootloader before main acquisition.
- No prior performance rows exist, so no migration or recollection is required.
