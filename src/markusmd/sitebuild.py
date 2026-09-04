"""Build a static GitHub Pages site from Markus sources."""

from __future__ import annotations

import shutil
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from markusmd.api import convert
from markusmd.render import default_css

NAV = [
    ("index.html", "Overview"),
    ("gallery.html", "Gallery"),
    ("gfm.html", "GitHub Flavored Markdown"),
]


def build_site(source_dir: Path, dest_dir: Path) -> Path:
    source_dir = source_dir.resolve()
    dest_dir = dest_dir.resolve()
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Site source directory not found: {source_dir}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / ".nojekyll").write_text("", encoding="utf-8")
    (dest_dir / "markus.css").write_text(default_css(), encoding="utf-8")
    site_css = Path(__file__).parent.joinpath("static", "site.css")
    shutil.copyfile(site_css, dest_dir / "site.css")

    assets = source_dir / "assets"
    if assets.is_dir():
        dest_assets = dest_dir / "assets"
        if dest_assets.exists():
            shutil.rmtree(dest_assets)
        shutil.copytree(assets, dest_assets)

    pages = sorted(source_dir.glob("*.md"))
    if not pages:
        raise FileNotFoundError(f"No Markus pages found in {source_dir}")

    for page in pages:
        source = page.read_text(encoding="utf-8")
        article = convert(source, include_css=False, full_document=False)
        html = _wrap_page(page.stem, article, current=_output_name(page))
        (dest_dir / _output_name(page)).write_text(html, encoding="utf-8")
    return dest_dir


def serve_directory(directory: Path, *, host: str, port: int) -> None:
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, format: str, *args) -> None:  # noqa: A003
            print(f"[markus] {format % args}")

    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"Serving {directory} at http://{host}:{port}/")
    httpd.serve_forever()


def _output_name(page: Path) -> str:
    return "index.html" if page.stem == "index" else f"{page.stem}.html"


def _wrap_page(stem: str, article: str, *, current: str) -> str:
    parts = []
    for href, label in NAV:
        current_attr = ' aria-current="page"' if href == current else ""
        parts.append(f'<a href="{href}"{current_attr}>{label}</a>')
    nav = "".join(parts)
    title = {
        "index": "Markus — semantic Markdown for real layouts",
        "gallery": "Markus gallery — every directive",
        "gfm": "Markus — GitHub Flavored Markdown",
    }.get(stem, "Markus")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="markus.css">
  <link rel="stylesheet" href="site.css">
</head>
<body class="markus-body markus-site">
  <header class="site-banner">
    <a class="site-wordmark" href="index.html">Markus</a>
    <p class="site-tagline">GitHub-flavored Markdown, plus a small vocabulary for layout intent.</p>
    <nav class="site-nav" aria-label="Demo">{nav}</nav>
  </header>
  <main>
    {article}
  </main>
  <footer class="site-footer">
    <p>Markus is an MIT-licensed Python module by
    <a href="https://github.com/AnthusAI">Anthus AI Solutions</a>.
    Install with <code>pip install anthus-markus</code>.</p>
  </footer>
</body>
</html>
"""
