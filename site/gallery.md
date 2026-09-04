---
title: Markus gallery
description: Every built-in directive, rendered from Markus source.
---

# Every directive, live

This page is itself Markus. Each section is a real block from the 0.1 registry, followed by the source that produced it.

## Callouts

:::callout{kind="note" title="Note"}
Use a note for editorial guidance, not for warnings the reader must not miss.
:::

:::warning{title="Warning"}
`:::warning` is an alias for `:::callout{kind="warning"}`.
:::

:::tip
Tips can omit a title; Markus supplies one from the kind.
:::

:::caution{title="Caution"}
Unknown attributes are rejected. This keeps the language from decaying into a CSS API.
:::

:::details{summary="Callout source"}
```md
:::callout{kind="note" title="Note"}
Use a note for editorial guidance, not for warnings the reader must not miss.
:::

:::warning{title="Warning"}
`:::warning` is an alias for `:::callout{kind="warning"}`.
:::
```
:::

## Pull quote

:::pull-quote{attribution="Donella Meadows" source="Thinking in Systems" tone="primary"}
The least obvious part of a system, its function or purpose, is often its most crucial determinant of the system’s behavior.
:::

:::details{summary="Pull-quote source"}
```md
:::pull-quote{attribution="Donella Meadows" source="Thinking in Systems" tone="primary"}
The least obvious part of a system, its function or purpose, is often its most crucial determinant of the system’s behavior.
:::
```
:::

Inline attribute lists also work, which is handy when the quote is already a Markdown blockquote:

:::pull-quote
> Measure what matters, then improve what you can.
{: attribution="Editorial principle" tone="quiet" }
:::

## Card grid

:::card-grid{columns=3 label="Authoring rules"}
:::card{icon="book" title="Keep Markdown"}
Ordinary paragraphs, lists, tables, and code fences stay GFM. Directives wrap them.
:::

:::card{icon="lock" title="Validate attributes"}
Each block has a Pydantic schema. Extra keys fail the build.
:::

:::card{icon="eye" title="Render meaning"}
Output is semantic HTML: `figure`, `aside`, `article`, `section` — not anonymous `div`s.
:::
:::

`:::feature-grid` / `:::feature-card` are aliases for the same blocks.

## Two-up

:::two-up{ratio="1:1"}
:::column
### Conventional Markdown

Authors reach for raw HTML or a pile of images when the page needs structure.
:::

:::column
### Markus

Authors name the structure. The theme chooses a responsive layout, including print.
:::
:::

On a three-column track, `ratio` divides the row into proportional parts:

:::two-up{ratio="2:1"}
:::column
### Primary (2 parts)

Wider column for the main narrative.
:::

:::column
### Aside (1 part)

Narrow column for a sidebar or counterpoint.
:::
:::

:::two-up{ratio="1:2"}
:::column
### Lead (1 part)

Narrow setup or qualifier.
:::

:::column
### Body (2 parts)

Wider column when the second side should dominate.
:::
:::

:::card-grid{columns=3}
:::card{span=full}
### Full width

`span=full` on a card spans every column in the grid.
:::
:::

## Figure

:::figure{src="assets/pipeline.svg" alt="Markus processing pipeline" caption="Source becomes a directive AST, then semantic HTML." credit="Anthus AI"}
:::

## Details and aside

:::details{summary="Progressive disclosure" open=true}
Details are for material that is true but not on the main path: caveats, source listings, extra procedure.
:::

:::aside{title="Supporting material"}
An aside is non-linear. It should still make sense if a later renderer flattens the page to a single column.
:::

## Metric

::metric{value="12ms" unit="p95" label="Local round trip" delta="-38%"}

Leaf directives use two colons and take no body: `::metric{value="12ms" unit="p95" label="Local round trip" delta="-38%"}`.

## Tabs

:::tabs
:::tab{label="macOS"}
```bash
brew install anthus-markus
```
:::
:::tab{label="Linux"}
```bash
pip install anthus-markus
```
:::
:::

## Step list

:::step-list
:::step
### 1. Author intent
Choose semantic directives that declare structure without presentation classes.
:::
:::step
### 2. Validate strictly
Compile through strict Pydantic schemas that reject arbitrary CSS.
:::
:::step
### 3. Render anywhere
Generate accessible HTML, styled for web and print.
:::
:::

## Video

::video{src="assets/pipeline.svg" title="Pipeline demonstration"}
