"""setup.py - install the linters prose-lint drives into ~/.prose-lint.

    python setup.py

Copies the textlint and vale configs from assets/ to ~/.prose-lint (or
$PROSE_LINT_HOME), runs `npm install` for textlint and `vale sync` for proselint,
and copies the sample register to vocabulary.md unless one is already there.
The directory sits outside the plugin, so an update of the plugin keeps it.
Safe to run again: package.json is refreshed, while a config file already in
place (.textlintrc*.json, .vale.ini) is kept as edited. A missing or failing npm
or vale is reported and skipped.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
HOME = Path(os.environ.get("PROSE_LINT_HOME") or Path.home() / ".prose-lint")


def run(tool, args, cwd):
    exe = shutil.which(tool)
    if not exe:
        print(f"skip: {tool} not found on PATH")
        return
    print(f"run: {tool} {' '.join(args)} in {cwd}")
    try:
        subprocess.run([exe, *args], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"fail: {tool} exited {exc.returncode}; rerun setup.py once the cause is fixed")


def main():
    HOME.mkdir(parents=True, exist_ok=True)
    for name in ("textlint", "vale"):
        for src in (ASSETS / name).iterdir():
            dst = HOME / name / src.name
            dst.parent.mkdir(exist_ok=True)
            if src.name.startswith(".") and dst.exists():
                continue
            shutil.copy(src, dst)
    run("npm", ["install", "--no-audit", "--no-fund"], HOME / "textlint")
    run("vale", ["--config", str(HOME / "vale" / ".vale.ini"), "sync"], HOME / "vale")
    reg = HOME / "vocabulary.md"
    if not reg.exists():
        shutil.copy(ASSETS / "vocabulary.sample.md", reg)
    print(f"ready: {HOME}")


if __name__ == "__main__":
    sys.exit(main())
