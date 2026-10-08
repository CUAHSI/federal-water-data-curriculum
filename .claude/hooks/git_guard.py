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
ALLOWED_REMOTES = {"upstream"}
BRANCH_PATTERN = re.compile(r"^(content|chore|env|fix|docs)/[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*$")


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
    # Pushes must name the remote and the branch: `git push -u upstream <branch>`.
    if not positional:
        block("name the remote and branch explicitly: `git push -u upstream <branch>`.")
    remote, refspecs = positional[0], positional[1:]
    if remote not in ALLOWED_REMOTES:
        block(f"pushes go only to {', '.join(sorted(ALLOWED_REMOTES))} (the CUAHSI repo), not '{remote}'.")
    if not refspecs:
        block("name the branch explicitly: `git push -u upstream <branch>`.")
    for spec in refspecs:
        spec = spec.lstrip("+")
        if spec.startswith(":"):
            block("deleting remote branches is not allowed.")
        src, _, dest = spec.partition(":")
        dest = (dest or src).removeprefix("refs/heads/")
        if dest in ("HEAD", "@"):
            dest = current_branch(cwd)
        if dest in PROTECTED:
            block(f"pushing to '{dest}' is never allowed. Open a PR from a feature branch.")
        if not BRANCH_PATTERN.match(dest or ""):
            block(f"'{dest}' isn't an agent branch name. Use <type>/<topic> with type one of "
                  "content, chore, env, fix, docs (e.g. content/p6-m03-swot).")


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
            if re.search(r"\bpr\s+ready\b", joined):
                block("marking a PR ready for review is Lindsay's call; leave it as a draft.")
            if re.search(r"\bpr\s+create\b", joined):
                if "--draft" not in tokens and "-d" not in tokens:
                    block("open pull requests as drafts: add --draft.")
                base = None
                for i, tok in enumerate(tokens):
                    if tok in ("--base", "-B") and i + 1 < len(tokens):
                        base = tokens[i + 1]
                    elif tok.startswith("--base="):
                        base = tok.split("=", 1)[1]
                if base != "dev":
                    block("pull requests target dev: add --base dev.")
            if re.search(r"\bpr\s+edit\b", joined) and re.search(r"(--base|-B)[ =](?!dev\b)", joined):
                block("PRs stay based on dev.")
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
