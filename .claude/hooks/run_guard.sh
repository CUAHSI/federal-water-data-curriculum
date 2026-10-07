#!/usr/bin/env bash
# Runs git_guard.py with whatever Python is available (python3, python, or the Windows `py` launcher).
# Fails CLOSED: if no working Python 3.10+ is found, every Bash command is blocked with a message,
# so the guardrails can never silently switch off (e.g. Windows' Microsoft Store "python3" stub).
GUARD="${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/git_guard.py"
for py in python3 python py; do
  if command -v "$py" >/dev/null 2>&1 && \
     "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' </dev/null >/dev/null 2>&1; then
    exec "$py" "$GUARD"
  fi
done
echo "git_guard: no Python 3.10+ found on PATH, so all shell commands are blocked to keep the git guardrails on. Fix: make 'python' available in Git Bash (e.g. run 'conda init bash' and reopen the terminal), then restart Claude Code." >&2
exit 2
