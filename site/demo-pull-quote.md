---
title: Pull quote
description: pull-quote with attribution, source, tone, and align.
theme: catppuccin
---

# Pull quote

A pull quote is an editorial quotation lifted out of the text. The body is Markdown; the theme chooses the quotation styling.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `attribution` | any text | none |
| `source` | any text; rendered as a citation | none |
| `tone` | `default`, `primary`, `quiet` | `default` |
| `align` | `inline`, `left`, `right` | `inline` |

### Plain

:::pull-quote
A quotation with no attribution.
:::

:::details{summary="Markus source" open=true}
```md
:::pull-quote
A quotation with no attribution.
:::
```
:::

### Attribution

:::pull-quote{attribution="Donella Meadows"}
The least obvious part of a system is often its most crucial determinant.
:::

:::details{summary="Markus source" open=true}
```md
:::pull-quote{attribution="Donella Meadows"}
The least obvious part of a system is often its most crucial determinant.
:::
```
:::

### Attribution and source

:::pull-quote{attribution="Donella Meadows" source="Thinking in Systems"}
The source renders as a citation after the attribution.
:::

:::details{summary="Markus source" open=true}
```md
:::pull-quote{attribution="Donella Meadows" source="Thinking in Systems"}
The source renders as a citation after the attribution.
:::
```
:::

### Source only

:::pull-quote{source="Thinking in Systems"}
A citation without a named person.
:::

:::details{summary="Markus source" open=true}
```md
:::pull-quote{source="Thinking in Systems"}
A citation without a named person.
:::
```
:::

## Tone

### tone="default"

:::pull-quote{attribution="Tone demo" tone="default"}
The default tone.
:::

:::details{summary="Markus source" open=true}
```md
:::pull-quote{attribution="Tone demo" tone="default"}
The default tone.
:::
```
:::

### tone="primary"

:::pull-quote{attribution="Tone demo" tone="primary"}
The primary tone, for the quotation that carries the page.
:::

:::details{summary="Markus source" open=true}
```md
:::pull-quote{attribution="Tone demo" tone="primary"}
The primary tone, for the quotation that carries the page.
:::
```
:::

### tone="quiet"

:::pull-quote{attribution="Tone demo" tone="quiet"}
The quiet tone, for a quotation that should not shout.
:::

:::details{summary="Markus source" open=true}
```md
:::pull-quote{attribution="Tone demo" tone="quiet"}
The quiet tone, for a quotation that should not shout.
:::
```
:::

## Align

### align="inline"

:::pull-quote{attribution="Align demo" align="inline"}
Inline: the quote sits in the text flow.
:::

This paragraph follows the quote and wraps beside it when the theme floats it. Keep writing a few lines so the wrap is visible: the quick brown fox jumps over the lazy dog, and then does it again for good measure so that the text is long enough.

:::details{summary="Markus source" open=true}
```md
:::pull-quote{attribution="Align demo" align="inline"}
Inline: the quote sits in the text flow.
:::

This paragraph follows the quote and wraps beside it when the theme floats it. Keep writing a few lines so the wrap is visible: the quick brown fox jumps over the lazy dog, and then does it again for good measure so that the text is long enough.
```
:::

### align="left"

:::pull-quote{attribution="Align demo" align="left"}
Left: the quote floats to the left of the text.
:::

This paragraph follows the quote and wraps beside it when the theme floats it. Keep writing a few lines so the wrap is visible: the quick brown fox jumps over the lazy dog, and then does it again for good measure so that the text is long enough.

:::details{summary="Markus source" open=true}
```md
:::pull-quote{attribution="Align demo" align="left"}
Left: the quote floats to the left of the text.
:::

This paragraph follows the quote and wraps beside it when the theme floats it. Keep writing a few lines so the wrap is visible: the quick brown fox jumps over the lazy dog, and then does it again for good measure so that the text is long enough.
```
:::

### align="right"

:::pull-quote{attribution="Align demo" align="right"}
Right: the quote floats to the right of the text.
:::

This paragraph follows the quote and wraps beside it when the theme floats it. Keep writing a few lines so the wrap is visible: the quick brown fox jumps over the lazy dog, and then does it again for good measure so that the text is long enough.

:::details{summary="Markus source" open=true}
```md
:::pull-quote{attribution="Align demo" align="right"}
Right: the quote floats to the right of the text.
:::

This paragraph follows the quote and wraps beside it when the theme floats it. Keep writing a few lines so the wrap is visible: the quick brown fox jumps over the lazy dog, and then does it again for good measure so that the text is long enough.
```
:::

## Blockquote body and inline attribute list

### Attributes from a trailing list

A kramdown-style attribute line inside the directive supplies attributes, which is handy when the body is already a blockquote. The directive below has a blockquote body, then a final line of the form `{: attribution="Editorial principle" tone="quiet" }`. (The source is described rather than shown because the attribute-line scanner also matches lines inside code fences; see the improvement notes.)

:::pull-quote
> Measure what matters, then improve what you can.
{: attribution="Editorial principle" tone="quiet" }
:::
