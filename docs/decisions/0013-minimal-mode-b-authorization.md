# Decision 0013 — minimal Mode B authorization and profile freeze

Date: 2026-08-09

The completed Mode A suite is immutable. The researcher authorizes a minimal
Mode B campaign on the same physical ESP32-C6.

The primary profile is COMPILER_PERF: ESP-IDF Optimize for performance for
C/C++ (effective project compile option verified as -O2) and Cargo release
opt-level 3 for Rust. These configurations are language/toolchain-specific,
not equivalent optimization levels. Vectors, algorithms, numeric semantics,
correctness, timing boundaries and device controls remain unchanged.

SHA also receives an independently identified HW_SHA profile. CRC IRAM is
rejected absent cache/fetch measurements or a concrete Mode A fetch anomaly.
Rust FFT unchecked code is permitted only if exact COMPILER_PERF code retains
relevant checks and the safe preconditions can be audited. Fast-math, changed
precision/scaling/coefficients, overclocking and optimization combinations are
excluded.
