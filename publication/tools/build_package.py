"""Build an allowlisted local analysis package without publishing or editing evidence."""
from pathlib import Path
import argparse
import csv
import hashlib
import importlib.util
import json
import math
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    ("crc32_mode_a_esp32c6_observations.csv", "CRC32", "input_bytes"),
    ("sha256_mode_a_esp32c6_observations.csv", "SHA256", "input_bytes"),
    ("fft_mode_a_esp32c6_observations.csv", "FFT_I16", "input_complex_samples"),
    ("fir_mode_a_esp32c6_observations.csv", "FIR_F32", "input_samples"),
    ("iir_mode_a_esp32c6_observations.csv", "IIR_BQ_F32", "input_samples"),
    ("mode_b_observations.csv", None, "input_size"),
]
FIELDS = ["export_schema_version", "source_dataset", "source_dataset_sha256", "source_row_number", "source_schema_version", "run_id", "chip", "workload", "language", "mode", "optimization", "input_size", "input_size_field", "iteration", "batch_count", "total_batch_time_us", "normalized_time_per_call_us", "correctness_pass", "measurement_status", "board_model", "board_instance_id", "chip_revision", "cpu_frequency_hz", "flash_size_bytes", "flash_mode", "flash_frequency_hz", "timer", "toolchain", "optimization_profile_id", "artifact_sha256"]
METRICS = ["workload", "language", "mode", "instruction_count", "code_span_bytes", "branch_count", "call_count", "bounds_panic_refs"]
SPECIAL = ["profile", "instruction_count", "code_span_bytes", "branch_count", "call_count", "bounds_panic_refs"]
FIGURES = ("mode_a_historical_local", "mode_a_rust_cpp", "mode_b_compiler_response", "mode_b_sha_profiles")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))

