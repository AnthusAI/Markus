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

A trailing kramdown-style attribute list is also accepted inside a directive:

```md
:::pull-quote
> Measure what matters.
{: attribution="Editorial principle" }
:::
```

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
- Other containers may nest Markdown and further directives
- Fenced code blocks are not scanned for directives

## What does not belong in source

Do not add `margin`, `width`, `font-size`, or other presentation keys.
Unknown directive names and unknown attributes fail validation.
