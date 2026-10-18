---
title: Syntax and metadata
description: front matter, attribute syntax, ids, nesting, and the editorial-finding directive.
theme: catppuccin
---

# Syntax and metadata

The rules that apply to every directive.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| any directive `id` | any text; becomes the HTML id | none |
| finding `id` | `finding-` plus 16 hex characters (required) |  |
| finding `kind` | any non-empty text (required) |  |
| finding `rationale` | any text | none |
| finding `decision` | `skip`, `rewrite`, `delete`, `keep`, `add` | none |
| finding `group` | any text | none |

## Front matter

Every page here starts with YAML front matter. Optional fields are `title`, `description`, `authors`, `date`, and `theme`.

### Front matter

---
title: The future of local inference
description: A short summary.
authors:
  - Ada
  - Grace
date: 2026-09-04
theme: catppuccin
---

# The future of local inference

:::details{summary="Markus source" open=true}
```md
---
title: The future of local inference
description: A short summary.
authors:
  - Ada
  - Grace
date: 2026-09-04
theme: catppuccin
---

# The future of local inference
```
:::

## Attribute syntax

### Quoting and bare values

Values may use double quotes, single quotes, or no quotes. A bare name is `true`; `true`, `false`, and numbers are coerced.

:::card-grid{columns=2 label='Single quotes work'}
:::card{title="Double quotes" span=1}
Bare numbers are integers.
:::
:::

:::details{summary="Flags" open}
A bare name with no value is `true`.
:::

:::details{summary="Markus source" open=true}
```md
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

### Element id

:::callout{kind="note" id="anchor-demo" title="Linkable"}
Every directive accepts `id`, which becomes the HTML id, so [this link](#anchor-demo) can point at it.
:::

:::details{summary="Markus source" open=true}
```md
:::callout{kind="note" id="anchor-demo" title="Linkable"}
Every directive accepts `id`, which becomes the HTML id, so [this link](#anchor-demo) can point at it.
:::
```
:::

## Nesting

Containers nest freely except where a parent restricts its children.

### Directives inside directives

Use longer colon fences on the outer directive when inner and outer would otherwise close at the same fence.

::::callout{kind="note" title="Outer"}
Outer body.

:::details{summary="Inner"}
An inner directive.
:::
::::

:::details{summary="Markus source" open=true}
```md
::::callout{kind="note" title="Outer"}
Outer body.

:::details{summary="Inner"}
An inner directive.
:::
::::
```
:::

### Directives in code fences are not scanned

```md
:::callout{kind="note"}
This is shown, not rendered.
:::
```

:::details{summary="Markus source" open=true}
````md
```md
:::callout{kind="note"}
This is shown, not rendered.
:::
```
````
:::

## Editorial finding

`editorial-finding` is a machine-oriented block used by the editorial diagnose tooling. It requires an `id` of the form `finding-` followed by 16 lowercase hex characters, and a `kind`.

### Editorial finding

:::editorial-finding{id="finding-0123456789abcdef" kind="clarity" rationale="Sentence is long" decision="rewrite" group="intro"}
The sentence under review.
:::

:::details{summary="Markus source" open=true}
```md
:::editorial-finding{id="finding-0123456789abcdef" kind="clarity" rationale="Sentence is long" decision="rewrite" group="intro"}
The sentence under review.
:::
```
:::
