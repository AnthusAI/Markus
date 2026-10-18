"""Line-oriented parser for GFM Markdown plus nested colon-fenced directives.

Provides functions to extract YAML front matter and parse Markus documents into
a hierarchy of typed AST nodes (Document, Directive, and MarkdownBlock).
"""

from __future__ import annotations

import re
from typing import Any

import yaml

from markusmd._frontmatter_yaml import FrontMatterLoader
from markusmd.ast import Directive, Document, MarkdownBlock, Node, SourceSpan
from markusmd.attributes import (
    IAL_LINE_RE,
    find_attribute_block_end,
    parse_attribute_block,
    parse_attribute_body,
)
from markusmd.errors import MarkusSyntaxError

_FRONT_MATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)\n(?:---|\.\.\.)[ \t]*\n?", re.DOTALL)

_OPEN_RE = re.compile(
    r"^(?P<indent> {0,3})(?P<fence>:{3,})\s*(?P<name>[A-Za-z][\w-]*)"
    r"(?P<attrs>\{.*)?[ \t]*$"
)
_CLOSE_RE = re.compile(r"^(?P<indent> {0,3})(?P<fence>:{3,})[ \t]*$")
_LEAF_RE = re.compile(
    r"^(?P<indent> {0,3})::(?!:)(?P<name>[A-Za-z][\w-]*)"
    r"(?P<attrs>\{.*)?[ \t]*$"
)
_CODE_FENCE_RE = re.compile(r"^(?P<indent> {0,3})(?P<fence>`{3,}|~{3,})")


def _scan_directive_head(
    lines: list[str],
    index: int,
    pattern: re.Pattern[str],
    *,
    line_no: int,
) -> tuple[re.Match[str], str | None, int] | None:
    """Match a directive opening line and gather its attribute block.

    The block opens with `{` on the directive line and may continue over
    following lines until the first `}` outside quotes. Returns the match, the
    full attribute text (or None), and the index of the first line after the
    head; returns None when the line is not a directive head.
    """
    match = pattern.match(lines[index].rstrip("\n"))
    if not match:
        return None
    first = match.group("attrs")
    if first is None:
        return match, None, index + 1
    first = first.rstrip()
    end = find_attribute_block_end(first)
    if end is not None:
        if first[end + 1 :].strip():
            return None
        return match, first[: end + 1], index + 1
    collected = first
    cursor = index + 1
    while cursor < len(lines):
        collected += "\n" + lines[cursor].rstrip("\n")
        end = find_attribute_block_end(collected)
        if end is not None:
            if collected[end + 1 :].strip():
                raise MarkusSyntaxError(
                    f"Unexpected text after the closing '}}' of the attribute block "
                    f"starting at line {line_no}",
                    line=line_no + (cursor - index),
                )
            return match, collected[: end + 1], cursor + 1
        cursor += 1
    raise MarkusSyntaxError(
        f"Unterminated attribute block for directive {match.group('name')!r} "
        f"starting at line {line_no}: expected a closing '}}'",
        line=line_no,
    )


def parse_document(source: str) -> Document:
    """Parse Markus source text into a document AST.

    Normalizes line endings, separates optional YAML front matter, and parses
    the body into a sequence of block AST nodes. Registry validation of directives
    is intentionally not performed by this function.

    Args:
        source: Markus markdown source string to parse.

    Returns:
        A Document node containing the parsed front matter dictionary and child AST nodes.

    Raises:
        MarkusSyntaxError: If the YAML front matter is not a mapping or has invalid syntax,
            or if directives contain syntax errors.
    """
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    front_matter, body, body_line = _split_front_matter(source)
    children = parse_blocks(body, start_line=body_line)
    return Document(front_matter=front_matter, children=children)


def parse_blocks(source: str, *, start_line: int = 1) -> list[Node]:
    """Parse Markus body text into a list of AST nodes.

    Scans lines sequentially, preserving code fence boundaries so directives
    inside code blocks are not interpreted. Parses container directives (fenced
    with `:::`) and leaf directives (prefixed with `::`), grouping all other
    lines into MarkdownBlock nodes.

    Args:
        source: Markus body source text to parse into blocks.
        start_line: 1-based starting line number in the source file, used to record
            accurate source spans. Defaults to 1.

    Returns:
        List of parsed AST nodes (Directive and MarkdownBlock).

    Raises:
        MarkusSyntaxError: If directive fences are unclosed or attribute blocks are malformed.
    """
    lines = source.splitlines(keepends=True)
    nodes: list[Node] = []
    markdown_lines: list[str] = []
    markdown_start = start_line
    index = 0
    code_fence: tuple[str, int] | None = None

    def flush_markdown() -> None:
        """Flush accumulated markdown lines into a MarkdownBlock node."""
        nonlocal markdown_lines, markdown_start
        if any(part.strip() for part in markdown_lines):
            text = "".join(markdown_lines)
            if not text.endswith("\n") and text:
                text += "\n"
            nodes.append(MarkdownBlock(source=text, span=SourceSpan(line=markdown_start)))
        markdown_lines = []

    while index < len(lines):
        line = lines[index]
        stripped = line.rstrip("\n")
        line_no = start_line + index

        fence_match = _CODE_FENCE_RE.match(stripped)
        if fence_match:
            marker = fence_match.group("fence")[0]
            count = len(fence_match.group("fence"))
            if code_fence is None:
                code_fence = (marker, count)
            elif marker == code_fence[0] and count >= code_fence[1]:
                code_fence = None
            markdown_lines.append(line)
            index += 1
            continue

        if code_fence is not None:
            markdown_lines.append(line)
            index += 1
            continue

        open_head = _scan_directive_head(lines, index, _OPEN_RE, line_no=line_no)
        if open_head:
            flush_markdown()
            directive, index = _parse_container(
                lines,
                start_index=index,
                start_line=start_line,
                head=open_head,
            )
            nodes.append(directive)
            markdown_start = start_line + index
            continue

        leaf_head = _scan_directive_head(lines, index, _LEAF_RE, line_no=line_no)
        if leaf_head:
            leaf_match, leaf_attrs, leaf_next = leaf_head
            flush_markdown()
            nodes.append(
                Directive(
                    name=leaf_match.group("name"),
                    attributes=parse_attribute_block(leaf_attrs, line=line_no),
                    children=[],
                    span=SourceSpan(line=line_no),
                    leaf=True,
                )
            )
            index = leaf_next
            markdown_start = start_line + index
            continue

        if not markdown_lines:
            markdown_start = line_no
        markdown_lines.append(line)
        index += 1

    flush_markdown()
    return nodes


