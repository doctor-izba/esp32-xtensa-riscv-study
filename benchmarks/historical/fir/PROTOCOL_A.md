# FIR_F32 Mode A protocol v1.0.0

This is a reproduction-oriented reconstruction of Plauska FIR_F32, not an exact
reproduction. Authority: Decision 0011.

- Algorithm: 256-tap direct-form FIR with circular zero-initialized delay line.
- Coefficients: frozen 256-value binary32 set recovered from the pinned source;
  a 255th-order band-pass design (`fir1(255,[0.35 0.65])`).
- Input: first `N` shared upstream uint8 values converted before timing as
  binary32 `value * 2.15f`; `N = 0,16,32,64,128,256,512,1024` samples.
- Arithmetic: C++ and Rust binary32 sequential multiply then add; MicroPython
  uses its ordinary floating-number semantics with mathematically equivalent
  source loops. No explicit saturation, fused operation, or state carry between
  measured observations.
- Correctness: every output sample must have absolute error `<= 0.0005` against
  the independent host binary32 oracle. The frozen source reference agrees at
  its checkable points. A mutated-input negative test must fail.
- Boundary: only the FIR kernel over already prepared input/state/output is
  timed. Allocation, conversion, zeroing, GC, validation, and output are outside.
- Pilot: choose a power-of-two batch producing at least 200 us total, subject to
  memory; N=0 uses 1024 native/256 MicroPython. Independent prepared states are
  used for every non-empty batched operation.
- Acquisition: one unmeasured warm-up and 100 accepted samples per condition;
  preserve batch count, whole-batch microseconds, and normalized microseconds.
- Platform: physical ESP32-C6 revision v0.2, 160 MHz, 4 MB DIO flash at 80 MHz;
  power management, sleep, Wi-Fi, BLE and IEEE 802.15.4 disabled/not initialized.

Historical limitations: native runners warm up through the common runner while
the checked-in MicroPython launcher does not; MicroPython validates only 32
outputs because of interpreter memory limits; C uses `calloc` with scalar
`delete`; published aggregates omit exact flashed binaries and full run context.
