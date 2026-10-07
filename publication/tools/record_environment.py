"""Preserve actual supporting tool versions, not inferred metadata."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
lines = []
for command in ([sys.executable, "--version"], [str(root / ".tools/tectonic/tectonic.exe"), "--version"], ["pdfinfo", "-v"], ["pdffonts", "-v"], ["pdftoppm", "-v"]):
    result = subprocess.run(["rtk", "proxy", *command], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert result.returncode == 0
    lines.extend(["COMMAND " + " ".join(command), result.stdout, result.stderr, "EXIT " + str(result.returncode)])
path = root / "publication/validation/ENVIRONMENT.txt"
path.write_text("\n".join(lines), encoding="utf-8")
print("SUPPORTING_TOOL_VERSIONS_RECORDED")
