# Decision 0009: use one scheduler tick between SHA-256 observations

- Date: 2026-08-08
- Status: accepted
- Protocol transition: `sha256-mode-a-v1.1.1` to `sha256-mode-a-v1.1.2`

## Evidence and correction

The v1.1.1 C++ capture was rejected because `pdMS_TO_TICKS(1)` evaluates to
zero at the frozen `CONFIG_FREERTOS_HZ=100`; watchdog diagnostics therefore
still interrupted serial rows. No accepted bundle was created.

Use exactly one FreeRTOS tick after each observation's validation/output in
C/C++ and Rust, and the equivalent 10 ms `sleep_ms` in MicroPython. This is
outside the timed interval. The strict main capture is repeated from a new
clean build.

## Impact

Only inter-observation scheduler service changes. The kernel, batching, timer,
inputs, warm-up, iteration count, and timed boundary are unchanged. No accepted
SHA-256 data existed under v1.1.0 or v1.1.1. Both rejected console logs remain
excluded evidence under `data/validation/acquisition_failures/`.
