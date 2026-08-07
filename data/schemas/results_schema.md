# Research Data Schema

Schema family version: `1.0.0-draft`  
Status: normative design; no result rows exist yet.

## 1. Why there are multiple CSV files

Run configuration, timed invocations, build sizes, static assembly counts, long power-meter windows, and published aggregates have different observation grains. Combining them in one wide row would create ambiguous nulls and encourage invalid pooling. This schema therefore defines small linked tables with stable interfaces.

The primary key names and hashes connect the tables. MATLAB and other parsers must address columns by name, not position.

## 2. General encoding and null rules

- UTF-8, comma delimiter, RFC 4180 quoting, header row required, decimal point `.`.
- ISO 8601 UTC timestamps use `YYYY-MM-DDTHH:MM:SS[.ffffff]Z`.
- Booleans are lowercase `true` or `false`.
- Blank means missing/unknown. `0` is a real value. Do not use `N/A`, `null`, sentinel `-1`, or whitespace-only values.
- Integer fields contain base-10 digits without grouping separators.
- Hexadecimal result values use lowercase, fixed width where defined by the benchmark, and a `0x` prefix. SHA-256 file hashes are 64 lowercase hexadecimal characters without `0x`.
- Units are encoded in field names or explicit unit fields. Unit conversion is a derived operation with lineage.
- Notes are informational, not a place to hide required metadata.
- Every file contains a `schema_version`; a raw bundle uses one compatible version across its tables.

## 3. `run.csv` — one row per acquisition run

| Column | Type | Required | Definition/invariant |
|---|---|---:|---|
| `schema_version` | string | yes | Exact schema version, initially `1.0.0` after freeze |
| `run_id` | UUID string | yes | Host-generated persistent run identity; primary key |
| `started_at_utc` | timestamp | yes | Acquisition start |
| `ended_at_utc` | timestamp | yes | Acquisition end; not earlier than start |
| `measurement_origin` | enum | yes | Exactly `local_measurement` for this table |
| `suite` | enum | yes | `historical`, `microarchitecture`, or `modern` |
| `benchmark_id` | string | yes | Version-independent workload name, e.g. `crc32` |
| `protocol_id` | string | yes | Frozen timing/acquisition protocol version |
| `benchmark_mode` | enum | yes | Exactly `A`, `B1`, or `B2` |
| `implementation_id` | string | yes | Immutable language implementation/version identifier |
| `language` | enum | yes | For first paper: `c_cpp`, `rust`, or `micropython` |
| `language_version` | string | yes | Standard/compiler language edition where applicable |
| `runtime` | string | yes | `freertos`, `micropython`, bare-metal environment, etc.; use `none` only when verified |
| `runtime_version` | string | yes | Exact version/build identifier |
| `compiler` | string | conditional | Required for compiled implementations; blank for a purely interpreted artifact |
| `compiler_version` | string | conditional | Full version output for compiled implementations |
| `sdk` | string | yes | Framework/SDK name |
| `sdk_version` | string | yes | Exact tag/commit/version |
| `target_triple` | string | conditional | Required for compiled builds |
| `optimization_profile_id` | string | yes | Versioned profile; not merely `release` |
| `compiler_flags` | string | conditional | Exact ordered flags/config encoded as a quoted field or referenced manifest |
| `git_commit` | string | yes | 40-character repository commit |
| `git_dirty` | boolean | yes | Whether authored tree differed from commit |
| `source_tree_sha256` | SHA-256 | yes | Hash of reproducible source archive/patch state |
| `build_id` | string | yes | Foreign key to build artifacts/metrics |
| `firmware_sha256` | SHA-256 | yes | Exact flashed firmware/interpreter image hash |
| `board_model` | string | yes | Full marketed/development-board model; not just chip |
| `board_revision` | string | no | Printed/supplier board revision |
| `board_instance_id` | string | yes | Stable pseudonymous physical-device ID |
| `chip` | string | yes | Exact SoC/variant marking |
| `chip_revision` | string | yes | Read-back silicon revision; blank fails strict validation |
| `flash_size_bytes` | integer | yes | Physical detected flash capacity in bytes |
| `isa` | string | yes | Exact implemented/target ISA string supported by evidence |
| `core` | string | yes | Executing CPU/core name |
| `cpu_frequency_hz` | integer | yes | Configured and read-back frequency in Hz |
| `core_affinity` | string | yes | Core/task affinity or `single_hp_core` when verified |
| `test_vector_set_id` | string | yes | Frozen vector set version |
| `test_vector_sha256` | SHA-256 | yes | Hash defined by the vector manifest |
| `timer` | string | yes | Exact timing primitive/counter |
| `timer_resolution_us` | decimal | yes | Documented or empirically verified resolution |
| `timing_scope` | string | yes | Frozen semantic boundary ID, not free prose alone |
| `warmup_iterations` | integer | yes | Planned unreported/recorded warm-ups per condition |
| `planned_iterations` | integer | yes | Measured iterations per input condition |
| `radio_state` | string | yes | Wi-Fi/Bluetooth/802.15.4 state |
| `power_management` | string | yes | Frequency/sleep/dynamic-power policy |
| `scheduler_config` | string | yes | RTOS/task/tick/priority configuration or verified absence |
| `gc_policy` | string | yes | Runtime garbage-collection policy; `not_applicable` if justified |
| `host_os` | string | yes | Capture host OS and version |
| `capture_tool` | string | yes | Serial/acquisition tool name |
| `capture_tool_version` | string | yes | Exact tool version/commit |
| `operator_id` | string | yes | Pseudonymous operator identity |
| `notes` | string | no | Non-normative context |

