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

## Container directives

```
:::name{key="value" flag other=1}
Markdown, including nested directives.
:::
```

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
| `editorial-finding` | Editorial diagnose finding (machine or human) | `id`, `kind`, `rationale`, `decision`, `group` |

A trailing kramdown-style attribute list is also accepted inside a directive:

```md
:::pull-quote
> Measure what matters.
{: attribution="Editorial principle" }
:::
```

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

## Nesting rules

- `card-grid` may contain only `card` (or the `feature-card` alias)
- `two-up` must contain exactly two `column` children
- `tabs` may contain only `tab`
- `step-list` may contain only `step`
- `timeline` may contain only `timeline-event`
- Other containers may nest Markdown and further directives
- Fenced code blocks are not scanned for directives

## What does not belong in source

Do not add `margin`, `width`, `font-size`, or other presentation keys.
Unknown directive names and unknown attributes fail validation.
