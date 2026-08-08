# Decision 0012 — IIR Mode A authorization

- Date: 2026-08-09
- Status: approved
- Approver: doctor-izba, by explicit instruction to complete the fifth vertical slice
- Affected protocol: `iir-bq-f32-mode-a-v1.0.0`
- Existing evidence affected: none

IIR is authorized after CRC-32, SHA-256, FFT, and FIR Mode A. The recovered
single direct-form-II binary32 biquad, coefficients, input conversion, zero
state, source operation order, eight sizes, and absolute tolerance `0.0005` are
frozen. Each language receives one warm-up, 100 accepted samples, kernel-only
timing, and a workload-specific resolution pilot. No operation reordering,
precision change, architecture optimization, DSP library, Mode B, or additional
workload is authorized.
