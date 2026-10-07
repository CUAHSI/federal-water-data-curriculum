#!/usr/bin/env python3
"""Check that every link in the course's Markdown pages resolves.

Usage:
    python3 .claude/scripts/check_links.py                 # all .md files in the repo
    python3 .claude/scripts/check_links.py 03-*/*.md       # specific files
    python3 .claude/scripts/check_links.py --changed       # only files changed vs upstream/dev (falls back to origin/dev, then main)

Checks
  * external http(s) links: HEAD then GET, follows redirects; 2xx/3xx = ok
    (401/403/429 are reported as "unverified", not broken — many APIs and
    Earthdata pages refuse anonymous bots)
  * relative links to other files in the repo, including #anchors that must
    match a heading in the target page
  * bare URLs inside code blocks are skipped (they are often API templates)

Exit code 1 if any link is broken. Standard library only.
"""
import argparse
import concurrent.futures as cf
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
AUTO_LINK = re.compile(r"<(https?://[^>\s]+)>")
BARE_URL = re.compile(r"(?<![(<\"'`])\bhttps?://[^\s)>\]\"'`]+")
FENCE = re.compile(r"^\s*(```|~~~)")
UA = "Mozilla/5.0 (CUAHSI curriculum link checker)"
SKIP_HOSTS = ("localhost", "127.0.0.1", "example.com")


def strip_code(text: str) -> str:
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def slug(heading: str) -> str:
    h = re.sub(r"[`*_\[\]()]", "", heading.strip().lower())
    h = re.sub(r"[^\w\s-]", "", h)
    return re.sub(r"\s+", "-", h).strip("-")


def anchors(path: pathlib.Path) -> set[str]:
    found = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^#{1,6}\s+(.*)", line)
        if m:
            found.add(slug(m.group(1)))
        m = re.match(r"^\(([\w-]+)\)=\s*$", line)  # MyST label
        if m:
            found.add(m.group(1))
    return found


def check_url(url: str):
    url = url.rstrip(".,;:")
    if any(h in url for h in SKIP_HOSTS):
        return url, "skipped", ""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return url, "ok", str(r.status)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 429):
                status = ("unverified", str(e.code))
            elif method == "HEAD" and e.code in (400, 404, 405, 501):
                continue  # some servers reject HEAD; retry with GET
            else:
                return url, "broken", str(e.code)
            if method == "GET":
                return url, *status
        except Exception as e:  # DNS, TLS, timeout
            if method == "GET":
                return url, "broken", type(e).__name__
    return url, "unverified", "?"


def online() -> bool:
    for probe in ("https://www.usgs.gov", "https://www.noaa.gov", "https://www.nasa.gov"):
        try:
            urllib.request.urlopen(urllib.request.Request(probe, headers={"User-Agent": UA}), timeout=10)
            return True
        except urllib.error.HTTPError:
            return True
        except Exception:
            continue
    return False


def changed_files():
    out = ""
    for base in ("upstream/dev", "origin/dev", "upstream/main", "origin/main"):
        r = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"],
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            out = r.stdout
            break
    return [ROOT / p for p in out.split() if p.endswith(".md") and (ROOT / p).exists()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--changed", action="store_true")
    a = ap.parse_args()
    if a.changed:
        files = changed_files()
    elif a.files:
        files = [pathlib.Path(f).resolve() for f in a.files]
    else:
        files = [p for p in ROOT.rglob("*.md")
                 if "_build" not in p.parts and ".claude" not in p.parts
                 and "node_modules" not in p.parts]

    external, problems = {}, []
    for f in files:
        text = strip_code(f.read_text(encoding="utf-8"))
        links = set(MD_LINK.findall(text)) | set(AUTO_LINK.findall(text)) | set(BARE_URL.findall(text))
        rel = f.relative_to(ROOT)
        for link in links:
            if link.startswith(("http://", "https://")):
                external.setdefault(link.rstrip(".,;:"), []).append(str(rel))
            elif link.startswith(("mailto:", "#")):
                if link.startswith("#") and link[1:] not in anchors(f):
                    problems.append((str(rel), link, "missing anchor"))
            else:
                target, _, anchor = link.partition("#")
                tpath = (f.parent / target).resolve()
                if not tpath.exists():
                    problems.append((str(rel), link, "file not found"))
                elif anchor and tpath.suffix == ".md" and anchor not in anchors(tpath):
                    problems.append((str(rel), link, "missing anchor"))

    signed = [u for u in external if re.search(r"[?&](Expires|X-Amz-Expires|Signature|X-Amz-Signature)=", u)]
    for u in signed:
        for src in external.pop(u):
            problems.append((src, u[:90] + "...", "signed/expiring URL; link the landing page instead"))

    if external and not online():
        print("Network unavailable: external URLs were NOT checked. Run this where the web is reachable.")
        external = {}

    unverified = []
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        for url, status, code in pool.map(check_url, external):
            if status == "broken":
                for src in external[url]:
                    problems.append((src, url, f"HTTP {code}"))
            elif status == "unverified":
                unverified.append((url, code, external[url]))

    print(f"Checked {len(files)} files, {len(external)} external URLs.")
    for src, link, why in sorted(problems):
        print(f"BROKEN      {src}: {link}  ({why})")
    for url, code, srcs in sorted(unverified):
        print(f"UNVERIFIED  {', '.join(sorted(set(srcs)))}: {url}  ({code}; check by hand)")
    if not problems:
        print("No broken links.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
