# Decision 0010 — FFT Mode A authorization

- Date: 2026-08-08
- Status: approved
- Approver: doctor-izba, by explicit instruction to complete the third vertical slice
- Affected protocol: `fft-i16-mode-a-v1.0.0`
- Existing evidence affected: none

## Decision

FFT is authorized as the third Mode A full vertical slice after completed CRC-32
and SHA-256 slices. The implementation must preserve the recovered Plauska
radix-2 complex `int16` fixed-point arithmetic, Q15 twiddle coefficients,
rounding constant, per-butterfly right shift, interleaved complex layout, and
the eight recoverable transform lengths.

The three implementations use one prepared input buffer per condition, one
unmeasured warm-up, 100 measured observations, a frozen pilot-derived batch
count, kernel-only timing, and validation outside the timed interval. No ESP-DSP
library, hardware accelerator, DSP intrinsic, assembly, or other
architecture-specific optimization is allowed in Mode A.

## Consequences

The FFT audit, correctness, timing-pilot, acquisition, artifact-preservation,
validation, MATLAB, historical-context, and static-analysis gates are open.
Mode B, FIR, and IIR remain closed.
