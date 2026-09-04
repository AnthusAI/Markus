"""Parse colon-fenced directive attributes and kramdown-style IALs."""

from __future__ import annotations

import re
from typing import Any

from markusmd.errors import MarkusSyntaxError

_ATTR_RE = re.compile(
    r"""
    (?P<name>[A-Za-z_][\w-]*)
    (?:
        \s*=\s*
        (?:
            "(?P<double>[^"]*)"
            | '(?P<single>[^']*)'
            | (?P<bare>[^\s}'"]+)
        )
    )?
    """,
    re.VERBOSE,
)

_IAL_LINE_RE = re.compile(
    r"^[ \t]*\{:\s*(?P<body>.*?)\}\s*$",
    re.MULTILINE,
)


def parse_attribute_block(raw: str | None, *, line: int) -> dict[str, Any]:
    """Parse `{key="value" flag other=1}` into a dictionary."""
    if not raw:
        return {}
    body = raw.strip()
    if body.startswith("{") and body.endswith("}"):
        body = body[1:-1].strip()
    if not body:
        return {}
    return parse_attribute_body(body, line=line)


def parse_attribute_body(body: str, *, line: int) -> dict[str, Any]:
    attrs: dict[str, Any] = {}
    index = 0
    length = len(body)
    while index < length:
        while index < length and body[index].isspace():
            index += 1
        if index >= length:
            break
        match = _ATTR_RE.match(body, index)
        if not match:
            snippet = body[index : index + 16]
            raise MarkusSyntaxError(
                f"Could not parse directive attributes starting at {snippet!r}",
                line=line,
            )
        name = match.group("name")
        if match.group("double") is not None:
            value: Any = match.group("double")
        elif match.group("single") is not None:
            value = match.group("single")
        elif match.group("bare") is not None:
            value = _coerce_bare(match.group("bare"))
        else:
            value = True
        attrs[name] = value
        index = match.end()
    return attrs


def extract_inline_attribute_lists(source: str, *, line: int) -> tuple[str, dict[str, Any]]:
    """Lift `{: key=value }` lines out of a directive body into attributes."""
    attrs: dict[str, Any] = {}

    def _replace(match: re.Match[str]) -> str:
        attrs.update(parse_attribute_body(match.group("body"), line=line))
        return ""

    remainder = _IAL_LINE_RE.sub(_replace, source)
    return remainder, attrs


def _coerce_bare(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value