def write(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields or list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def build(out):
    assert not out.exists(), "use a fresh destination; existing approved packages are not overwritten"
    assert ROOT in out.parents and out != ROOT
    out.mkdir(parents=True)
    base_commit = subprocess.check_output(["rtk", "proxy", "git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["rtk", "proxy", "git", "status", "--porcelain"], cwd=ROOT))
    lineage = []
    def record(source, target, rule):
        lineage.append(dict(source_path=source.relative_to(ROOT).as_posix(), source_sha256=sha(source), export_path=target, projection_rule=rule, private_source_base_commit=base_commit, source_tree_dirty=str(dirty).lower()))
    def copy(relative, target=None):
        source = ROOT / relative
        destination = out / (target or relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        record(source, destination.relative_to(out).as_posix(), "byte-identical authored/derived file copy; not a copy of full private history")
    export = []
    for filename, workload, field in FILES:
        source = ROOT / "data/processed" / filename
        digest = sha(source)
        rows = read(source)
        assert len(rows) == (9600 if workload is None else 2400)
        for number, row in enumerate(rows, 2):
            assert row["correctness_pass"] == "true" and row["measurement_status"] == "valid"
            assert row["mode"] == ("B" if workload is None else "A")
            result = dict.fromkeys(FIELDS, "")
            result.update(export_schema_version="1.0.0-analysis-archive", source_dataset=source.relative_to(ROOT).as_posix(), source_dataset_sha256=digest, source_row_number=number, source_schema_version=row["schema_version"], run_id=row.get("run_id", ""), chip=row["chip"], workload=workload or row["workload"], language=row["language"], mode=row["mode"], optimization="none" if workload else row["optimization"], input_size=row[field], input_size_field=field if workload else row["input_size_field"])
            for name in FIELDS[13:]:
                result[name] = row.get(name, "")
            export.append(result)
        record(source, "data/local_timings.csv", "named-column projection of accepted observations; stored strings retained; CRC/SHA result values and console contents excluded")
    write(out / "data/local_timings.csv", export, FIELDS)
    source = ROOT / "data/processed/mode_a_cross_workload_summary.csv"
    locators = read(ROOT / "data/baselines/plauska_sources_v1.csv")
    benchmark = {"CRC32": "crc32", "SHA256": "sha256", "FFT_I16": "fft", "FIR_F32": "fir", "IIR_BQ_F32": "iir"}
    historical = []
    for row in read(source):
        locator = next(r for r in locators if r["benchmark_id"] == benchmark[row["workload"]] and r["derived_path"].endswith("_historical_summary.csv"))
        historical.append(dict(workload=row["workload"], language=row["language"], input_size=row["input_size"], input_size_field=row["input_size_field"], mean_us=row["plauska_mean_us"], measurement_origin="published_aggregate" if row["workload"] in {"FFT_I16", "FIR_F32"} else "upstream_recording_derived_summary", source_id="plauska2023performance", doi="10.3390/electronics12010143", source_locator=locator["source_locator"], source_detail=locator["source_detail"], derived_source_sha256=locator["derived_sha256"]))
    assert len(historical) == 120
    write(out / "data/historical_means.csv", historical)
    record(source, "data/historical_means.csv", "project-derived historical numerical aggregates only; imported evidence, not local raw or bundled source recording")
    for filename, fields in (("mode_b_codegen_metrics.csv", METRICS), ("mode_b_fft_unchecked_codegen.csv", SPECIAL)):
        source = ROOT / "data/processed" / filename
        write(out / "data/processed" / filename, [{field: row[field] for field in fields} for row in read(source)], fields)
        record(source, "data/processed/" + filename, "imported numeric static metrics; source paths/symbol text/disassembly excluded; not a new compiler audit")
    for name in ("README.md", "LICENSING.md", "ZENODO_METADATA.json", "analysis.py", "verify_package.py", "build_paper.py"):
        copy("publication/" + name, name)
    copy("publication/PLATFORM_REVIEW.md", "PLATFORM_REVIEW.md")
    copy("LICENSE", "LICENSE-MIT.txt")
    copy("matlab/run_publication_analysis.m")
    copy("paper/manuscript.tex")
    copy("paper/references.bib")
    copy("paper/CLAIM_AUDIT_2.md")
    copy("paper/supplement/supplement.tex")
    copy("paper/preflight/PDF_PREFLIGHT_ANALYSIS_ARCHIVE_2026_10_07.txt", "validation/REVIEW_PDF_PREFLIGHT.txt")
    copy("data/baselines/plauska_sources_v1.csv")
    source = ROOT / "paper/tables/experimental_inventory.csv"
    fields = ["workload", "mode", "profile", "language", "accepted_samples", "exact_elf_status", "exact_elf_sha256"]
    write(out / "data/retained_artifact_hashes.csv", [{field: row[field] for field in fields} for row in read(source)], fields)
    record(source, "data/retained_artifact_hashes.csv", "artifact identity/count/status facts only; underlying binary/code not supplied")
    validation = ROOT / "publication/validation"
    if validation.exists():
        for path in sorted(validation.iterdir()):
            if path.is_file() and path.suffix in {".txt", ".json", ".md"}:
                copy(path.relative_to(ROOT).as_posix(), "validation/" + path.name)
    for name in ("review-manuscript.pdf", "review-supplement.pdf"):
        copy("paper/" + name)
    for stem in FIGURES:
        for extension in (".pdf", ".png"):
            copy("paper/figures/" + stem + extension)
    spec = importlib.util.spec_from_file_location("scoped_analysis", out / "analysis.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    summaries = module.analyse(out)
    frozen_a = {(r["workload"], r["language"], r["input_size"]): r for r in read(ROOT / "data/processed/mode_a_cross_workload_summary.csv")}
    frozen_b = {(r["workload"], r["language"], r["optimization"], r["input_size"]): r for r in read(ROOT / "data/processed/mode_b_summary.csv")}
    for row in summaries:
        if row["mode"] == "A":
            frozen = frozen_a[(row["workload"], row["language"], row["input_size"])]
            columns = [("n", "esp32c6_n"), ("mean_us", "esp32c6_mean_us"), ("median_us", "esp32c6_median_us"), ("sample_std_us", "esp32c6_sample_std_us")]
        else:
            frozen = frozen_b[(row["workload"], row["language"], row["optimization"], row["input_size"])]
            columns = [("n", "n"), ("mean_us", "mode_b_mean_us"), ("median_us", "mode_b_median_us"), ("sample_std_us", "mode_b_std_us")]
        for current, previous in columns:
            assert math.isclose(float(row[current]), float(frozen[previous]), rel_tol=1e-12, abs_tol=1e-6), (row, current)
    for relative in ("paper/tables/headline_results.tex", "paper/tables/mode_b_selected.tex", "paper/tables/fft_transformation.tex", "paper/supplement/historical_local_matrix.tex"):
        assert (out / relative).read_bytes() == (ROOT / relative).read_bytes(), "generated table differs: " + relative
        record(ROOT / relative, relative, "independently regenerated; byte identity with frozen publication table checked")
    for source in ("data/processed/mode_a_largest_input_summary.csv", "data/processed/mode_b_summary.csv"):
        record(ROOT / source, source, "independently regenerated from timing projection; all local groups numerically checked")
    write(out / "source_lineage.csv", lineage)
    assert all(sha(ROOT / r["source_path"]) == r["source_sha256"] for r in lineage)
    print("FROZEN_STATISTICS_AND_TABLES_MATCH_PASS groups=216 tables=4")
    seal(out)

def seal(out):
    files = sorted(p for p in out.rglob("*") if p.is_file() and p.name != "manifest.csv" and "__pycache__" not in p.parts)
    forbidden = {".elf", ".bin", ".o", ".a", ".map", ".fig"}
    for path in files:
        assert path.suffix not in forbidden and ".git" not in path.parts, path
        assert not any(name in path.name for name in ("generated_vector", "console", "disassembly")), path
    write(out / "manifest.csv", [dict(path=p.relative_to(out).as_posix(), byte_size=p.stat().st_size, sha256=sha(p)) for p in files])
    archive = Path(str(out) + ".zip")
    assert not archive.exists(), "existing archives are not replaced"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as target:
        for path in files + [out / "manifest.csv"]:
            target.write(path, arcname=path.relative_to(out).as_posix())
    with zipfile.ZipFile(archive) as target:
        assert target.testzip() is None
        assert set(target.namelist()) == {p.relative_to(out).as_posix() for p in files} | {"manifest.csv"}
    print("LOCAL_ARCHIVE_CREATED", archive)
    print("ARCHIVE_SHA256", sha(archive))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seal", action="store_true", help="seal an already built and validated local staging directory")
    args = parser.parse_args()
    destination = args.output.resolve()
    assert ROOT in destination.parents and destination != ROOT
    seal(destination) if args.seal else build(destination)
