# Decision 0006 — SHA-256 Mode A authorization

- Date: 2026-08-08
- Status: approved
- Approver: doctor-izba, by explicit instruction to complete the second vertical slice
- Affected protocol: `sha256-mode-a-v1.0.0`
- Existing evidence affected: none

## Context

CRC-32 completed the first full vertical slice. The researcher explicitly
authorized SHA-256 as the second slice and prohibited FFT, FIR, IIR, and Mode B.
The pinned Plauska paper/repository were audited before implementation.

## Decision

- Implement equivalent, independently authored software SHA-256 in C/C++, Rust,
  and ordinary MicroPython bytecode.
- Use the eight historical prefixes of the pinned 4,096-byte Plauska vector.
- Time prepared-input `initialize + update + final` only.
- Use one unmeasured warm-up and 100 measured observations per size/language.
- Apply the CRC prospective timer-resolution rule independently to SHA-256;
  do not reuse CRC batch counts without measurement.
- Fix/read back 160 MHz and retain the approved radio, sleep, flash, correctness,
  raw-data, validation, and metadata policies.
- Preserve the exact accepted C++ and Rust native artifacts before acquisition.
- Reject any native build whose benchmark path calls SHA hardware, ROM SHA,
  mbedTLS SHA, or another accelerated/native replacement.

## Consequences

The SHA-256 correctness and pilot gates are open. Main acquisition becomes
permitted only after all three implementations pass the standard and historical
vectors, the pilot freezes batch counts, and native artifact inspection passes.
Mode B and all later workloads remain closed.
