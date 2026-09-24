# Decision 0014 — location of the published historical aggregates

Date: 2026-09-23

Status: **approved and implemented 2026-09-24.** The owner approved separation
of external source evidence from derived summaries. No historical value, raw
observation, or pre-existing processed/lineage file was moved or rewritten.

## Context

`METHODOLOGY.md` section 2 assigns the unit "Historical row/aggregate" to
`data/baselines/` with origin `published_aggregate` or `upstream_recording`.
`REPRODUCIBILITY.md` lists `data/baselines/` among the directory seams, and
`data/baselines/README.md` is its scoped contract.

On disk this is not what happened. `data/baselines/` contains exactly one file —
its own contract README — and that README still states "No baseline values have
been imported at the foundation phase." The fifteen published Plauska 2023
aggregates that drive every historical ratio in the manuscript are transcribed
in the processed layer instead:

| File | Origin |
|---|---|
| `data/processed/plauska_fft_historical_summary.csv` | Table 5 of the publication |
| `data/processed/plauska_fir_historical_summary.csv` | Table 5 of the publication |
| `data/processed/plauska_crc32_historical_summary.csv` | pinned upstream CSV, commit `c42dba0d41d547960b73e63b3d4e09917d61e171` |
| `data/processed/plauska_sha256_historical_summary.csv` | pinned upstream CSV, same commit |
| `data/processed/plauska_iir_historical_summary.csv` | pinned upstream CSV, same commit |

Each has a matching `plauska_*_historical_lineage.csv` recording the input
locator, input hash, producer, and creation time. The rows carry
`measurement_origin` values of `upstream_recording_derived_summary` or an
equivalent, so the provenance is recorded even though the location is wrong.

Consequence: a reader who follows `METHODOLOGY.md` or the directory contract
finds an empty directory, and the contract README contradicts the repository
state.

## Why this was not corrected directly

`paper/tools/validate_manuscript.py` asserts that
`git diff HEAD -- data/baselines` is empty. This was verified empirically on
2026-09-23: appending a single probe line to `data/baselines/README.md` produced
`AssertionError: baseline changed` and a non-zero exit. The guard is deliberate —
it is the mechanism that fails closed when frozen baseline evidence has been
modified locally — so it was not weakened, and the probe was reverted.

Two further facts constrain the options:

- Relocating the transcriptions would invalidate the `output_path` values already
  recorded in the five lineage CSVs, so it is a lineage migration, not a move.
- `data/baselines/README.md` is itself the contract document for the directory.
  Editing it is a contract change, which is why it is part of this decision
  rather than a silent fix.

## Options

**Option A — honour the contract.** Move the five summary CSVs and their five
lineage CSVs into `data/baselines/`, rewrite the recorded `output_path` values
through a documented migration that preserves the original lineage rows, correct
`data/baselines/README.md`, and extend the `validate_manuscript.py` guard so it
protects the evidence files rather than a placeholder README. This makes the
guard meaningful for the first time and matches `METHODOLOGY.md` unchanged.
Cost: a lineage migration touching ten tracked files plus the validator.

**Option B — amend the contract.** Change the `Location` cell of
`METHODOLOGY.md` section 2 for the historical-row unit to name
`data/processed/`, correct `data/baselines/README.md` to state that the seam is
reserved but unused, and bump `METHODOLOGY.md`'s version. Cost: a normative
contract revision with a new version identifier, and the repository loses the
directory-level separation between published evidence and derived data that
`PROJECT_CHARTER.md` and `REPRODUCIBILITY.md` both argue for.

The owner approved a third, non-destructive implementation: **Option C — source
locator manifest plus preserved derivations.** `data/baselines/plauska_sources_v1.csv`
records the publisher Table 5 or exact pinned upstream CSV locator for each
workload, available upstream hashes, redistribution status, and SHA-256 of the
pre-existing processed summary. The five derived summaries and their five
original lineage files remain at their recorded paths. No third-party PDF,
source file, or upstream CSV is newly redistributed. The source-manifest builder
checks these exact derived bytes and provides an explicit versioned update path.

This differs from A because the CRC/SHA/IIR means are *calculated* from upstream
recordings, not source observations to relabel as baseline rows; the FFT/FIR
files are numeric Table 5 transcriptions with existing locators. It differs
from B because `data/baselines/` now has a distinct source-evidence role.

## Interim state

The original summaries remain authoritative for the manuscript's numerical
historical comparison. Source pointers are now under `data/baselines/`; no
claim is made that the source bytes are vendored. The old guard tested a Git
working-tree diff, which is unsuitable during an intentional, versioned
manifest addition. It is replaced by content validation of the source
manifest and the exact processed-summary hashes. This is not a weakening:
silent mutation of either the manifest or a summary fails validation.

## Affected versions and evidence

- `data/processed/plauska_*_historical_summary.csv` and
  `plauska_*_historical_lineage.csv` (10 tracked files).
- `data/baselines/README.md` (stale status sentence).
- `METHODOLOGY.md` section 2 (deviation note added 2026-09-23; mapping unchanged).
- `REPRODUCIBILITY.md` directory-deviations section (deviation recorded 2026-09-23).
- `paper/tools/validate_manuscript.py` (guard scope, if Option A is chosen).
- No measured value, raw bundle, vector, or manuscript number is affected.

Impact: paths, numeric results, and original lineage hashes are unchanged.
The new source-locator manifest is prospective metadata at version `1.0.0`;
the methodology mapping is clarified at version `0.3.0`. No recollection is
required. Redistribution and repository-license decisions remain release gates.

Pre-existing processed-summary **canonical Git blob** SHA-256 values pinned at
this decision. The first manifest draft accidentally hashed local checkout
bytes; Windows line-ending conversion made those values worktree-dependent.
The follow-up correction changed only the manifest and its builder, never the
processed files or historical values:

| Workload | SHA-256 |
|---|---|
| CRC-32 | `ae3cff214ed0e7c65dd291d0d2dc69a1d2574c7ae4d4f6ee8dcb1e2c1e26c3a3` |
| SHA-256 | `7b9da45459afedadc08c15d2c2da775de30772c43693d827793e470901aacff5` |
| FFT | `e8395c4f2254de53ad6c99c80039c2ebc080d470cbd781076f6d1039c3f2bfb5` |
| FIR | `4c0942eed8f53c698ef44df857690ae5f1ef005fc2b1d8ff51f713850fb356d5` |
| IIR | `f65503d4ac0a23e8641a2e79cf437565300025fa3e2b4df571cdb61d51adeb42` |

Approver: repository owner, 2026-09-24.
