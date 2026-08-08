#!/usr/bin/env python3
"""Regenerate and validate the Mode A cross-workload synthesis tables."""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"
VAL = ROOT / "data" / "validation" / "mode_a_cross_workload"

CONFIG = {
    "CRC32": dict(local="crc32_mode_a_esp32c6_observations.csv", size="input_bytes",
                  historical="plauska_crc32_historical_summary.csv", hist_size="input_bytes",
                  hist_mean="mean_us", numeric="uint8 / uint32", cls="integer checksum",
                  provenance="C++ exact: artifacts/assembly/crc32/cpp/riscv/measured_mode_a/manifest.csv; Rust exact accepted ELF not retained: artifacts/assembly/crc32/rust/riscv/reconstructed_mode_a/manifest.csv",
                  mechanism="C6 Rust pointer/bottom-tested loop differs from C++ indexing; matched C++ RV32IMAC loop is larger than Xtensa",
                  evidence="OBSERVED exact C6 C++; reconstructed C6 Rust; matched C++ reconstruction; MEDIUM"),
    "SHA256": dict(local="sha256_mode_a_esp32c6_observations.csv", size="input_bytes",
                   historical="plauska_sha256_historical_summary.csv", hist_size="input_bytes",
                   hist_mean="mean_us", numeric="uint8 / uint32", cls="integer cryptographic hash",
                   provenance="artifacts/builds/sha256/c_cpp/26ab7a9-mode-a/manifest.csv; artifacts/builds/sha256/rust/26ab7a9-mode-a/manifest.csv",
                   mechanism="Xtensa matched transform uses src rotations; RV32IMAC uses shift/OR sequences; Rust exact transform has more branches and a larger frame",
                   evidence="OBSERVED exact C6 and matched reconstruction; HIGH for codegen, MEDIUM for timing mechanism"),
    "FFT_I16": dict(local="fft_mode_a_esp32c6_observations.csv", size="input_complex_samples",
                    historical="plauska_fft_historical_summary.csv", hist_size="input_complex_samples",
                    hist_mean="mean_us", numeric="Q15 int16 complex", cls="fixed-point transform",
                    provenance="artifacts/builds/fft/ARTIFACT_MANIFEST.md",
                    mechanism="Scalar multiply/shift code on both targets; exact Rust retains bounds branches and panic paths; no emitted DSP/MAC",
                    evidence="OBSERVED exact C6; matched reconstruction; HIGH for codegen, MEDIUM for timing mechanism"),
    "FIR_F32": dict(local="fir_mode_a_esp32c6_observations.csv", size="input_samples",
                    historical="plauska_fir_historical_summary.csv", hist_size="input_samples",
                    hist_mean="mean_us", numeric="IEEE-754 binary32", cls="floating-point feed-forward filter",
                    provenance="artifacts/builds/fir/ARTIFACT_MANIFEST.md",
                    mechanism="RV32IMAC exact kernels call software-float helpers; matched Xtensa emits madd.s",
                    evidence="OBSERVED generated code; historical/local timing is descriptive; HIGH mechanism presence, MEDIUM contribution"),
    "IIR_BQ_F32": dict(local="iir_mode_a_esp32c6_observations.csv", size="input_samples",
                       historical="plauska_iir_historical_summary.csv", hist_size="input_samples",
                       hist_mean="mean_us", numeric="IEEE-754 binary32", cls="floating-point feedback filter",
                       provenance="artifacts/builds/iir/ARTIFACT_MANIFEST.md",
                       mechanism="Nine serialized software-float helper calls/sample on RV32IMAC; matched Xtensa emits fused FP operations",
                       evidence="OBSERVED generated code; feedback-cost interpretation INFERRED; HIGH mechanism presence, MEDIUM contribution"),
}

LANGS = ("c_cpp", "rust", "micropython")
HIST_FREQ_MHZ = 160.0  # verified Plauska configuration, not ESP32 maximum rating
C6_FREQ_MHZ = 160.0


def rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(data)


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def static_metrics():
    result = {}
    # Select exact C6 kernels/transforms, never whole-artifact counts.
    for r in rows(OUT / "sha256_static_analysis.csv"):
        if r["artifact_class"] == "measured_exact" and "transform" in r["function"]:
            result[("SHA256", r["language"])] = {k: r[k] for k in
                ("code_bytes", "instructions", "loads", "stores", "branches", "calls", "stack_frame_bytes")}
    for bench, filename in (("FFT_I16", "fft_exact_kernel_analysis.csv"),
                            ("FIR_F32", "fir_codegen_analysis.csv"),
                            ("IIR_BQ_F32", "iir_codegen_analysis.csv")):
        for r in rows(OUT / filename):
            if r.get("identity", "").startswith("exact_c6_"):
                lang = "c_cpp" if r["identity"].endswith("cpp") else "rust"
                result[(bench, lang)] = {k: v for k, v in r.items()
                    if k not in ("identity", "architecture", "artifact", "symbol")}
    # CRC is stored in metric-per-row form.
    grouped = defaultdict(dict)
    for r in rows(OUT / "crc32_static_analysis.csv"):
        impl = r["implementation_id"]
        if r["scope"] == "hot_loop" and ("measured" in impl or "rust" in impl):
            lang = "rust" if "rust" in impl else "c_cpp"
            grouped[lang][r["metric_name"]] = r["metric_value"]
    result.update({("CRC32", k): v for k, v in grouped.items()})
    return result


def load_historical(cfg):
    out = {}
    for r in rows(OUT / cfg["historical"]):
        lang = r["language"]
        size = int(r[cfg["hist_size"]])
        out[(size, lang)] = float(r[cfg["hist_mean"]])
    return out


