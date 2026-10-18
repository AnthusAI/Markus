# Markus language

Markus is **GitHub Flavored Markdown** plus a small registry of colon-fenced
semantic directives. Authors encode intent. The renderer chooses layout.

## Document metadata

Optional YAML front matter:

```md
---
title: The future of local inference
authors:
  - Ada
date: 2026-09-04
---
```

`authors` stays a list of strings or `{name, url}` mappings, for example
`- name: Ryan Porter` with `url: /ryan`. Markus carries these values through
unchanged; the consuming publishing system decides how an author is resolved
and linked. Do not put HTML in front matter.

## Container directives

```
:::name{key="value" flag other=1}
Markdown, including nested directives.
:::
```

### Multi-line attribute blocks

Leaf and container directives may spread their attribute block over several
lines. The opening `{` must be on the directive line; the block ends at the
first `}` outside quotes. Inside a quoted value, a backslash escapes the next
character, so `\"` is a literal double quote and `}` is just text.

```md
::metric{
  value="12"
  unit="ms"
  label="Two quote kinds: ' and \""
}

:::card{
  title="Title"
  icon="bolt"
}
Body.
:::
```

An attribute block with no closing `}` is a syntax error reported at the
directive's first line. A malformed attribute inside a multi-line block is
reported at the offending line and names the line where the block starts.
Unknown attributes are still rejected, and `{: key=value }` attribute-list
lines inside a container work as before.

| Name | Meaning | Notable attributes |
| --- | --- | --- |
| `callout` | Note, warning, tip, or caution | `kind`, `title` |
| `note`, `warning`, `tip`, `caution` | Aliases for `callout` | `title` |
| `pull-quote` | Editorial quotation | `attribution`, `source`, `tone`, `align` |
| `card-grid` / `feature-grid` | Peer cards | `label`, `columns` (hint) |
| `card` / `feature-card` | One peer item | `icon`, `title`, `span` (`1`–`6` or `full`) |
| `two-up` | A conceptual pair | `ratio` (`1:1`, `2:1`, `1:2`), `align` |
| `column` | One side of `two-up` | — |
| `figure` | Media with caption | `src`, `alt`, `caption`, `credit` |
| `details` | Progressive disclosure | `summary`, `open` |
| `aside` | Supporting, non-linear material | `title` |
| `tabs` | Tabbed container | `label` |
| `tab` | One tab panel | `label` |
| `step-list` | Ordered sequence of steps | — |
| `step` | Single step | — |
| `timeline` | Chronological sequence | `label` |
| `timeline-event` | Single event in a timeline | `date`, `time`, `title`, `icon` |
| `bar-chart` | Labeled bars from a Markdown table | `title`, `max`, `unit`, `caption` |
| `conversation` | Transcript of role-labeled messages | `title`, `kind` (`request`, `response`) |
| `message-group` | Labeled run of messages inside a conversation | `label` |
| `message` | One message in a conversation | `role` |
| `diagram` | Vertical flow of boxes and arrows | `title` |
| `row` | Nodes side by side inside a diagram | — |
| `node` | One box in a diagram | `title`, `tone` |
| `editorial-finding` | Editorial diagnose finding (machine or human) | `id`, `kind`, `rationale`, `decision`, `group` |
| `example` | Markus source shown beside its rendered preview | `layout` (`side-by-side`, `stacked`), `title` |

A trailing kramdown-style attribute list is also accepted inside a directive.
It applies to the directive whose body it sits in directly; a `{: ... }` line
inside a nested directive belongs to that directive, and one inside a code
fence is ordinary code:

```md
:::pull-quote
> Measure what matters.
{: attribution="Editorial principle" }
:::
```

## Example

`example` documents Markus in Markus. Its body is exactly one fenced code
block of Markus source; the renderer shows that source, with directive fences,
names and attributes marked, beside the HTML it renders. There is one copy of
the source, so the two cannot drift apart.

````md
:::example{title="A tip"}
```markus
:::tip
The preview renders this source.
:::
```
:::
````

