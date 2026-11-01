#!/usr/bin/env bash
# lint.sh - run hooks/lint.py with the tools setup.py downloaded on PATH.
#
# hooks.json calls this for PostToolUse (file), Stop (reply), UserPromptSubmit
# (inject) and PreToolUse (plan). The userConfig option lint_hooks reaches it as
# CLAUDE_PLUGIN_OPTION_LINT_HOOKS: false or 0 turns the hooks off, and an unset
# option counts as on, since an update shows no install dialog.

case "$CLAUDE_PLUGIN_OPTION_LINT_HOOKS" in false | False | 0) exit 0 ;; esac
dir=$(dirname "$0")
# Exit 0 on any failure, a missing uv included: exit 2 would hold a Stop or erase a prompt.
run() { sh "$dir/../bin/prose-lint-run" uv run -q --no-project --script "$dir/lint.py" "$1" 2>/dev/null || true; }
if [ "$1" = inject ]; then
  # A prompt with no findings waiting for its session needs no Python.
  input=$(cat)
  sid=$(printf '%s' "$input" | sed -n 's/.*"session_id" *: *"\([A-Za-z0-9_-]*\)".*/\1/p' | head -n 1)
  [ -f "${CLAUDE_PLUGIN_DATA:-/nonexistent}/reply-${sid:-nosid}.txt" ] || exit 0
  printf '%s' "$input" | run inject
else
  run "$1"
fi
