---
title: Bar chart
description: bar-chart, labeled horizontal bars written as a plain Markdown table.
theme: catppuccin
---

# Bar chart

A bar chart is a container whose body is a Markdown table: label, value, and an optional note. The table is also the accessible output and the fallback in any plain Markdown renderer.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `title` | any text | none |
| `max` | number that fills a bar completely | `100` |
| `unit` | suffix shown after values | `%` |
| `caption` | caption text when no paragraph follows the table | none |

Each value must be a number from 0 to `max`. A non-numeric value or a value above `max` is a validation error that names the row.

## Context Snowball

The trailing paragraph is the caption, rendered italic and centered.

:::bar-chart{title="Context Snowball"}
| Turn | Context used | Size |
| --- | --- | --- |
| Turn 1 | 2 | ~4K tokens |
| Turn 10 | 35 | ~70K tokens |
| Turn 25 | 75 | ~150K tokens |
| Turn 50 | 100 | ~200K (full window) |

Every turn re-sends the whole conversation. On a 50-turn session, that's roughly **25 input tokens for every 1 output token** - illustrative, not a measured trace.
:::

:::details{summary="Markus source" open=true}
```md
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

:::bar-chart
| Resolved tasks | Rate |
| --- | --- |
| GPT-5 mini | 58.8 |
| GPT-5 | 58.0 |
| Devstral 2 Small | 42.2 |
| Qwen 3 Coder | 32.3 |
:::

:::details{summary="Markus source" open=true}
```md
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

:::bar-chart{title="Build stages" max=200 unit="ms" caption="Lower is better."}
| Stage | Time | Share |
| --- | --- | --- |
| Parse | 40 ms | cheap |
| Render | 150 ms | most of the build |
| Write | 20 | negligible |
:::

:::details{summary="Markus source" open=true}
```md
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
