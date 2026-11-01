#!/usr/bin/env python3
"""Build the static HTML site from the Markdown docs.

Pure standard library: no accounts, no API keys, no external dependencies.
Run: python3 scripts/build_site.py
Output: site/*.html
"""

from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

PAGE_ORDER = [
    ("index", "Home"),
    ("getting-started", "Getting Started"),
    ("model-cards", "Model Cards"),
    ("ollama-cheatsheet", "Ollama Setup Cheat Sheet"),
    ("prompt-starters", "Prompt Starters"),
    ("privacy-basics", "Privacy Basics"),
]

CSS = """\
:root {
  --ink: #1f2937;
  --muted: #4b5563;
  --bg: #ffffff;
  --soft: #f3f4f6;
  --border: #d1d5db;
  --accent: #2563eb;
  --accent-hover: #1d4ed8;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  color: var(--ink);
  background: var(--bg);
  margin: 0;
  line-height: 1.6;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
header, footer, main, nav { max-width: 860px; margin: 0 auto; padding: 0 1.25rem; }
header {
  background: var(--soft);
  border-bottom: 1px solid var(--border);
  padding: 2rem 1.25rem;
  text-align: center;
}
header h1 { margin: 0 0 0.5rem; font-size: 1.75rem; letter-spacing: -0.01em; }
header p { margin: 0; color: var(--muted); font-size: 1rem; }
nav {
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  background: var(--bg);
  z-index: 10;
}
nav ul {
  display: flex;
  flex-wrap: wrap;
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
}
nav li { flex: 1 1 auto; min-width: 140px; }
nav a {
  display: block;
  padding: 0.75rem 1rem;
  border-right: 1px solid var(--border);
  color: var(--ink);
  font-weight: 500;
  font-size: 0.95rem;
  text-align: center;
}
nav a:hover { background: var(--soft); text-decoration: none; }
main { padding: 2rem 1.25rem 4rem; }
h1 { font-size: 1.5rem; margin-top: 2rem; margin-bottom: 0.75rem; border-bottom: 1px solid var(--border); padding-bottom: 0.35rem; }
h2 { font-size: 1.25rem; margin-top: 1.75rem; margin-bottom: 0.5rem; }
h3 { font-size: 1.1rem; margin-top: 1.5rem; margin-bottom: 0.4rem; }
p { margin: 0 0 1rem; }
ul, ol { margin: 0.25rem 0 1rem 1.5rem; }
li { margin: 0.25rem 0; }
pre {
  background: var(--soft);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.85rem 1rem;
  overflow-x: auto;
  margin: 1rem 0;
}
code { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.9em; }
pre code { font-size: 0.9em; padding: 0; background: transparent; }
code:not(pre code) {
  background: var(--soft);
  padding: 0.15rem 0.35rem;
  border-radius: 4px;
  border: 1px solid var(--border);
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem 0;
  font-size: 0.95rem;
}
th, td {
  border: 1px solid var(--border);
  padding: 0.5rem 0.75rem;
  text-align: left;
}
th { background: var(--soft); }
hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
blockquote {
  border-left: 4px solid var(--border);
  margin: 1rem 0;
  padding: 0.5rem 1.25rem;
  color: var(--muted);
}
footer {
  border-top: 1px solid var(--border);
  padding: 2rem 1.25rem;
  color: var(--muted);
  font-size: 0.9rem;
  text-align: center;
}
.small { font-size: 0.85rem; color: var(--muted); }
@media (max-width: 600px) {
  nav li { min-width: 100%; }
  main { padding: 1rem 1rem 3rem; }
}
"""

NAV_TEMPLATE = """\
<nav>
  <ul>{items}</ul>
</nav>
"""


def nav_html(active: str | None = None) -> str:
    items = []
    for slug, label in PAGE_ORDER:
        active_attr = ' aria-current="page"' if active == slug else ""
        href = "index.html" if slug == "index" else f"{slug}.html"
        items.append(f'<li><a href="{href}"{active_attr}>{html.escape(label)}</a></li>')
    return NAV_TEMPLATE.format(items="".join(items))


def escape_text(text: str) -> str:
    return html.escape(text)


