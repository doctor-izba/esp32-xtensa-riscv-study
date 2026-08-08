# Decision 0004 — preserve batch elapsed and checked per-call time

- Date: 2026-08-08
- Status: approved by explicit acquisition instruction
- Affected protocol: `crc32-mode-a-v1.1.1`
- Affected schema family: `2.2.0-draft`
- Existing performance evidence affected: none

## Context

The frozen batching policy requires whole-batch elapsed time and the operation
count to remain available. The approver additionally requires every released
observation row to carry the normalized per-call time so the dataset can be
inspected directly without losing the values needed for complete
recalculation.

## Decision

Add required `normalized_execution_us` to measured CRC-32 observation rows.
It is a redundant, deterministic value equal to
`execution_us / operations_per_observation`; it is not an independent timer
reading. `execution_us` continues to mean the untouched whole-batch elapsed
time. Validators recalculate the normalized value and reject disagreement
beyond the recorded nine-decimal-place representation.

This is a schema-interface addition and a protocol clarification. It does not
change batching, timing boundaries, warm-up, inputs, iteration count, mode, or
any accepted pilot result.

## Consequences

- Raw evidence retains batch elapsed time, operation count, and normalized
  time in each row.
- Analysis must be reproducible from the first two values and must verify the
  third before using it.
- No migration or recollection is necessary because main performance
  acquisition had not started.
