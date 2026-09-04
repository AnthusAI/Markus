"""Typed AST nodes for a Markus document.

Defines the core data structures used to represent parsed Markus documents,
including documents, container/leaf directives, raw Markdown blocks, and
source spans.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SourceSpan:
    """Source code location for an AST node.

    Attributes:
        line: 1-based line number where the node begins in the source text.
    """

    line: int


@dataclass(slots=True)
class MarkdownBlock:
    """A contiguous region of ordinary GFM Markdown text.

    Attributes:
        source: Raw Markdown content of the block.
        span: Source code location indicating where this block begins.
    """

    source: str
    span: SourceSpan

    def to_dict(self) -> dict[str, Any]:
        """Serialize the Markdown block to a dictionary.

        Returns:
            Dictionary with 'type', 'source', and 'line' keys representing
            this block.
        """
        return {
            "type": "markdown",
            "source": self.source,
            "line": self.span.line,
        }


@dataclass(slots=True)
class Directive:
    """A semantic layout or content directive with validated attributes.

    Attributes:
        name: Name identifier of the directive (e.g. 'callout', 'tabs').
        attributes: Dictionary of validated key-value attributes.
        children: List of nested child AST nodes contained in this directive.
        span: Source code location indicating where this directive begins.
        leaf: True if this is a self-closing leaf directive without children,
            False if it is a container directive.
    """

    name: str
    attributes: dict[str, Any]
    children: list[Node] = field(default_factory=list)
    span: SourceSpan = field(default_factory=lambda: SourceSpan(line=1))
    leaf: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize the directive and its nested children to a dictionary.

        Returns:
            Dictionary with 'type', 'name', 'attributes', 'leaf', 'line',
            and 'children' keys.
        """
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
    """A parsed Markus document consisting of front matter and block nodes.

    Attributes:
        front_matter: Key-value metadata extracted from YAML front matter.
        children: Top-level sequence of AST nodes in the document body.
    """

    front_matter: dict[str, Any] = field(default_factory=dict)
    children: list[Node] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the document and its AST child nodes to a dictionary.

        Returns:
            Dictionary with 'type', 'front_matter', and 'children' keys.
        """
        return {
            "type": "document",
            "front_matter": dict(self.front_matter),
            "children": [child.to_dict() for child in self.children],
        }
