---
title: Details
description: details, collapsed and open.
theme: catppuccin
---

# Details

Details is progressive disclosure for material that is true but not on the main path. It is a native HTML `details` element.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `summary` | any text | `Details` |
| `open` | `true` or `false` | `false` |

### Collapsed (default)

:::details{summary="Click to expand"}
Hidden until opened. The body is Markdown, including other directives.
:::

:::details{summary="Markus source" open=true}
```md
:::details{summary="Click to expand"}
Hidden until opened. The body is Markdown, including other directives.
:::
```
:::

### Open

:::details{summary="Starts open" open=true}
Visible on load.
:::

:::details{summary="Markus source" open=true}
```md
:::details{summary="Starts open" open=true}
Visible on load.
:::
```
:::

### Default summary

:::details
With no `summary` the label is "Details".
:::

:::details{summary="Markus source" open=true}
```md
:::details
With no `summary` the label is "Details".
:::
```
:::

### Nested directive

:::details{summary="Contains a callout"}
:::callout{kind="tip"}
A callout inside details.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::details{summary="Contains a callout"}
:::callout{kind="tip"}
A callout inside details.
:::
:::
```
:::
