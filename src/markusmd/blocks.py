"""Typed Markdown block/inline nodes for the Markus document IR.

`markusmd.ast` models Markus *directives* (colon-fenced semantic blocks) plus a
single opaque ``MarkdownBlock`` node holding a raw region of ordinary GFM
Markdown text. That was enough for rendering (the region is handed whole to
markdown-it) but not enough to serve as a shared content IR: downstream
consumers (e.g. layout engines) need typed block-level structure -- headings,
paragraphs, lists, tables, and so on -- rather than an opaque string.

This module converts a raw Markdown region into a tree of typed block nodes
by parsing it with the *same* markdown-it instance/tokenizer used for
rendering (see ``markusmd.render.make_markdown``) and walking its token
stream. Doing the conversion from the parser's own token stream (rather than
re-implementing Markdown parsing) means:

- Structure always agrees with what markdown-it actually parsed (including
  GFM extensions: tables, strikethrough, task lists, autolinks).
- Reference-style links/footnotes defined anywhere in the region are resolved
  correctly, because the whole region is tokenized in one pass; the explosion
  into peer block nodes happens *after* tokenizing, not by re-parsing smaller
  fragments.
- Rendering (`markusmd.render`) is completely untouched: it keeps calling
  ``markdown.render(source)`` on the raw region text, so HTML output for
  existing documents cannot regress from this module existing.

Inline content (the text inside a paragraph, heading, list item, or table
cell) is converted to a typed inline node tree (text/emphasis/strong/
strikethrough/code span/link/image/line breaks/raw inline HTML) rather than
left as a raw Markdown string, since markdown-it already hands us that
structure for free via its inline token stream -- there was no meaningful
extra risk in taking it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.token import Token

# Schema version for the Markus document IR (`Document.to_dict()` output).
# Bump this when the shape of the IR changes in a way downstream consumers
# should know about.
IR_SCHEMA_VERSION = 1


# --------------------------------------------------------------------------- #
# Inline nodes
# --------------------------------------------------------------------------- #


@dataclass(slots=True)
class Text:
    """Plain inline text."""

    text: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": "text", "text": self.text}


@dataclass(slots=True)
class Emphasis:
    """Emphasized (``*italic*``) inline span."""

    children: list[Inline] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"type": "emphasis", "children": [c.to_dict() for c in self.children]}


@dataclass(slots=True)
class Strong:
    """Strongly emphasized (``**bold**``) inline span."""

    children: list[Inline] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"type": "strong", "children": [c.to_dict() for c in self.children]}


@dataclass(slots=True)
class Strikethrough:
    """Struck-through (``~~text~~``) inline span (GFM extension)."""

    children: list[Inline] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"type": "strikethrough", "children": [c.to_dict() for c in self.children]}


@dataclass(slots=True)
class CodeSpan:
    """Inline code span (`` `code` ``)."""

    code: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": "code_span", "code": self.code}


@dataclass(slots=True)
class Link:
    """Inline link."""

    href: str | None
    title: str | None = None
    children: list[Inline] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "link",
            "href": self.href,
            "title": self.title,
            "children": [c.to_dict() for c in self.children],
        }


@dataclass(slots=True)
class Image:
    """Inline image."""

    src: str | None
    alt: str = ""
    title: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"type": "image", "src": self.src, "alt": self.alt, "title": self.title}


@dataclass(slots=True)
class SoftBreak:
    """A line break in the source that does not force a rendered ``<br>``."""

    def to_dict(self) -> dict[str, Any]:
        return {"type": "soft_break"}


@dataclass(slots=True)
class HardBreak:
    """An explicit forced line break (rendered as ``<br>``)."""

    def to_dict(self) -> dict[str, Any]:
        return {"type": "hard_break"}


@dataclass(slots=True)
class HtmlInline:
    """Raw inline HTML (e.g. a task-list checkbox, or literal HTML if allowed)."""

    value: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": "html_inline", "value": self.value}


Inline = (
    Text | Emphasis | Strong | Strikethrough | CodeSpan | Link | Image | SoftBreak | HardBreak
    | HtmlInline
)


# --------------------------------------------------------------------------- #
# Block nodes
# --------------------------------------------------------------------------- #


@dataclass(slots=True)
class Heading:
    """A Markdown heading (``#`` through ``######``)."""

    level: int
    inline: list[Inline] = field(default_factory=list)
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "heading",
            "level": self.level,
            "inline": [c.to_dict() for c in self.inline],
            "line": self.line,
        }


