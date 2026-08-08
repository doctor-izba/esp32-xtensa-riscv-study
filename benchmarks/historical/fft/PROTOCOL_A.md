# FFT_I16 Mode A protocol v1.0.0

This is a reproduction-oriented reconstruction of the Plauska FFT benchmark,
not an exact reproduction. Authority: Decision 0010.

- Kernel: recovered in-place radix-2 DIF complex FFT; no bit reversal.
- Input: the first `2*N` signed-i16 values from vector v1, interleaved real,
  imaginary; `N = 0, 16, 32, 64, 128, 256, 512, 1024` complex samples.
- Arithmetic: Q15 table, `0x7fff` rounding, arithmetic `>>16` at every
  butterfly. C++ and Rust retain i16 storage; MicroPython preserves the
  historical source's Python integer assignments.
- Correctness: every output component must be within 2 of the pinned expected
  component. Preparation, copying, allocation, GC, validation and reporting
  are outside timing.
- Timing: one unmeasured warm-up then 100 accepted samples per size and
  language. `esp_timer_get_time()` (native) and `time.ticks_us()` (MicroPython)
  surround only a batch of already prepared kernel calls. Batch counts are
  selected by the pilot's deterministic resolution rule and frozen before
  acquisition.
- Platform: ESP32-C6 at read-back 160 MHz; dynamic frequency scaling, sleep,
  Wi-Fi, BLE and IEEE 802.15.4 disabled. Record flash size/mode/frequency,
  toolchain versions, image hashes and vector hashes.

Historical limitations: the original native runners warmed up once but the
MicroPython runner did not; local Mode A harmonizes one warm-up. The historical
MicroPython source does not explicitly narrow results to i16. Published
Plauska rows remain descriptive historical evidence, not local samples.