def main():
    static = static_metrics()
    summary = []
    largest = []
    validation = []
    for workload, cfg in CONFIG.items():
        local = rows(OUT / cfg["local"])
        assert len(local) == 2400, (workload, len(local))
        assert all(r["mode"] == "A" and r["measurement_status"] == "valid" and r["correctness_pass"] == "true" for r in local)
        grouped = defaultdict(list)
        for r in local:
            grouped[(int(r[cfg["size"]]), r["language"])].append(float(r["normalized_time_per_call_us"]))
        assert len(grouped) == 24 and all(len(v) == 100 for v in grouped.values())
        historical = load_historical(cfg)
        sizes = sorted({k[0] for k in grouped})
        for size in sizes:
            med = {lang: statistics.median(grouped[(size, lang)]) for lang in LANGS}
            for lang in LANGS:
                vals = grouped[(size, lang)]
                hist = historical.get((size, lang))
                record = {
                    "workload": workload, "input_size": size, "input_size_field": cfg["size"], "language": lang,
                    "esp32c6_n": len(vals), "esp32c6_mean_us": f"{statistics.mean(vals):.9f}",
                    "esp32c6_median_us": f"{med[lang]:.9f}", "esp32c6_sample_std_us": f"{statistics.stdev(vals):.9f}",
                    "plauska_mean_us": "" if hist is None else f"{hist:.9f}",
                    "plauska_over_esp32c6_mean": "" if hist is None else f"{hist/statistics.mean(vals):.9f}",
                    "rust_over_cpp_median": f"{med['rust']/med['c_cpp']:.9f}",
                    "micropython_over_cpp_median": f"{med['micropython']/med['c_cpp']:.9f}",
                    "execution_class": "interpreted" if lang == "micropython" else "native",
                    "numeric_type": cfg["numeric"], "workload_class": cfg["cls"],
                    "artifact_provenance": cfg["provenance"],
                    "static_metrics_json": json.dumps(static.get((workload, lang), {}), sort_keys=True, separators=(",", ":")),
                    "principal_mechanism": cfg["mechanism"], "evidence_confidence": cfg["evidence"],
                }
                summary.append(record)
                if size == sizes[-1]:
                    largest.append({**record,
                        "plauska_nominal_cycle_scale": "" if hist is None else f"{hist*HIST_FREQ_MHZ:.6f}",
                        "esp32c6_nominal_cycle_scale": f"{statistics.mean(vals)*C6_FREQ_MHZ:.6f}",
                        "historical_frequency_mhz": f"{HIST_FREQ_MHZ:.1f}", "esp32c6_frequency_mhz": f"{C6_FREQ_MHZ:.1f}",
                        "cycle_scale_warning": "time_us*nominal_MHz; derived descriptive scale, not measured cycles or IPC"})
        validation.append(f"- PASS {workload}: 2,400 valid/correct rows; 24 groups; 100 observations/group; 8 sizes.")

    write_csv(OUT / "mode_a_cross_workload_summary.csv", list(summary[0]), summary)
    write_csv(OUT / "mode_a_largest_input_summary.csv", list(largest[0]), largest)
    matrix = []
    for workload, cfg in CONFIG.items():
        lrows = [r for r in largest if r["workload"] == workload]
        rank = sorted(lrows, key=lambda r: float(r["esp32c6_median_us"]))
        matrix.append({"workload": workload, "workload_class": cfg["cls"], "dominant_arithmetic": cfg["numeric"],
                       "c6_language_ranking_largest_input": " < ".join(r["language"] for r in rank),
                       "c6_vs_historical_native": "; ".join(f"{r['language']} Plauska/C6={float(r['plauska_over_esp32c6_mean']):.3f}" for r in lrows if r["language"] != "micropython"),
                       "principal_mechanism": cfg["mechanism"],
                       "alternative_explanations": "compiler/runtime generation; SDK; cache/memory/SoC; protocol differences",
                       "evidence_confidence": cfg["evidence"]})
    write_csv(OUT / "mode_a_workload_mechanism_matrix.csv", list(matrix[0]), matrix)

    VAL.mkdir(parents=True, exist_ok=True)
    outputs = [OUT / "mode_a_cross_workload_summary.csv", OUT / "mode_a_largest_input_summary.csv", OUT / "mode_a_workload_mechanism_matrix.csv"]
    report = ["# Mode A cross-workload validation", "", *validation, "", "## Generated artifacts", ""]
    report += [f"- `{p.relative_to(ROOT).as_posix()}`: SHA-256 `{sha256(p)}`" for p in outputs]
    matlab_dir = ROOT / "artifacts" / "matlab" / "mode_a_cross_workload"
    expected_matlab = [
        f"figure{i}_{name}.{ext}"
        for i, name in ((1, "historical_local_ratio"), (2, "rust_cpp_ratio"),
                        (3, "native_historical_local"), (4, "arithmetic_class_contrast"))
        for ext in ("png", "pdf", "fig")
    ] + ["largest_input_plot_data.csv", "language_ratio_plot_data.csv"]
    if matlab_dir.exists():
        missing = [name for name in expected_matlab if not (matlab_dir / name).is_file()]
        assert not missing, f"Missing MATLAB outputs: {missing}"
        manifest = [{"path": name, "sha256": sha256(matlab_dir / name),
                     "byte_size": (matlab_dir / name).stat().st_size}
                    for name in expected_matlab]
        write_csv(matlab_dir / "manifest.csv", ["path", "sha256", "byte_size"], manifest)
        report += ["", "## MATLAB R2024b execution", "",
                   f"- PASS: {len(expected_matlab)} expected figure/supporting files exist.",
                   "- Manifest: artifacts/matlab/mode_a_cross_workload/manifest.csv."]
    report += ["", "Historical Plauska and local C6 observations remain separate. The nominal cycle-scale fields are derived from time and the verified 160 MHz configurations; they are not measured cycles or IPC.", ""]
    (VAL / "validation_report.md").write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
