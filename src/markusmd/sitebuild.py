"""Build a static GitHub Pages site from Markus sources."""

from __future__ import annotations

import re
import shutil
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from markusmd.api import convert, parse
from markusmd.render import default_css

NAV = [
    ("index.html", "Overview"),
    ("gallery.html", "Gallery"),
    ("gfm.html", "GitHub Flavored Markdown"),
]


def build_site(source_dir: Path, dest_dir: Path, default_theme: str = "catppuccin") -> Path:
    source_dir = source_dir.resolve()
    dest_dir = dest_dir.resolve()
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Site source directory not found: {source_dir}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / ".nojekyll").write_text("", encoding="utf-8")
    (dest_dir / "markus.css").write_text(default_css(), encoding="utf-8")
    site_css = source_dir / "site.css"
    if not site_css.is_file():
        site_css = Path(__file__).parent.joinpath("static", "site.css")
    shutil.copyfile(site_css, dest_dir / "site.css")

    themes_dir = Path(__file__).parent.joinpath("static", "themes")
    if themes_dir.is_dir():
        dest_themes = dest_dir / "themes"
        dest_themes.mkdir(parents=True, exist_ok=True)
        for theme_file in themes_dir.glob("*.css"):
            shutil.copyfile(theme_file, dest_themes / theme_file.name)

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
        doc = parse(source, strict=False)
        theme = doc.front_matter.get("theme") or default_theme
        article = convert(source, include_css=False, full_document=False, theme=theme)
        html = _wrap_page(page.stem, article, current=_output_name(page), theme=theme)
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


_COPY_BUTTON_HTML = (
    '  <button type="button" class="copy-button" '
    'aria-label="Copy code to clipboard" title="Copy code to clipboard">\n'
    '    <svg class="copy-icon" aria-hidden="true" width="14" height="14" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">\n'
    '      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>\n'
    '      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>\n'
    "    </svg>\n"
    '    <svg class="check-icon" aria-hidden="true" width="14" height="14" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">\n'
    '      <polyline points="20 6 9 17 4 12"></polyline>\n'
    "    </svg>\n"
    '    <span class="copy-button-text">Copy</span>\n'
    "  </button>"
)


def _add_copy_buttons(html: str) -> str:
    pattern = re.compile(
        r"(<pre\b[^>]*>\s*<code\b[^>]*>[\s\S]*?</code>\s*</pre>)", re.IGNORECASE
    )

    def replace_block(match: re.Match[str]) -> str:
        pre_block = match.group(1)
        return (
            '<div class="code-block-wrapper">\n'
            f"  {pre_block}\n"
            f"{_COPY_BUTTON_HTML}\n"
            "</div>"
        )

    return pattern.sub(replace_block, html)


