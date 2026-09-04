"""Typed AST nodes for a Markus document."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SourceSpan:
    """1-based line number where a node begins in the source."""

    line: int


@dataclass(slots=True)
class MarkdownBlock:
    """A contiguous region of ordinary GFM Markdown."""

    source: str
    span: SourceSpan

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "markdown",
            "source": self.source,
            "line": self.span.line,
        }


@dataclass(slots=True)
class Directive:
    """A semantic layout/content directive with validated attributes."""

    name: str
    attributes: dict[str, Any]
    children: list[Node] = field(default_factory=list)
    span: SourceSpan = field(default_factory=lambda: SourceSpan(line=1))
    leaf: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "directive",
            "name": self.name,
            "attributes": dict(self.attributes),
            "leaf": self.leaf,
            "line": self.span.line,
            "children": [child.to_dict() for child in self.children],
        }


Node = Directive | MarkdownBlock


@dataclass(slots=True)
class Document:
    """A parsed Markus document: YAML front matter plus a block tree."""

    front_matter: dict[str, Any] = field(default_factory=dict)
    children: list[Node] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "document",
            "front_matter": dict(self.front_matter),
            "children": [child.to_dict() for child in self.children],
        }
