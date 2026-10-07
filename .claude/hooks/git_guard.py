#!/usr/bin/env python3
"""PreToolUse guard for Bash commands in the federal-water-data-curriculum repo.

Blocks (exit code 2, reason on stderr) any command that would:
  * push to main/master/dev (explicitly, via HEAD:main, or implicitly while on main)
  * push with --all / --mirror / --force / --delete or a ":branch" delete refspec
  * commit while the current branch is main/master
  * merge a pull request (gh pr merge, gh api .../merge) or run `git merge` on main

Permission rules in settings.json cover the common spellings; this hook catches
the variants (chained commands, `git -C`, flags in odd positions).
"""
import json
import re
import shlex
import subprocess
import sys

PROTECTED = {"main", "master", "dev", "develop"}


def block(msg: str) -> None:
    print(f"BLOCKED by git_guard: {msg}", file=sys.stderr)
    sys.exit(2)


def current_branch(cwd: str | None) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def segments(command: str):
    """Split a shell line on ; && || | and newlines, then tokenize each piece."""
    for part in re.split(r"&&|\|\||;|\||\n", command):
        part = part.strip()
        if not part:
            continue
        try:
            yield shlex.split(part)
        except ValueError:
            yield part.split()


def strip_git_globals(tokens):
    """Return (subcommand, args, -C dir) for a `git ...` token list."""
    i, cdir = 1, None
    while i < len(tokens) and tokens[i].startswith("-"):
        if tokens[i] in ("-C", "-c", "--git-dir", "--work-tree") and i + 1 < len(tokens):
            if tokens[i] == "-C":
                cdir = tokens[i + 1]
            i += 2
        else:
            i += 1
    if i >= len(tokens):
        return None, [], cdir
    return tokens[i], tokens[i + 1:], cdir


def check_push(args, cwd):
    flags = [a for a in args if a.startswith("-")]
    positional = [a for a in args if not a.startswith("-")]
    bad_flags = {"--all", "--mirror", "--force", "-f", "--force-with-lease",
                 "--delete", "-d", "--prune", "--force-if-includes"}
    for f in flags:
        if f in bad_flags or f.startswith("--force-with-lease") or (
            re.fullmatch(r"-[a-zA-Z]+", f) and "f" in f[1:]
        ):
            block(f"`git push {f}` is not allowed. Push a feature branch normally.")
    refspecs = positional[1:]  # first positional is the remote
    if not refspecs:
        branch = current_branch(cwd)
        if branch in PROTECTED or branch == "HEAD" or not branch:
            block(f"implicit push while on '{branch or 'unknown'}'. "
                  "Switch to a feature branch and push it by name.")
        return
    for spec in refspecs:
        spec = spec.lstrip("+")
        if spec.startswith(":"):
            block("deleting remote branches is not allowed.")
        dest = spec.split(":", 1)[-1]
        dest = dest.removeprefix("refs/heads/")
        src = spec.split(":", 1)[0]
        if dest in PROTECTED:
            block(f"pushing to '{dest}' is never allowed. Open a PR from a feature branch.")
        if src in ("HEAD", "@") and ":" not in spec:
            if current_branch(cwd) in PROTECTED:
                block("pushing HEAD while on a protected branch.")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if payload.get("tool_name") != "Bash":
        sys.exit(0)
    command = (payload.get("tool_input") or {}).get("command", "")
    cwd = payload.get("cwd")

    for tokens in segments(command):
        # skip leading env assignments like FOO=bar git push
        while tokens and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0]):
            tokens = tokens[1:]
        if not tokens:
            continue
        prog = tokens[0].rsplit("/", 1)[-1]

        if prog == "gh":
            joined = " ".join(tokens[1:])
            if re.search(r"\bpr\s+merge\b", joined):
                block("Claude never merges pull requests. Ask Lindsay to review and merge.")
            if tokens[1:2] == ["api"] and re.search(r"merge|/git/refs", joined):
                block("merging or moving refs through the GitHub API is not allowed.")
            if re.search(r"\bpr\s+(create|edit)\b.*--auto", joined):
                block("auto-merge is not allowed.")
            continue

        if prog != "git":
            continue
        sub, args, cdir = strip_git_globals(tokens)
        wd = cdir or cwd
        if sub == "push":
            check_push(args, wd)
        elif sub == "commit":
            if current_branch(wd) in PROTECTED:
                block("committing on a protected branch (main/dev) is not allowed. "
                      "Run `git switch -c <type>/<topic>` first; your changes come with you.")
        elif sub == "merge":
            if current_branch(wd) in PROTECTED:
                block("merging into main/dev is not allowed; that happens through a reviewed PR.")
        elif sub in ("update-ref",) or (sub == "branch" and any(a in ("-f", "--force", "-D") for a in args)):
            block(f"`git {sub}` with force/ref rewriting is not allowed.")

    sys.exit(0)


if __name__ == "__main__":
    main()
