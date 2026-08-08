# IIR_BQ_F32 Mode A protocol v1.0.0

This is a reproduction-oriented reconstruction of Plauska IIR_BQ_F32, not an
exact reproduction. Authority: Decision 0012.

- Algorithm: one direct-form-II biquad with two delay-state values.
- Coefficients: binary32 `[0.0738017187, 0.1476034373, 0.0738017187,
  -1.2505164146, 0.5457233191]`, interpreted as three feed-forward then two
  feedback coefficients.
- Recurrence, in source order: `d0=x-c3*w0-c4*w1`;
  `y=c0*d0+c1*w0+c2*w1`; then `w1=w0; w0=d0`.
- Input: first `N` shared upstream uint8 values converted before timing as
  binary32 `value * 2.15f`; `N=0,16,32,64,128,256,512,1024` samples.
- State: `[0,0]` before every logical kernel execution; state evolves across
  samples inside that execution and never carries between observations.
- Arithmetic: C++/Rust binary32 preserving expression order; MicroPython
  ordinary floating semantics with identical recurrence order. No saturation.
- Correctness: all outputs within absolute error `0.0005` of the independent
  host binary32 oracle; upstream reference agreement, finite/stability check,
  and negative mutation are mandatory.
- Timing: prepared kernel call only. Allocation, input conversion, state reset,
  GC, validation and serial output remain outside.
- Pilot: power-of-two batching targeting at least 200 us; independent prepared
  state/output per non-empty batched execution. N=0 uses 1024 native or 256
  MicroPython calls.
- Acquisition: one unmeasured warm-up plus 100 accepted samples per condition;
  preserve batch count, whole-batch microseconds, and normalized microseconds.
- Platform: physical ESP32-C6 revision v0.2, 160 MHz, 4 MB DIO flash at 80 MHz;
  sleep, dynamic frequency scaling and radios disabled/not initialized.

Historical limitations match FIR: native common-runner warm-up versus no
checked-in MicroPython warm-up; MicroPython validates only its first 32 outputs;
C allocation uses `calloc` with scalar `delete`; exact historical flashed
binaries and complete run context are unavailable. One historical MicroPython
cycle-counter value overflows negative, but elapsed microseconds remain valid.
