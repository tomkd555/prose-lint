"""setup.py - install the linters prose-lint drives into ~/.prose-lint.

    python setup.py

Copies the textlint and vale configs from assets/ to ~/.prose-lint (or
$PROSE_LINT_HOME), runs `npm install` for textlint and `vale sync` for the vale
packages, and copies the sample registers to vocabulary.md and academic.md unless
they are already there. The directory sits outside the plugin, so an update of the plugin keeps
it. Safe to run again: package.json, the prh rule file and the AISigns vale
style are refreshed, while a config file already in place (.textlintrc*.json,
.vale.ini) is kept as edited. A missing or failing npm or vale is reported and
skipped.
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


def copy_tree(src: Path, dst: Path):
    """Copy src into dst; a dotfile already in dst is kept, everything else is refreshed."""
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        target = dst / path.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.name.startswith(".") and target.exists():
            continue
        shutil.copy(path, target)


def main():
    HOME.mkdir(parents=True, exist_ok=True)
    for name in ("textlint", "vale"):
        copy_tree(ASSETS / name, HOME / name)
    run("npm", ["install", "--no-audit", "--no-fund"], HOME / "textlint")
    run("vale", ["--config", str(HOME / "vale" / ".vale.ini"), "sync"], HOME / "vale")
    for sample, name in (("vocabulary.sample.md", "vocabulary.md"), ("academic.sample.md", "academic.md")):
        if not (HOME / name).exists():
            shutil.copy(ASSETS / sample, HOME / name)
    print(f"ready: {HOME}")


if __name__ == "__main__":
    sys.exit(main())
