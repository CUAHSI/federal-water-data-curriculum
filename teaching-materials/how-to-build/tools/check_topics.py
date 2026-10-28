#!/usr/bin/env python3
"""Check the session topic lists in teaching-materials/how-to-build/topics/.

For each list it checks that:
- the deck minutes add up to the session length given in the header ("(90 min");
- every "Where" value is one of deck, notebook, reading, how-to, cut (or "deck + notebook", "deck + how-to");
- every "§ heading" in the Source column still exists as a heading in its lesson page, so a renamed or removed
  lesson section shows up here before a deck is built from it.

Usage (from the repo root):
    python teaching-materials/how-to-build/tools/check_topics.py            # all sessions
    python teaching-materials/how-to-build/tools/check_topics.py 3 4        # sessions 3 and 4
Exit code 1 if anything fails. Standard library only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOPICS = ROOT / "teaching-materials" / "how-to-build" / "topics"
WHERE = {"deck", "notebook", "reading", "how-to", "cut"}
MODULES = {
    "01": "01-data-best-practices",
    "02": "02-federal-water-data-landscape",
    "03": "03-federal-water-data-access-retrieval",
    "04": "04-federal-water-data-synthesis",
}


def page_headings(module, page):
    """Return the headings of lesson page NN in module MM, normalised for comparison."""
    folder = ROOT / MODULES[module]
    matches = sorted(folder.glob(f"{page}_*.md"))
    if not matches:
        return None
    text = matches[0].read_text(encoding="utf-8")
    return {norm(h) for h in re.findall(r"^#{1,4}\s+(.+?)\s*$", text, re.M)}


def norm(s):
    s = re.sub(r"\(intro\)$", "", s.strip())
    return re.sub(r"[`*_]", "", re.sub(r"\s+", " ", s)).strip().lower()


def check(path):
    problems = []
    text = path.read_text(encoding="utf-8")
    m = re.search(r"\((\d+) min", text)
    if not m:
        return [f"{path.name}: no session length like '(90 min' in the header"]
    length, total = int(m.group(1)), 0
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not cells[0].isdigit():
            continue
        num, topic, source, where, minutes = cells[0], cells[1], cells[2], cells[3], cells[4]
        parts = {w.strip() for w in where.split("+")}
        if not parts <= WHERE:
            problems.append(f"{path.name} row {num}: unknown Where value '{where}'")
        if minutes.isdigit():
            if "deck" not in parts and int(minutes):
                problems.append(f"{path.name} row {num}: minutes on a row that isn't on the deck")
            total += int(minutes)
        elif "deck" in parts:
            problems.append(f"{path.name} row {num}: deck row without minutes")
        # Source: "03/01 § Heading, § Heading" (several pages separated by ';' are allowed)
        for ref in source.split(";"):
            pm = re.match(r"\s*(\d\d)/(\d\d)\s*(.*)", ref)
            if not pm or "§" not in ref:
                continue
            module, page, rest = pm.groups()
            if module not in MODULES:
                continue
            heads = page_headings(module, page)
            if heads is None:
                problems.append(f"{path.name} row {num}: no lesson page {module}/{page}")
                continue
            for h in rest.split("§")[1:]:
                h = h.strip().rstrip(",").strip()
                if h.endswith("…"):
                    prefix = norm(h[:-1])
                    if not any(x.startswith(prefix) for x in heads):
                        problems.append(f"{path.name} row {num}: no heading starting '{h}' in {module}/{page}")
                elif norm(h) not in heads:
                    problems.append(f"{path.name} row {num}: no heading '{h}' in {module}/{page}")
    if total != length:
        problems.append(f"{path.name}: deck minutes add up to {total}, session is {length}")
    return problems


def main(argv):
    files = sorted(TOPICS.glob("session-*.md"))
    if argv:
        wanted = {f"session-{int(a):02d}.md" for a in argv}
        files = [f for f in files if f.name in wanted]
    problems = [p for f in files for p in check(f)]
    for p in problems:
        print(p)
    if not problems:
        print(f"{len(files)} topic list(s) OK.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
