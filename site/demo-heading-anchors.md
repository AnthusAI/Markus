---
title: Heading anchors
description: Every heading gets a stable id, and {#custom-id} sets one explicitly.
---

Every heading gets an `id` so it can be linked. End a heading with `{#custom-id}` to choose the id yourself, which keeps links stable when the title changes.

## Generated ids {#generated-ids}

The id is the heading text lowercased, with punctuation removed and words joined by single hyphens. Inline markup is ignored. When the same slug appears twice in a document, later headings get `-1`, `-2` and so on in document order.

The headings on this page demonstrate it: this section is `generated-ids` because of its custom id, while the next heading below gets the slug `a-plain-heading`.

### A plain heading

Open the page source in your browser to see `id="a-plain-heading"` on the heading above.

## Custom ids {#custom-ids}

A custom id must start with a letter or underscore and may use letters, digits, `-`, `_`, `:` and `.`. A duplicate custom id, or a malformed one, is a validation error that names the line.

### Slug only

:::example
```markus
## Example 1: Use AI models from any company's AI API

See [the multiplexer](#ai-api-multiplexer) for the next step.
```
:::

### With a custom id

:::example
```markus
## Multiplexing across vendors {#ai-api-multiplexer}

Links such as [this one](#ai-api-multiplexer) keep working when the title is reworded.
```
:::

## Linking to a section

Link to any heading with a fragment link, for example [the generated ids section](#generated-ids) or [custom ids](#custom-ids).
