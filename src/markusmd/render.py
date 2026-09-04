"""Render a Markus document AST to semantic HTML."""

from __future__ import annotations

import re
from html import escape
from importlib.resources import files

from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin

from markusmd.ast import Document, MarkdownBlock, Node
from markusmd.registry import Registry
from markusmd.themes import validate_theme


def make_markdown(*, allow_html: bool = False) -> MarkdownIt:
    """GitHub-flavored Markdown parser used for ordinary (non-directive) regions."""
    try:
        md = MarkdownIt(
            "gfm-like2",
            {"html": allow_html, "linkify": True, "typographer": True},
        )
    except (KeyError, ValueError):
        md = MarkdownIt(
            "gfm-like",
            {"html": allow_html, "linkify": True, "typographer": True},
        )
        md.use(tasklists_plugin)
    return md


def default_css() -> str:
    return files("markusmd").joinpath("static", "markus.css").read_text(encoding="utf-8")


def minify_css(css: str) -> str:
    """Minify CSS text by removing comments and unnecessary whitespace."""
    strings: list[str] = []

    def save_str(m: re.Match[str]) -> str:
        strings.append(m.group(0))
        return f"__CSS_STR_{len(strings) - 1}__"

    pattern = re.compile(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|/\*[\s\S]*?\*/)')

    def replace_match(m: re.Match[str]) -> str:
        val = m.group(0)
        if val.startswith("/*"):
            return ""
        return save_str(m)

    minified = pattern.sub(replace_match, css)
    minified = re.sub(r"\s+", " ", minified)
    minified = re.sub(r"\s*([\{\};,>])\s*", r"\1", minified)
    minified = re.sub(r"\s*:\s+", ":", minified)
    minified = re.sub(r"\(\s+", "(", minified)
    minified = re.sub(r"\s+\)", ")", minified)
    minified = re.sub(r";}", "}", minified)

    for i, s in enumerate(strings):
        minified = minified.replace(f"__CSS_STR_{i}__", s)

    return minified.strip()


_minify_css_helper = minify_css


def render_document(
    document: Document,
    *,
    registry: Registry | None = None,
    allow_html: bool = False,
    include_css: bool = True,
    full_document: bool = True,
    markdown: MarkdownIt | None = None,
    theme: str | None = None,
    minify_css: bool = False,
) -> str:
    registry = registry or Registry.default()
    markdown = markdown or make_markdown(allow_html=allow_html)
    resolved_theme = validate_theme(theme or document.front_matter.get("theme"))
    body = _render_nodes(document.children, registry=registry, markdown=markdown)
    article = _wrap_article(document, body, theme=resolved_theme)
    if not full_document:
        if include_css:
            raw_css = default_css()
            css_text = _minify_css_helper(raw_css) if minify_css else raw_css
            return f"<style>\n{css_text}\n</style>\n{article}"
        return article
    title = escape(str(document.front_matter.get("title") or "Markus"))
    if include_css:
        raw_css = default_css()
        css_text = _minify_css_helper(raw_css) if minify_css else raw_css
        css = f"<style>\n{css_text}\n</style>"
    else:
        css = ""
    theme_attr = (
        f' data-theme="{escape(resolved_theme)}"'
        if resolved_theme and resolved_theme != "default"
        else ""
    )
    return (
        "<!DOCTYPE html>\n"
        f'<html lang="en"{theme_attr}>\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{title}</title>\n"
        f"  {css}\n"
        "</head>\n"
        f'<body class="markus-body"{theme_attr}>\n'
        f"{article}\n"
        "</body>\n"
        "</html>\n"
    )


def _wrap_article(document: Document, body: str, *, theme: str | None = None) -> str:
    header = _render_header(document.front_matter)
    theme_attr = f' data-theme="{escape(theme)}"' if theme and theme != "default" else ""
    return f'<article class="markus-document"{theme_attr}>{header}{body}</article>'


def _render_header(front_matter: dict) -> str:
    title = front_matter.get("title")
    if not title:
        return ""
    authors = front_matter.get("authors") or front_matter.get("author")
    if isinstance(authors, list):
        author_text = ", ".join(str(item) for item in authors)
    elif authors:
        author_text = str(authors)
    else:
        author_text = ""
    date = front_matter.get("date")
    meta_bits = [bit for bit in (author_text, str(date) if date else "") if bit]
    meta = f'<p class="markus-byline">{escape(" · ".join(meta_bits))}</p>' if meta_bits else ""
    description = front_matter.get("description")
    lede = f'<p class="markus-lede">{escape(str(description))}</p>' if description else ""
    return f'<header class="markus-header"><h1>{escape(str(title))}</h1>{meta}{lede}</header>'


def _render_nodes(
    nodes: list[Node],
    *,
    registry: Registry,
    markdown: MarkdownIt,
) -> str:
    parts = []
    for node in nodes:
        if isinstance(node, MarkdownBlock):
            parts.append(markdown.render(node.source))
        else:
            inner = _render_nodes(node.children, registry=registry, markdown=markdown)
            parts.append(registry.render(node, inner))
    return "".join(parts)
