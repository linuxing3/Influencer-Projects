#!/usr/bin/env python3
"""Build PDFs for production-workflow buyer docs (optional).

Requires: pandoc, chromium (or google-chrome), same pattern as 02-Prompts/build_pdfs.py.
Markdown remains the source of truth if tools are missing.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

CSS = ROOT / "style.css"
CSS.write_text(
    """
@page { size: Letter; margin: 0.62in; }
body { font-family: Arial, Helvetica, sans-serif; color: #161616; line-height: 1.35; font-size: 12px; }
h1 { font-size: 28px; line-height: 1.08; margin: 0 0 10px; color: #111827; }
h2 { font-size: 16px; margin: 12px 0 7px; color: #7c2d12; }
h3 { font-size: 13px; margin: 9px 0 5px; color: #374151; }
p { margin: 6px 0; }
ul, ol { margin: 6px 0 6px 20px; padding: 0; }
li { margin: 3px 0; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 11px; }
th, td { border: 1px solid #e5e7eb; padding: 4px 6px; text-align: left; vertical-align: top; }
th { background: #f8fafc; }
pre { background: #f8fafc; border: 1px solid #e5e7eb; padding: 8px; border-radius: 7px; white-space: pre-wrap; font-size: 10.2px; line-height: 1.25; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
.pagebreak { break-before: page; page-break-before: always; }
"""
)

# (source markdown relative to repo, output stem directory)
FILES = [
    REPO / "09-Production-Workflow" / "AI-Influencer-Production-Workflow.md",
    REPO / "03-Content-Ideas" / "100-Content-Ideas.md",
    REPO / "03-Content-Ideas" / "Content-Idea-Formulas.md",
    REPO / "03-Content-Ideas" / "Idea-Bank-Worksheet.md",
    REPO / "04-Calendar" / "7-Day-Launch-Calendar.md",
    REPO / "04-Calendar" / "30-Day-Content-Calendar.md",
    REPO / "04-Calendar" / "Weekly-Batch-Planner.md",
    REPO / "04-Calendar" / "Instagram-Posting-Cadence.md",
    REPO / "05-Canva" / "Canva-Workflow.md",
    REPO / "05-Canva" / "Instagram-Size-Specs.md",
    REPO / "05-Canva" / "Design-System-Checklist.md",
    REPO / "05-Canva" / "Canva-Template-Brief.md",
]


def find_chromium() -> str | None:
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        path = shutil.which(name)
        if path:
            return path
    return None


def main() -> int:
    if not shutil.which("pandoc"):
        print("pandoc not found — skip PDF build; markdown is source of truth", file=sys.stderr)
        return 0

    chrome = find_chromium()
    if not chrome:
        print("chromium/chrome not found — skip PDF build", file=sys.stderr)
        return 0

    out_dir = ROOT / "pdf"
    out_dir.mkdir(exist_ok=True)

    for src in FILES:
        if not src.exists():
            print(f"missing: {src}", file=sys.stderr)
            continue
        text = src.read_text(encoding="utf-8")
        text = text.replace("\\newpage", '<div class="pagebreak"></div>')
        tmp = out_dir / (src.stem + ".print.md")
        html = out_dir / (src.stem + ".html")
        pdf = out_dir / (src.stem + ".pdf")
        tmp.write_text(text, encoding="utf-8")
        subprocess.run(
            ["pandoc", str(tmp), "-s", "--css", str(CSS), "-o", str(html)],
            check=True,
        )
        url = "file://" + str(html).replace(" ", "%20")
        subprocess.run(
            [
                chrome,
                "--headless",
                "--no-sandbox",
                "--disable-gpu",
                f"--print-to-pdf={pdf}",
                url,
            ],
            check=True,
        )
        print(pdf)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
