---
title: Example
description: example shows a Markus snippet beside the page it renders, from one copy of the source.
---

`example` is for writing about Markus in Markus. It holds one fenced code block of Markus source and renders that source twice: as highlighted code and as a live preview. The two can never drift apart, because there is only one copy. Every example on this site is an `example` block.

The panes sit side by side when there is room and stack, source first, on narrow screens.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `layout` | `side-by-side`, `stacked` | `side-by-side` |
| `title` | any text; a caption above the panes | none |
| `id` | any text; becomes the HTML id | none |

## Side by side

The body is a single code fence. Use the `markus` (or `md`) info string so other Markdown renderers still show sensible code.

:::example
`````markus
:::example
```markus
:::tip
The preview renders this source.
:::
```
:::
`````
:::

## Stacked, with a title

Use `layout="stacked"` when the preview needs the full width: card grids, two-up pairs, and wide tables collapse to one column inside a half-width pane.

:::example{layout="stacked"}
`````markus
:::example{layout="stacked" title="Three peer cards"}
```markus
:::card-grid{columns=3}
:::card{title="Parse"}
Read the source.
:::
:::card{title="Validate"}
Check every directive.
:::
:::card{title="Render"}
Emit semantic HTML.
:::
:::
```
:::
`````
:::

## Code fences inside an example

When the snippet has its own code fence, give the outer fence more backticks.

:::example
``````markus
:::example
````markus
```python
print("hello")
```
````
:::
``````
:::

## Rules

- The body must be exactly one fenced code block. Anything else is a validation error.
- The snippet is parsed and validated like the page around it, so a broken example fails the build at its real line number.
- Front matter in the snippet renders as a document header in the preview.
