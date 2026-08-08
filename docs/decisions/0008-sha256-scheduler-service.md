# Decision 0008: service the scheduler between SHA-256 observations

- Date: 2026-08-08
- Status: accepted
- Protocol transition: `sha256-mode-a-v1.1.0` to `sha256-mode-a-v1.1.1`

## Evidence and decision

The first native main capture produced 799 parseable rows. Its preserved
rejected log shows the FreeRTOS task watchdog diagnostic between C++ rows
`(512,87)` and `(512,89)`, specifically reporting that the idle task had not
run. No raw bundle was accepted.

Add a 1 ms scheduler-service delay after each completed observation's
validation and output in C/C++, Rust, and MicroPython. The delay is outside the
timed kernel interval. Apply it prospectively and rebuild native artifacts.

## Impact

The timing boundary, batching, inputs, algorithm, and correctness rules do not
change. No accepted SHA-256 evidence is invalidated because none existed. The
rejected console remains under `data/validation/acquisition_failures/` and is
excluded from processing.
