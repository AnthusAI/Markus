---
title: Step list
description: step-list and step.
---

A step list is an ordered sequence. `step-list` may contain only `step` blocks; the numbering comes from the theme.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `step-list` | no attributes |  |
| `step` | no attributes |  |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

### Basic

:::example
```markus
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

:::example
```markus
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

:::example
````markus
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