Exactly one data row is allowed. A validator rejects a missing required value rather than guessing it.

## 4. `observations.csv` — one row per invocation

| Column | Type | Required | Definition/invariant |
|---|---|---:|---|
| `schema_version` | string | yes | Compatible with `run.csv` |
| `observation_id` | UUID/string | yes | Globally unique primary key |
| `run_id` | UUID string | yes | Foreign key to the bundle's `run.csv` |
| `input_id` | string | yes | Stable input condition/vector identifier |
| `input_size_value` | integer | yes | Count expressed by `input_size_unit` |
| `input_size_unit` | enum | yes | `bytes`, `samples`, or `elements` as frozen by protocol |
| `operations_per_observation` | integer | yes | Logical kernel operations represented by this invocation; normally 1 for timing |
| `iteration` | integer | yes | One-based within `(run_id,input_id,phase)` |
| `phase` | enum | yes | `warmup` or `measured` |
| `execution_us` | decimal | conditional | Elapsed microseconds; required for a valid measured row |
| `cycles` | integer | no | Direct reliable counter delta only; never derived from time |
| `result_kind` | string | yes | e.g. `crc32_u32_hex` |
| `result_value` | string | yes | Actual result encoded by the protocol |
| `expected_value` | string | yes | Frozen oracle value in the same encoding |
| `correctness_pass` | boolean | yes | Exact/tolerance match as defined by protocol |
| `measurement_status` | enum | yes | `valid`, `invalid`, or `incomplete` at acquisition time |
| `notes` | string | no | Acquisition anomaly only |

The natural uniqueness constraint is `(run_id,input_id,phase,iteration)`. A zero-byte input is represented by `input_size_value=0`, not blank.

## 5. `manifest.csv` — bundle integrity

| Column | Type | Required | Definition/invariant |
|---|---|---:|---|
| `schema_version` | string | yes | Manifest schema version |
| `run_id` | UUID string | yes | Bundle identity |
| `relative_path` | string | yes | Forward-slash path contained within bundle; no `..` |
| `role` | enum/string | yes | `run_context`, `observations`, `console_log`, `firmware`, or documented extension |
| `byte_size` | integer | yes | File size |
| `sha256` | SHA-256 | yes | Hash of exact bytes |

Every bundle file except the manifest itself is listed. If a self-hashing archive manifest is later used, its convention must be separately versioned.

## 6. `artifact_metrics.csv` — one build metric per row

Required columns:

```text
schema_version,metric_id,build_id,benchmark_id,protocol_id,benchmark_mode,
implementation_id,artifact_role,metric_name,metric_value,metric_unit,
collection_tool,collection_tool_version,source_artifact_sha256,collected_at_utc,notes
```