| Attribute | Meaning | Default |
| --- | --- | --- |
| `layout` | `side-by-side` places source and preview in two panes when the example is at least 44rem wide and stacks them below that; `stacked` always puts the source above the preview | `side-by-side` |
| `title` | Caption above the panes | none |

The snippet is parsed and validated with the page, so an invalid example fails
the build at its real line number. Front matter in the snippet renders as a
document header in the preview. When the snippet has its own code fences, use
a longer outer fence. The preview pane is its own CSS container, so layouts
inside it respond to the pane's width, not the page's; use `stacked` for wide
layouts such as card grids and two-up pairs.

## Bar chart

`bar-chart` turns a plain GFM table into labeled horizontal bars. The body is
the table: column 1 is the row label, column 2 the value, and optional column 3
a note shown at the end of the row. Any Markdown after the table is the chart
caption (rendered italic and centered), or use the `caption` attribute.

```md
:::bar-chart{title="Context Snowball"}
| Turn | Context used | Size |
| --- | --- | --- |
| Turn 1 | 2 | ~4K tokens |
| Turn 10 | 35 | ~70K tokens |
| Turn 25 | 75 | ~150K tokens |
| Turn 50 | 100 | ~200K (full window) |

Every turn re-sends the whole conversation. On a 50-turn session, that's
roughly **25 input tokens for every 1 output token** - illustrative, not a
measured trace.
:::
```

| Attribute | Meaning | Default |
| --- | --- | --- |
| `title` | Chart title (the table caption) | none |
| `max` | Value that fills the bar completely | `100` |
| `unit` | Suffix shown after each value; a matching suffix in a cell is accepted | `%` |
| `caption` | Caption text when no paragraph follows the table | none |

Each value must be a number from 0 to `max`; otherwise validation fails with
the offending row named. The output is a real `<table>` (row headers, values as
text, bars hidden from assistive technology), so it reads correctly with no CSS
and degrades to a plain table in other Markdown renderers.

## Conversation

`conversation` writes a transcript, such as an API request or response, as
role-labeled messages. Each `message` body is ordinary Markdown, so lists and
code blocks need no HTML.

```md
:::conversation{title="request from application to OpenAI" kind="request"}
:::message-group{label="conversation history"}
:::message{role="system"}
You are a helpful agent for an online store.
:::
:::message{role="user"}
What's the status of order 123456789?
:::
:::
:::message-group{label="functions"}
:::message{role="check order status"}
Call this function with the order ID.
:::
:::
:::
```

| Directive | Attribute | Meaning |
| --- | --- | --- |
| `conversation` | `title` | Heading and accessible name |
| `conversation` | `kind` | `request` or `response`; changes the accent color |
| `message-group` | `label` | Required name of the group, such as `functions` |
| `message` | `role` | Required free text shown as the speaker label |

A conversation holds `message` blocks directly, or `message-group` blocks that
hold messages, never both, and needs at least one message. `message` and
`message-group` are valid only inside a conversation. The output is a `section`
containing ordered lists, with the role label before each body; on narrow
screens the label sits above the body. The roles `system`, `user`, `assistant`,
`tool` and `function` get distinct theme accents.

## Highlight

`==text==` renders `<mark>text</mark>`.

```md
A preview of ==a new type of software solution.==
==**Run the counterfactual as a smoke test.**== Then compare.
```

The opening `==` must touch the first character and the closing `==` the last,
so `x == y` stays literal. A highlight nests with emphasis, strong text, links
and code, and may span soft line breaks inside one paragraph, but not a blank
line. It is never applied inside code spans or fenced code. The highlight color
comes from the theme.

## Diagram

`diagram` draws a vertical flow as accessible HTML and CSS (an ordered list;
no script, no image). `node` is a box, `row` places nodes side by side, and the
leaf `::link` is the arrow between two items.

```md
:::diagram{title="The Cybernetic Loop"}
:::node{title="Engine" tone="agent"}
LLM generation. Fast, prolific, tireless.
:::
::link{label="output" back="correction"}
:::node{title="Governor" tone="human"}
Specs, tests, CI gates, telemetry.
:::
Skip the loop and it stops being cybernetic: it is just an Engine running open.
:::
```

