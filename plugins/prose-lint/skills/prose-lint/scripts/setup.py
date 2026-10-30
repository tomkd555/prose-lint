"""setup.py - install the linters prose-lint drives into ~/.prose-lint.

    python setup.py

Copies the textlint and vale configs from assets/ to ~/.prose-lint (or
$PROSE_LINT_HOME), runs `npm install` for textlint and `vale sync` for the vale
packages, and copies the sample registers to vocabulary.md, academic.md,
translationese.md and slop.md unless they are already there. The directory
sits outside the plugin, so an update of the plugin keeps it; a register that
differs from the shipped sample is named so the new rows can be merged. Safe to run again: package.json, the prh rule file, the fukushi dictionary
and the AISigns vale style are refreshed, while a config file already in place (.textlintrc*.json,
.vale.ini) is kept as edited.

When vale or npm is not on PATH, the pinned release below is downloaded from
its official site, checked against its SHA-256 and unpacked under the home:
vale to bin/, Node with npm to node/. A failed download or a failing npm or
vale is reported and skipped. On success the plugin version goes to
.setup-version, which the plugin's SessionStart hook compares to decide on a
rerun.
"""
import hashlib
import io
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
HOME = Path(os.environ.get("PROSE_LINT_HOME") or Path.home() / ".prose-lint")
PLUGIN_JSON = Path(__file__).resolve().parents[3] / ".claude-plugin" / "plugin.json"
WINDOWS = sys.platform == "win32"

VALE = "3.25.1"
NODE = "v24.22.2"
# SHA-256 from vale_<VALE>_checksums.txt and node's SHASUMS256.txt.
SHA256 = {
    f"vale_{VALE}_Linux_64-bit.tar.gz": "4bf5c5176b682b1da0830f471584d3494f1c2e27ee3029e1ad6f6661d4962182",
    f"vale_{VALE}_Linux_arm64.tar.gz": "2a69755b68118c612c455fc0c5ea1b9438519aa1c852e3fb303b3ad97141bbb0",
    f"vale_{VALE}_Windows_64-bit.zip": "5f4b5cefee5d0f7ee0621d7cc035886515888fd732c4e8add36d3c922f2adc68",
    f"vale_{VALE}_Windows_arm64.zip": "d9182694306dfb9f8f22c27504822cd7829c42d969e13a20f2302bc989e93005",
    f"vale_{VALE}_macOS_64-bit.tar.gz": "e27097e84a812d45546de8d6a4ffa75538cab39c96f79b153b601240f8cefaf9",
    f"vale_{VALE}_macOS_arm64.tar.gz": "fbcaa68d9b9e229b9c8dc918f209e93572ce943039700b7e04a423ff12f684cd",
    f"node-{NODE}-darwin-arm64.tar.gz": "aa9549349e47dffaa42dcf95d6e06ade8c4bdafc980979883b88767670df385a",
    f"node-{NODE}-darwin-x64.tar.gz": "d5e336d588c45be0c37dbd52cc29895593009ca4997a77a1fd02815131ed0e52",
    f"node-{NODE}-linux-arm64.tar.gz": "95c264150aceb7f3437a29fd6984924f5f8d1511ea3cbd6c508b83f6c555dae2",
    f"node-{NODE}-linux-x64.tar.gz": "361718c444e49af2ca5a110c83ba6a8901143f23ab285ebbef0341f391f482a9",
    f"node-{NODE}-win-arm64.zip": "f47968c213105077f64c6510f007632c0ca2574802a0b5067c327c49abe1c468",
    f"node-{NODE}-win-x64.zip": "ca1bff5d8ead13c9f2ea404a176db46bd430704d5b5113734049fa365e7799e2",
}


def arm() -> bool:
    return platform.machine().lower() in ("arm64", "aarch64")


def fetch(url: str, name: str) -> bytes:
    """Download url and return its bytes once they match the pinned SHA-256 of name."""
    print(f"download: {url}")
    with urllib.request.urlopen(url, timeout=120) as resp:
        data = resp.read()
    if hashlib.sha256(data).hexdigest() != SHA256[name]:
        raise ValueError(f"SHA-256 mismatch for {name}")
    return data


