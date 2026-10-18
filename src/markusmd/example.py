"""The example directive: one fenced Markus snippet, shown as source and as its rendered preview.

The snippet is written once. Validation parses it as a Markus document so a
broken example fails the build at its real line; rendering parses it again and
renders the preview through the same pipeline as the page around it.
"""

from __future__ import annotations

import re
from html import escape
from typing import Any

from markdown_it import MarkdownIt

from markusmd.ast import Directive, Document, MarkdownBlock
from markusmd.errors import MarkusValidationError
from markusmd.parse import _split_front_matter, parse_blocks

_FENCE_PARSER = MarkdownIt("commonmark")

_DIRECTIVE_HEAD_RE = re.compile(
    r"^(?P<indent> {0,3})(?P<fence>:{2,})(?P<name>[A-Za-z][\w-]*)(?P<attrs>\{.*)?(?P<rest>[ \t]*)$"
)
_DIRECTIVE_CLOSE_RE = re.compile(r"^(?P<indent> {0,3})(?P<fence>:{3,})(?P<rest>[ \t]*)$")
_CODE_FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def example_snippet(directive: Directive) -> tuple[str, int]:
    """Return the example's snippet text and the source line its first line sits on."""
    if any(isinstance(child, Directive) for child in directive.children):
        raise _shape_error(directive)
    blocks = [
        child
        for child in directive.children
        if isinstance(child, MarkdownBlock) and child.source.strip()
    ]
    if len(blocks) != 1:
        raise _shape_error(directive)
    block = blocks[0]
    top_level = [token for token in _FENCE_PARSER.parse(block.source) if token.level == 0]
    if len(top_level) != 1 or top_level[0].type != "fence" or not top_level[0].map:
        raise _shape_error(directive)
    fence = top_level[0]
    return fence.content, block.span.line + fence.map[0] + 1


def parse_example(snippet: str, first_line: int) -> Document:
    """Parse an example snippet as a Markus document, keeping the page's line numbers."""
    front_matter, body, body_line = _split_front_matter(snippet)
    children = parse_blocks(body, start_line=first_line + body_line - 1)
    return Document(front_matter=front_matter, children=children)


def highlight_markus_source(snippet: str) -> str:
    """Escape a snippet for a code block, marking directive fences, names, and attributes."""
    lines = []
    code_fence: str | None = None
    for line in snippet.split("\n"):
        fence_match = _CODE_FENCE_RE.match(line)
        if code_fence is not None:
            if fence_match and fence_match.group(1).startswith(code_fence):
                code_fence = None
            lines.append(escape(line))
            continue
        if fence_match:
            code_fence = fence_match.group(1)
            lines.append(escape(line))
            continue
        lines.append(_highlight_line(line))
    return "\n".join(lines)


def _highlight_line(line: str) -> str:
    head = _DIRECTIVE_HEAD_RE.match(line)
    if head:
        attrs = head.group("attrs")
        return (
            escape(head.group("indent"))
            + f'<span class="markus-src-fence">{escape(head.group("fence"))}</span>'
            + f'<span class="markus-src-name">{escape(head.group("name"))}</span>'
            + (f'<span class="markus-src-attrs">{escape(attrs)}</span>' if attrs else "")
            + escape(head.group("rest"))
        )
    close = _DIRECTIVE_CLOSE_RE.match(line)
    if close:
        return (
            escape(close.group("indent"))
            + f'<span class="markus-src-fence">{escape(close.group("fence"))}</span>'
            + escape(close.group("rest"))
        )
    return escape(line)


def render_example(source_html: str, preview_html: str, attrs: dict[str, Any]) -> str:
    ident = attrs.get("id")
    id_attr = f' id="{escape(str(ident))}"' if ident is not None and str(ident).strip() else ""
    title = attrs.get("title")
    caption = (
        f'<figcaption class="markus-example-title">{escape(str(title))}</figcaption>'
        if title
        else ""
    )
    return (
        f'<figure{id_attr} class="markus-example" data-layout="{escape(attrs["layout"])}">'
        f"{caption}"
        '<div class="markus-example-panes">'
        '<div class="markus-example-source">'
        '<p class="markus-example-label">Markus</p>'
        f'<pre><code class="language-markus">{source_html}</code></pre>'
        "</div>"
        '<div class="markus-example-preview">'
        '<p class="markus-example-label">Preview</p>'
        f'<div class="markus-example-render">{preview_html}</div>'
        "</div>"
        "</div>"
        "</figure>"
    )


def _shape_error(directive: Directive) -> MarkusValidationError:
    return MarkusValidationError(
        "Directive 'example' must contain exactly one fenced code block holding the "
        "Markus source to show; use a longer outer fence (````) when the source has "
        "its own code fences",
        line=directive.span.line,
    )