@dataclass(slots=True)
class Paragraph:
    """A Markdown paragraph."""

    inline: list[Inline] = field(default_factory=list)
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "paragraph",
            "inline": [c.to_dict() for c in self.inline],
            "line": self.line,
        }


@dataclass(slots=True)
class ListItem:
    """One item of a bullet or ordered list."""

    children: list[Block] = field(default_factory=list)
    checked: bool | None = None
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "list_item",
            "checked": self.checked,
            "children": [c.to_dict() for c in self.children],
            "line": self.line,
        }


@dataclass(slots=True)
class List:
    """A bullet or ordered list."""

    ordered: bool
    items: list[ListItem] = field(default_factory=list)
    start: int | None = None
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "list",
            "ordered": self.ordered,
            "start": self.start,
            "items": [item.to_dict() for item in self.items],
            "line": self.line,
        }


@dataclass(slots=True)
class Blockquote:
    """A ``>`` blockquote."""

    children: list[Block] = field(default_factory=list)
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "blockquote",
            "children": [c.to_dict() for c in self.children],
            "line": self.line,
        }


@dataclass(slots=True)
class CodeBlock:
    """A fenced or indented code block."""

    value: str
    lang: str | None = None
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"type": "code", "lang": self.lang, "value": self.value, "line": self.line}


@dataclass(slots=True)
class ThematicBreak:
    """A ``---`` thematic break (horizontal rule)."""

    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"type": "thematic_break", "line": self.line}


@dataclass(slots=True)
class HtmlBlock:
    """A raw HTML block. Only produced when raw HTML is permitted (`allow_html=True`);
    otherwise markdown-it's html_block rule is disabled and the same source parses
    as ordinary paragraph text, matching rendering behavior exactly."""

    value: str
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"type": "html", "value": self.value, "line": self.line}


@dataclass(slots=True)
class Table:
    """A GFM table."""

    header: list[list[Inline]] = field(default_factory=list)
    align: list[str | None] = field(default_factory=list)
    rows: list[list[list[Inline]]] = field(default_factory=list)
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "table",
            "align": list(self.align),
            "header": [[c.to_dict() for c in cell] for cell in self.header],
            "rows": [[[c.to_dict() for c in cell] for cell in row] for row in self.rows],
            "line": self.line,
        }


Block = Heading | Paragraph | List | Blockquote | CodeBlock | ThematicBreak | HtmlBlock | Table


# --------------------------------------------------------------------------- #
# Token-stream -> typed tree conversion
# --------------------------------------------------------------------------- #


def parse_markdown_blocks(
    source: str,
    markdown: MarkdownIt,
    *,
    line_offset: int = 0,
) -> list[Block]:
    """Parse a raw Markdown region into a list of typed block nodes.

    Args:
        source: Raw Markdown text (e.g. the contents of a `MarkdownBlock`).
        markdown: The markdown-it instance to tokenize with. Passing the same
            configured instance used for rendering (see
            `markusmd.render.make_markdown`) guarantees the block structure
            reported here matches what was actually rendered.
        line_offset: 0-based line number that `source` starts at within the
            enclosing document, used to compute absolute `line` numbers on
            each node (markdown-it token maps are 0-based and relative to
            `source`).

    Returns:
        A list of top-level typed block nodes, in document order.
    """
    tokens = markdown.parse(source)
    blocks, _ = _parse_blocks(tokens, 0, len(tokens), line_offset)
    return blocks


def _line(token: Token, line_offset: int) -> int | None:
    if token.map is None:
        return None
    return line_offset + token.map[0] + 1


