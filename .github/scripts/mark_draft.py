#!/usr/bin/env python3
"""CI-only: label the dev preview build as a draft. Edits files in the CI checkout; never committed."""
import datetime
import pathlib
import re
import subprocess

root = pathlib.Path(__file__).resolve().parents[2]
sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root,
                     capture_output=True, text=True).stdout.strip() or "unknown"
today = datetime.date.today().isoformat()

# 1. Suffix the project title (the first `title:` under `project:` only, not toc section titles).
cfg = root / "myst.yml"
text = cfg.read_text()
text, n = re.subn(r'(?m)^(  title:\s*)"?([^"\n]+?)"?\s*$', r'\1"\2 — DRAFT (dev)"', text, count=1)
cfg.write_text(text)

# 2. Banner under the first H1 of every course page.
banner = (
    ":::{warning} Draft preview\n"
    f"This site is built automatically from the `dev` branch (commit {sha}, {today}) "
    "for internal and partner review. It is **not** the final course; content is incomplete "
    "and will change.\n:::\n"
)
pages = [root / "index.md", *sorted(root.glob("0*/[0-9]*.md"))]
for page in pages:
    body = page.read_text()
    m = re.search(r"(?m)^# .*\n", body)
    if m:
        body = body[: m.end()] + "\n" + banner + "\n" + body[m.end():]
    else:
        body = banner + "\n" + body
    page.write_text(body)
print(f"title updated: {bool(n)}; banner added to {len(pages)} pages")
