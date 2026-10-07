"""Validate and record the exact local archive approved for preparation only."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--package", required=True, type=Path)
args = parser.parse_args()
package = args.package.resolve()
assert ROOT in package.parents
archive = Path(str(package) + ".zip")
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))
subprocess.run(["rtk", "proxy", "python", "verify_package.py"], cwd=package, check=True)
manifest = read(package / "manifest.csv")
paths = {row["path"] for row in manifest}
roots = {"README.md", "LICENSING.md", "LICENSE-MIT.txt", "ZENODO_METADATA.json", "PLATFORM_REVIEW.md", "analysis.py", "verify_package.py", "build_paper.py", "source_lineage.csv"}
prefixes = ("data/", "results/", "paper/", "matlab/", "validation/")
assert all(p in roots or p.startswith(prefixes) for p in paths)
assert not any(p.endswith((".elf", ".bin", ".o", ".a", ".map", ".fig")) for p in paths)
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    assert set(bundle.namelist()) == paths | {"manifest.csv"}
    assert all(hashlib.sha256(bundle.read(row["path"])).hexdigest() == row["sha256"] for row in manifest)
# Compare every critical input with the files actually exercised after extraction.
exercised = json.loads((ROOT / "publication/validation/EXERCISED_INPUT_HASHES.json").read_text(encoding="utf-8"))
assert all(sha(package / p) == digest for p, digest in exercised.items())
assert "REPRODUCTION_PASS" in (package / "validation/REPRODUCTION.txt").read_text(encoding="utf-8")
preflight = (package / "validation/REVIEW_PDF_PREFLIGHT.txt").read_text(encoding="utf-8")
for name in ("review-manuscript.pdf", "review-supplement.pdf"):
    assert sha(package / "paper" / name) in preflight
# Detect common credential formats; never print a match or credential value.
patterns = (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", r"gh[pousr]_[A-Za-z0-9]{30,}", r"github_pat_[A-Za-z0-9_]{40,}", r"AKIA[0-9A-Z]{16}")
scanned = 0
for relative in paths:
    if Path(relative).suffix in {".md", ".txt", ".json", ".csv", ".tex", ".bib", ".py", ".m"}:
        text = (package / relative).read_text(encoding="utf-8-sig")
        assert not any(re.search(pattern, text) for pattern in patterns), "credential-pattern check failed: " + relative
        scanned += 1
assert archive.stat().st_size < 50_000_000_000
metadata = json.loads((package / "ZENODO_METADATA.json").read_text(encoding="utf-8"))
assert metadata["doi"] is None and metadata["record_url"] is None and metadata["publication_date"] is None
rows = read(package / "data/local_timings.csv")
assert len(rows) == 21600
retained = ROOT / "publication/packages" / archive.name
retained.parent.mkdir(parents=True, exist_ok=True)
if retained.exists():
    assert sha(retained) == sha(archive), "never overwrite a different approved archive"
else:
    shutil.copyfile(archive, retained)
approval = dict(prepared_on="2026-10-07", status="approved_for_preparation_only", public_deposit_authorized=False,
    platform="Zenodo", version="1.0.0-analysis-archive", doi=None, record_url=None,
    archive_path=retained.relative_to(ROOT).as_posix(), archive_sha256=sha(archive), archive_bytes=archive.stat().st_size,
    manifest_sha256=sha(package / "manifest.csv"), file_count_including_manifest=len(manifest)+1,
    observations=21600, timing_groups=216, ratios=176, tables=4, figures=4,
    manuscript_pages=9, supplement_pages=2,
    manuscript_sha256=sha(package / "paper/review-manuscript.pdf"),
    supplement_sha256=sha(package / "paper/review-supplement.pdf"),
    credential_pattern_scanned_text_files=scanned, exercised_input_hashes=exercised,
    limitation="Analysis-only reproduction; imported historical/static metrics are not re-audited. No firmware, hardware, correctness rerun or full binary audit. Not external peer review or full-repository rights clearance.")
(ROOT / "publication/APPROVED_PACKAGE.json").write_text(json.dumps(approval, indent=2) + "\n", encoding="utf-8")
print("LOCAL_PREPARATION_APPROVAL_PASS", sha(archive), "files", len(manifest)+1, "bytes", archive.stat().st_size)
