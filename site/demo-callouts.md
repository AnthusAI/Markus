---
title: Callouts and asides
description: callout, note, tip, warning, caution, and aside.
theme: catppuccin
---

# Callouts and asides

Callouts mark editorial guidance. `callout` takes a `kind`; `note`, `tip`, `warning`, and `caution` are aliases that fix the kind. `aside` is for non-linear supporting material.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `kind` | `note`, `tip`, `warning`, `caution` (callout only) | `note` |
| `title` | any text | the kind, capitalized (aside: no title) |
| `id` | any text; becomes the HTML id | none |

## Callout

### Default kind

:::callout
With no attributes a callout is a note and the title is the kind, capitalized.
:::

:::details{summary="Markus source" open=true}
```md
:::callout
With no attributes a callout is a note and the title is the kind, capitalized.
:::
```
:::

### kind="note"

:::callout{kind="note"}
The note kind with the automatic title.
:::

:::details{summary="Markus source" open=true}
```md
:::callout{kind="note"}
The note kind with the automatic title.
:::
```
:::

### kind="tip"

:::callout{kind="tip"}
The tip kind with the automatic title.
:::

:::details{summary="Markus source" open=true}
```md
:::callout{kind="tip"}
The tip kind with the automatic title.
:::
```
:::

### kind="warning"

:::callout{kind="warning"}
The warning kind with the automatic title.
:::

:::details{summary="Markus source" open=true}
```md
:::callout{kind="warning"}
The warning kind with the automatic title.
:::
```
:::

### kind="caution"

:::callout{kind="caution"}
The caution kind with the automatic title.
:::

:::details{summary="Markus source" open=true}
```md
:::callout{kind="caution"}
The caution kind with the automatic title.
:::
```
:::

### Custom title

:::callout{kind="tip" title="Save a step"}
Use `title` to replace the automatic title.
:::

:::details{summary="Markus source" open=true}
```md
:::callout{kind="tip" title="Save a step"}
Use `title` to replace the automatic title.
:::
```
:::

### Body with Markdown

:::callout{kind="note" title="Rich body"}
A callout body is full Markdown:

- lists
- **emphasis** and `code`

```bash
markus site site --out _site
```
:::

:::details{summary="Markus source" open=true}
````md
:::callout{kind="note" title="Rich body"}
A callout body is full Markdown:

- lists
- **emphasis** and `code`

```bash
markus site site --out _site
```
:::
````
:::

## Alias directives: note, tip, warning, caution

Each kind is also a directive of its own. `kind` is implied by the name; only `title` is accepted.

### :::note

:::note
The `note` alias without a title.
:::

:::note{title="Custom note title"}
The `note` alias with a title.
:::

:::details{summary="Markus source" open=true}
```md
:::note
The `note` alias without a title.
:::

:::note{title="Custom note title"}
The `note` alias with a title.
:::
```
:::

### :::tip

:::tip
The `tip` alias without a title.
:::

:::tip{title="Custom tip title"}
The `tip` alias with a title.
:::

:::details{summary="Markus source" open=true}
```md
:::tip
The `tip` alias without a title.
:::

:::tip{title="Custom tip title"}
The `tip` alias with a title.
:::
```
:::

### :::warning

:::warning
The `warning` alias without a title.
:::

:::warning{title="Custom warning title"}
The `warning` alias with a title.
:::

:::details{summary="Markus source" open=true}
```md
:::warning
The `warning` alias without a title.
:::

:::warning{title="Custom warning title"}
The `warning` alias with a title.
:::
```
:::

### :::caution

:::caution
The `caution` alias without a title.
:::

:::caution{title="Custom caution title"}
The `caution` alias with a title.
:::

:::details{summary="Markus source" open=true}
```md
:::caution
The `caution` alias without a title.
:::

:::caution{title="Custom caution title"}
The `caution` alias with a title.
:::
```
:::

## Aside

An aside is supporting material that sits apart from the main flow. It is a separate directive from callout.

### Aside without title

:::aside
Supporting material with no heading.
:::

:::details{summary="Markus source" open=true}
```md
:::aside
Supporting material with no heading.
:::
```
:::

### Aside with title

:::aside{title="Why this matters"}
An aside should still make sense if a renderer flattens the page to one column.
:::

:::details{summary="Markus source" open=true}
```md
:::aside{title="Why this matters"}
An aside should still make sense if a renderer flattens the page to one column.
:::
```
:::
