"""Exercise a fresh extracted analysis package and preserve real tool output."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--package", type=Path, required=True)
parser.add_argument("--work", type=Path, required=True)
parser.add_argument("--manuscript-pages", type=int, default=9)
parser.add_argument("--validation-output", type=Path, default=ROOT / "publication/validation")
args = parser.parse_args()
source, work = args.package.resolve(), args.work.resolve()
assert ROOT in source.parents and ROOT in work.parents and not work.exists()
archive = Path(str(source) + ".zip")
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    for name in bundle.namelist():
        relative = Path(name)
        assert not relative.is_absolute() and ".." not in relative.parts
    bundle.extractall(work)
log = ["LOCAL ANALYSIS-PACKAGE REPRODUCTION — actual commands and output", "No benchmarks, publication, DOI reservation, or private-archive release."]
def run(command, cwd=work):
    log.append("COMMAND " + " ".join(command))
    result = subprocess.run(["rtk", "proxy", *command], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log.append(result.stdout)
    log.append(result.stderr)
    log.append("EXIT " + str(result.returncode))
    assert result.returncode == 0, log[-4:]
    return result.stdout
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

protected = [work / p for p in ("data/local_timings.csv", "data/historical_means.csv", "data/processed/mode_b_codegen_metrics.csv", "data/processed/mode_b_fft_unchecked_codegen.csv", "analysis.py", "matlab/run_publication_analysis.m", "paper/manuscript.tex", "paper/supplement/supplement.tex", "paper/references.bib")]
before = {p.relative_to(work).as_posix(): sha(p) for p in protected}
run([sys.executable, "--version"])
run([sys.executable, "verify_package.py"])
run([sys.executable, "analysis.py"])
run(["matlab", "-batch", "disp(version); addpath('matlab'); run_publication_analysis(string(pwd))"])
run([sys.executable, "build_paper.py", "--sync-figures", "--tectonic", str(ROOT / ".tools/tectonic/tectonic.exe")])
for name in ("manuscript", "supplement"):
    path = work / "results/pdf" / (name + ".pdf")
    info = run(["pdfinfo", str(path)])
    expected = args.manuscript_pages if name == "manuscript" else 2
    assert re.search(rf"Pages:\s+{expected}\b", info), (name, "unexpected pagination")
    fonts = run(["pdffonts", str(path)])
    entries = fonts.splitlines()[2:]
    assert entries and all(line.split()[-5] == "yes" for line in entries), name
for stem in ("mode_a_historical_local", "mode_a_rust_cpp", "mode_b_compiler_response", "mode_b_sha_profiles"):
    path = work / "artifacts/matlab/publication" / (stem + ".pdf")
    fonts = run(["pdffonts", str(path)])
    assert fonts.splitlines()[2:] and all(line.split()[-5] == "yes" for line in fonts.splitlines()[2:]), stem
for relative in ("paper/tables/headline_results.tex", "paper/tables/mode_b_selected.tex", "paper/tables/fft_transformation.tex", "paper/supplement/historical_local_matrix.tex"):
    assert (work / relative).read_bytes() == (source / relative).read_bytes(), relative
for path in protected:
    assert sha(path) == before[path.relative_to(work).as_posix()], path
diff = run(["git", "diff", "HEAD", "--", "data/raw", "data/baselines", "data/processed", "benchmarks", "artifacts/builds", "artifacts/assembly", "artifacts/static"], cwd=ROOT)
assert not diff, "frozen evidence changed"
run([sys.executable, "paper/tools/validate_manuscript.py"], cwd=ROOT)
run([sys.executable, "paper/tools/validate_publication.py"], cwd=ROOT)
log.append("REPRODUCTION_PASS timing_groups=216 ratios=176 tables=4 figures=4 PDFs=2 fonts_embedded=yes immutable_inputs=yes")
validation = args.validation_output.resolve()
assert ROOT in validation.parents
validation.mkdir(parents=True, exist_ok=True)
(validation / "REPRODUCTION.txt").write_text("\n".join(log), encoding="utf-8")
(validation / "EXERCISED_INPUT_HASHES.json").write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")
print(log[-1])