def _find_close(tokens: list[Token], open_index: int, close_type: str) -> int:
    """Return the index of the token that closes the container opened at `open_index`."""
    open_type = tokens[open_index].type
    depth = 0
    for j in range(open_index, len(tokens)):
        if tokens[j].type == open_type:
            depth += 1
        elif tokens[j].type == close_type:
            depth -= 1
            if depth == 0:
                return j
    raise ValueError(f"Unmatched {open_type!r} at token {open_index}")


def _parse_blocks(
    tokens: list[Token], start: int, end: int, line_offset: int
) -> tuple[list[Block], int]:
    nodes: list[Block] = []
    i = start
    while i < end:
        token = tokens[i]

        if token.type == "heading_open":
            inline_children = _parse_inline(tokens[i + 1])
            nodes.append(
                Heading(
                    level=int(token.tag[1:]) if token.tag[1:].isdigit() else 1,
                    inline=inline_children,
                    line=_line(token, line_offset),
                )
            )
            i += 3
            continue

        if token.type == "paragraph_open":
            inline_children = _parse_inline(tokens[i + 1])
            nodes.append(Paragraph(inline=inline_children, line=_line(token, line_offset)))
            i += 3
            continue

        if token.type in ("bullet_list_open", "ordered_list_open"):
            ordered = token.type == "ordered_list_open"
            close_type = "ordered_list_close" if ordered else "bullet_list_close"
            close_index = _find_close(tokens, i, close_type)
            items = _parse_list_items(tokens, i + 1, close_index, line_offset)
            start_attr = token.attrs.get("start") if ordered else None
            nodes.append(
                List(
                    ordered=ordered,
                    items=items,
                    start=int(start_attr) if start_attr is not None else None,
                    line=_line(token, line_offset),
                )
            )
            i = close_index + 1
            continue

        if token.type == "blockquote_open":
            close_index = _find_close(tokens, i, "blockquote_close")
            children, _ = _parse_blocks(tokens, i + 1, close_index, line_offset)
            nodes.append(Blockquote(children=children, line=_line(token, line_offset)))
            i = close_index + 1
            continue

        if token.type == "fence":
            info = (token.info or "").strip()
            lang = info.split()[0] if info else None
            nodes.append(
                CodeBlock(value=token.content, lang=lang, line=_line(token, line_offset))
            )
            i += 1
            continue

        if token.type == "code_block":
            nodes.append(CodeBlock(value=token.content, lang=None, line=_line(token, line_offset)))
            i += 1
            continue

        if token.type == "hr":
            nodes.append(ThematicBreak(line=_line(token, line_offset)))
            i += 1
            continue

        if token.type == "html_block":
            nodes.append(HtmlBlock(value=token.content, line=_line(token, line_offset)))
            i += 1
            continue

        if token.type == "table_open":
            close_index = _find_close(tokens, i, "table_close")
            nodes.append(_parse_table(tokens, i, close_index, line_offset))
            i = close_index + 1
            continue

        # Unknown/unhandled token type: skip it rather than fail the whole
        # document. This keeps the IR forward-compatible with markdown-it
        # plugins that introduce new block-level token types.
        i += 1

    return nodes, i


def _parse_list_items(
    tokens: list[Token], start: int, end: int, line_offset: int
) -> list[ListItem]:
    items: list[ListItem] = []
    i = start
    while i < end:
        token = tokens[i]
        if token.type != "list_item_open":
            i += 1
            continue
        close_index = _find_close(tokens, i, "list_item_close")
        children, _ = _parse_blocks(tokens, i + 1, close_index, line_offset)
        checked = _task_list_checked(token, children)
        items.append(ListItem(children=children, checked=checked, line=_line(token, line_offset)))
        i = close_index + 1
    return items


