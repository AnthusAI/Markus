---
title: Syntax and metadata
description: Front matter, container and leaf directives, attributes, ids, nesting, and validation.
---

Markus is GitHub Flavored Markdown plus colon-fenced directives. These rules apply to every directive on every other page.

## Front matter

A document may start with YAML front matter. Markus renders `title`, `description`, `authors`, and `date` as the document header and carries every other key through unchanged for the publishing system to use.

| Key | Meaning |
| --- | --- |
| `title` | Document title, rendered as the page heading |
| `description` | One-line summary, rendered as the lede |
| `authors` | A list of names, or of `{name, url}` mappings |
| `date` | Publication date |
| `theme` | A named Markus theme for the whole document |

:::example
```markus
---
title: The future of local inference
description: A short summary.
authors:
  - Ada
  - Grace
date: 2026-09-04
---

The body starts here.
```
:::

`authors` entries may also be mappings. Markus passes them through as data; it never turns them into HTML.

```md
---
authors:
  - name: Ada Lovelace
    url: /authors/ada
---
```

## Container directives

A container opens with three or more colons and a name, holds Markdown (including other directives), and closes with a line of colons.

:::example
```markus
:::callout{kind="tip"}
A container holds **Markdown**, lists, code, and other directives.
:::
```
:::

## Leaf directives

A leaf is two colons and a name on one line. It has attributes and no body. `metric`, `video`, and the diagram `link` are leaves.

:::example
```markus
::metric{value="12" unit="ms" label="p95 latency" delta="-8%"}
```
:::

## Attributes

### Quoting and bare values

Values may use double quotes, single quotes, or no quotes. A bare name with no value is `true`; `true`, `false`, and numbers are coerced to their types.

:::example{layout="stacked"}
```markus
:::card-grid{columns=2 label='Single quotes work'}
:::card{title="Double quotes" span=1}
Bare numbers are integers.
:::
:::

:::details{summary="Flags" open}
A bare name with no value is `true`.
:::
```
:::

### Multi-line attribute blocks

Long attribute blocks may span several lines. The opening `{` stays on the directive line; the block ends at the first `}` outside quotes. Inside a quoted value, a backslash escapes the next character.

:::example
```markus
::metric{
  value="12"
  unit="ms"
  label="Two quote kinds: ' and \""
}

:::callout{
  kind="note"
  title="Spread over lines"
}
Same meaning, easier to read.
:::
```
:::

### Trailing attribute lists

A kramdown-style `{: key=value }` line inside a container sets attributes after the content, which reads naturally for quotations.

:::example
```markus
:::pull-quote
> Measure what matters.
{: attribution="Editorial principle" }
:::
```
:::

### Element id

Every directive accepts `id`, which becomes the HTML id, so links can point at it.

:::example
```markus
:::callout{kind="note" id="anchor-demo" title="Linkable"}
[This link](#anchor-demo) points at the callout it sits in.
:::
```
:::

## Nesting

Containers nest freely except where a parent restricts its children, such as `column` inside `two-up` or `tab` inside `tabs`. Give the outer directive a longer colon fence when that makes the structure easier to read.

:::example
```markus
::::callout{kind="note" title="Outer"}
Outer body.

:::details{summary="Inner"}
An inner directive.
:::
::::
```
:::

### Directives in code fences are not scanned

Colon fences inside a code block are shown, not rendered, so documentation can quote Markus.

:::example
````markus
```md
:::callout{kind="note"}
This is shown, not rendered.
:::
```
````
:::

## Validation

Markus parses, validates, then renders. An unknown directive, an unknown attribute, a value outside its allowed set, or a child in the wrong parent stops the build with the line number. Attributes describe meaning, so there is no `margin`, `color`, or `columns-template` to reach for.

```md
:::callout{kind="loud"}
Fails: kind must be note, tip, warning, or caution.
:::

:::callout{color="red"}
Fails: unknown attribute 'color'. Attributes describe meaning, not presentation.
:::
```

Check a file without rendering it:

```bash
markus validate page.md
```
