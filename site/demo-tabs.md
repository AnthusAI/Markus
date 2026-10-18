---
title: Tabs
description: tabs and tab.
---

Tabs group alternatives. `tabs` may contain only `tab` blocks, and every tab needs a `label`.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| tabs `label` | any text; accessible name | none |
| tab `label` | any text (required) |  |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

### Basic

:::example
````markus
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
````
:::

### Tabs with a label

The `label` on `tabs` is the accessible name of the tab list.

:::example
```markus
:::tabs{label="Install methods"}
:::tab{label="pip"}
Use pip.
:::

:::tab{label="uv"}
Use uv.
:::

:::tab{label="From source"}
Clone and install.
:::
:::
```
:::

### Rich panels

:::example
```markus
:::tabs
:::tab{label="Prose"}
Any Markdown works in a panel.

- list item
:::

:::tab{label="Directive"}
:::callout{kind="note"}
A callout in a panel.
:::
:::
:::
```
:::
