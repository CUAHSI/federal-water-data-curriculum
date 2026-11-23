"""Build the final-assessment PDFs: the grader packet and the learner instructions.

Usage (from the repo root, base Python with the `markdown` package):
    python teaching-materials/how-to-build/tools/assessment_pdfs.py teaching-materials/materials/assessment

Reads, from the assessment folder:
    final-assessment_grader-key.md   the grader packet source (figures linked as dryrun-figures/*.png)
    final-assessment_canvas.html     the learner page (the HTML pasted into Canvas)
Writes, into the same folder:
    final-assessment_grader-packet.pdf          figures embedded; sections 3-5 and each option start a page
    final-assessment_learner-instructions.pdf   the Canvas page as-is

PDFs are printed with headless Microsoft Edge or Chrome (whichever is found). The intermediate HTML goes in
a `_pdf_build/` subfolder, which is safe to delete.
"""
import base64
import pathlib
import re
import shutil
import subprocess
import sys

import markdown

CSS = """
@page { size: Letter; margin: 0.6in 0.6in; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; line-height: 1.4; color: #1a1a1a; background: #fff; }
h1 { font-size: 18pt; margin: 0 0 8pt; }
h2 { font-size: 14pt; margin: 16pt 0 6pt; border-bottom: 1px solid #ccc; padding-bottom: 2pt; }
h3 { font-size: 11.5pt; margin: 12pt 0 4pt; } h4 { font-size: 10.5pt; margin: 10pt 0 4pt; }
h2, h3, h4 { page-break-after: avoid; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 8.8pt; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: #2a3850; color: #fff; }
code { font-family: Consolas, monospace; font-size: 8.8pt; background: #f2f2f2; padding: 0 2px; }
pre { background: #f5f5f5; border: 1px solid #ddd; padding: 6pt; font-size: 8.5pt; white-space: pre-wrap; }
img { max-width: 100%; max-height: 3.6in; display: block; margin: 4pt auto 8pt; page-break-inside: avoid; }
a { color: #0b5cad; }
.pb { page-break-before: always; }
"""

LIST_ITEM = re.compile(r"^\s*(- |\d+\. )")


def page(title, body):
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title>"
            f"<style>{CSS}</style></head><body>{body}</body></html>")


def normalize_lists(md):
    """Python-Markdown needs a blank line before a list and 4-space indents for nested items."""
    lines = [("    " + line[2:]) if re.match(r"^  \S", line) else line for line in md.splitlines()]
    out = []
    for line in lines:
        prev = out[-1] if out else ""
        prev_is_list = bool(LIST_ITEM.match(prev)) or prev.startswith("  ")
        if LIST_ITEM.match(line) and prev.strip() and not prev_is_list:
            out.append("")
        out.append(line)
    return "\n".join(out)


def grader_html(folder):
    md = normalize_lists((folder / "final-assessment_grader-key.md").read_text(encoding="utf-8"))
    html = markdown.markdown(md, extensions=["tables", "toc", "sane_lists"])

    def embed(match):
        data = (folder / match.group(1)).read_bytes()
        return f'src="data:image/png;base64,{base64.b64encode(data).decode()}"'

    html = re.sub(r'src="(dryrun-figures/[^"]+)"', embed, html)
    html = html.replace("<hr />\n", "")
    # sections 3, 4 and 5 start new pages, and so does each option after the first
    for sec in re.findall(r'<h2 id="([345]-[^"]+)">', html):
        html = html.replace(f'<h2 id="{sec}">', f'<h2 class="pb" id="{sec}">')
    for opt in re.findall(r'<h3 id="(option-[^"]+)">', html)[1:]:
        html = html.replace(f'<h3 id="{opt}">', f'<h3 class="pb" id="{opt}">')
    return page("Final assessment: grader packet", html)


def learner_html(folder):
    frag = (folder / "final-assessment_canvas.html").read_text(encoding="utf-8")
    frag = re.sub(r"<!--.*?-->", "", frag, flags=re.S)
    return page("Final assessment: learner instructions", frag)


def find_browser():
    for path in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                 r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                 r"C:\Program Files\Google\Chrome\Application\chrome.exe"]:
        if pathlib.Path(path).exists():
            return path
    for name in ["msedge", "google-chrome", "chromium", "chrome"]:
        if shutil.which(name):
            return shutil.which(name)
    sys.exit("No Edge or Chrome found to print the PDFs.")


def print_pdf(browser, html_file, pdf_file):
    subprocess.run([browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_file}", html_file.resolve().as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)


def main():
    folder = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "teaching-materials/materials/assessment")
    work = folder / "_pdf_build"
    work.mkdir(exist_ok=True)
    browser = find_browser()
    for html, name in [(grader_html(folder), "final-assessment_grader-packet"),
                       (learner_html(folder), "final-assessment_learner-instructions")]:
        html_file = work / f"{name}.html"
        html_file.write_text(html, encoding="utf-8")
        print_pdf(browser, html_file, (folder / f"{name}.pdf").resolve())
        print("wrote", folder / f"{name}.pdf")


if __name__ == "__main__":
    main()
