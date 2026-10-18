---
title: Bar chart
description: bar-chart, labeled horizontal bars written as a plain Markdown table.
---

A bar chart is a container whose body is a Markdown table: label, value, and an optional note. The table is also the accessible output and the fallback in any plain Markdown renderer.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `title` | any text | none |
| `max` | number that fills a bar completely | `100` |
| `unit` | suffix shown after values | `%` |
| `caption` | caption text when no paragraph follows the table | none |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

Each value must be a number from 0 to `max`. A non-numeric value or a value above `max` is a validation error that names the row.

## Context Snowball

The trailing paragraph is the caption, rendered italic and centered.

:::example
```markus
:::bar-chart{title="Context Snowball"}
| Turn | Context used | Size |
| --- | --- | --- |
| Turn 1 | 2 | ~4K tokens |
| Turn 10 | 35 | ~70K tokens |
| Turn 25 | 75 | ~150K tokens |
| Turn 50 | 100 | ~200K (full window) |

Every turn re-sends the whole conversation. On a 50-turn session, that's roughly **25 input tokens for every 1 output token** - illustrative, not a measured trace.
:::
```
:::

## Two columns, no title

The note column is optional.

:::example
```markus
:::bar-chart
| Resolved tasks | Rate |
| --- | --- |
| GPT-5 mini | 58.8 |
| GPT-5 | 58.0 |
| Devstral 2 Small | 42.2 |
| Qwen 3 Coder | 32.3 |
:::
```
:::

## Custom max and unit

`max` is the value that fills the bar. Cells may repeat the unit.

:::example
```markus
:::bar-chart{title="Build stages" max=200 unit="ms" caption="Lower is better."}
| Stage | Time | Share |
| --- | --- | --- |
| Parse | 40 ms | cheap |
| Render | 150 ms | most of the build |
| Write | 20 | negligible |
:::
```
:::

## In a card

:::card{title="Disk usage"}
:::bar-chart{max=500 unit="GB"}
| Volume | Used |
| --- | --- |
| system | 120 |
| data | 340 |
:::
:::
