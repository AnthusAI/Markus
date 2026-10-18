---
title: Highlight
description: ==text==, inline highlighting that renders a mark element.
---

Wrap a phrase in double equals signs to highlight it. The renderer emits a `<mark>` element, and the color comes from the theme, so it is readable in every theme.

## Rules

- The opening `==` must touch the first word and the closing `==` the last word, so `x == y` stays plain text.
- A highlight may contain emphasis, strong text, links and code, and may sit inside them.
- A highlight may span soft line breaks inside one paragraph. It cannot cross a blank line.
- Highlights are never applied inside inline code or fenced code.

## A phrase

:::example
```markus
A preview of ==a new type of software solution.== that arrived early.
```
:::

## Strong text inside

:::example
```markus
==**Run the counterfactual as a smoke test.**== Then compare the numbers.
```
:::

## Across two lines

:::example
```markus
The sentence starts ==with a highlight that runs
across two source lines== and then ends normally.
```
:::

## Next to code

:::example
```markus
Inline code stays literal: `a ==b== c`, and ==a *nested emphasis* phrase== is fine.
```
:::
