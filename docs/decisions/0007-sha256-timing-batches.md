# Decision 0007: freeze SHA-256 Mode A timing batches

- Date: 2026-08-08
- Status: accepted
- Protocol transition: `sha256-mode-a-v1.0.0` to `sha256-mode-a-v1.1.0`

## Decision

Freeze the per-size operation counts measured by the physical timing-resolution
pilot: C/C++ and Rust use `4,4,4,2,1,1,1,1`; MicroPython uses one operation for
all eight sizes. Each main observation records the whole batch duration and
the operation count; normalized time is derived.

## Rationale

The predeclared quantization rule was satisfied at these smallest powers of
two. Native short inputs required batching; every MicroPython invocation was
already far above 100 timer quanta. The rule was evaluated before main data
collection and without reference to desired language ordering.

## Impact

No accepted SHA-256 measurements existed before this decision. It applies
prospectively to the first SHA-256 Mode A dataset. It does not modify CRC-32,
the research questions, Mode A semantics, or any future benchmark gate.
