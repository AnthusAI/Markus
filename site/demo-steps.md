---
title: Step list
description: step-list and step.
theme: catppuccin
---

# Step list

A step list is an ordered sequence. `step-list` may contain only `step` blocks; the numbering comes from the theme.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `step-list` | no attributes |  |
| `step` | no attributes |  |

### Basic

:::step-list
:::step
### Author intent

Choose semantic directives.
:::

:::step
### Validate strictly

Compile through strict schemas.
:::

:::step
### Render anywhere

Generate accessible HTML.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::step-list
:::step
### Author intent

Choose semantic directives.
:::

:::step
### Validate strictly

Compile through strict schemas.
:::

:::step
### Render anywhere

Generate accessible HTML.
:::
:::
```
:::

### Steps without headings

:::step-list
:::step
Install the package.
:::

:::step
Write a document.
:::

:::step
Run the builder.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::step-list
:::step
Install the package.
:::

:::step
Write a document.
:::

:::step
Run the builder.
:::
:::
```
:::

### Rich steps

:::step-list
:::step
### Install

```bash
pip install anthus-markus
```
:::

:::step
### Build

```bash
markus site site --out _site
```

:::callout{kind="tip"}
Use `--serve` to preview.
:::
:::
:::

:::details{summary="Markus source" open=true}
````md
:::step-list
:::step
### Install

```bash
pip install anthus-markus
```
:::

:::step
### Build

```bash
markus site site --out _site
```

:::callout{kind="tip"}
Use `--serve` to preview.
:::
:::
:::
````
:::
