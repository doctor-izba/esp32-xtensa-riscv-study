# SHA-256 Mode A protocol

- Protocol ID: `sha256-mode-a-v1.1.2`
- Vector set: `sha256-plauska-v1`
- Status: frozen; correctness and physical timing pilot passed 2026-08-08
- Mode: A, software only

## Algorithm and semantic boundary

Use standard SHA-256 with 512-bit blocks, eight 32-bit state words, the standard
64 constants, 64 expanded schedule words, standard padding with a 64-bit
big-endian bit length, and a 32-byte big-endian digest. Arithmetic is modulo
2^32. The timed kernel is one complete digest operation over a prepared
contiguous prefix: context initialization, update, and finalization.

Allocation, input copying/slicing, imports, GC preparation, validation, output,
and cleanup are outside time. The implementation must be direct software code.
ESP SHA peripherals, ROM SHA helpers, mbedTLS SHA paths, `hashlib`, and native
MicroPython emitters are prohibited in Mode A.

## Inputs and correctness

Use byte prefixes of the pinned Plauska 4,096-byte `DATA` vector. Full-vector
SHA-256: `5b6d630c1c5693224e1d31416b495146cace11da0c296c82f11e9024fd36f121`.
The upstream generator and seed are unknown; bytes are acquired from the pinned
commit and never regenerated.

| Bytes | Expected SHA-256 digest |
|---:|---|
| 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 16 | `a2fdd25f8fce58f6829a03edc73e6cd70ec5b60c1cf82452e9cced47b954f91c` |
| 32 | `0e87ba53cd4e8ecd23758be6b08d45f1a80d86a47470c8cc64935b72a407e446` |
| 64 | `ff550705bc14ed52dbcb1df67df0b13a2bbdc316e280ed126a503faca2a4933e` |
| 128 | `7dfae2c397ae32f77c5a83710bb75c3db31ff45dc58eecd3f2753647f23edf23` |
| 256 | `d7823ab54d20a252f68a0205c313a2aeadeb275da047ea20a13695ca12af07fc` |
| 512 | `4af3313f32f27ae2539ab285e0c8d89b7e7e8bfb84b94286992b5dcba9c3fb09` |
| 1024 | `7e2cbd238a7863e9e57d72535cb7101cce7402690ecad6f90efd331161b0cad7` |

The standard vector ASCII `abc` must produce
`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.
All expected values require two independent host oracle implementations. A
one-bit mutation must fail the frozen 16-byte expected digest. Every device
warm-up and measured batch must produce the exact expected digest.

## Iteration and pilot policy

For every language and size: prepare input, perform one unmeasured warm-up, then
100 measured observations. A measured observation contains a deterministic
number of repeated complete SHA-256 operations.

The pilot first tests one operation over 100 intervals. It measures timer-call
overhead and minimum positive resolution. One operation is accepted only when
at least 99 intervals are nonzero and the median is at least 100 observed timer
quanta. Otherwise choose the smallest power of two satisfying both conditions.
The rule is applied independently to each language/size and frozen before main
collection. Whole-batch microseconds and operation count are raw; normalized
time is derived as their quotient to nine decimal places.

The physical pilot froze these operation counts prospectively for the main
dataset. They are part of protocol v1.1.0 and must not be changed within an
accepted run:

| Bytes | C/C++ | Rust | MicroPython |
|---:|---:|---:|---:|
| 0 | 4 | 4 | 1 |
| 16 | 4 | 4 | 1 |
| 32 | 4 | 4 | 1 |
| 64 | 2 | 2 | 1 |
| 128 | 1 | 1 | 1 |
| 256 | 1 | 1 | 1 |
| 512 | 1 | 1 | 1 |
| 1024 | 1 | 1 | 1 |

Observed timer quanta were 1 us for native `esp_timer_get_time()` and 6--7 us
for MicroPython `ticks_us()`. The selection medians and pilot evidence are
recorded in `TIMING_PILOT.md`. The pilot does not enter the performance
dataset.

After validation/output for each observation, every language performs one
FreeRTOS scheduler tick (10 ms at the frozen 100 Hz tick rate) of service delay.
This pause is outside the timed interval and prevents
long native serial runs from starving the FreeRTOS idle task. It is not part of
`total_batch_time_us` or normalized execution time.

Timers are `esp_timer_get_time()` for C/C++ and Rust, and wrap-safe
`time.ticks_us()`/`time.ticks_diff()` for MicroPython. No timer overhead is
subtracted. No cross-language cycle comparison is required.

## Device and toolchains

- ESP32-C6 revision v0.2 on the DoIT ESPC6-32 N4 relay carrier;
- CPU configured/read back at 160 MHz; dynamic frequency scaling and sleep off;
- Wi-Fi, BLE, and IEEE 802.15.4 stacks not started;
- 4 MiB flash, DIO, 80 MHz;
- C/C++: ESP-IDF v5.5.5/GCC 14.2.0, `-Os`, LTO off;
- Rust: Rust 1.97.1, `esp-idf-sys` 0.37.2, ESP-IDF v5.5.5,
  `riscv32imac-esp-espidf`, `opt-level=z`, LTO off;
- MicroPython: official ESP32_GENERIC_C6 v1.28.0, ordinary bytecode.

Exact versions, flags, source commit, firmware hashes, locks, configuration,
flash state, scheduler, GC, host, and capture metadata are mandatory.

## Artifact and acceptance gates

Before each native main run preserve and hash the exact ELF, application image,
map/link information, useful object, sdkconfig or Cargo configuration/lock,
compiler version, disassembly, symbols, and section sizes. Inspect the exact
benchmark call graph/symbols for forbidden hardware/ROM/mbedTLS SHA paths.

A raw run is accepted only when its bounded serial segment contains exactly 800
unique observations, all expected warm-ups and summaries, frozen batch counts,
positive elapsed times, exact digests, correct hardware metadata, and immutable
manifest coverage. Invalid runs remain retained and are excluded by validation.

## Historical limitations

The source/CSV iteration conflict, asymmetric warm-up, MicroPython timed slice,
latent non-historical-size padding defects, missing exact historical binaries,
and incomplete build/device state are documented in `SHA256_AUDIT.md`. They do
not create another mode. Cross-platform results are descriptive only.