def convert_inline(text: str) -> str:
    # Inline code first so we do not touch its contents
    def escape_code(match: re.Match[str]) -> str:
        return "<code>" + html.escape(match.group(1)) + "</code>"

    text = re.sub(r"`([^`\n]+)`", escape_code, text)
    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text, flags=re.S)
    # Italic: *text*
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text, flags= re.S)
    # Links: [text](url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def convert_block(text: str) -> str:
    """Convert a full Markdown document to HTML body content."""
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    in_code_block = False
    code_lang = ""
    code_lines: list[str] = []
    in_list = False
    list_type = ""
    list_items: list[str] = []
    pending_paragraph: list[str] = []
    in_table = False
    table_rows: list[str] = []

    def flush_paragraph() -> None:
        nonlocal pending_paragraph
        if pending_paragraph:
            body = " ".join(pending_paragraph).strip()
            if body:
                out.append(f"<p>{convert_inline(body)}</p>")
            pending_paragraph = []

    def flush_list() -> None:
        nonlocal in_list, list_type, list_items
        if list_items:
            tag = "ul" if list_type == "unordered" else "ol"
            items_html = "".join(f"<li>{convert_inline(it)}</li>" for it in list_items)
            out.append(f"<{tag}>{items_html}</{tag}>")
            list_items = []
        in_list = False
        list_type = ""

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if table_rows:
            out.append("<table>")
            out.append(f"<thead><tr>{''.join(f'<th>{convert_inline(c.strip())}</th>' for c in table_rows[0].split('|') if c.strip())}</tr></thead>")
            out.append("<tbody>")
            for row in table_rows[1:]:
                cells = [c.strip() for c in row.split("|") if c.strip()]
                out.append("<tr>" + "".join(f"<td>{convert_inline(c)}</td>" for c in cells) + "</tr>")
            out.append("</tbody></table>")
            table_rows = []
        in_table = False

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Fenced code blocks
        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_table()
            if not in_code_block:
                in_code_block = True
                code_lang = stripped[3:].strip()
            else:
                pre = f'<pre><code class="lang-{html.escape(code_lang)}">' + "\n".join(code_lines) + "</code></pre>"
                out.append(pre)
                in_code_block = False
                code_lines = []
            i += 1
            continue
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Horizontal rule
        if re.fullmatch(r"[-*_]{3,}", stripped):
            flush_paragraph()
            flush_list()
            flush_table()
            out.append("<hr>")
            i += 1
            continue

        # ATX headers
        m = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if m:
            flush_paragraph()
            flush_list()
            flush_table()
            level = len(m.group(1))
            content = convert_inline(m.group(2).strip())
            anchor = re.sub(r"[^a-z0-9]+", "-", m.group(2).strip().lower()).strip("-")
            out.append(f"<h{level} id=\"{anchor}\">{content}</h{level}>")
            i += 1
            continue

        # Table rows
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_list()
            if re.fullmatch(r"\|[\s:|-]+\|", stripped):
                i += 1
                continue
            in_table = True
            table_rows.append(stripped)
            i += 1
            continue
        if in_table and not stripped:
            flush_table()
            i += 1
            continue
        if in_table:
            flush_table()
            # fall through to normal handling

        # Blank line -> end paragraph
        if not stripped:
            flush_paragraph()
            flush_list()
            flush_table()
            i += 1
            continue

        # List items
        m = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        if m:
            flush_paragraph()
            flush_table()
            if not in_list or list_type != "ordered":
                flush_list()
                in_list = True
                list_type = "ordered"
            list_items.append(m.group(2))
            i += 1
            continue
        m = re.match(r"^[-*+]\s+(.+)$", stripped)
        if m:
            flush_paragraph()
            flush_table()
            if not in_list or list_type != "unordered":
                flush_list()
                in_list = True
                list_type = "unordered"
            list_items.append(m.group(1))
            i += 1
            continue

        # Blockquote
        m = re.match(r"^>\s?(.*)$", stripped)
        if m:
            flush_paragraph()
            flush_list()
            flush_table()
            out.append("<blockquote>" + convert_inline(m.group(1)) + "</blockquote>")
            i += 1
            continue

        # Regular paragraph line
        pending_paragraph.append(stripped)
        i += 1

    flush_paragraph()
    flush_list()
    flush_table()
    return "\n".join(out)


def page_template(title: str, body: str, active: str | None = None) -> str:
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — Free LLM Starter Kit</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>Free LLM Starter Kit</h1>
  <p>Run large language models on your own computer. No account, no API key.</p>
</header>
{nav_html(active)}
<main>
{body}
</main>
<footer>
  <p class="small">Made by <strong>Asdale Dynamics, LLC</strong> — beginner-friendly AI education.<br>
  Plain English, step by step, never condescending. Education only, never medical advice.<br>
  <a href="https://dylanasdale.github.io" target="_blank" rel="noopener">dylanasdale.github.io</a> &middot;
  <a href="LICENSE.html">MIT License &copy; 2026 Asdale Dynamics, LLC</a></p>
</footer>
</body>
</html>
"""


def build() -> int:
    SITE.mkdir(parents=True, exist_ok=True)
    built: list[str] = []

    # Root index.md if present, else docs/index.md
    index_source = ROOT / "index.md"
    if not index_source.exists():
        index_source = DOCS / "index.md"

    # docs/<slug>.md for each entry in PAGE_ORDER
    for slug, label in PAGE_ORDER:
        source = DOCS / f"{slug}.md"
        if not source.exists():
            print(f"warning: missing {source}, skipping", file=sys.stderr)
            continue
        raw = source.read_text(encoding="utf-8")
        body = convert_block(raw)
        # Use the first H1 as the page title if present
        m = re.search(r"^#\s+(.+)$", raw, re.M)
        title = m.group(1).strip() if m else label
        html_doc = page_template(title, body, active=slug)
        out_name = "index.html" if slug == "index" else f"{slug}.html"
        (SITE / out_name).write_text(html_doc, encoding="utf-8")
        built.append(out_name)

    # Copy LICENSE to site/LICENSE.html so the footer link works
    license_source = ROOT / "LICENSE"
    if license_source.exists():
        raw = license_source.read_text(encoding="utf-8")
        body = f"<pre>{escape_text(raw)}</pre>"
        (SITE / "LICENSE.html").write_text(page_template("License", body, active=None), encoding="utf-8")
        built.append("LICENSE.html")

    print(f"Built {len(built)} page(s) into {SITE}:")
    for name in built:
        print(f"  site/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
