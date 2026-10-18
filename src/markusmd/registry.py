"""Default semantic directive registry: schemas, nesting rules, and HTML renderers."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field
from html import escape
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from markusmd.ast import Directive
from markusmd.errors import MarkusValidationError

TRAILING_HTML_KEY = "_trailing_html"

RenderFn = Callable[["Directive", str, dict[str, Any]], str]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    id: str | None = None


class CalloutAttrs(_Strict):
    kind: Literal["note", "warning", "tip", "caution"] = "note"
    title: str | None = None


class PullQuoteAttrs(_Strict):
    attribution: str | None = None
    source: str | None = None
    tone: Literal["default", "primary", "quiet"] = "default"
    align: Literal["inline", "left", "right"] = "inline"


class CardAttrs(_Strict):
    icon: str | None = None
    title: str | None = None
    span: int | Literal["full"] | None = None

    @field_validator("span")
    @classmethod
    def _validate_span(cls, value: int | Literal["full"] | None) -> int | Literal["full"] | None:
        if value is None or value == "full":
            return value
        if not 1 <= int(value) <= 6:
            raise ValueError("span must be between 1 and 6, or 'full'")
        return int(value)


class CardGridAttrs(_Strict):
    label: str | None = None
    columns: int | None = Field(default=None, ge=1, le=6)


class TwoUpAttrs(_Strict):
    ratio: Literal["1:1", "2:1", "1:2"] = "1:1"
    align: Literal["start", "center", "end", "stretch"] = "start"


class ColumnAttrs(_Strict):
    pass


class FigureAttrs(_Strict):
    src: str | None = None
    alt: str = ""
    credit: str | None = None
    caption: str | None = None


class DetailsAttrs(_Strict):
    summary: str = "Details"
    open: bool = False


class AsideAttrs(_Strict):
    title: str | None = None


class MetricAttrs(_Strict):
    value: str
    unit: str | None = None
    label: str | None = None
    delta: str | None = None


class BarChartAttrs(_Strict):
    title: str | None = None
    max: float = Field(default=100, gt=0)
    unit: str = "%"
    caption: str | None = None


class ConversationAttrs(_Strict):
    title: str | None = None
    kind: Literal["request", "response"] | None = None


class MessageGroupAttrs(_Strict):
    label: str


class MessageAttrs(_Strict):
    role: str

    @field_validator("role")
    @classmethod
    def _validate_role(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("role is required")
        return value.strip()


DiagramTone = Literal["neutral", "human", "agent", "risk", "ok"]


class DiagramAttrs(_Strict):
    title: str | None = None


class DiagramNodeAttrs(_Strict):
    title: str
    tone: DiagramTone = "neutral"


class DiagramRowAttrs(_Strict):
    pass


class DiagramLinkAttrs(_Strict):
    label: str | None = None
    back: str | None = None


def _id_attr(attrs: dict[str, Any]) -> str:
    ident = attrs.get("id")
    if ident is not None and str(ident).strip():
        return f' id="{escape(str(ident))}"'
    return ""
class TabsAttrs(_Strict):
    label: str | None = None


class TabAttrs(_Strict):
    label: str


class StepListAttrs(_Strict):
    pass


class StepAttrs(_Strict):
    pass


class VideoAttrs(_Strict):
    src: str
    title: str | None = None
    poster: str | None = None


class TimelineAttrs(_Strict):
    label: str | None = None


class TimelineEventAttrs(_Strict):
    date: str | None = None
    time: str | None = None
    title: str | None = None
    icon: str | None = None


_FINDING_ID_RE = re.compile(r"^finding-[a-f0-9]{16}$")


class EditorialFindingAttrs(_Strict):
    id: str
    kind: str
    rationale: str | None = None
    decision: Literal["skip", "rewrite", "delete", "keep", "add"] | None = None
    group: str | None = None

    @field_validator("id")
    @classmethod
    def _validate_finding_id(cls, value: str) -> str:
        if not _FINDING_ID_RE.match(value):
            raise ValueError("id must match finding-[16 lowercase hex chars]")
        return value

    @field_validator("kind")
    @classmethod
    def _validate_kind(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("kind is required")
        return value.strip()


def _render_callout(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    kind = attrs["kind"]
    title = attrs.get("title") or kind.capitalize()
    return (
        f'<aside{_id_attr(attrs)} class="markus-callout markus-callout--{escape(kind)}" '
        f'role="note">'
        f'<p class="markus-callout-title">{escape(title)}</p>'
        f'<div class="markus-callout-body">{inner}</div>'
        f"</aside>"
    )


def _render_pull_quote(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    tone = attrs["tone"]
    align = attrs["align"]
    classes = (
        f"markus-pull-quote markus-pull-quote--{escape(tone)} "
        f"markus-pull-quote--{escape(align)}"
    )
    caption = ""
    attribution = attrs.get("attribution")
    source = attrs.get("source")
    if attribution or source:
        parts = []
        if attribution:
            parts.append(escape(str(attribution)))
        if source:
            parts.append(f'<cite>{escape(str(source))}</cite>')
        caption = f"<figcaption>{' · '.join(parts)}</figcaption>"
    return (
        f'<figure{_id_attr(attrs)} class="{classes}">'
        f"<blockquote>{inner}</blockquote>"
        f"{caption}"
        f"</figure>"
    )


_ICON_MARKS = {
    "bolt": "⚡",
    "lock": "🔒",
    "gauge": "⏱",
    "eye": "◉",
    "brain": "◈",
    "quote": "❝",
    "grid": "▦",
    "scale": "⚖",
    "book": "▣",
}


def _icon_mark(icon: str) -> str:
    return _ICON_MARKS.get(icon, icon)


def _render_card(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    icon = attrs.get("icon")
    title = attrs.get("title")
    span = attrs.get("span")
    span_attr = ""
    if span == "full":
        span_attr = ' data-span="full"'
    elif span is not None:
        span_attr = f' data-span="{int(span)}"'
    icon_html = (
        f'<span class="markus-card-icon" aria-hidden="true">{escape(_icon_mark(str(icon)))}</span>'
        if icon
        else ""
    )
    title_html = f'<h3 class="markus-card-title">{escape(str(title))}</h3>' if title else ""
    return (
        f'<article{_id_attr(attrs)} class="markus-card"{span_attr}>'
        f"{icon_html}{title_html}"
        f'<div class="markus-card-body">{inner}</div>'
        f"</article>"
    )


def _render_card_grid(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    label = attrs.get("label") or "Related items"
    columns = attrs.get("columns")
    style = f' style="--markus-columns: {int(columns)}"' if columns else ""
    return (
        f'<section{_id_attr(attrs)} class="markus-card-grid" '
        f'aria-label="{escape(str(label))}"{style}>'
        f"{inner}"
        f"</section>"
    )


def _render_two_up(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    ratio = attrs["ratio"]
    align = attrs["align"]
    return (
        f'<section{_id_attr(attrs)} class="markus-two-up markus-two-up--{escape(align)}" '
        f'data-ratio="{escape(ratio)}">'
        f"{inner}"
        f"</section>"
    )


def _render_column(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    return f'<div{_id_attr(attrs)} class="markus-column">{inner}</div>'


def _render_figure(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    src = attrs.get("src")
    alt = attrs.get("alt") or ""
    media = ""
    if src:
        media = f'<img src="{escape(str(src), quote=True)}" alt="{escape(str(alt))}">'
    caption_bits = []
    if attrs.get("caption"):
        caption_bits.append(escape(str(attrs["caption"])))
    if attrs.get("credit"):
        caption_bits.append(f'<span class="markus-credit">{escape(str(attrs["credit"]))}</span>')
    caption = f"<figcaption>{' · '.join(caption_bits)}</figcaption>" if caption_bits else ""
    return f'<figure{_id_attr(attrs)} class="markus-figure">{media}{inner}{caption}</figure>'


def _render_details(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    opened = " open" if attrs.get("open") else ""
    summary = escape(str(attrs.get("summary") or "Details"))
    return (
        f'<details{_id_attr(attrs)} class="markus-details"{opened}>'
        f"<summary>{summary}</summary>"
        f'<div class="markus-details-body">{inner}</div>'
        f"</details>"
    )


def _render_aside(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    title = attrs.get("title")
    heading = f'<p class="markus-aside-title">{escape(str(title))}</p>' if title else ""
    return f'<aside{_id_attr(attrs)} class="markus-aside">{heading}{inner}</aside>'


def _render_metric(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    label = attrs.get("label") or "Metric"
    value = escape(str(attrs["value"]))
    unit = (
        f'<span class="markus-metric-unit">{escape(str(attrs["unit"]))}</span>'
        if attrs.get("unit")
        else ""
    )
    delta_html = ""
    delta = attrs.get("delta")
    if delta:
        text = str(delta)
        direction = "flat"
        if text.startswith("-"):
            direction = "down"
        elif text.startswith("+"):
            direction = "up"
        delta_html = (
            f'<span class="markus-metric-delta markus-metric-delta--{direction}">'
            f"{escape(text)}</span>"
        )
    return (
        f'<dl{_id_attr(attrs)} class="markus-metric">'
        f"<dt>{escape(str(label))}</dt>"
        f"<dd><span class=\"markus-metric-value\">{value}</span>{unit}{delta_html}</dd>"
        f"</dl>"
    )


def _css_token(text: str) -> str:
    token = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return token or "other"


def _render_conversation(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    title = attrs.get("title")
    kind = attrs.get("kind")
    kind_class = f" markus-conversation--{kind}" if kind else ""
    label = escape(str(title) if title else "Conversation", quote=True)
    title_html = f'<p class="markus-conversation-title">{escape(str(title))}</p>' if title else ""
    has_groups = any(
        isinstance(child, Directive) and child.name == "message-group"
        for child in directive.children
    )
    body = inner if has_groups else f'<ol class="markus-messages">{inner}</ol>'
    return (
        f'<section{_id_attr(attrs)} class="markus-conversation{kind_class}" aria-label="{label}">'
        f"{title_html}{body}</section>"
    )


def _render_message_group(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    label = escape(str(attrs["label"]), quote=True)
    return (
        f'<div{_id_attr(attrs)} class="markus-message-group" role="group" aria-label="{label}">'
        f'<p class="markus-message-group-label">{escape(str(attrs["label"]))}</p>'
        f'<ol class="markus-messages">{inner}</ol></div>'
    )


def _render_message(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    role = str(attrs["role"])
    return (
        f'<li{_id_attr(attrs)} class="markus-message markus-message--{_css_token(role)}">'
        f'<span class="markus-message-role">{escape(role)}</span>'
        f'<div class="markus-message-body">{inner}</div></li>'
    )


def _render_diagram(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    title = attrs.get("title")
    label = escape(str(title) if title else "Diagram", quote=True)
    title_html = f'<p class="markus-diagram-title">{escape(str(title))}</p>' if title else ""
    trailing = attrs.get(TRAILING_HTML_KEY, "")
    caption_html = (
        f'<figcaption class="markus-diagram-caption">{trailing}</figcaption>' if trailing else ""
    )
    return (
        f'<figure{_id_attr(attrs)} class="markus-diagram" role="group" aria-label="{label}">'
        f'{title_html}<ol class="markus-diagram-flow">{inner}</ol>{caption_html}</figure>'
    )


def _render_diagram_node(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    tone = attrs["tone"]
    body = f'<div class="markus-diagram-node-body">{inner}</div>' if inner.strip() else ""
    return (
        f'<li{_id_attr(attrs)} class="markus-diagram-node markus-diagram-node--{escape(tone)}">'
        f'<p class="markus-diagram-node-title">{escape(str(attrs["title"]))}</p>{body}</li>'
    )


def _render_diagram_row(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    return (
        f'<li{_id_attr(attrs)} class="markus-diagram-row">'
        f'<ul class="markus-diagram-row-items">{inner}</ul></li>'
    )


def _render_diagram_link(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    if attrs.get("label"):
        forward_text = (
            '<span class="markus-visually-hidden">Then: </span>' + escape(str(attrs["label"]))
        )
    else:
        forward_text = '<span class="markus-visually-hidden">Then</span>'
    forward = (
        '<p class="markus-diagram-link-forward"><span aria-hidden="true">&darr;</span>'
        f"{forward_text}</p>"
    )
    back = ""
    if attrs.get("back"):
        back = (
            '<p class="markus-diagram-link-back"><span aria-hidden="true">&uarr;</span>'
            '<span class="markus-visually-hidden">Feeds back: </span>'
            f'{escape(str(attrs["back"]))}</p>'
        )
    return f'<li{_id_attr(attrs)} class="markus-diagram-link">{forward}{back}</li>'


def _format_bar_number(number: float) -> str:
    return f"{number:g}"


def _bar_value_text(number: float, unit: str) -> str:
    text = _format_bar_number(number)
    if not unit:
        return text
    return f"{text}{unit}" if unit == "%" else f"{text} {unit}"


def _parse_bar_value(raw: str, unit: str, *, line: int, label: str) -> float:
    cleaned = raw.strip()
    if unit and cleaned.endswith(unit):
        cleaned = cleaned[: -len(unit)].strip()
    try:
        number = float(cleaned)
    except ValueError:
        raise MarkusValidationError(
            f"bar-chart row {label!r}: value {raw.strip()!r} is not a number",
            line=line,
        ) from None
    if number != number or number in (float("inf"), float("-inf")):
        raise MarkusValidationError(
            f"bar-chart row {label!r}: value {raw.strip()!r} is not a finite number",
            line=line,
        )
    return number


def _render_bar_chart(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    from markusmd.ast import MarkdownBlock
    from markusmd.render import make_markdown

    line = directive.span.line
    source = "\n\n".join(
        child.source for child in directive.children if isinstance(child, MarkdownBlock)
    )
    markdown = make_markdown()
    tokens = markdown.parse(source)
    table_start = next((i for i, tok in enumerate(tokens) if tok.type == "table_open"), None)
    if table_start is None:
        raise MarkusValidationError(
            "Directive 'bar-chart' needs a Markdown table body with columns "
            "label, value and an optional note",
            line=line,
        )
    if table_start != 0:
        raise MarkusValidationError(
            "Directive 'bar-chart' must start with its table; "
            "put the caption after the table or in the caption attribute",
            line=line,
        )
    table_end = next(i for i, tok in enumerate(tokens) if tok.type == "table_close")
    end_line = tokens[0].map[1] if tokens[0].map else 0
    rows: list[list[str]] = []
    header: list[str] = []
    in_head = False
    current: list[str] | None = None
    for tok in tokens[: table_end + 1]:
        if tok.type == "thead_open":
            in_head = True
        elif tok.type == "thead_close":
            in_head = False
        elif tok.type == "tr_open":
            current = []
        elif tok.type == "tr_close":
            if in_head:
                header = current or []
            else:
                rows.append(current or [])
            current = None
        elif tok.type == "inline" and current is not None:
            html = markdown.renderer.renderInline(tok.children or [], markdown.options, {})
            current.append(html)
    if not 2 <= len(header) <= 3:
        raise MarkusValidationError(
            f"Directive 'bar-chart' table needs 2 or 3 columns (label, value, note), "
            f"found {len(header)}",
            line=line,
        )
    if not rows:
        raise MarkusValidationError("Directive 'bar-chart' needs at least one data row", line=line)
    unit = attrs["unit"]
    maximum = float(attrs["max"])
    has_note = len(header) == 3
    body_rows = []
    for row in rows:
        cells = row + [""] * (len(header) - len(row))
        label_html, value_html = cells[0], cells[1]
        note_html = cells[2] if has_note else ""
        plain_label = re.sub(r"<[^>]+>", "", label_html)
        plain_value = re.sub(r"<[^>]+>", "", value_html)
        number = _parse_bar_value(plain_value, unit, line=line, label=plain_label)
        if number < 0 or number > maximum:
            raise MarkusValidationError(
                f"bar-chart row {plain_label!r}: value {_format_bar_number(number)} "
                f"is outside 0 to {_format_bar_number(maximum)}",
                line=line,
            )
        percent = number / maximum * 100
        note_cell = f'<td class="markus-bar-chart-note">{note_html}</td>' if has_note else ""
        body_rows.append(
            f'<tr><th scope="row" class="markus-bar-chart-label">{label_html}</th>'
            f'<td class="markus-bar-chart-bar"><div class="markus-bar-chart-line">'
            f'<span class="markus-bar-chart-track" aria-hidden="true">'
            f'<span class="markus-bar-chart-fill" style="--markus-bar-percent: {percent:.4g}%">'
            f"</span></span>"
            f'<span class="markus-bar-chart-value">{escape(_bar_value_text(number, unit))}</span>'
            f"</div></td>{note_cell}</tr>"
        )
    head_cells = [
        f'<th scope="col">{header[0]}</th>',
        f'<th scope="col">{header[1]}</th>',
    ]
    if has_note:
        head_cells.append(f'<th scope="col">{header[2]}</th>')
    title = attrs.get("title")
    caption_element = (
        f'<caption class="markus-bar-chart-title">{escape(str(title))}</caption>' if title else ""
    )
    caption_html = ""
    trailing = "\n".join(source.splitlines()[end_line:]).strip()
    if trailing:
        caption_html = markdown.render(trailing)
    elif attrs.get("caption"):
        caption_html = f"<p>{escape(str(attrs['caption']))}</p>"
    figcaption = (
        f'<figcaption class="markus-bar-chart-caption">{caption_html}</figcaption>'
        if caption_html
        else ""
    )
    return (
        f'<figure{_id_attr(attrs)} class="markus-bar-chart">'
        f'<table class="markus-bar-chart-table">{caption_element}'
        f'<thead class="markus-bar-chart-head"><tr>{"".join(head_cells)}</tr></thead>'
        f'<tbody>{"".join(body_rows)}</tbody></table>'
        f"{figcaption}</figure>"
    )


def _render_tabs(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    label = attrs.get("label")
    aria_label = f' aria-label="{escape(str(label))}"' if label else ""
    buttons = []
    for idx, child in enumerate(directive.children):
        if isinstance(child, Directive) and child.name == "tab":
            tab_label = child.attributes.get("label", "")
            active = " markus-tab-button--active" if idx == 0 else ""
            aria_selected = ' aria-selected="true"' if idx == 0 else ' aria-selected="false"'
            buttons.append(
                f'<button class="markus-tab-button{active}" '
                f'type="button" role="tab"{aria_selected}>'
                f"{escape(str(tab_label))}"
                f"</button>"
            )
    nav = (
        f'<div class="markus-tabs-nav" role="tablist"{aria_label}>{"".join(buttons)}</div>'
        if buttons
        else ""
    )
    return f'<div{_id_attr(attrs)} class="markus-tabs">{nav}{inner}</div>'


def _render_tab(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    label = attrs["label"]
    return (
        f'<div{_id_attr(attrs)} class="markus-tab" role="tabpanel" '
        f'aria-label="{escape(str(label))}" '
        f'data-label="{escape(str(label))}">'
        f"{inner}"
        f"</div>"
    )


def _render_step_list(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    return f'<ol{_id_attr(attrs)} class="markus-step-list">{inner}</ol>'


def _render_step(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    return f'<li{_id_attr(attrs)} class="markus-step">{inner}</li>'


def _render_video(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    src = attrs["src"]
    title = attrs.get("title")
    poster = attrs.get("poster")
    title_attr = f' title="{escape(str(title), quote=True)}"' if title else ""
    poster_attr = f' poster="{escape(str(poster), quote=True)}"' if poster else ""
    return (
        f'<video{_id_attr(attrs)} class="markus-video" src="{escape(str(src), quote=True)}"'
        f"{title_attr}{poster_attr} controls>"
        f"</video>"
    )


def _render_timeline(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    label = attrs.get("label")
    aria_label = f' aria-label="{escape(str(label))}"' if label else ""
    return f'<ol{_id_attr(attrs)} class="markus-timeline"{aria_label}>{inner}</ol>'


def _render_editorial_finding(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    kind = escape(str(attrs["kind"]))
    finding_id = escape(str(attrs["id"]))
    decision = attrs.get("decision")
    group = attrs.get("group")
    rationale = attrs.get("rationale")
    data_attrs = [
        f'data-finding-id="{finding_id}"',
        f'data-kind="{kind}"',
    ]
    if decision:
        data_attrs.append(f'data-decision="{escape(str(decision))}"')
    if group:
        data_attrs.append(f'data-group="{escape(str(group))}"')
    meta_parts = [f"<span class=\"markus-editorial-finding-kind\">{kind}</span>"]
    if rationale:
        meta_parts.append(
            f'<span class="markus-editorial-finding-rationale">{escape(str(rationale))}</span>'
        )
    meta = f'<p class="markus-editorial-finding-meta">{" · ".join(meta_parts)}</p>'
    body = inner.strip()
    body_html = f'<div class="markus-editorial-finding-body">{inner}</div>' if body else ""
    return (
        f'<aside id="{finding_id}" class="markus-editorial-finding markus-editorial-finding--{kind}" '
        f'{" ".join(data_attrs)} role="note">'
        f"{meta}{body_html}"
        f"</aside>"
    )


def _render_timeline_event(directive: Directive, inner: str, attrs: dict[str, Any]) -> str:
    date = attrs.get("date")
    time = attrs.get("time")
    title = attrs.get("title")
    icon = attrs.get("icon")

    date_parts = []
    if date:
        date_parts.append(escape(str(date)))
    if time:
        date_parts.append(escape(str(time)))
    date_str = " · ".join(date_parts)

    date_attr = f' data-date="{escape(str(date))}"' if date else ""
    time_attr = f' data-time="{escape(str(time))}"' if time else ""
    date_html = f'<time class="markus-timeline-date">{date_str}</time>' if date_str else ""
    icon_text = escape(_icon_mark(str(icon))) if icon else ""
    icon_html = (
        f'<span class="markus-timeline-icon" aria-hidden="true">{icon_text}</span>'
        if icon
        else ""
    )
    if title:
        title_html = f'<h3 class="markus-timeline-title">{icon_html}{escape(str(title))}</h3>'
    elif icon_html:
        title_html = icon_html
    else:
        title_html = ""
    return (
        f'<li{_id_attr(attrs)} class="markus-timeline-event"{date_attr}{time_attr}>'
        f"{date_html}"
        f"{title_html}"
        f'<div class="markus-timeline-body">{inner}</div>'
        f"</li>"
    )


@dataclass(frozen=True, slots=True)
class DirectiveSpec:
    """A registered Markus directive: name, schema, nesting, and HTML renderer."""

    name: str
    schema: type[BaseModel]
    renderer: RenderFn
    allowed_children: frozenset[str] | None = None
    aliases: tuple[str, ...] = ()
    leaf: bool = False
    canonical: str | None = None
    extra_attributes: dict[str, Any] = field(default_factory=dict)
    allowed_parents: frozenset[str] | None = None
    trailing_markdown: bool = False


class Registry:
    """Versioned catalog of semantic blocks the renderer knows how to honor."""

    def __init__(self) -> None:
        self._specs: dict[str, DirectiveSpec] = {}

    def register(self, spec: DirectiveSpec) -> None:
        self._specs[spec.name] = spec
        for alias in spec.aliases:
            self._specs[alias] = spec

    def resolve(self, name: str) -> DirectiveSpec | None:
        return self._specs.get(name)

    def names(self) -> list[str]:
        return sorted({spec.name for spec in self._specs.values()})

    def validate(self, directive: Directive, *, parent: str | None = None) -> Directive:
        spec = self.resolve(directive.name)
        if spec is None:
            known = ", ".join(self.names())
            raise MarkusValidationError(
                f"Unknown directive {directive.name!r}. "
                f"Markus encodes intent, not CSS. Known directives: {known}.",
                line=directive.span.line,
            )
        if spec.leaf and not directive.leaf:
            raise MarkusValidationError(
                f"Directive {spec.name!r} is a leaf (::name) and cannot wrap content",
                line=directive.span.line,
            )
        if directive.leaf and not spec.leaf:
            raise MarkusValidationError(
                f"Directive {spec.name!r} is a container and cannot be used as a leaf",
                line=directive.span.line,
            )
        canonical_name = spec.canonical or spec.name
        if parent is not None:
            parent_spec = self.resolve(parent)
            if (
                parent_spec is not None
                and parent_spec.allowed_children is not None
                and canonical_name not in parent_spec.allowed_children
            ):
                allowed = ", ".join(sorted(parent_spec.allowed_children))
                raise MarkusValidationError(
                    f"Directive {spec.name!r} cannot appear inside {parent_spec.name!r}. "
                    f"Allowed children: {allowed}.",
                    line=directive.span.line,
                )
        if spec.allowed_parents is not None and parent not in spec.allowed_parents:
            allowed_parent_names = ", ".join(sorted(spec.allowed_parents))
            where = f"inside {parent!r}" if parent else "at the top level"
            raise MarkusValidationError(
                f"Directive {spec.name!r} cannot appear {where}. "
                f"It must be placed inside: {allowed_parent_names}.",
                line=directive.span.line,
            )
        try:
            validated = spec.schema.model_validate(directive.attributes)
        except ValidationError as exc:
            raise MarkusValidationError(
                _format_pydantic(spec.name, exc),
                line=directive.span.line,
            ) from exc

        attributes = validated.model_dump()
        attributes.update(spec.extra_attributes)
        children = [
            self.validate(child, parent=canonical_name)
            if isinstance(child, Directive)
            else child
            for child in directive.children
        ]
        if spec.allowed_children is not None:
            _assert_only_allowed_children(directive, spec, children)
        _assert_cardinality(canonical_name, children, line=directive.span.line)
        _assert_structure(canonical_name, children, line=directive.span.line)
        return Directive(
            name=canonical_name,
            attributes=attributes,
            children=children,
            span=directive.span,
            leaf=directive.leaf,
        )

    def render(
        self,
        directive: Directive,
        inner_html: str,
        *,
        trailing_html: str | None = None,
    ) -> str:
        spec = self.resolve(directive.name)
        if spec is None:
            raise MarkusValidationError(
                f"Cannot render unknown directive {directive.name!r}",
                line=directive.span.line,
            )
        attributes = directive.attributes
        if trailing_html is not None:
            attributes = {**attributes, TRAILING_HTML_KEY: trailing_html}
        return spec.renderer(directive, inner_html, attributes)

    @classmethod
    def default(cls) -> Registry:
        registry = cls()
        for spec in default_specs():
            registry.register(spec)
        return registry


def default_specs() -> list[DirectiveSpec]:
    return [
        DirectiveSpec(
            name="callout",
            schema=CalloutAttrs,
            renderer=_render_callout,
        ),
        DirectiveSpec(
            name="note",
            schema=CalloutAttrs,
            renderer=_render_callout,
            canonical="callout",
            extra_attributes={"kind": "note"},
        ),
        DirectiveSpec(
            name="warning",
            schema=CalloutAttrs,
            renderer=_render_callout,
            canonical="callout",
            extra_attributes={"kind": "warning"},
        ),
        DirectiveSpec(
            name="tip",
            schema=CalloutAttrs,
            renderer=_render_callout,
            canonical="callout",
            extra_attributes={"kind": "tip"},
        ),
        DirectiveSpec(
            name="caution",
            schema=CalloutAttrs,
            renderer=_render_callout,
            canonical="callout",
            extra_attributes={"kind": "caution"},
        ),
        DirectiveSpec(
            name="pull-quote",
            schema=PullQuoteAttrs,
            renderer=_render_pull_quote,
        ),
        DirectiveSpec(
            name="card",
            schema=CardAttrs,
            renderer=_render_card,
            aliases=("feature-card",),
        ),
        DirectiveSpec(
            name="feature-card",
            schema=CardAttrs,
            renderer=_render_card,
            canonical="card",
        ),
        DirectiveSpec(
            name="card-grid",
            schema=CardGridAttrs,
            renderer=_render_card_grid,
            allowed_children=frozenset({"card"}),
            aliases=("feature-grid",),
        ),
        DirectiveSpec(
            name="feature-grid",
            schema=CardGridAttrs,
            renderer=_render_card_grid,
            allowed_children=frozenset({"card"}),
            canonical="card-grid",
        ),
        DirectiveSpec(
            name="two-up",
            schema=TwoUpAttrs,
            renderer=_render_two_up,
            allowed_children=frozenset({"column"}),
        ),
        DirectiveSpec(
            name="column",
            schema=ColumnAttrs,
            renderer=_render_column,
        ),
        DirectiveSpec(
            name="figure",
            schema=FigureAttrs,
            renderer=_render_figure,
        ),
        DirectiveSpec(
            name="details",
            schema=DetailsAttrs,
            renderer=_render_details,
        ),
        DirectiveSpec(
            name="aside",
            schema=AsideAttrs,
            renderer=_render_aside,
        ),
        DirectiveSpec(
            name="metric",
            schema=MetricAttrs,
            renderer=_render_metric,
            leaf=True,
        ),
        DirectiveSpec(
            name="bar-chart",
            schema=BarChartAttrs,
            renderer=_render_bar_chart,
        ),
        DirectiveSpec(
            name="conversation",
            schema=ConversationAttrs,
            renderer=_render_conversation,
            allowed_children=frozenset({"message", "message-group"}),
        ),
        DirectiveSpec(
            name="message-group",
            schema=MessageGroupAttrs,
            renderer=_render_message_group,
            allowed_children=frozenset({"message"}),
            allowed_parents=frozenset({"conversation"}),
        ),
        DirectiveSpec(
            name="message",
            schema=MessageAttrs,
            renderer=_render_message,
            allowed_parents=frozenset({"conversation", "message-group"}),
        ),
        DirectiveSpec(
            name="diagram",
            schema=DiagramAttrs,
            renderer=_render_diagram,
            allowed_children=frozenset({"node", "row", "link"}),
            trailing_markdown=True,
        ),
        DirectiveSpec(
            name="row",
            schema=DiagramRowAttrs,
            renderer=_render_diagram_row,
            allowed_children=frozenset({"node"}),
            allowed_parents=frozenset({"diagram"}),
        ),
        DirectiveSpec(
            name="node",
            schema=DiagramNodeAttrs,
            renderer=_render_diagram_node,
            allowed_parents=frozenset({"diagram", "row"}),
        ),
        DirectiveSpec(
            name="link",
            schema=DiagramLinkAttrs,
            renderer=_render_diagram_link,
            leaf=True,
            allowed_parents=frozenset({"diagram"}),
        ),
        DirectiveSpec(
            name="tabs",
            schema=TabsAttrs,
            renderer=_render_tabs,
            allowed_children=frozenset({"tab"}),
        ),
        DirectiveSpec(
            name="tab",
            schema=TabAttrs,
            renderer=_render_tab,
        ),
        DirectiveSpec(
            name="step-list",
            schema=StepListAttrs,
            renderer=_render_step_list,
            allowed_children=frozenset({"step"}),
        ),
        DirectiveSpec(
            name="step",
            schema=StepAttrs,
            renderer=_render_step,
        ),
        DirectiveSpec(
            name="video",
            schema=VideoAttrs,
            renderer=_render_video,
            leaf=True,
        ),
        DirectiveSpec(
            name="timeline",
            schema=TimelineAttrs,
            renderer=_render_timeline,
            allowed_children=frozenset({"timeline-event"}),
        ),
        DirectiveSpec(
            name="timeline-event",
            schema=TimelineEventAttrs,
            renderer=_render_timeline_event,
        ),
        DirectiveSpec(
            name="editorial-finding",
            schema=EditorialFindingAttrs,
            renderer=_render_editorial_finding,
        ),
    ]


def _assert_only_allowed_children(
    directive: Directive,
    spec: DirectiveSpec,
    children: list[Any],
) -> None:
    from markusmd.ast import MarkdownBlock

    allowed = spec.allowed_children or frozenset()
    for child in children:
        if isinstance(child, MarkdownBlock):
            if spec.trailing_markdown:
                continue
            if child.source.strip():
                allowed_names = ", ".join(sorted(allowed))
                raise MarkusValidationError(
                    f"Directive {spec.name!r} may only contain {allowed_names} blocks, "
                    f"not free Markdown.",
                    line=child.span.line,
                )
        elif isinstance(child, Directive) and child.name not in allowed:
            allowed_names = ", ".join(sorted(allowed))
            raise MarkusValidationError(
                f"Directive {spec.name!r} may only contain {allowed_names} blocks, "
                f"not {child.name!r}.",
                line=child.span.line,
            )


def _assert_cardinality(name: str, children: list[Any], *, line: int) -> None:
    if name == "two-up":
        count = sum(
            1 for child in children if isinstance(child, Directive) and child.name == "column"
        )
        if count != 2:
            raise MarkusValidationError(
                f"Directive 'two-up' requires exactly two column children, found {count}",
                line=line,
            )
    if name == "card-grid":
        count = sum(
            1 for child in children if isinstance(child, Directive) and child.name == "card"
        )
        if count < 1:
            raise MarkusValidationError(
                "Directive 'card-grid' requires at least one card child",
                line=line,
            )
    if name == "tabs":
        count = sum(
            1 for child in children if isinstance(child, Directive) and child.name == "tab"
        )
        if count < 1:
            raise MarkusValidationError(
                "Directive 'tabs' requires at least one tab child",
                line=line,
            )
    if name == "step-list":
        count = sum(
            1 for child in children if isinstance(child, Directive) and child.name == "step"
        )
        if count < 1:
            raise MarkusValidationError(
                "Directive 'step-list' requires at least one step child",
                line=line,
            )
    if name == "timeline":
        count = sum(
            1
            for child in children
            if isinstance(child, Directive) and child.name == "timeline-event"
        )
        if count < 1:
            raise MarkusValidationError(
                "Directive 'timeline' requires at least one timeline-event child",
                line=line,
            )


def _assert_structure(name: str, children: list[Any], *, line: int) -> None:
    directive_children = [child for child in children if isinstance(child, Directive)]
    if name == "conversation":
        kinds = {child.name for child in directive_children}
        if kinds == {"message", "message-group"}:
            raise MarkusValidationError(
                "Directive 'conversation' cannot mix bare message blocks with "
                "message-group blocks; put every message in a group or none",
                line=line,
            )
        if not directive_children:
            raise MarkusValidationError(
                "Directive 'conversation' needs at least one message", line=line
            )
        if kinds == {"message-group"} and not any(
            grandchild.name == "message"
            for child in directive_children
            for grandchild in child.children
            if isinstance(grandchild, Directive)
        ):
            raise MarkusValidationError(
                "Directive 'conversation' needs at least one message", line=line
            )
    if name == "message-group" and not any(child.name == "message" for child in directive_children):
        raise MarkusValidationError(
                "Directive 'message-group' needs at least one message", line=line
            )
    if name == "diagram":
        _assert_diagram_structure(children, line=line)
    if name == "row" and not any(child.name == "node" for child in directive_children):
        raise MarkusValidationError("Directive 'row' needs at least one node", line=line)


def _assert_diagram_structure(children: list[Any], *, line: int) -> None:
    from markusmd.ast import MarkdownBlock

    structural = [child for child in children if isinstance(child, Directive)]
    if not any(child.name in ("node", "row") for child in structural):
        raise MarkusValidationError("Directive 'diagram' needs at least one node or row", line=line)
    last_structural_index = max(
        index for index, child in enumerate(children) if isinstance(child, Directive)
    )
    for index, child in enumerate(children):
        if (
            isinstance(child, MarkdownBlock)
            and child.source.strip()
            and index < last_structural_index
        ):
            raise MarkusValidationError(
                "Directive 'diagram' accepts prose only after its last node or row, "
                "as the caption",
                line=child.span.line,
            )
    for index, child in enumerate(structural):
        if child.name != "link":
            continue
        before = structural[index - 1] if index > 0 else None
        after = structural[index + 1] if index + 1 < len(structural) else None
        if (
            before is None
            or after is None
            or before.name == "link"
            or after.name == "link"
        ):
            raise MarkusValidationError(
                "A diagram link must sit between two nodes (or rows)",
                line=child.span.line,
            )


def _format_pydantic(name: str, exc: ValidationError) -> str:
    parts = []
    for error in exc.errors():
        loc = ".".join(str(item) for item in error.get("loc", ())) or "attributes"
        kind = error.get("type")
        if kind == "extra_forbidden":
            parts.append(
                f"Unknown attribute {loc!r} on {name!r}. "
                "Attributes describe meaning, not presentation."
            )
        else:
            parts.append(f"{name}.{loc}: {error.get('msg')}")
    return " ".join(parts)
