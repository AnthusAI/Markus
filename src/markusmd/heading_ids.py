"""Heading anchors: stable generated slug ids and explicit ``{#custom-id}`` suffixes.

Every heading receives an ``id`` so it can be linked to. An author overrides the
generated slug by ending the heading with ``{#custom-id}``. Generated slugs are
lowercase, drop punctuation, join words with single hyphens, and take a numeric
suffix (``-1``, ``-2``) when the same slug appeared earlier in the document, so
a given heading keeps the same id until a heading above it with the same text
is added or removed.
"""

from __future__ import annotations

import re
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.token import Token

from markusmd.errors import MarkusValidationError

HEADING_IDS_ENV_KEY = "markus_heading_ids"
LINE_OFFSET_ENV_KEY = "markus_line_offset"

_EXPLICIT_ID_SUFFIX = re.compile(r"[ \t]*\{#([^{}]*)\}[ \t]*$")
_VALID_EXPLICIT_ID = re.compile(r"^[A-Za-z_][\w:.-]*$")
_SLUG_DROPPED_CHARACTERS = re.compile(r"[^\w\s-]", re.UNICODE)
_SLUG_SEPARATORS = re.compile(r"[\s-]+")
_FALLBACK_SLUG = "section"


def slugify_heading_text(text: str) -> str:
    """Return the generated anchor slug for plain heading text."""
    lowered = text.strip().lower()
    without_punctuation = _SLUG_DROPPED_CHARACTERS.sub("", lowered)
    joined = _SLUG_SEPARATORS.sub("-", without_punctuation).strip("-")
    return joined or _FALLBACK_SLUG


def _plain_text_of(inline_token: Token) -> str:
    parts: list[str] = []
    for child in inline_token.children or []:
        if child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
        elif child.type == "image":
            parts.append(child.content)
    return "".join(parts)


def _take_explicit_id(inline_token: Token, *, line: int | None) -> str | None:
    children = inline_token.children or []
    if not children or children[-1].type != "text":
        return None
    last = children[-1]
    match = _EXPLICIT_ID_SUFFIX.search(last.content)
    if match is None:
        return None
    candidate = match.group(1)
    if not _VALID_EXPLICIT_ID.match(candidate):
        raise MarkusValidationError(
            f"Invalid heading id {candidate!r}: use letters, digits, '-', '_', ':' or '.', "
            "starting with a letter or underscore",
            line=line,
        )
    last.content = last.content[: match.start()]
    if not last.content:
        children.pop()
    inline_token.content = _EXPLICIT_ID_SUFFIX.sub("", inline_token.content)
    return candidate


def _unique_generated_id(base: str, used: set[str]) -> str:
    if base not in used:
        return base
    counter = 1
    while f"{base}-{counter}" in used:
        counter += 1
    return f"{base}-{counter}"


def _assign_heading_ids(state: Any) -> None:
    used: set[str] = state.env.setdefault(HEADING_IDS_ENV_KEY, set())
    line_offset: int = state.env.get(LINE_OFFSET_ENV_KEY, 0)
    tokens = state.tokens
    explicit: list[tuple[Token, str, int | None]] = []
    generated: list[int] = []
    for index, token in enumerate(tokens):
        if token.type != "heading_open" or index + 1 >= len(tokens):
            continue
        inline_token = tokens[index + 1]
        line = token.map[0] + 1 + line_offset if token.map else None
        custom = _take_explicit_id(inline_token, line=line)
        if custom is not None:
            explicit.append((token, custom, line))
        else:
            generated.append(index)
    seen_explicit: set[str] = set()
    for token, custom, line in explicit:
        if custom in seen_explicit or custom in used:
            raise MarkusValidationError(f"Duplicate heading id {custom!r}", line=line)
        seen_explicit.add(custom)
        token.attrSet("id", custom)
    used.update(seen_explicit)
    for index in generated:
        slug = slugify_heading_text(_plain_text_of(tokens[index + 1]))
        unique = _unique_generated_id(slug, used)
        used.add(unique)
        tokens[index].attrSet("id", unique)


def heading_ids_plugin(md: MarkdownIt) -> None:
    """Register the heading id core rule on a markdown-it parser."""
    md.core.ruler.push("markus_heading_ids", _assign_heading_ids)
