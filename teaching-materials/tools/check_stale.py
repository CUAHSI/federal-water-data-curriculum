"""List teaching materials that need rebuilding because their sources changed (STYLE_GUIDE §11).

Every generated output has an entry in ``teaching-materials/manifest.json``:

    {
      "output": "teaching-materials/slides/session-03_module-03_lesson-01_retrieve-nasa-swot-data.qmd",
      "kind": "slides",
      "sources": ["03-federal-water-data-access-retrieval/01_access_nasa_swot.md", "images/m03/..."],
      "source_commit": "<full SHA the output was built from>",
      "built_at": "2026-10-24T15:02:11Z",
      "builder": "build-slides"
    }

Paths are relative to the repo root. A directory in ``sources`` (e.g. ``images/m03``) covers every file
under it.

Usage:
    python teaching-materials/tools/check_stale.py
        For each entry, runs ``git diff --quiet <source_commit> HEAD -- <sources>`` and prints the stale
        outputs. Exit code 1 if any are stale (or can't be checked), 0 otherwise. Uncommitted edits to
        sources aren't counted: commit the lesson change first.

    python teaching-materials/tools/check_stale.py --update OUTPUT [--kind KIND] [--builder SKILL]
                                                   [--source PATH ...]
        After a rebuild: sets the entry's ``source_commit`` to HEAD and ``built_at`` to now (UTC). Creates the
        entry if it's new (then ``--kind``, ``--builder`` and at least one ``--source`` are required).
        ``--source`` replaces the entry's sources; leave it out to keep them.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "teaching-materials" / "manifest.json"
KINDS = ("slides", "reading", "notebook", "environment", "bundle-readme", "quiz", "instructor-guide")
FIELDS = ("output", "kind", "sources", "source_commit", "built_at", "builder")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True)


def repo_path(path: str) -> str:
    """Normalize a path to repo-relative POSIX form, whether given relative to the repo or the cwd."""
    p = Path(path)
    if not p.is_absolute():
        p = Path.cwd() / p
    try:
        return p.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def load() -> dict:
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def save(manifest: dict) -> None:
    manifest["outputs"].sort(key=lambda e: e["output"])
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")


def stale_reason(entry: dict) -> str | None:
    """Why an entry needs rebuilding, or None if it's current."""
    if not (REPO_ROOT / entry["output"]).exists():
        return "output file is missing"
    commit = entry.get("source_commit")
    if not commit:
        return "no source_commit recorded"
    if not entry.get("sources"):
        return "no sources recorded"
    if git("cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
        return f"source_commit {commit[:12]} is not in this clone (fetch, or rebuild)"
    diff = git("diff", "--quiet", commit, "HEAD", "--", *entry["sources"])
    if diff.returncode == 1:
        changed = git("diff", "--name-only", commit, "HEAD", "--", *entry["sources"]).stdout.split()
        return "sources changed: " + ", ".join(changed)
    if diff.returncode != 0:
        return f"git diff failed: {diff.stderr.strip()}"
    return None


def check(manifest: dict) -> int:
    stale = [(e["output"], r) for e in manifest["outputs"] if (r := stale_reason(e))]
    if not manifest["outputs"]:
        print("manifest.json has no outputs yet.")
    elif not stale:
        print(f"All {len(manifest['outputs'])} outputs are up to date.")
    for output, reason in stale:
        print(f"STALE  {output}\n       {reason}")
    if stale:
        print(f"\n{len(stale)} of {len(manifest['outputs'])} outputs need rebuilding.")
    return 1 if stale else 0


def update(manifest: dict, args: argparse.Namespace) -> int:
    output = repo_path(args.update)
    head = git("rev-parse", "HEAD")
    if head.returncode != 0:
        sys.exit(f"git rev-parse HEAD failed: {head.stderr.strip()}")
    entry = next((e for e in manifest["outputs"] if e["output"] == output), None)
    if entry is None:
        missing = [flag for flag, value in (("--kind", args.kind), ("--builder", args.builder),
                                            ("--source", args.source)) if not value]
        if missing:
            sys.exit(f"{output} is new to the manifest; also give {', '.join(missing)}")
        entry = {"output": output}
        manifest["outputs"].append(entry)
    if args.kind:
        entry["kind"] = args.kind
    if args.builder:
        entry["builder"] = args.builder
    if args.source:
        entry["sources"] = sorted({repo_path(s) for s in args.source})
    entry["source_commit"] = head.stdout.strip()
    entry["built_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # Keep the field order readable.
    entry_sorted = {k: entry[k] for k in FIELDS if k in entry}
    entry.clear()
    entry.update(entry_sorted)
    save(manifest)
    print(f"Updated {output} at {entry['source_commit'][:12]}")
    if not (REPO_ROOT / output).exists():
        print(f"Warning: {output} doesn't exist yet", file=sys.stderr)
    dirty = git("status", "--porcelain", "--", *entry["sources"]).stdout.strip()
    if dirty:
        print("Warning: these sources have uncommitted changes, so the output may not match HEAD:\n"
              + dirty, file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--update", metavar="OUTPUT", help="record a rebuild of OUTPUT at HEAD")
    parser.add_argument("--kind", choices=KINDS, help="with --update: the kind of output")
    parser.add_argument("--builder", help="with --update: the skill that built it, e.g. build-slides")
    parser.add_argument("--source", action="append", metavar="PATH",
                        help="with --update: a source path (repeat for each)")
    args = parser.parse_args(argv)
    if not args.update and (args.kind or args.builder or args.source):
        parser.error("--kind, --builder and --source go with --update")
    manifest = load()
    return update(manifest, args) if args.update else check(manifest)


if __name__ == "__main__":
    sys.exit(main())
