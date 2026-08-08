# Decision 0002 — CRC-32 Mode A protocol approval

- Date: 2026-08-08
- Status: approved
- Approver: doctor-izba, by explicit research instruction
- Affected protocol: `crc32-mode-a-v1.1.0`
- Affected schema family: `2.1.0-draft`

## Context

Decision 0001 left the CRC-32 implementation gate closed. The proposed protocol specified CRC-32/ISO-HDLC, the audited Plauska vector, eight historical prefix sizes, a harmonized warm-up and timing boundary, 100 measured observations, and a fixed 160 MHz/radios-off ESP32-C6 state. The approver accepted those choices and required a timer-resolution pilot before final performance acquisition.

The physical test device was then identified as a DoIT ESPC6-32 N4 module on an `ESP32-C6_Relay_X1_V1.1` carrier. Read-only and erase-tool interrogation identified an ESP32-C6 revision v0.2, a 40 MHz crystal, and 4 MiB flash. Secure Boot and Flash Encryption were disabled. The old test firmware was erased with the approver's explicit permission.

## Decision

The CRC-32 correctness implementation gate is open for C/C++, Rust, and MicroPython.

The following conditions are approved:

- CRC-32/ISO-HDLC and vector set `crc32-plauska-v1`, including the eight frozen prefix outputs;
- one unmeasured warm-up followed by 100 measured observations per size;
- a prepared kernel-only timing boundary, with allocation, slicing, table construction, GC preparation, validation, and output outside timing;
- fixed and read-back 160 MHz operation, with dynamic frequency scaling, sleep, Wi-Fi, BLE, and IEEE 802.15.4 disabled;
- no required cross-language cycle comparison in the initial CRC protocol;
- exact flash size, flash mode, and flash frequency captured where available;
- exact toolchain versions/configurations frozen only after physical feasibility is demonstrated.

Before performance timing is enabled, all three correctness implementations must pass. The timer pilot must measure timer-call overhead and empirical resolution and test the shortest CRC conditions. Single-kernel observations remain the default. If quantization is material, the protocol uses repeated kernels in one interval and records `operations_per_observation`; elapsed time is divided only in downstream analysis.

The prospective batching selection rule is independent of the measured performance ranking: for each language/input-size condition, use one operation when at least 99 of 100 pilot intervals are non-zero and the median interval is at least 100 empirically observed timer quanta. Otherwise choose the smallest power-of-two operation count that meets both criteria. The same rule applies to every language and size. The selected counts are frozen before main acquisition and may not be tuned to improve a result.

## Toolchain compatibility decision

ESP-IDF v5.5.5 is the preferred mature 5.5 bugfix release for C/C++ and the first feasibility candidate for Rust. ESP-IDF v6.0.2 is not the common project base because the selected MicroPython v1.28.0 release documents ESP-IDF support only through v5.5.1. MicroPython therefore remains on its supported v5.5.1 base unless a separately documented feasibility result establishes another supported exact build.

Different language toolchains may consequently use different SDK patch releases. This is a recorded runtime/toolchain difference, not an experimental-mode difference. Exact commits, compilers, configs, dependency locks, and firmware hashes remain mandatory. Any failed feasibility check remains evidence and requires an explicit prospective protocol/toolchain amendment; no silent fallback is allowed.

## Energy-measurement boundary

The available KWS-V20 USB meter and unmodified relay carrier cannot isolate the module 3.3 V rail. Its readings include carrier regulator loss, LEDs, USB circuitry, relay-driver circuitry, and background loads. They can support only coarse, long-window board-input measurements. They cannot be reported as ESP32-C6 chip, core, ISA, or module-only energy. No software dashboard can remove unmeasured carrier current.

Without buying hardware or modifying the board to insert a validated sensor/shunt in an isolated supply rail, exact module-only energy is unavailable. This limitation does not block CRC timing/correctness work. Any later KWS-V20 experiment must remain explicitly board-level and follow the existing energy-window schema.

## Consequences and impact

- CRC-32 correctness source may now be implemented.
- Performance timing remains gated until three-language correctness and the timing pilot pass.
- The approved protocol advances from proposed v1.0.0 to approved v1.1.0.
- Flash configuration fields are added prospectively to the draft run schema.
- There are no existing local result rows to migrate or recollect.
- SHA-256 and all later benchmarks remain closed.