def _parse_container(
    lines: list[str],
    *,
    start_index: int,
    start_line: int,
    head: tuple[re.Match[str], str | None, int],
) -> tuple[Directive, int]:
    """Parse a container directive and its nested children from line tokens.

    Scans ahead from `start_index` to find the matching closing fence while accounting
    for nested container directives and ignoring fences inside code blocks. Extracts
    any trailing inline attribute lists (IALs), recursively parses children, and
    constructs a Directive node.

    Args:
        lines: Full list of lines in the block being parsed.
        start_index: 0-based index of the opening directive line in `lines`.
        start_line: 1-based starting line offset for the lines list.
        head: The opening match, its attribute text, and the index after the head.

    Returns:
        A tuple of `(directive, next_index)` where `directive` is the parsed Directive
        AST node, and `next_index` is the line index following the closing fence.

    Raises:
        MarkusSyntaxError: If the container directive is not closed before the end
            of lines, or if attribute syntax is invalid.
    """
    match, attribute_text, body_index = head
    name = match.group("name")
    line_no = start_line + start_index
    attributes = parse_attribute_block(attribute_text, line=line_no)
    index = body_index
    depth = 1
    inner: list[str] = []
    code_fence: tuple[str, int] | None = None

    while index < len(lines):
        stripped = lines[index].rstrip("\n")
        fence_match = _CODE_FENCE_RE.match(stripped)
        if fence_match:
            marker = fence_match.group("fence")[0]
            count = len(fence_match.group("fence"))
            if code_fence is None:
                code_fence = (marker, count)
            elif marker == code_fence[0] and count >= code_fence[1]:
                code_fence = None
            inner.append(lines[index])
            index += 1
            continue

        if code_fence is None:
            if depth == 1:
                ial = IAL_LINE_RE.match(stripped)
                if ial:
                    # A trailing `{: key=value }` line belongs to this directive only when it
                    # sits directly in its body: not in a code fence, not in a nested directive.
                    attributes.update(
                        parse_attribute_body(ial.group("body"), line=start_line + index)
                    )
                    inner.append("\n")
                    index += 1
                    continue
            nested_head = _scan_directive_head(
                lines, index, _OPEN_RE, line_no=start_line + index
            )
            if nested_head:
                depth += 1
                inner.extend(lines[index : nested_head[2]])
                index = nested_head[2]
                continue
            if _CLOSE_RE.match(stripped):
                depth -= 1
                if depth == 0:
                    children = parse_blocks("".join(inner), start_line=start_line + body_index)
                    directive = Directive(
                        name=name,
                        attributes=attributes,
                        children=children,
                        span=SourceSpan(line=line_no),
                    )
                    return directive, index + 1
        inner.append(lines[index])
        index += 1

    raise MarkusSyntaxError(
        f"Unclosed directive {name!r} starting at line {line_no}",
        line=line_no,
    )


def _split_front_matter(source: str) -> tuple[dict[str, Any], str, int]:
    """Extract and parse leading YAML front matter from document source.

    Args:
        source: Raw Markus document source string.

    Returns:
        A tuple of `(front_matter, body, body_line)` where:
            - `front_matter`: Dictionary of parsed front matter key-value pairs.
            - `body`: Source text following the front matter.
            - `body_line`: 1-based line number where `body` starts.

    Raises:
        MarkusSyntaxError: If the YAML front matter is not a valid mapping of keys to values.
    """
    match = _FRONT_MATTER_RE.match(source)
    if not match:
        return {}, source, 1
    raw = match.group(1)
    loaded = yaml.load(raw, Loader=FrontMatterLoader) if raw.strip() else {}
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise MarkusSyntaxError(
            "YAML front matter must be a mapping of keys to values",
            line=1,
        )
    body = source[match.end() :]
    consumed = source[: match.end()]
    body_line = consumed.count("\n") + 1
    return loaded, body, body_line
