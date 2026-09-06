"""High-level parse / validate / convert helpers."""

from __future__ import annotations

from typing import Any

from markusmd.ast import Directive, Document
from markusmd.parse import parse_document as _parse_document_ast
from markusmd.registry import Registry
from markusmd.render import make_markdown, render_document
from markusmd.themes import validate_theme


def parse(source: str, *, registry: Registry | None = None, strict: bool = True) -> Document:
    """Parse Markus source into a validated document AST."""
    document = _parse_document_ast(source)
    if not strict:
        return document
    registry = registry or Registry.default()
    if "theme" in document.front_matter:
        validate_theme(document.front_matter.get("theme"))
    document.children = [
        registry.validate(child) if isinstance(child, Directive) else child
        for child in document.children
    ]
    return document


def parse_document(
    source: str,
    *,
    registry: Registry | None = None,
    strict: bool = True,
    allow_html: bool = False,
) -> dict[str, Any]:
    """Parse Markus source into the canonical document IR.

    This is the documented Python entry point for the same structure the
    `markus ast` CLI command prints: a JSON-serializable dict with a
    `schema_version` marker, `front_matter`, and a single ordered `children`
    list mixing directive nodes with typed Markdown block nodes (heading,
    paragraph, list, blockquote, code, table, thematic_break, and -- when
    `allow_html=True` -- raw HTML) as peers, in document order. See
    `markusmd.blocks` for the node shapes.

    Args:
        source: Markus source text to parse.
        registry: Directive registry to validate against. Defaults to
            `Registry.default()`.
        strict: If True (default), validate directives against the registry
            (unknown directives / invalid attributes raise). If False, skip
            validation.
        allow_html: If True, raw HTML blocks/inline HTML are surfaced as
            typed `html`/`html_inline` nodes, matching `markus convert
            --allow-html`. If False (default), raw HTML source parses as
            ordinary paragraph text, matching `markus convert`'s default.

    Returns:
        The document IR as a plain dict (the same shape `markus ast` prints
        as JSON).
    """
    document = parse(source, registry=registry, strict=strict)
    markdown = make_markdown(allow_html=allow_html)
    return document.to_dict(markdown=markdown)


def render(
    document: Document,
    *,
    registry: Registry | None = None,
    allow_html: bool = False,
    include_css: bool = True,
    full_document: bool = True,
    theme: str | None = None,
    minify_css: bool = False,
) -> str:
    """Render a parsed document to HTML."""
    return render_document(
        document,
        registry=registry,
        allow_html=allow_html,
        include_css=include_css,
        full_document=full_document,
        theme=theme,
        minify_css=minify_css,
    )


def convert(
    source: str,
    *,
    registry: Registry | None = None,
    strict: bool = True,
    allow_html: bool = False,
    include_css: bool = True,
    full_document: bool = True,
    theme: str | None = None,
    minify_css: bool = False,
) -> str:
    """Parse, validate, and render Markus source to HTML."""
    if theme is not None:
        validate_theme(theme)
    document = parse(source, registry=registry, strict=strict)
    return render(
        document,
        registry=registry,
        allow_html=allow_html,
        include_css=include_css,
        full_document=full_document,
        theme=theme,
        minify_css=minify_css,
    )
