"""Highlight syntax: ``==text==`` renders as ``<mark>text</mark>``.

The rule follows the same delimiter-run scheme markdown-it uses for
strikethrough, so a highlight nests with emphasis, links and other inline
markup, may span soft line breaks inside one paragraph, and is never applied
inside code spans or fenced code.
"""

from __future__ import annotations

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline
from markdown_it.rules_inline.state_inline import Delimiter

HIGHLIGHT_MARKER_CODE = 0x3D
HIGHLIGHT_MARKER_TEXT = "="


def _tokenize_highlight_markers(state: StateInline, silent: bool) -> bool:
    start = state.pos
    if state.src[start] != HIGHLIGHT_MARKER_TEXT or silent:
        return False
    scanned = state.scanDelims(start, True)
    length = scanned.length
    if length < 2:
        return False
    if length % 2:
        token = state.push("text", "", 0)
        token.content = HIGHLIGHT_MARKER_TEXT
        length -= 1
    for _ in range(length // 2):
        token = state.push("text", "", 0)
        token.content = HIGHLIGHT_MARKER_TEXT * 2
        state.delimiters.append(
            Delimiter(
                marker=HIGHLIGHT_MARKER_CODE,
                length=0,
                token=len(state.tokens) - 1,
                end=-1,
                open=scanned.can_open,
                close=scanned.can_close,
            )
        )
    state.pos += scanned.length
    return True


def _convert_paired_delimiters(state: StateInline, delimiters: list[Delimiter]) -> None:
    lone_marker_indexes: list[int] = []
    for start_delimiter in delimiters:
        if start_delimiter.marker != HIGHLIGHT_MARKER_CODE or start_delimiter.end == -1:
            continue
        end_delimiter = delimiters[start_delimiter.end]
        open_token = state.tokens[start_delimiter.token]
        open_token.type = "mark_open"
        open_token.tag = "mark"
        open_token.nesting = 1
        open_token.markup = "=="
        open_token.content = ""
        close_token = state.tokens[end_delimiter.token]
        close_token.type = "mark_close"
        close_token.tag = "mark"
        close_token.nesting = -1
        close_token.markup = "=="
        close_token.content = ""
        previous = state.tokens[end_delimiter.token - 1]
        if previous.type == "text" and previous.content == HIGHLIGHT_MARKER_TEXT:
            lone_marker_indexes.append(end_delimiter.token - 1)
    while lone_marker_indexes:
        lone_index = lone_marker_indexes.pop()
        last_close_index = lone_index + 1
        while (
            last_close_index < len(state.tokens)
            and state.tokens[last_close_index].type == "mark_close"
        ):
            last_close_index += 1
        last_close_index -= 1
        if lone_index != last_close_index:
            state.tokens[last_close_index], state.tokens[lone_index] = (
                state.tokens[lone_index],
                state.tokens[last_close_index],
            )


def _post_process_highlight(state: StateInline) -> None:
    _convert_paired_delimiters(state, state.delimiters)
    for token_meta in state.tokens_meta:
        if token_meta and "delimiters" in token_meta:
            _convert_paired_delimiters(state, token_meta["delimiters"])


def highlight_plugin(md: MarkdownIt) -> None:
    """Register the ``==highlight==`` inline rule on a markdown-it parser."""
    md.inline.ruler.before("emphasis", "highlight", _tokenize_highlight_markers)
    md.inline.ruler2.before("emphasis", "highlight", _post_process_highlight)