def _wrap_page(stem: str, article: str, *, current: str, theme: str | None = "catppuccin") -> str:
    from markusmd.themes import AVAILABLE_THEMES

    effective_theme = theme or "catppuccin"
    article = _add_copy_buttons(article)

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

    theme_options = []
    for t in sorted(AVAILABLE_THEMES):
        selected = " selected" if t == effective_theme else ""
        theme_options.append(f'<option value="{escape(t)}"{selected}>{escape(t)}</option>')

    theme_switcher = f"""
    <div class="theme-switcher">
      <label for="theme-select">Theme:</label>
      <select id="theme-select">
        {"".join(theme_options)}
      </select>
    </div>"""

    default_theme_js = (
        f"'{escape(effective_theme)}'" if effective_theme != "default" else "'default'"
    )
    theme_attr = f' data-theme="{escape(effective_theme)}"' if effective_theme != "default" else ""
    theme_link = (
        f'<link id="theme-link" rel="stylesheet" href="themes/{escape(effective_theme)}.css">\n  '
        if effective_theme != "default"
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en"{theme_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="markus.css">
  <link rel="stylesheet" href="site.css">
  {theme_link}<script>
    (function() {{
      const saved = localStorage.getItem('markus-theme');
      const currentTheme = saved || {default_theme_js};
      function applyTheme(t) {{
        if (t !== 'default') {{
          document.documentElement.setAttribute('data-theme', t);
          let link = document.getElementById('theme-link');
          if (!link) {{
            link = document.createElement('link');
            link.id = 'theme-link';
            link.rel = 'stylesheet';
            document.head.appendChild(link);
          }}
          link.href = 'themes/' + t + '.css';
        }} else {{
          document.documentElement.removeAttribute('data-theme');
          const link = document.getElementById('theme-link');
          if (link) link.remove();
        }}
        const article = document.querySelector('article.markus-document');
        if (article) {{
          if (t !== 'default') {{
            article.setAttribute('data-theme', t);
          }} else {{
            article.removeAttribute('data-theme');
          }}
        }}
      }}
      applyTheme(currentTheme);
      
      document.addEventListener('DOMContentLoaded', () => {{
        if (currentTheme !== 'default') {{
          document.body.setAttribute('data-theme', currentTheme);
        }} else {{
          document.body.removeAttribute('data-theme');
        }}
        const select = document.getElementById('theme-select');
        if (select) {{
          select.value = currentTheme;
          select.addEventListener('change', (e) => {{
            const t = e.target.value;
            localStorage.setItem('markus-theme', t);
            applyTheme(t);
            if (t !== 'default') {{
              document.body.setAttribute('data-theme', t);
            }} else {{
              document.body.removeAttribute('data-theme');
            }}
          }});
        }}

        function initCopyButtons() {{
          document.querySelectorAll('.copy-button').forEach((btn) => {{
            if (btn.dataset.copyInitialized) return;
            btn.dataset.copyInitialized = 'true';

            btn.addEventListener('click', async () => {{
              const wrapper = btn.closest('.code-block-wrapper');
              const code = wrapper ? wrapper.querySelector('pre code') : null;
              const text = code ? code.textContent : '';

              async function copy(str) {{
                if (navigator.clipboard && window.isSecureContext) {{
                  try {{
                    await navigator.clipboard.writeText(str);
                    return true;
                  }} catch (e) {{}}
                }}
                const ta = document.createElement('textarea');
                ta.value = str;
                ta.style.position = 'fixed';
                ta.style.left = '-9999px';
                ta.style.top = '-9999px';
                document.body.appendChild(ta);
                ta.focus();
                ta.select();
                let res = false;
                try {{
                  res = document.execCommand('copy');
                }} catch (e) {{}}
                ta.remove();
                return res;
              }}

              const ok = await copy(text);
              if (ok) {{
                btn.classList.add('copied');
                btn.setAttribute('aria-label', 'Copied to clipboard');
                const textSpan = btn.querySelector('.copy-button-text');
                if (textSpan) textSpan.textContent = 'Copied!';
                setTimeout(() => {{
                  btn.classList.remove('copied');
                  btn.setAttribute('aria-label', 'Copy code to clipboard');
                  if (textSpan) textSpan.textContent = 'Copy';
                }}, 2000);
              }}
            }});
          }});
        }}

        document.querySelectorAll('pre code').forEach((code) => {{
          const pre = code.parentElement;
          if (!pre || pre.closest('.code-block-wrapper')) return;
          const wrapper = document.createElement('div');
          wrapper.className = 'code-block-wrapper';
          pre.parentNode.insertBefore(wrapper, pre);
          wrapper.appendChild(pre);
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'copy-button';
          btn.setAttribute('aria-label', 'Copy code to clipboard');
          btn.innerHTML = (
            '<svg class="copy-icon" aria-hidden="true" width="14" height="14" ' +
            'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
            'stroke-linecap="round" stroke-linejoin="round">' +
            '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>' +
            '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>' +
            '<svg class="check-icon" aria-hidden="true" width="14" height="14" ' +
            'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
            'stroke-linecap="round" stroke-linejoin="round">' +
            '<polyline points="20 6 9 17 4 12"></polyline></svg>' +
            '<span class="copy-button-text">Copy</span>'
          );
          wrapper.appendChild(btn);
        }});
        initCopyButtons();
      }});
    }})();
  </script>
</head>
<body class="markus-body markus-site"{theme_attr}>
  <header class="site-banner">
    <a class="site-wordmark" href="index.html">Markus</a>
    <p class="site-tagline">GitHub-flavored Markdown, plus a small vocabulary for layout intent.</p>
    <div class="site-nav-container" style="display: flex; gap: 1rem; align-items: center;">
      <nav class="site-nav" aria-label="Demo">{nav}</nav>
      {theme_switcher}
    </div>
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
