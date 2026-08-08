# CRC-32 Mode A Protocol

- Protocol ID: `crc32-mode-a-v1.0.0-proposed`
- Vector set ID: `crc32-plauska-v1`
- Status: proposed; methodological approval required
- Implementation gate: closed
- Applies to: ESP32-C6 C/C++, Rust, and MicroPython Mode A

This is the minimum correctness and timing contract needed before implementation. It is a reproduction-oriented reconstruction/extension of the recoverable Plauska CRC-32 method, not an exact reproduction. Approval of this document must be recorded before benchmark source is written.

## 1. Algorithm

Use the table-driven, byte-at-a-time reflected **CRC-32/ISO-HDLC** form recovered from the pinned Plauska source:

| Parameter | Value |
|---|---|
| Width | 32 bits |
| Normal polynomial | `0x04c11db7` |
| Reflected polynomial | `0xedb88320` |
| Initial register | `0xffffffff` |
| Input/reflection | LSB-first reflected byte processing |
| Final XOR | `0xffffffff` (final complement) |
| Output | Unsigned 32-bit numeric value |
| Standard check | ASCII `123456789` gives `0xcbf43926` |

Mode A uses one 256-entry table created before timing. It must not call an ESP32-C6 CRC peripheral, ROM CRC helper, architecture-specific intrinsic, or alternative optimized CRC library.

## 2. Canonical input and expected outputs

The canonical source is the exact 4,096-byte `DATA` array at Plauska repository commit `c42dba0d41d547960b73e63b3d4e09917d61e171`. Its byte-level SHA-256 is:

```text
5b6d630c1c5693224e1d31416b495146cace11da0c296c82f11e9024fd36f121
```

The timed conditions use these prefixes, in ascending order:

| Bytes | Prefix SHA-256 | Expected CRC-32 |
|---:|---|---|
| 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `0x00000000` |
| 16 | `a2fdd25f8fce58f6829a03edc73e6cd70ec5b60c1cf82452e9cced47b954f91c` | `0x9ce7b8fc` |
| 32 | `0e87ba53cd4e8ecd23758be6b08d45f1a80d86a47470c8cc64935b72a407e446` | `0xf8550f72` |
| 64 | `ff550705bc14ed52dbcb1df67df0b13a2bbdc316e280ed126a503faca2a4933e` | `0x9a28b34d` |
| 128 | `7dfae2c397ae32f77c5a83710bb75c3db31ff45dc58eecd3f2753647f23edf23` | `0x56fc5282` |
| 256 | `d7823ab54d20a252f68a0205c313a2aeadeb275da047ea20a13695ca12af07fc` | `0x632f02de` |
| 512 | `4af3313f32f27ae2539ab285e0c8d89b7e7e8bfb84b94286992b5dcba9c3fb09` | `0x83c03459` |
| 1024 | `7e2cbd238a7863e9e57d72535cb7101cce7402690ecad6f90efd331161b0cad7` | `0x6d7fa5f0` |

The full vector hash and all expected values were independently checked with Python 3.14.4 `zlib.crc32`; the standard check vector was also confirmed. The upstream RNG/generator and seed are unknown, so the bytes must be preserved and never regenerated. The byte array is not vendored until its redistribution status is resolved; acquisition must use the pinned source and must fail if the full-vector hash differs.

## 3. Iterations and warm-up

For every language and input size:

1. prepare the table and input view;
2. perform exactly **one unmeasured warm-up** kernel invocation;
3. perform exactly **100 measured invocations**;
4. validate every returned value after its timed interval.

Warm-up output must pass correctness. It is represented in metadata as `warmup_iterations=1`, not as a measured row. The number of separately initialized acquisition runs will be chosen after the timer/variance pilot and frozen before the main collection; this does not change the 100 measured invocations per condition.

## 4. Timing boundary and timer

The timed boundary contains only one CRC kernel call over an already prepared contiguous prefix/view and the minimum timer-call overhead surrounding it.

Outside timing: table construction, imports/startup, allocation, prefix copying or slicing, view construction, garbage collection, validation, serial output, and cleanup. MicroPython must therefore create its prefix view before the start timestamp. Compiled builds must consume the result so the compiler cannot remove the call.

Primary elapsed-time primitives:

| Implementation | Primitive |
|---|---|
| C/C++ | `esp_timer_get_time()` before and after the kernel |
| Rust | the same ESP-IDF `esp_timer_get_time()` primitive through pinned bindings |
| MicroPython | `time.ticks_us()` with wrap-safe `time.ticks_diff()` |

The primary stored metric is integer microseconds. These are equivalent monotonic microsecond semantics, not an assertion that the three call paths have identical overhead. Timer resolution and paired empty-boundary overhead are characterized in the pilot and recorded without subtracting overhead from observations. No cross-language cycle metric is part of this minimum Mode A CRC protocol; cycles may be added only by a separately approved, directly measured counter protocol.

