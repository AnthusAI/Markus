---
title: Two-up and columns
description: two-up and column, with every ratio and alignment.
---

A two-up is a conceptual pairing: contrast, before and after, claim and caveat. It must contain exactly two `column` children. On a narrow screen the columns stack.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `ratio` | `1:1`, `2:1`, `1:2` | `1:1` |
| `align` | `start`, `center`, `end`, `stretch` | `start` |
| `column` | no attributes |  |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

### Default

:::example{layout="stacked"}
```markus
:::two-up
:::column
### Before

Defaults to a 1:1 ratio and start alignment.
:::

:::column
### After

The second column.
:::
:::
```
:::

## Ratio

### ratio="1:1"

:::example{layout="stacked"}
```markus
:::two-up{ratio="1:1"}
:::column
### Left

First column.
:::

:::column
### Right

Second column.
:::
:::
```
:::

### ratio="2:1"

:::example{layout="stacked"}
```markus
:::two-up{ratio="2:1"}
:::column
### Wide

First column.
:::

:::column
### Narrow

Second column.
:::
:::
```
:::

### ratio="1:2"

:::example{layout="stacked"}
```markus
:::two-up{ratio="1:2"}
:::column
### Narrow

First column.
:::

:::column
### Wide

Second column.
:::
:::
```
:::

## Align

`align` controls how columns of different heights line up.

### align="start"

:::example{layout="stacked"}
```markus
:::two-up{ratio="1:1" align="start"}
:::column
### Short

One line.
:::

:::column
### Tall

Many lines follow.

Second paragraph.

Third paragraph.

Fourth paragraph.
:::
:::
```
:::

### align="center"

:::example{layout="stacked"}
```markus
:::two-up{ratio="1:1" align="center"}
:::column
### Short

One line.
:::

:::column
### Tall

Many lines follow.

Second paragraph.

Third paragraph.

Fourth paragraph.
:::
:::
```
:::

### align="end"

:::example{layout="stacked"}
```markus
:::two-up{ratio="1:1" align="end"}
:::column
### Short

One line.
:::

:::column
### Tall

Many lines follow.

Second paragraph.

Third paragraph.

Fourth paragraph.
:::
:::
```
:::

### align="stretch"

:::example{layout="stacked"}
```markus
:::two-up{ratio="1:1" align="stretch"}
:::column
### Short

One line.
:::

:::column
### Tall

Many lines follow.

Second paragraph.

Third paragraph.

Fourth paragraph.
:::
:::
```
:::

### Nested directives in a column

:::example{layout="stacked"}
```markus
:::two-up{ratio="1:1"}
:::column
:::callout{kind="warning" title="Claim"}
A callout inside a column.
:::
:::

:::column
:::callout{kind="tip" title="Caveat"}
Another in the second.
:::
:::
:::
```
:::
