# CRC-32 Mode A Protocol

- Protocol ID: `crc32-mode-a-v1.1.1`
- Vector set ID: `crc32-plauska-v1`
- Status: approved by Decision 0002
- Correctness implementation gate: open
- Performance timing gate: passed by Decision 0003; first main acquisition complete
- Applies to: ESP32-C6 C/C++, Rust, and MicroPython Mode A

This is the minimum correctness and timing contract for implementation. It is a reproduction-oriented reconstruction/extension of the recoverable Plauska CRC-32 method, not an exact reproduction. Approval and the timing refinement are recorded in `docs/decisions/0002-crc32-mode-a-protocol-approval.md`.

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

The timed boundary contains only the approved number of repeated CRC kernel calls over an already prepared contiguous prefix/view and the minimum timer-call overhead surrounding the batch. Single-kernel timing remains the default until the pilot demonstrates that batching is required.

Outside timing: table construction, imports/startup, allocation, prefix copying or slicing, view construction, garbage collection, validation, serial output, and cleanup. MicroPython must therefore create its prefix view before the start timestamp. Compiled builds must consume the result so the compiler cannot remove the call.

Primary elapsed-time primitives:

| Implementation | Primitive |
|---|---|
| C/C++ | `esp_timer_get_time()` before and after the kernel |
| Rust | the same ESP-IDF `esp_timer_get_time()` primitive through pinned bindings |
| MicroPython | `time.ticks_us()` with wrap-safe `time.ticks_diff()` |

The primary stored metric is integer microseconds. These are equivalent monotonic microsecond semantics, not an assertion that the three call paths have identical overhead. Timer resolution and paired empty-boundary overhead are characterized in the pilot and recorded without subtracting overhead from observations. No cross-language cycle metric is part of this minimum Mode A CRC protocol; cycles may be added only by a separately approved, directly measured counter protocol.

For each language/input-size condition, the pilot first tests `operations_per_observation=1` over 100 diagnostic intervals. Single-kernel timing is accepted only if at least 99 intervals are non-zero and the median is at least 100 empirically observed timer quanta. Otherwise use the smallest power-of-two operation count meeting both criteria. This prospective rule is applied to every language and size; counts are frozen before main acquisition and are never selected to improve a ranking. A batched observation returns the result of every kernel execution to a consuming accumulator, validates outside timing, records the batch count, and leaves per-operation division to downstream analysis.

## 5. Device state

- CPU frequency: **160,000,000 Hz**, configured and read back before acquisition.
- Dynamic frequency scaling and automatic light sleep: disabled.
- Wi-Fi, Bluetooth LE, and IEEE 802.15.4: disabled and their application stacks not started.
- Execution: ESP32-C6 single high-performance core; exact task priority, scheduler configuration, board identity, chip revision, flash size, flash mode, and flash frequency readback must be captured in `run.csv` before a run is valid.
- MicroPython: run `gc.collect()` before the warm-up for each input condition; do not force collection inside the warm-up/measured sequence. Record the GC policy.

## 6. Correctness gate

- Verify the canonical file SHA-256 before build or execution.
- Verify `123456789 -> 0xcbf43926` and all eight prefix values with an independent host oracle.
- Require exact unsigned 32-bit equality for the warm-up and every measured invocation.
- Run a correctness-only negative test showing that a one-byte mutation is rejected; it is not a timed condition.
- Any mismatch invalidates the build/run for performance analysis. Timing remains disabled until all three implementations pass the correctness-only gate.

## 7. Mode A build/toolchain feasibility pins

All dependencies, commits, locks, flags, firmware images, and complete version outputs must be captured. Exact pins are frozen after the approved physical feasibility checks; different language SDK patch releases are recorded as toolchain differences, not silently normalized.

| Path | Feasibility pin | Mode A build profile |
|---|---|---|
| C/C++ | ESP-IDF `v5.5.5` commit `b774170ff46c393eeb5e495ea37936038d3f4f4f`; GCC 14.2.0 package `esp-14.2.0_20260121` | `-Os`; LTO off; no target-specific tuning beyond the SDK's required ESP32-C6 target; software CRC only |
| Rust | Rust `1.97.1` plus `rust-src` and explicit bootstrap `build-std`; `esp-idf-sys` `0.37.2`; `embuild` `0.33.3`; ESP-IDF `v5.5.5` at the same commit; target `riscv32imac-esp-espidf` | `opt-level="z"`; LTO off; software CRC only; committed dependency lock required |
| MicroPython | official `ESP32_GENERIC_C6` firmware `v1.28.0`, SHA-256 `d338042d2dd87a00dad2163071f44bf67da1401e1d1d0686f2bb2e336e78f0e6`; built on ESP-IDF `v5.5.1` | ordinary bytecode/interpreter path; no native/viper decorator or native CRC helper |

ESP-IDF v6.0.2 is not a common-base candidate because MicroPython v1.28.0 documents support only through ESP-IDF v5.5.1. Feasibility details and retained failures are in `TOOLCHAIN_FEASIBILITY.md`; Decision 0003 records the prospective substitutions made before accepted timing. Rust main acquisition must use exact flashed build artifacts rather than the convenience bootloader supplied by `espflash` during feasibility testing.

## 7.1 Frozen batching result

The completed pilot froze these `operations_per_observation` values:

| Bytes | C/C++ | Rust | MicroPython |
|---:|---:|---:|---:|
| 0 | 1024 | 512 | 64 |
| 16 | 64 | 128 | 2 |
| 32 | 32 | 64 | 1 |
| 64 | 16 | 32 | 1 |
| 128 | 8 | 16 | 1 |
| 256 | 4 | 8 | 1 |
| 512 | 2 | 4 | 1 |
| 1024 | 1 | 2 | 1 |

The diagnostic observations and timer characterization are recorded in `TIMING_PILOT.md`. Main acquisition preserves whole-batch elapsed time and operation count. It also stores a checked, redundant per-operation value without replacing either raw input to that calculation.

## 8. Required CSV values and fields

Use results schema family `2.2.0`. `run.csv` must include all normative fields, with at least these protocol values:

```text
suite=historical
benchmark_id=crc32
protocol_id=crc32-mode-a-v1.1.1
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

Each `observations.csv` measured row records `input_id`, byte size, iteration 1–100, `phase=measured`, `operations_per_observation`, whole-batch elapsed `execution_us`, checked `normalized_execution_us`, `result_kind=crc32_u32_hex`, actual and expected values, correctness, and measurement status. There is one row per timed observation; setup and validation are not separate timed rows. `normalized_execution_us` is serialized to nine decimal places, must equal `execution_us / operations_per_observation`, and never overwrites either source value.

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

Decision 0002 approved the harmonized one-warm-up policy, kernel-only timing boundary, equivalent timer choice, 160 MHz/radios-off device state, 100-observation policy, canonical vector/outputs, feasibility-gated toolchains, flash metadata, and prospective quantization rule. Decision 0003 records successful three-language correctness, exact feasible toolchains, timer characterization, and frozen batching. Decision 0004 adds the checked normalized-time column while retaining the two raw batch values. The first main acquisition is complete under this protocol: accepted runs are `d9af8172-54f9-4ca9-86a6-cbfcdd21bbf7` (C++), `00b4308f-3f3e-49bf-afd0-455bbc17b1a4` (Rust), and `237f262c-cb1d-47ee-8fb5-9efe0d08b69f` (MicroPython). Decision 0005 preserves and excludes the superseded MicroPython run with inaccurate GC metadata.