def unpack(data: bytes, name: str, dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    if name.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            z.extractall(dest)
    else:
        with tarfile.open(fileobj=io.BytesIO(data)) as t:
            if hasattr(tarfile, "data_filter"):
                t.extractall(dest, filter="data")
            else:
                t.extractall(dest)


def ensure_vale():
    """Put the pinned vale in HOME/bin when no vale is on PATH."""
    exe = HOME / "bin" / ("vale.exe" if WINDOWS else "vale")
    if shutil.which("vale") or exe.exists():
        return
    osname = "Windows" if WINDOWS else "macOS" if sys.platform == "darwin" else "Linux"
    name = f"vale_{VALE}_{osname}_{'arm64' if arm() else '64-bit'}.{'zip' if WINDOWS else 'tar.gz'}"
    try:
        data = fetch(f"https://github.com/vale-cli/vale/releases/download/v{VALE}/{name}", name)
        tmp = HOME / "bin" / ".vale-unpack"
        shutil.rmtree(tmp, ignore_errors=True)
        unpack(data, name, tmp)
        shutil.move(str(tmp / exe.name), exe)
        shutil.rmtree(tmp, ignore_errors=True)
        exe.chmod(0o755)
    except (OSError, ValueError, KeyError) as exc:
        print(f"fail: vale download: {exc}")


def ensure_node():
    """Put the pinned Node with npm in HOME/node when no npm is on PATH."""
    if shutil.which("npm") or (HOME / "node").exists():
        return
    osname = "win" if WINDOWS else "darwin" if sys.platform == "darwin" else "linux"
    stem = f"node-{NODE}-{osname}-{'arm64' if arm() else 'x64'}"
    name = stem + (".zip" if WINDOWS else ".tar.gz")
    try:
        data = fetch(f"https://nodejs.org/dist/{NODE}/{name}", name)
        unpack(data, name, HOME)
        (HOME / stem).rename(HOME / "node")
    except (OSError, ValueError, KeyError) as exc:
        print(f"fail: node download: {exc}")


def tool_path():
    """Put HOME/bin and the downloaded Node in front of PATH for npm and vale."""
    dirs = [HOME / "bin", HOME / "node" if WINDOWS else HOME / "node" / "bin"]
    os.environ["PATH"] = os.pathsep.join([*map(str, dirs), os.environ.get("PATH", "")])


def run(tool, args, cwd) -> bool:
    exe = shutil.which(tool)
    if not exe:
        print(f"skip: {tool} not found on PATH")
        return False
    print(f"run: {tool} {' '.join(args)} in {cwd}")
    try:
        subprocess.run([exe, *args], cwd=cwd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"fail: {tool} exited {exc.returncode}; rerun setup.py once the cause is fixed")
        return False
    return True


def same(a: Path, b: Path) -> bool:
    """Compare two text files, ignoring CRLF against LF from a git checkout."""
    return a.read_bytes().replace(b"\r\n", b"\n") == b.read_bytes().replace(b"\r\n", b"\n")


def copy_tree(src: Path, dst: Path):
    """Copy src into dst; a dotfile the user edited is kept, everything else is refreshed."""
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        target = dst / path.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.name.startswith("."):
            # The copy of the last shipped config tells an untouched config from an edited one.
            shipped = target.with_name(target.name + ".shipped")
            edited = target.exists() and not (shipped.exists() and same(shipped, target))
            shutil.copy(path, shipped)
            if edited and not same(target, path):
                # A kept config can name a rule package this release dropped.
                print(f"kept: {target} differs from the shipped {path}; merge the changes by hand")
                continue
        shutil.copy(path, target)


def main():
    HOME.mkdir(parents=True, exist_ok=True)
    for name in ("textlint", "vale"):
        copy_tree(ASSETS / name, HOME / name)
    tool_path()
    ensure_node()
    ensure_vale()
    ok = run("npm", ["install", "--no-audit", "--no-fund"], HOME / "textlint")
    ok &= run("vale", ["--config", str(HOME / "vale" / ".vale.ini"), "sync"], HOME / "vale")
    for sample, name in (
        ("vocabulary.sample.md", "vocabulary.md"),
        ("academic.sample.md", "academic.md"),
        ("translationese.sample.md", "translationese.md"),
        ("slop.sample.md", "slop.md"),
    ):
        if not (HOME / name).exists():
            shutil.copy(ASSETS / sample, HOME / name)
        elif (HOME / name).read_bytes() != (ASSETS / sample).read_bytes():
            print(f"kept: {HOME / name} differs from the shipped {ASSETS / sample}; merge new rows by hand")
    if ok:
        version = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["version"] if PLUGIN_JSON.exists() else "manual"
        (HOME / ".setup-version").write_text(version + "\n", encoding="utf-8")
    print(f"ready: {HOME}")


if __name__ == "__main__":
    sys.exit(main())
