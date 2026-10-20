"""Verify every file in an extracted deposited snapshot before reproduction."""
from pathlib import Path
import csv
import hashlib

root = Path(__file__).resolve().parent
with (root / "manifest.csv").open(encoding="utf-8", newline="") as stream:
    rows = list(csv.DictReader(stream))
assert len({row["path"] for row in rows}) == len(rows)
actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name != "manifest.csv" and "__pycache__" not in p.parts}
assert actual == {row["path"] for row in rows}, "snapshot has missing or extra files"
for row in rows:
    relative = Path(row["path"])
    assert not relative.is_absolute() and ".." not in relative.parts
    path = root / relative
    assert path.is_file(), row["path"]
    assert path.stat().st_size == int(row["byte_size"]), row["path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], row["path"]
print(f"PACKAGE_HASH_PASS files={len(rows)}")