## 5. Device state

- CPU frequency: **160,000,000 Hz**, configured and read back before acquisition.
- Dynamic frequency scaling and automatic light sleep: disabled.
- Wi-Fi, Bluetooth LE, and IEEE 802.15.4: disabled and their application stacks not started.
- Execution: ESP32-C6 single high-performance core; exact task priority, scheduler configuration, board identity, chip revision, and flash readback must be captured in `run.csv` before a run is valid.
- MicroPython: run `gc.collect()` before the warm-up for each input condition; do not force collection inside the warm-up/measured sequence. Record the GC policy.

## 6. Correctness gate

- Verify the canonical file SHA-256 before build or execution.
- Verify `123456789 -> 0xcbf43926` and all eight prefix values with an independent host oracle.
- Require exact unsigned 32-bit equality for the warm-up and every measured invocation.
- Run a correctness-only negative test showing that a one-byte mutation is rejected; it is not a timed condition.
- Any mismatch invalidates the build/run for performance analysis. Timing remains disabled until all three implementations pass the correctness-only gate.

## 7. Mode A build/toolchain proposal

All dependencies, commits, locks, flags, firmware images, and complete version outputs must be captured. The proposed common SDK base is ESP-IDF 5.5.1 because it supports ESP32-C6 and is supported by the proposed MicroPython release.

| Path | Proposed exact pin | Mode A build profile |
|---|---|---|
| C/C++ | ESP-IDF `v5.5.1`; bundled `riscv32-esp-elf` package `esp-14.2.0_20241119` | `-Os`; LTO off; no target-specific tuning beyond the SDK's required ESP32-C6 target; software CRC only |
| Rust | Rust toolchain `1.97.1`; `esp-idf-sys` `0.37.2`; ESP-IDF `v5.5.1`; target `riscv32imac-esp-espidf` | `opt-level="z"`; LTO off; software CRC only; dependency lock required |
| MicroPython | source tag `v1.28.0`; board `ESP32_GENERIC_C6`; ESP-IDF `v5.5.1` | ordinary bytecode/interpreter path; no native/viper decorator or native CRC helper |

These are protocol pins, not claims that the tools are installed. Before implementation, a feasibility capture must verify the exact release commits, compiler/linker/version outputs, target, configuration, and dependency locks. A failed feasibility check requires a new protocol proposal; it must not be silently replaced with a newer tool.

## 8. Required CSV values and fields

Use results schema family `2.0.0` after it is frozen. `run.csv` must include all normative fields, with at least these protocol values:

```text
suite=historical
benchmark_id=crc32
protocol_id=crc32-mode-a-v1.0.0
benchmark_mode=A
optimization_profile_id=mode-a-size-profile-v1
optimization=none
test_vector_set_id=crc32-plauska-v1
test_vector_sha256=5b6d630c1c5693224e1d31416b495146cace11da0c296c82f11e9024fd36f121
timing_scope=crc32-kernel-only-v1
warmup_iterations=1
planned_iterations=100
cpu_frequency_hz=160000000
radio_state=wifi_off;ble_off;ieee802154_off
```

It also records implementation/language/runtime/compiler/SDK versions, target, complete flags, repository/build/firmware hashes, board/chip/flash identity, timer and measured resolution, power/scheduler/GC state, host/capture tool, and timestamps.

Each `observations.csv` measured row records `input_id`, byte size, iteration 1–100, `phase=measured`, `execution_us`, `result_kind=crc32_u32_hex`, actual and expected values, correctness, and measurement status. There is one row per invocation; setup and validation are not separate timed rows.

## 9. Known Plauska limitations

- The paper/released CSV contain 100 MicroPython rows per size, but the pinned launcher requests five; the production path for 100 is unavailable.
- C/C++ and Rust make one discarded warm-up call per size; pinned MicroPython does not.
- C/C++ and Rust exclude prefix preparation; pinned MicroPython includes slice allocation/copy inside timing.
- Historical cycle fields do not share one cross-language counter semantic, and C/Rust time/cycle reads do not share identical instruction boundaries.
- The input bytes are recoverable, but their RNG/generator/seed are unknown.
- Historical build, firmware, affinity, radio, interrupt, board-instance, and exact toolchain provenance are incomplete.
- The upstream C++ cleanup mismatches allocation/deallocation outside timing and is undefined behavior; Mode A will not reproduce it.

These limitations are disclosed against the published historical baseline. They do not create `A-Historical` or any other experimental mode.

## 10. Approval boundary

Approval must cover the harmonized one-warm-up policy, kernel-only timing boundary, equivalent timer choice, 160 MHz/radios-off device state, 100-iteration policy, canonical vector/outputs, and proposed toolchain pins. Approval opens only the correctness-first implementation step; timing still remains gated on correctness.
