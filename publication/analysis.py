"""Recompute the scoped archive's timing statistics and publication tables.

This never rebuilds firmware, calculates new correctness outputs, or generates
machine-code metrics. Historical means and static counts are imported evidence.
"""
from collections import defaultdict
from pathlib import Path
import argparse
import csv
import math
import statistics

KEY = ("mode", "workload", "language", "optimization", "input_size", "input_size_field")
WORKLOADS = ("CRC32", "SHA256", "FFT_I16", "FIR_F32", "IIR_BQ_F32")
LANGUAGES = ("c_cpp", "rust", "micropython")
NAMES = dict(zip(WORKLOADS, ("CRC-32", "SHA-256", "FFT (Q15)", "FIR (binary32)", "IIR (binary32)")))
LABELS = {"c_cpp": "C/C++", "rust": "Rust", "micropython": "MicroPython"}

def read(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))

def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def table(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def analyse(root):
    rows = read(root / "data/local_timings.csv")
    assert len(rows) == 21600
    groups = defaultdict(list)
    for row in rows:
        assert row["measurement_status"] == "valid" and row["correctness_pass"] == "true"
        total, count = int(row["total_batch_time_us"]), int(row["batch_count"])
        stored = float(row["normalized_time_per_call_us"])
        assert total >= 0 and count > 0 and math.isfinite(stored) and stored >= 0
        legacy = row["mode"] == "A" and row["language"] == "micropython" and row["workload"] in {"FFT_I16", "FIR_F32", "IIR_BQ_F32"}
        assert abs(total / count - stored) <= (1e-3 if legacy else 0.51e-9)
        assert row["mode"] in {"A", "B"}
        assert (row["mode"] != "A" or row["optimization"] == "none")
        groups[tuple(row[name] for name in KEY)].append(row)
    assert len(groups) == 216
    summaries = []
    for key, group in sorted(groups.items()):
        assert len(group) == 100
        assert sorted(int(row["iteration"]) for row in group) == list(range(1, 101))
        assert len({row["batch_count"] for row in group}) == 1
        values = [float(row["normalized_time_per_call_us"]) for row in group]
        summaries.append(dict(zip(KEY, key), n=100, mean_us=statistics.mean(values), median_us=statistics.median(values), sample_std_us=statistics.stdev(values), minimum_us=min(values), maximum_us=max(values), batch_count=int(group[0]["batch_count"])))
    write(root / "results/local_summary.csv", summaries)
    by_key = {tuple(row[name] for name in KEY): row for row in summaries}
    ratios = []
    for row in summaries:
        mode, workload, language, profile, size, field = (row[name] for name in KEY)
        if mode == "A" and language != "c_cpp":
            reference = by_key[("A", workload, "c_cpp", "none", size, field)]
            kind = "within_C6_language_median"
        elif mode == "B":
            base = {"SHA256_HW": "SHA256", "FFT_I16_UNCHECKED": "FFT_I16"}.get(workload, workload)
            reference = by_key[("A", base, language, "none", size, field)]
            kind = "B_over_same_language_A_median"
        else:
            continue
        ratios.append(dict(ratio_kind=kind, workload=workload, language=language, optimization=profile, input_size=size, input_size_field=field, numerator_median_us=row["median_us"], denominator_median_us=reference["median_us"], ratio=row["median_us"] / reference["median_us"]))
    write(root / "results/local_ratios.csv", ratios)

    historical = read(root / "data/historical_means.csv")
    assert len(historical) == 120
    hist = {(r["workload"], r["language"], r["input_size"]): r for r in historical}
    assert len(hist) == 120
    combined = []
    for workload in WORKLOADS:
        for language in LANGUAGES:
            for size in (0, 16, 32, 64, 128, 256, 512, 1024):
                h = hist[(workload, language, str(size))]
                field = h["input_size_field"]
                a = by_key[("A", workload, language, "none", str(size), field)]
                cpp = by_key[("A", workload, "c_cpp", "none", str(size), field)]
                rust = by_key[("A", workload, "rust", "none", str(size), field)]
                mp = by_key[("A", workload, "micropython", "none", str(size), field)]
                combined.append(dict(workload=workload, input_size=size, input_size_field=field, language=language,
                    esp32c6_n=a["n"], esp32c6_mean_us=f'{a["mean_us"]:.9f}', esp32c6_median_us=f'{a["median_us"]:.9f}',
                    esp32c6_sample_std_us=f'{a["sample_std_us"]:.9f}', plauska_mean_us=h["mean_us"],
                    plauska_over_esp32c6_mean=f'{float(h["mean_us"])/a["mean_us"]:.9f}',
                    rust_over_cpp_median=f'{rust["median_us"]/cpp["median_us"]:.9f}',
                    micropython_over_cpp_median=f'{mp["median_us"]/cpp["median_us"]:.9f}'))
    write(root / "data/processed/mode_a_cross_workload_summary.csv", combined)
    largest = [row for row in combined if row["input_size"] == 1024]
    write(root / "data/processed/mode_a_largest_input_summary.csv", largest)
    mode_b = []
    for row in summaries:
        if row["mode"] != "B":
            continue
        base = {"SHA256_HW": "SHA256", "FFT_I16_UNCHECKED": "FFT_I16"}.get(row["workload"], row["workload"])
        a = by_key[("A", base, row["language"], "none", row["input_size"], row["input_size_field"])]
        mode_b.append(dict(workload=row["workload"], language=row["language"], optimization=row["optimization"], input_size=row["input_size"],
            n=row["n"], mode_b_mean_us=f'{row["mean_us"]:.9f}', mode_b_median_us=f'{row["median_us"]:.9f}',
            mode_b_std_us=f'{row["sample_std_us"]:.9f}', mode_a_mean_us=f'{a["mean_us"]:.9f}',
            mode_a_median_us=f'{a["median_us"]:.9f}', mode_b_over_mode_a_median=f'{row["median_us"]/a["median_us"]:.9f}',
            speedup_a_over_b=f'{a["median_us"]/row["median_us"]:.9f}'))
    write(root / "data/processed/mode_b_summary.csv", mode_b)
    make_tables(root, largest, mode_b)
    print(f"ARCHIVE_ANALYSIS_PASS observations={len(rows)} groups={len(summaries)} ratios={len(ratios)} tables=4")
    return summaries

def make_tables(root, largest, mode_b):
    end = r"\\"
    fmt = lambda x: f"{x:.3f}" if x < 10000 else f"{x:.0f}"
    lines = [r'\begin{tabular}{@{}lrrr@{}}', r'\toprule', r'Workload & C/C++ median & Rust median & MicroPython median \\', r' & \multicolumn{3}{c}{Local C6 time (\(\mu\)s)} \\', r'\midrule']
    for workload in WORKLOADS:
        group = {r["language"]: r for r in largest if r["workload"] == workload}
        values = [fmt(float(group[lang]["esp32c6_median_us"])) for lang in LANGUAGES]
        lines.append(f"{NAMES[workload]} & " + " & ".join(values) + " " + end)
    table(root / "paper/tables/headline_results.tex", lines + [r'\bottomrule', r'\end{tabular}'])
    lines = [r'\begin{tabular}{@{}llrrrrr@{}}', r'\toprule', r'Kernel & Profile & Instr. & Bytes & Branches & Calls & Panic refs. \\', r'\midrule']
    metrics = read(root / "data/processed/mode_b_codegen_metrics.csv")
    safe = next(r for r in metrics if r["workload"] == "FFT_I16" and r["language"] == "rust" and r["mode"] == "B")
    unchecked = next(r for r in read(root / "data/processed/mode_b_fft_unchecked_codegen.csv") if r["profile"] == "RUST_UNCHECKED")
    for label, row in (("Safe Rust", safe), ("Audited transform", unchecked)):
        lines.append(f"FFT & {label} & " + " & ".join(row[k] for k in ("instruction_count", "code_span_bytes", "branch_count", "call_count", "bounds_panic_refs")) + " " + end)
    table(root / "paper/tables/fft_transformation.tex", lines + [r'\bottomrule', r'\end{tabular}'])
    lines = [r'\begin{tabular}{@{}llrr@{}}', r'\toprule', r'Workload/profile & Language & Median (\(\mu\)s) & B/A \\', r'\midrule']
    selected = [('CRC32','COMPILER_PERF','c_cpp','CRC GCC -O2'),('CRC32','COMPILER_PERF','rust','CRC Rust opt-3'),('SHA256','COMPILER_PERF','c_cpp','SHA GCC -O2'),('SHA256','COMPILER_PERF','rust','SHA Rust opt-3'),('FFT_I16_UNCHECKED','RUST_UNCHECKED','rust','FFT audited transform'),('SHA256_HW','HW_SHA','c_cpp','SHA hardware path')]
    for workload, profile, language, label in selected:
        row = next(r for r in mode_b if r["workload"] == workload and r["optimization"] == profile and r["language"] == language and r["input_size"] == "1024")
        lines.append(f'{label} & {LABELS[language]} & {float(row["mode_b_median_us"]):.3f} & {float(row["mode_b_over_mode_a_median"]):.3f} ' + end)
    table(root / "paper/tables/mode_b_selected.tex", lines + [r'\bottomrule', r'\end{tabular}'])
    lines = [r'\begin{longtable}{@{}llrrr@{}}', r'\toprule', r'Workload & Language & Local C6 median & Published mean & Published/local mean \\', r' & & \multicolumn{2}{c}{Time (\(\mu\)s)} & \\', r'\midrule', r'\endhead']
    for row in largest:
        lines.append(f'{NAMES[row["workload"]]} & {LABELS[row["language"]]} & {fmt(float(row["esp32c6_median_us"]))} & {fmt(float(row["plauska_mean_us"]))} & {float(row["plauska_over_esp32c6_mean"]):.3f} ' + end)
    table(root / "paper/supplement/historical_local_matrix.tex", lines + [r'\bottomrule', r'\end{longtable}'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    analyse(parser.parse_args().root.resolve())
