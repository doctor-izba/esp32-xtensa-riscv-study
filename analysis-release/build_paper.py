"""Compile the supplied multi-file paper; optionally sync regenerated figures."""
from pathlib import Path
import argparse
import shutil
import subprocess

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tectonic", default="tectonic")
parser.add_argument("--sync-figures", action="store_true")
args = parser.parse_args()
if args.sync_figures:
    for stem in ("mode_a_historical_local", "mode_a_rust_cpp", "mode_b_compiler_response", "mode_b_sha_profiles"):
        for extension in (".pdf", ".png"):
            shutil.copyfile(root / "artifacts/matlab/publication" / (stem + extension), root / "paper/figures" / (stem + extension))
output = root / "results/pdf"
output.mkdir(parents=True, exist_ok=True)
for source, cwd, name in (("manuscript.tex", root / "paper", "manuscript"), ("supplement.tex", root / "paper/supplement", "supplement")):
    subprocess.run([args.tectonic, source, "--outdir", str(output), "--keep-logs"], cwd=cwd, check=True)
    assert (output / (name + ".pdf")).is_file()
print("PACKAGE_PDF_BUILD_PASS")
