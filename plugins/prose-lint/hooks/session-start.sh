#!/usr/bin/env bash
# session-start.sh - run setup.py once per plugin version, in the background.
#
# The SessionStart hook calls this on every session. It returns at once when
# $PROSE_LINT_HOME/.setup-version names this plugin's version. Otherwise it
# fetches uv into $PROSE_LINT_HOME/bin when uv is not on PATH (uv then fetches
# Python), runs setup.py, and prints one line for Claude with the log's path.

H="${PROSE_LINT_HOME:-$HOME/.prose-lint}"
# Git Bash: C:/x would split PATH at its colon.
command -v cygpath >/dev/null 2>&1 && H=$(cygpath -u "$H")
ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
want=$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$ROOT/.claude-plugin/plugin.json" | head -n 1)
[ "$(cat "$H/.setup-version" 2>/dev/null)" = "$want" ] && exit 0

mkdir -p "$H/bin"
# Two sessions starting together would run npm install into one directory.
lock="$H/.setup-lock"
[ -n "$(find "$lock" -maxdepth 0 -mmin +30 2>/dev/null)" ] && rmdir "$lock"
if ! mkdir "$lock" 2>/dev/null; then
  echo "prose-lint: setup is already running in another session; its log is $H/setup.log"
  exit 0
fi
trap 'rmdir "$lock"' EXIT
log="$H/setup.log"
export PATH="$PATH:$H/bin"

UV=0.13.6
if ! command -v uv >/dev/null 2>&1; then
  case "$(uname -m)" in arm64 | aarch64) arch=aarch64 ;; *) arch=x86_64 ;; esac
  case "$(uname -s)" in
    Darwin) asset="uv-$arch-apple-darwin.tar.gz" ;;
    Linux) asset="uv-$arch-unknown-linux-gnu.tar.gz" ;;
    *) asset="uv-$arch-pc-windows-msvc.zip" ;;
  esac
  # SHA-256 from the .sha256 file beside each asset of the uv release.
  case "$asset" in
    uv-x86_64-pc-windows-msvc.zip) sum=a2a8820d5eea32f08ef467ef3b7f66883a9b076d5737a2fc2fbb5f458d1bb50f ;;
    uv-aarch64-pc-windows-msvc.zip) sum=c2426c0c8e28b53d8c440e47a18d96ad4db51e159866c0e81435b196d7f0081c ;;
    uv-x86_64-unknown-linux-gnu.tar.gz) sum=f29c3e94ffabd7e6f3ba521dba169a9b7ec12100bf3257087f0f24f6123f3645 ;;
    uv-aarch64-unknown-linux-gnu.tar.gz) sum=229e194255c7958d86d56e8790d969a6f74736592133f0dfd0076f754c642c1d ;;
    uv-x86_64-apple-darwin.tar.gz) sum=63ba17fdda55ad1a230d4b37fc6017ffa10c23688c83818bd3bfdf914c652a02 ;;
    uv-aarch64-apple-darwin.tar.gz) sum=60fbd5c8a1ed681845eea28d9d622fcde03c51e91a43465b64a1e17db1ed3472 ;;
  esac
  tmp=$(mktemp -d)
  if curl -fsSL -o "$tmp/$asset" "https://github.com/astral-sh/uv/releases/download/$UV/$asset" &&
    [ "$( (sha256sum "$tmp/$asset" 2>/dev/null || shasum -a 256 "$tmp/$asset") | cut -d ' ' -f 1)" = "$sum" ]; then
    case "$asset" in
      *.zip) unzip -qo "$tmp/$asset" -d "$H/bin" ;;
      *) tar xzf "$tmp/$asset" -C "$H/bin" --strip-components 1 ;;
    esac
  fi
  rm -rf "$tmp"
fi
if ! command -v uv >/dev/null 2>&1; then
  echo "prose-lint: setup could not fetch uv; install uv, then run: uv run python \"$ROOT/skills/prose-lint/scripts/setup.py\""
  exit 0
fi

# --no-project keeps uv away from a pyproject.toml in the session's directory.
uv run --no-project python "$ROOT/skills/prose-lint/scripts/setup.py" >"$log" 2>&1
if [ "$(cat "$H/.setup-version" 2>/dev/null)" = "$want" ]; then
  echo "prose-lint: linters set up in $H (log: $log)"
else
  echo "prose-lint: setup left a layer unready; its skip and fail lines are in $log:"
  grep -E '^(skip|fail):' "$log"
fi
