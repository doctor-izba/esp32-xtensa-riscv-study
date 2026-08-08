# Decision 0011 — FIR Mode A authorization

- Date: 2026-08-09
- Status: approved
- Approver: doctor-izba, by explicit instruction to complete the fourth vertical slice
- Affected protocol: `fir-f32-mode-a-v1.0.0`
- Existing evidence affected: none

FIR is authorized after the complete CRC-32, SHA-256, and FFT Mode A slices.
The recovered 256-tap binary32 circular-delay FIR, coefficients, input
conversion, zero state, output order, eight sizes, and `0.0005` absolute
tolerance are frozen. Each language receives one warm-up, 100 accepted samples,
kernel-only timing, and a FIR-specific resolution pilot. No architecture-specific
optimization, DSP library, assembly, hardware acceleration, Mode B, or IIR work
is authorized.
