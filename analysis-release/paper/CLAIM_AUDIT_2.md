# Claim Audit 2.0

| Claim | Class | Evidence | Boundary |
|---|---|---|---|
| Mode A contains 12,000 accepted observations | MEASURED | workload processed CSVs and experimental inventory | one board; sequential repetitions |
| Mode B contains 9,600 accepted observations | MEASURED | Mode B processed CSV and inventory | declared profiles only |
| Largest-input medians and ratios | DERIVED | publication MATLAB script and generated tables | ratios inherit source limitations |
| Plauska historical means | PUBLISHED | frozen baseline transcription and cited paper | not local raw samples |
| C6 FIR/IIR call software-FP helpers | MEASURED-BUILD | exact preserved ELF/disassembly reports | static call sites, not dynamic counts |
| Matched Xtensa FIR/IIR emit FP instructions | RECONSTRUCTED | matched reconstruction disassemblies | not Plauska binaries; not executed |
| No matched FFT DSP/MAC instruction appeared | RECONSTRUCTED | audited FFT matched disassembly | absence only in this artifact |
| Rust FFT transform is 22.7% faster | MEASURED + DERIVED | Mode B FFT raw/processed data | whole transformation, not isolated checks |
| C6 HW SHA is 8.70x faster than Mode A software | MEASURED + DERIVED | Mode B SHA raw/processed data | full SoC/API path, not ISA acceleration |
| Software FP plausibly contributes to FIR/IIR direction | INFERRED | exact helpers + reconstructed Xtensa FP + timing direction | contribution not isolated or quantified |
| Results are not pure ISA causal effects | DESIGN LIMIT | unmatched historical/local experiments | central interpretation constraint |

All architecture facts used to bound these claims have atomic records in `docs/verification_ledger.md`. No claim derives cycles from elapsed time and nominal frequency.
