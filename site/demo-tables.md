---
title: Tables
description: GFM tables with alignment, wrapping, numeric columns, and horizontal scrolling.
theme: catppuccin
---

# Tables

Tables are plain GFM. Markus themes them in every theme: header styling, striped rows, tabular numerals, wrapped cell text, and a focusable scroll region so a wide table never breaks the page on a small screen.

[All features](features.html)

## Benchmark results

The delimiter row sets alignment: `:---` left, `---:` right, `:---:` center. Numeric columns are right aligned so digits line up.

| Model / agent configuration | Resolved tasks | Cost per task |
| :--- | ---: | ---: |
| GPT-5 mini + schema-guided agent | 58.8% | $0.24 |
| GPT-5 + schema-guided agent | 58.0% | $0.86 |
| Qwen 3 Coder + schema-guided agent | 32.3% | $0.13 |
| Devstral 2 Small + interactive agent | 42.2% | $0.30 |

:::details{summary="Markus source" open=true}
```md
| Model / agent configuration | Resolved tasks | Cost per task |
| :--- | ---: | ---: |
| GPT-5 mini + schema-guided agent | 58.8% | $0.24 |
| GPT-5 + schema-guided agent | 58.0% | $0.86 |
| Qwen 3 Coder + schema-guided agent | 32.3% | $0.13 |
| Devstral 2 Small + interactive agent | 42.2% | $0.30 |
```
:::

## Center alignment

| Left | Center | Right |
| :--- | :---: | ---: |
| a | b | c |
| longer left | longer center | longer right |

## Long cell text

Long text wraps inside its cell instead of stretching the table.

| Topic | Notes |
| --- | --- |
| Why Markus | Authors encode intent in colon-fenced blocks, and the renderer turns that intent into accessible HTML and CSS without any presentation keys in the source. |
| Why GFM | Every table stays readable in a plain Markdown renderer, so documents degrade gracefully. |

## Wide tables scroll

This table is wider than a phone screen. It scrolls sideways inside its own region (keyboard focusable) and the rest of the page stays put.

| Region | Q1 revenue | Q2 revenue | Q3 revenue | Q4 revenue | Full-year revenue | Year-over-year growth | Headcount |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| North America | $12,400,000 | $13,100,000 | $14,250,000 | $15,900,000 | $55,650,000 | +18.2% | 142 |
| Europe | $8,900,000 | $9,300,000 | $9,750,000 | $10,400,000 | $38,350,000 | +11.7% | 96 |

## Inline formatting in cells

| Syntax | Result |
| --- | --- |
| `**bold**` | **bold** |
| `[link](features.html)` | [link](features.html) |
| `~~strike~~` | ~~strike~~ |

## Table next to a bar chart

For values that benefit from a visual, [bar-chart](demo-bar-chart.html) takes the same table and draws bars.
