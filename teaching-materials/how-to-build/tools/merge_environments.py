"""Merge the lesson environments (``environments/*.yml``) into the one course environment learners get.

The repo keeps one environment per lesson, so each lesson stays modular. Learners get a single file next to the
notebooks, ``teaching-materials/materials/notebooks/environment.yml`` (git-ignored, like the notebooks), with
the conda environment name ``open-water-data``. It lists every package any lesson needs, once, with the
strictest version constraint any lesson gives it, and says in a comment which notebooks need it (unless all do).

Usage (from the repo root):
    python teaching-materials/how-to-build/tools/merge_environments.py [--out PATH]

The build stops if two lessons give the same package different constraints (e.g. ``zarr>=3`` and ``zarr<3``)
or different channels: fix the lesson environments first. Standard library only; it reads only the simple
layout the lesson files use (``name``, ``channels``, ``dependencies`` with an optional ``pip:`` list).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ENVIRONMENTS = REPO_ROOT / "environments"
OUT = REPO_ROOT / "teaching-materials" / "materials" / "notebooks" / "environment.yml"
NAME = "open-water-data"
# lesson environments in course order (agency order NASA -> NOAA -> USGS), with the notebooks that use them
LESSONS = {
    "m03-swot": "Module 3 SWOT",
    "m03-nwm": "Module 3 NWM",
    "m03-wdfn": "Module 3 WDFN",
    "m04-synthesis": "Module 4",
}
JUPYTER = ("ipykernel", "jupyterlab", "ipywidgets")
SPEC = re.compile(r"^([A-Za-z0-9_.\-]+)\s*(.*)$")


def parse(path: Path) -> tuple[list[str], list[str], list[str]]:
    """Channels, conda dependencies and pip dependencies of one lesson file, without comments."""
    channels, conda, pip = [], [], []
    section, in_pip = None, False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" "):
            section, in_pip = line.split(":", 1)[0].strip(), False
            continue
        item = line.strip()
        if not item.startswith("- "):
            continue
        item = item[2:].strip()
        if section == "channels":
            channels.append(item)
        elif section == "dependencies":
            if item == "pip:":
                in_pip = True
            elif in_pip and len(line) - len(line.lstrip()) > 4:
                pip.append(item)
            else:
                in_pip = False
                conda.append(item)
    return channels, conda, pip


def add(merged: dict, spec: str, env: str, where: str) -> None:
    m = SPEC.match(spec.replace(" ", ""))
    if not m:
        raise SystemExit(f"{env}: can't read the {where} dependency {spec!r}")
    name, constraint = m.group(1).lower(), m.group(2)
    entry = merged.setdefault(name, {"constraint": "", "envs": []})
    if constraint and entry["constraint"] and constraint != entry["constraint"]:
        raise SystemExit(f"{name}: {env} needs {constraint!r} but another lesson needs {entry['constraint']!r}; "
                         "make the lesson environments agree first")
    entry["constraint"] = entry["constraint"] or constraint
    entry["envs"].append(env)


def line(name: str, entry: dict) -> str:
    text = f"{name}{entry['constraint']}"
    envs = entry["envs"]
    if len(envs) == len(LESSONS) or name in JUPYTER:
        return text
    return f"{text:<26}# {', '.join(LESSONS[e] for e in envs)}"


def merge() -> str:
    channels, conda, pip = None, {}, {}
    for env in LESSONS:
        path = ENVIRONMENTS / f"{env}.yml"
        if not path.exists():
            raise SystemExit(f"missing {path.relative_to(REPO_ROOT)}")
        ch, deps, pips = parse(path)
        if channels is not None and ch != channels:
            raise SystemExit(f"{env}: channels {ch} differ from the other lessons' {channels}")
        channels = ch
        for d in deps:
            add(conda, d, env, "conda")
        for d in pips:
            add(pip, d, env, "pip")
    unknown = sorted(p.stem for p in ENVIRONMENTS.glob("*.yml") if p.stem not in LESSONS)
    if unknown:
        raise SystemExit(f"environments not in LESSONS (add them to this script): {', '.join(unknown)}")

    first = [n for n in ("python",) if n in conda]
    jupyter = [n for n in JUPYTER if n in conda]
    rest = [n for n in conda if n not in first + jupyter + ["pip"]]
    out = ["# Conda environment for all the notebooks of Reproducible Workflows with Open Water Data:",
           "# NASA, NOAA, USGS River Data Access (CUAHSI).",
           "# Create it once, in a terminal in this folder, then choose the \"Python (open-water-data)\" kernel:",
           "#   conda env create -f environment.yml",
           f"#   conda run -n {NAME} python -m ipykernel install --user --name {NAME} "
           f"--display-name \"Python ({NAME})\"",
           f"name: {NAME}", "channels:"]
    out += [f"  - {c}" for c in channels]
    out += ["dependencies:"]
    out += [f"  - {line(n, conda[n])}" for n in first + rest]
    out += ["  # for running the notebooks in Jupyter"]
    out += [f"  - {line(n, conda[n])}" for n in jupyter]
    if pip:
        out += ["  - pip", "  - pip:"]
        out += [f"      - {line(n, pip[n])}" for n in pip]
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=OUT, help=f"where to write it (default: {OUT.relative_to(REPO_ROOT)})")
    args = ap.parse_args(argv)
    text = merge()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {args.out} from {len(LESSONS)} lesson environments.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