def _task_list_checked(item_token: Token, children: list[Block]) -> bool | None:
    """Detect a GFM task-list item's checked state.

    The tasklists-aware GFM preset marks a task-list `list_item_open` token
    with `class="task-list-item"` and records the checkbox state in
    `token.meta["checked"]`; the "[x]"/"[ ]" marker text is already stripped
    from the item's inline content by the time we see it. If a different
    markdown-it configuration instead represents the checkbox as a raw
    `html_inline` token (e.g. the `mdit_py_plugins.tasklists` plugin used as
    a fallback), fall back to sniffing and stripping that.
    """
    classes = item_token.attrs.get("class") or ""
    if "task-list-item" not in str(classes).split():
        return None
    if "checked" in item_token.meta:
        return bool(item_token.meta["checked"])
    if not children or not isinstance(children[0], Paragraph):
        return None
    inline = children[0].inline
    if not inline or not isinstance(inline[0], HtmlInline):
        return None
    checkbox = inline[0]
    if "checkbox" not in checkbox.value:
        return None
    checked = "checked" in checkbox.value
    del inline[0]
    return checked


def _parse_table(tokens: list[Token], start: int, end: int, line_offset: int) -> Table:
    header: list[list[Inline]] = []
    align: list[str | None] = []
    rows: list[list[list[Inline]]] = []
    i = start + 1
    while i < end:
        token = tokens[i]
        if token.type == "thead_open":
            close_index = _find_close(tokens, i, "thead_close")
            row_group = _parse_row_group(tokens, i + 1, close_index)
            if row_group:
                header, align = row_group[0]
            i = close_index + 1
            continue
        if token.type == "tbody_open":
            close_index = _find_close(tokens, i, "tbody_close")
            for cells, _row_align in _parse_row_group(tokens, i + 1, close_index):
                rows.append(cells)
            i = close_index + 1
            continue
        i += 1
    return Table(header=header, align=align, rows=rows, line=_line(tokens[start], line_offset))


def _parse_row_group(
    tokens: list[Token], start: int, end: int
) -> list[tuple[list[list[Inline]], list[str | None]]]:
    result: list[tuple[list[list[Inline]], list[str | None]]] = []
    i = start
    while i < end:
        token = tokens[i]
        if token.type != "tr_open":
            i += 1
            continue
        close_index = _find_close(tokens, i, "tr_close")
        cells: list[list[Inline]] = []
        aligns: list[str | None] = []
        j = i + 1
        while j < close_index:
            cell_token = tokens[j]
            if cell_token.type in ("th_open", "td_open"):
                aligns.append(_cell_align(cell_token))
                cells.append(_parse_inline(tokens[j + 1]))
                j += 3
                continue
            j += 1
        result.append((cells, aligns))
        i = close_index + 1
    return result


def _cell_align(cell_open: Token) -> str | None:
    style = cell_open.attrs.get("style")
    if not style or "text-align" not in style:
        return None
    value = style.split(":", 1)[1].strip().rstrip(";").strip()
    return value or None


def _parse_inline(inline_token: Token) -> list[Inline]:
    children = inline_token.children or []
    root: list[Inline] = []
    stack: list[list[Inline]] = [root]
    for token in children:
        target = stack[-1]
        if token.nesting == 1:
            node = _open_inline_node(token)
            target.append(node)
            container_children = getattr(node, "children", None)
            stack.append(container_children if container_children is not None else [])
        elif token.nesting == -1:
            if len(stack) > 1:
                stack.pop()
        else:
            leaf = _leaf_inline_node(token)
            if leaf is not None:
                target.append(leaf)
    return root


def _open_inline_node(token: Token) -> Inline:
    if token.type == "strong_open":
        return Strong()
    if token.type == "em_open":
        return Emphasis()
    if token.type == "s_open":
        return Strikethrough()
    if token.type == "link_open":
        return Link(href=token.attrs.get("href"), title=token.attrs.get("title"))
    # Unknown container token type: degrade to a plain grouping with no markup semantics.
    return Emphasis()


def _leaf_inline_node(token: Token) -> Inline | None:
    if token.type == "text":
        return Text(text=token.content)
    if token.type == "code_inline":
        return CodeSpan(code=token.content)
    if token.type == "image":
        return Image(
            src=token.attrs.get("src"),
            alt=token.content,
            title=token.attrs.get("title"),
        )
    if token.type == "softbreak":
        return SoftBreak()
    if token.type == "hardbreak":
        return HardBreak()
    if token.type == "html_inline":
        return HtmlInline(value=token.content)
    if token.content:
        return Text(text=token.content)
    return None
