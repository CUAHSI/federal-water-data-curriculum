#!/usr/bin/env python3
"""Check that every external link on a course page has an entry in that page's reference file.

Each page in scope (Modules 2-4, the landing page and the Glossary) has one reference file,
references/<page-key>.md, where <page-key> is "m" + the module folder's number + "-" + the page's file name, e.g.
03-federal-water-data-access-retrieval/01_access_nasa_swot.md -> references/m03-01_access_nasa_swot.md.
Top-level pages use their own name (index.md -> references/index.md).
references.md includes all of them to make the course-wide References page (STYLE_GUIDE section 8).

Usage (from the repository root):
    python3 references/check_references.py               # every page in scope
    python3 references/check_references.py 03-*/*.md     # specific pages
    python3 references/check_references.py --changed     # pages (or their reference files) changed vs upstream/dev

A link "has an entry" when its URL (ignoring #fragment, trailing slash and http/https) appears in the
page's reference file. Links inside code blocks and inline code are skipped (they are often API templates).
Reference entries whose URL no longer appears on the page are reported as "unused" (warning only).

Exit code 1 if a page has no reference file or has a link with no entry. Standard library only.
"""
import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REF_DIR = ROOT / "references"
FENCE = re.compile(r"^\s*(```|~~~)")
URL = re.compile(r"https?://[^\s)>\]\"'`<]+")
SKIP_HOSTS = ("localhost", "127.0.0.1", "example.com")
# Pages that must keep references. Module 1 is read-only for this pass.
SCOPE = ["index.md", "glossary.md", "02-*/*.md", "03-*/*.md", "04-*/*.md"]


def page_key(page: pathlib.Path) -> str:
    rel = page.resolve().relative_to(ROOT)
    if len(rel.parts) == 1:
        return rel.stem
    return f"m{rel.parts[0][:2]}-{rel.stem}"


def ref_file(page: pathlib.Path) -> pathlib.Path:
    return REF_DIR / f"{page_key(page)}.md"


def strip_code(text: str) -> str:
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        out.append("" if in_fence else re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def norm(url: str) -> str:
    url = url.rstrip(".,;:").split("#", 1)[0]
    url = re.sub(r"^https?://", "", url)
    return url.rstrip("/").lower()


def urls(text: str) -> list[str]:
    seen, out = set(), []
    for u in URL.findall(text):
        u = u.rstrip(".,;:")
        if any(h in u for h in SKIP_HOSTS) or norm(u) in seen:
            continue
        seen.add(norm(u))
        out.append(u)
    return out


def in_scope() -> list[pathlib.Path]:
    pages = []
    for pat in SCOPE:
        pages += sorted(p.resolve() for p in ROOT.glob(pat))
    return pages


def changed_pages() -> list[pathlib.Path]:
    out = ""
    for base in ("upstream/dev", "origin/dev", "upstream/main", "origin/main"):
        r = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            out = r.stdout
            break
    r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    out += "\n" + "\n".join(line[3:] for line in r.stdout.splitlines())
    changed = {(ROOT / p.strip()).resolve() for p in out.split() if p.strip()}
    # a changed reference file means its page is re-checked too
    return [p for p in in_scope() if p in changed or ref_file(p).resolve() in changed]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--changed", action="store_true")
    a = ap.parse_args()
    if a.changed:
        pages = changed_pages()
    elif a.files:
        pages = [pathlib.Path(f).resolve() for f in a.files]
    else:
        pages = in_scope()

    missing_total, failed = 0, False
    for page in pages:
        rel = page.relative_to(ROOT).as_posix()
        rf = ref_file(page)
        page_urls = urls(strip_code(page.read_text(encoding="utf-8")))
        if not rf.exists():
            print(f"NO REFERENCE FILE  {rel} -> {rf.relative_to(ROOT).as_posix()} ({len(page_urls)} links)")
            failed = True
            continue
        ref_urls = URL.findall(rf.read_text(encoding="utf-8"))
        ref_norm = {norm(u) for u in ref_urls}
        page_norm = {norm(u) for u in page_urls}
        missing = [u for u in page_urls if norm(u) not in ref_norm]
        unused = sorted({u.rstrip(".,;:") for u in ref_urls if norm(u) not in page_norm})
        status = "ok" if not missing else f"{len(missing)} missing"
        print(f"{status:>12}  {rel}  ({len(page_urls)} links; {rf.relative_to(ROOT).as_posix()})")
        for u in missing:
            print(f"      MISSING  {u}")
        for u in unused:
            print(f"      unused   {u}")
        missing_total += len(missing)
        failed = failed or bool(missing)
    print(f"\n{len(pages)} pages checked, {missing_total} links without a reference entry")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
