---
title: Tabs
description: tabs and tab.
theme: catppuccin
---

# Tabs

Tabs group alternatives. `tabs` may contain only `tab` blocks, and every tab needs a `label`.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| tabs `label` | any text; accessible name | none |
| tab `label` | any text (required) |  |

### Basic

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

:::details{summary="Markus source" open=true}
````md
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

:::details{summary="Markus source" open=true}
```md
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

:::details{summary="Markus source" open=true}
```md
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
