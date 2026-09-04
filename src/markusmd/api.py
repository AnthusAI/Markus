"""High-level parse / validate / convert helpers."""

from __future__ import annotations

from markusmd.ast import Directive, Document
from markusmd.parse import parse_document
from markusmd.registry import Registry
from markusmd.render import render_document
from markusmd.themes import validate_theme


def parse(source: str, *, registry: Registry | None = None, strict: bool = True) -> Document:
    """Parse Markus source into a validated document AST."""
    document = parse_document(source)
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


def render(
    document: Document,
    *,
    registry: Registry | None = None,
    allow_html: bool = False,
    include_css: bool = True,
    full_document: bool = True,
    theme: str | None = None,
) -> str:
    """Render a parsed document to HTML."""
    return render_document(
        document,
        registry=registry,
        allow_html=allow_html,
        include_css=include_css,
        full_document=full_document,
        theme=theme,
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
    )
