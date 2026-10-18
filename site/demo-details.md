---
title: Details
description: details, collapsed and open.
---

Details is progressive disclosure for material that is true but not on the main path. It is a native HTML `details` element.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `summary` | any text | `Details` |
| `open` | `true` or `false` | `false` |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

### Collapsed (default)

:::example
```markus
:::details{summary="Click to expand"}
Hidden until opened. The body is Markdown, including other directives.
:::
```
:::

### Open

:::example
```markus
:::details{summary="Starts open" open=true}
Visible on load.
:::
```
:::

### Default summary

:::example
```markus
:::details
With no `summary` the label is "Details".
:::
```
:::

### Nested directive

:::example
```markus
:::details{summary="Contains a callout"}
:::callout{kind="tip"}
A callout inside details.
:::
:::
```
:::