| Directive | Attribute | Meaning |
| --- | --- | --- |
| `diagram` | `title` | Heading and accessible name |
| `node` | `title` | Required box heading |
| `node` | `tone` | `neutral` (default), `human`, `agent`, `risk`, `ok` |
| `link` | `label` | Text next to the downward arrow |
| `link` | `back` | Text next to an upward (feedback) arrow |

`tone` is a meaning: the theme chooses the color, so it stays readable in every
theme. A node body is Markdown. A `link` must sit between two nodes or rows
(never first, last, or beside another link). Prose after the last node or row
is the caption; prose before it is an error. A `row` holds only nodes and needs
at least one; rows stack into one column on narrow screens.

## Heading anchors

Every heading receives an `id`. The generated id is the heading text with
inline markup ignored, lowercased, punctuation removed, and words joined with
single hyphens (`## Example 1: Use AI` becomes `example-1-use-ai`). A repeated
slug takes `-1`, `-2` and so on in document order across the whole document,
including headings inside directives. A heading with no usable characters gets
`section`.

End a heading with `{#custom-id}` to choose the id; the suffix is not shown.

```md
## Use AI models from any API {#ai-api-multiplexer}

See [the multiplexer](#ai-api-multiplexer).
```

A custom id starts with a letter or underscore and may use letters, digits,
`-`, `_`, `:` and `.`. A malformed or duplicate custom id fails validation with
the line number. Generated ids are stable as long as no earlier heading with the
same text is added or removed; use a custom id for any heading that other
documents link to. Custom ids are reserved for the whole document before any slug is generated, so
a generated slug never steals an explicit id, even from a heading further down;
it takes the numeric suffix instead.

## Tables

GFM tables render with column alignment from the delimiter row (`:---`, `:---:`,
`---:`), wrapped cell text, tabular numerals, striped body rows, and horizontal
scrolling inside a focusable region when a table is wider than the screen.

## Leaf directives

```
::metric{value="12" unit="ms" label="p95 latency" delta="-8%"}
::video{src="screencast.mp4" title="Walkthrough"}
```

| Name | Meaning | Notable attributes |
| --- | --- | --- |
| `metric` | Key metric fact | `value`, `unit`, `label`, `delta` |
| `video` | Video player | `src`, `title`, `poster` |
| `link` | Arrow between diagram items | `label`, `back` |

## Nesting rules

- `card-grid` may contain only `card` (or the `feature-card` alias)
- `two-up` must contain exactly two `column` children
- `tabs` may contain only `tab`
- `step-list` may contain only `step`
- `timeline` may contain only `timeline-event`
- `conversation` may contain only `message` or `message-group` (not both); `message-group` may contain only `message`
- `diagram` may contain `node`, `row` and `link`, then optional caption prose; `row` may contain only `node`
- `message`, `message-group`, `node`, `row` and `link` are valid only inside their parent
- Other containers may nest Markdown and further directives
- Fenced code blocks are not scanned for directives

## What does not belong in source

Do not add `margin`, `width`, `font-size`, or other presentation keys.
Unknown directive names and unknown attributes fail validation.

## Themes

Name a theme with `theme:` in front matter or `markus convert --theme NAME`.
Themes set colors only; layout, spacing and type stay with the renderer.

Ten themes are **families** with a light and a dark palette: `solarized`,
`catppuccin` (Latte and Mocha), `everforest`, `flexoki`, `github`, `gruvbox`,
`kanagawa` (Lotus and Wave), `one`, `rose-pine` (Dawn and Rosé Pine) and
`tokyo-night` (Day and Night). A family follows the reader's
`prefers-color-scheme`. Set `data-color-scheme="light"` or `"dark"` on the root
element to force one palette, for example from a site's own light/dark switch.

The other themes have one palette each. Light: `catppuccin-latte`,
`flexoki-light`, `lupine`, `white`. Dark: `ethereal`, `hackerman`,
`last-horizon`, `lumon`, `matte-black`, `miasma`, `nord`, `osaka-jade`,
`retro-82`, `ristretto`, `solitude`, `vantablack`.

`markusmd.themes.THEME_MODES` maps every theme name to `both`, `light` or
`dark`.
