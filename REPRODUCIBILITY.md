# Reproducibility Contract

Version: `0.1.0-foundation`

## Current state

All five Mode A vertical slices and the minimal Mode B campaign are published
on `main`. Physical acquisition, validation, MATLAB analysis, and generated-
code scripts have been exercised with pinned toolchains. The exact accepted
Mode A Rust CRC ELF was not retained; its static inspection remains explicitly
labelled as a pinned-source reconstruction. The experimental record is frozen.

## Reproduction levels

1. **Analysis-only:** obtain the archived data and code, verify hashes, validate CSV, regenerate statistics, figures, tables, and paper.
2. **Firmware rebuild:** additionally reproduce each firmware/interpreter image and static build/assembly artifact from pinned tools and dependencies.
3. **Physical rerun:** additionally identify the board instance, flash the build, reproduce the acquisition protocol, and create new raw run bundles.

Each release states which levels were actually tested.

## Artifact classes

| Class | Examples | Mutability |
|---|---|---|
| Authored | source, protocol, MATLAB, LaTeX | Changed only through version control |
| Acquired | paper PDF, upstream source snapshot, external manual | Stored only when license permits; hash and provenance required |
| Raw local | console capture, run context, iteration observations, meter log | Immutable after capture |
| Baseline | published aggregate transcription, upstream historical CSV | Immutable evidence plus separate correction/version records |
| Validation | schema/integrity/correctness reports | Regenerated without editing evidence |
| Processed | statistics, normalized tables, analysis inclusion manifests | Fully derived with lineage |
| Generated | assembly summaries, plots, tables, PDF/site output | Rebuilt from authored/acquired/evidence inputs |
| Release | archive manifest, checksums, DOI deposit | Frozen and versioned |

## Required run provenance

Before a physical run is valid, capture:

- UTC start/end timestamps and operator;
- repository commit, dirty state, and source-tree/patch hash;
- benchmark, protocol, implementation, vector set, and optimization-profile identifiers;
- language, runtime/interpreter, compiler, SDK, target triple, dependency locks, and complete build flags;
- firmware/ELF SHA-256 and build identifier;
- chip, chip revision, board model/revision, persistent board-instance ID, flash size/topology, and power setup;
- CPU frequency readback, core/task placement, power-management, radio, scheduler, interrupt, cache/reset, and GC policy;
- timer/counter source, resolution, units, width/wrap assumptions, and timing scope;
- expected/measured iteration and warm-up counts;
- host OS, capture tool/version, serial configuration, MATLAB version/toolboxes for analysis, and relevant environment notes.

Unknown metadata are blank and explicitly reported by validation; they are never filled with a presumed default.

## Raw run bundle

```text
data/raw/<target>/<benchmark>/<run_id>/
  run.csv           # exactly one context row
  observations.csv  # one row per timed or explicitly recorded warm-up invocation
  manifest.csv      # SHA-256, role, and size for every bundle file
  console.log       # optional original device stream
```

UTF-8, comma-delimited RFC 4180 CSV and `.` as the decimal separator are the project defaults. Timestamps use ISO 8601 UTC (`Z`). Units appear in field names or explicit unit fields. Empty means missing; zero is a measurement.

## Immutability and corrections

- Never hand-edit a raw or baseline CSV.
- A capture error creates a new run; the failed run remains present and is marked invalid downstream.
- A transcription correction creates a new baseline version and a change record; the original remains archived.
- Validation emits reports under `data/validation/` and never modifies input.
- Processing reads an explicit list of validated run/file hashes, not a glob and not a file named `latest`.
- Old raw schema versions are not migrated in place. A migration creates derived rows with source row IDs and lineage.

## Lineage

Every processed dataset will include or accompany a `lineage.csv` containing output file/hash, processing commit, script/version, exact input file/hash list, parameters, creation timestamp, and validation report identifiers. MATLAB figures and tables will have a figure manifest with the same information.

MATLAB functions will accept input and output paths, avoid changing the process working directory, and fail if inputs contain unintended mixtures of benchmark mode, measurement origin, protocol, or units.

## Test vectors and randomness

- Test vectors are versioned artifacts with byte length and SHA-256.
- Randomly generated vectors record algorithm, implementation/tool version, seed, datatype, bounds, and generation script.
- If an upstream seed is unavailable, preserve the upstream bytes exactly and label the generation process unknown; do not regenerate a visually similar random vector.
- A frozen vector is never modified. A changed vector set receives a new ID and hash.

## Toolchain capture

Each implementation will eventually provide a lock/pin file and a machine-readable version capture. Containerization may be used for host tools where licenses allow, but it does not replace recording the target SDK, compiler, linker, runtime image, and chip configuration. Any Xtensa static-analysis toolchain must be pinned separately from the C6 execution toolchain.

## External sources

For each acquired source, record canonical URL/DOI, publisher/owner, exact version or commit, access date, SHA-256, local path if stored, license/redistribution status, and the claims or values it supports. A URL that always points to the newest manual is not a sufficient release pin; archive the licensed document or record its exact version and hash.

The Plauska repository is currently audited at commit `c42dba0d41d547960b73e63b3d4e09917d61e171`. Its source is not vendored here pending a licensing decision. See `references/original-study/README.md`.

## Directory deviations from the initial sketch

Three explicit seams were added:

- `data/baselines/` keeps published classic-ESP32 evidence out of local raw C6 measurements.
- `data/validation/` lets validators report problems without mutating evidence.
- `artifacts/` stores build/disassembly evidence separately from measured observations.

Decision 0014 gives `data/baselines/` an external-source-locator manifest, without redistributing the publisher PDF or upstream CSV. Plauska historical numeric summaries and their original lineage remain under `data/processed/`; the manifest pins each summary's exact SHA-256. The source-versus-derived distinction is normative in `METHODOLOGY.md` version `0.3.0`. No accepted historical or local measurement was moved or edited.

Placeholder directories use scoped `README.md` contracts instead of bare `.gitkeep` files.

## Release checklist

- Clean tagged commit and captured dirty-state policy.
- Machine-readable environment, dependencies, and build manifests.
- Validated raw/baseline hashes and processing lineage.
- Rebuilt statistics, MATLAB figures/tables, LaTeX PDF, and site from a clean checkout.
- Citation metadata, source/dataset/code licenses, third-party notices, and archive checksums.
- A frozen repository release and, when ready, a Zenodo DOI. Uploading elsewhere is dissemination, not peer review.
