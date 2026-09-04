"""Default semantic directive registry: schemas, nesting rules, and HTML renderers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from html import escape
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from markusmd.ast import Directive
from markusmd.errors import MarkusValidationError

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
        return Directive(
            name=canonical_name,
            attributes=attributes,
            children=children,
            span=directive.span,
            leaf=directive.leaf,
        )

    def render(self, directive: Directive, inner_html: str) -> str:
        spec = self.resolve(directive.name)
        if spec is None:
            raise MarkusValidationError(
                f"Cannot render unknown directive {directive.name!r}",
                line=directive.span.line,
            )
        return spec.renderer(directive, inner_html, directive.attributes)

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
