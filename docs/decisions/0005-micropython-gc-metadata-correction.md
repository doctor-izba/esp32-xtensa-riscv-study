# Decision 0005 — reject and recollect inaccurate MicroPython GC metadata

- Date: 2026-08-08
- Status: applied acquisition correction
- Affected protocol: `crc32-mode-a-v1.1.1` (no protocol change)
- Affected run: `20f7c618-c339-477b-887c-9ba96adc0e2d`

## Context

The first otherwise complete MicroPython acquisition encoded its `gc_policy`
as `disabled inside timed interval`. The program called `gc.collect()` once
before each condition and did not force collection during the warm-up or 100
measured observations, but it never called an API that disables automatic
garbage collection. The metadata therefore overstated the controlled state.

## Decision

Preserve the raw run and its manifest, mark it rejected for analysis, and
perform one prospective recollection with identical firmware, kernel, vector,
batch counts, warm-up, timing boundary, device state, and iteration count.
The corrected metadata is:

```text
gc.collect before each prepared input condition;automatic GC not disabled;no forced collection inside timed interval
```

The validator now requires this exact statement for MicroPython. C++ and Rust
runs are unaffected.

## Consequences

- No measurement row is edited or silently discarded.
- The original MicroPython run remains evidence of the acquisition incident
  but is excluded from processed data and figures.
- Rare MicroPython pauses remain valid observations in the replacement run;
  no claim assigns them to GC without additional instrumentation.
