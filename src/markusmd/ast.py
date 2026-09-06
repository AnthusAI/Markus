"""Typed AST nodes for a Markus document.

Defines the core data structures used to represent parsed Markus documents,
including documents, container/leaf directives, raw Markdown blocks, and
source spans.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from markusmd.blocks import IR_SCHEMA_VERSION, parse_markdown_blocks
from markusmd.errors import MarkusSerializationError

if TYPE_CHECKING:
    from markdown_it import MarkdownIt


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

    def to_dict(self, *, markdown: MarkdownIt | None = None) -> dict[str, Any]:
        """Serialize the directive and its nested children to a dictionary.

        Args:
            markdown: markdown-it instance used to explode any nested
                `MarkdownBlock` children into typed block nodes (see
                `markusmd.blocks`). Defaults to a standard GFM instance with
                raw HTML disabled, matching `markus ast`'s current behavior.

        Returns:
            Dictionary with 'type', 'name', 'attributes', 'leaf', 'line',
            and 'children' keys. `children` is a flat, ordered list mixing
            nested directive dicts with typed Markdown block dicts (heading,
            paragraph, list, ...) -- directives and Markdown blocks are peers.
        """
        return {
            "type": "directive",
            "name": self.name,
            "attributes": dict(self.attributes),
            "leaf": self.leaf,
            "line": self.span.line,
            "children": _serialize_children(self.children, markdown),
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

    def to_dict(self, *, markdown: MarkdownIt | None = None) -> dict[str, Any]:
        """Serialize the document and its AST child nodes to a dictionary.

        This is the canonical Markus document IR: a `schema_version` marker
        for downstream consumers, front matter, and a single ordered
        `children` list in document order. Directives and typed Markdown
        block nodes (heading, paragraph, list, blockquote, code, table,
        thematic_break, html) are peers in that list -- there is no opaque
        raw-Markdown node in the output.

        Contract: the IR is JSON-typed scalars, lists, and mappings only --
        never arbitrary Python objects. `front_matter` is YAML, and YAML's
        safe loader produces a few types `json.dump` rejects outright (most
        commonly `datetime.date`/`datetime.datetime` from an unquoted
        `date:` value). Those well-known types are normalized here to ISO
        8601 strings so the IR stays JSON-serializable; this method is the
        one boundary where that normalization happens, so both the Python
        `parse_document()` helper and the `markus ast` CLI (which just
        `json.dump`s this dict) get it for free. The `Document.front_matter`
        attribute on *this* dataclass is left untouched -- callers using the
        lower-level `parse()` API still get native `date`/`datetime` values
        if they want them; only the IR (this method's return value) commits
        to JSON-safe scalars. A front matter value with no safe, lossless
        JSON representation (e.g. a YAML `!!set` or `!!binary` value) is not
        silently stringified -- it raises `MarkusSerializationError` naming
        the offending key and type, since a silent fallback would hide data
        loss from downstream consumers like Papyrus.

        Args:
            markdown: markdown-it instance used to parse Markdown regions
                into typed block nodes. Defaults to a standard GFM instance
                with raw HTML disabled (matching `markus ast`'s current
                behavior); pass an instance built with `allow_html=True` to
                also surface raw HTML blocks/inline HTML as typed nodes.

        Returns:
            Dictionary with 'type', 'schema_version', 'front_matter', and
            'children' keys.

        Raises:
            MarkusSerializationError: A front matter value cannot be
                represented as JSON-typed scalars/lists/mappings.
        """
        return {
            "type": "document",
            "schema_version": IR_SCHEMA_VERSION,
            "front_matter": _json_safe_front_matter(self.front_matter),
            "children": _serialize_children(self.children, markdown),
        }


_JSON_SAFE_SCALARS = (str, int, float, bool, type(None))
_TEMPORAL_TYPES = (datetime.datetime, datetime.date, datetime.time)


def _json_safe_front_matter(front_matter: dict[str, Any]) -> dict[str, Any]:
    """Coerce a parsed front matter mapping into JSON-typed scalars only."""
    return {key: _to_json_safe(value, path=key) for key, value in front_matter.items()}


def _to_json_safe(value: Any, *, path: str) -> Any:
    """Recursively coerce a front matter value into JSON-serializable form.

    `datetime.date`/`datetime.datetime`/`datetime.time` (the values YAML's
    safe loader produces for unquoted date-like scalars) are normalized to
    ISO 8601 strings -- an unambiguous, lossless, JSON-native
    representation. `dict`/`list`/`tuple` are walked recursively so a date
    nested inside a list or mapping is caught too. Anything else that is not
    already a JSON-safe scalar (e.g. a YAML `!!set` or `!!binary` value)
    raises `MarkusSerializationError` naming the offending front matter key
    and type, rather than silently stringifying it -- a silent fallback
    would hide data loss from downstream consumers.
    """
    if isinstance(value, _JSON_SAFE_SCALARS):
        return value
    if isinstance(value, _TEMPORAL_TYPES):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _to_json_safe(v, path=f"{path}.{k}") for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_json_safe(v, path=f"{path}[{i}]") for i, v in enumerate(value)]
    raise MarkusSerializationError(
        f"front matter key {path!r} has value of type {type(value).__name__!r}, "
        "which cannot be represented in the Markus document IR (JSON-typed "
        "scalars, lists, and mappings only); use a string, number, boolean, "
        "null, list, or mapping in the source front matter instead"
    )


def _default_markdown() -> MarkdownIt:
    from markusmd.render import make_markdown

    return make_markdown(allow_html=False)


def _serialize_children(nodes: list[Node], markdown: MarkdownIt | None) -> list[dict[str, Any]]:
    """Serialize a list of AST nodes, exploding `MarkdownBlock` regions into
    their typed block nodes so that directives and Markdown blocks appear as
    peers in one ordered list, per the Markus document IR."""
    md = markdown or _default_markdown()
    out: list[dict[str, Any]] = []
    for node in nodes:
        if isinstance(node, MarkdownBlock):
            for block in parse_markdown_blocks(node.source, md, line_offset=node.span.line - 1):
                out.append(block.to_dict())
        else:
            out.append(node.to_dict(markdown=md))
    return out