Examples of separately defined metrics are ELF file bytes, flash image bytes, `.text`, `.rodata`, `.data`, `.bss`, static RAM estimate, peak heap, and stack high-water bytes. The metric dictionary must define inclusion/exclusion rules. Build-level values are never repeated as if measured per iteration.

## 7. `assembly_metrics.csv` — one static metric per function/object

Required columns:

```text
schema_version,analysis_id,build_id,benchmark_id,protocol_id,benchmark_mode,
implementation_id,target_triple,isa,function_name,metric_name,metric_value,
metric_unit,counting_rule_version,disassembler,disassembler_version,
source_artifact_sha256,listing_sha256,collected_at_utc,notes
```

Counting rules define instruction aliases, compressed widths, literal pools, alignment padding, calls, branches, stack accesses, and possible spills. Static metrics are never stored as dynamic runtime counters.

## 8. `energy_windows.csv` — one board-level meter interval

Required columns:

```text
schema_version,window_id,run_id,window_role,started_at_utc,ended_at_utc,
duration_s,operation_count,voltage_v,current_a,power_w,energy_j,meter_model,
meter_instance_id,meter_sampling_interval_s,source_log_sha256,
measurement_status,notes
```

`window_role` distinguishes workload, idle/control, and calibration windows. Per-operation energy is derived downstream from a documented formula; it is not a raw meter reading. Missing meter outputs remain blank rather than being algebraically filled into the raw record.

## 9. `historical_baseline.csv` — one externally supported value

Required columns:

```text
schema_version,baseline_id,source_id,source_version,measurement_origin,
record_kind,hardware,chip,isa,cpu_frequency_hz,language,language_version,
runtime,runtime_version,compiler,compiler_version,sdk,sdk_version,optimization,
benchmark_id,protocol_id,input_size_value,input_size_unit,iteration,
statistic_name,reported_value,reported_unit,reported_n,correctness_status,
source_locator,source_file_sha256,transcriber_id,transcribed_at_utc,
second_review_status,notes
```

`measurement_origin` is `published_aggregate` or `upstream_recording`. `record_kind` distinguishes a reported aggregate from an actual upstream observation. For an aggregate, `iteration` is blank and `statistic_name` might be `mean` or `standard_deviation`; for an upstream observation it may be `observation`. A published aggregate never becomes synthetic observations.

## 10. Validation and lineage tables

Validation report columns:

```text
schema_version,validation_id,validated_at_utc,validator,validator_version,
input_path,input_sha256,run_id,rule_id,severity,status,row_number,column_name,message
```

Lineage columns for processed/generated outputs:

```text
schema_version,lineage_id,output_path,output_sha256,created_at_utc,
producer,producer_version,git_commit,parameters_json,input_path,input_sha256,
validation_id,notes
```

A many-input output uses one lineage row per input under the same `lineage_id`.

## 11. Core validation invariants

- `benchmark_mode` is exactly one of `A`, `B1`, `B2` and never inferred from a folder.
- All observations in a bundle reference its one `run_id` and compatible schema version.
- Measured iteration numbers are contiguous per input unless an explicit invalid/incomplete record accounts for a gap.
- Expected measured row count equals the protocol/run plan; correctness passes for every included performance row.
- Manifest hashes and sizes match exact files.
- Mode A implementation/protocol/vector IDs belong to the approved comparability record.
- A run cannot combine languages, builds, modes, protocols, vector sets, or hardware instances.
- Historical and local origins cannot appear in the same raw table.
- Units are homogeneous within any statistical group; conversions are explicit and derived.
- `cycles` blank is acceptable; an inferred value is not.

## 12. Evolution policy

- Adding an optional backward-compatible column increments the minor version.
- Changing meaning, units, requiredness, identity, or grain increments the major version.
- Clarifying prose without data-interface change increments the patch version.
- Raw/baseline evidence retains its original schema. A migration writes a new derived file and lineage; it never overwrites evidence.
- Each parser declares supported schema versions and fails loudly on an unsupported major version.
