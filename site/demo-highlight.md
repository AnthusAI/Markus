---
title: Highlight
description: ==text==, inline highlighting that renders a mark element.
theme: catppuccin
---

# Highlight

Wrap a phrase in double equals signs to highlight it. The renderer emits a `<mark>` element, and the color comes from the theme, so it is readable in every theme.

[All features](features.html)

## Rules

- The opening `==` must touch the first word and the closing `==` the last word, so `x == y` stays plain text.
- A highlight may contain emphasis, strong text, links and code, and may sit inside them.
- A highlight may span soft line breaks inside one paragraph. It cannot cross a blank line.
- Highlights are never applied inside inline code or fenced code.

## A phrase

A preview of ==a new type of software solution.== that arrived early.

:::details{summary="Markus source" open=true}
```md
A preview of ==a new type of software solution.== that arrived early.
```
:::

## Strong text inside

==**Run the counterfactual as a smoke test.**== Then compare the numbers.

:::details{summary="Markus source" open=true}
```md
==**Run the counterfactual as a smoke test.**== Then compare the numbers.
```
:::

## Across two lines

The sentence starts ==with a highlight that runs
across two source lines== and then ends normally.

:::details{summary="Markus source" open=true}
```md
The sentence starts ==with a highlight that runs
across two source lines== and then ends normally.
```
:::

## Next to code

Inline code stays literal: `a ==b== c`, and ==a *nested emphasis* phrase== is fine.

:::details{summary="Markus source" open=true}
```md
Inline code stays literal: `a ==b== c`, and ==a *nested emphasis* phrase== is fine.
```
:::
