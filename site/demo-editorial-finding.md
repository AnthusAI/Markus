---
title: Editorial finding
description: editorial-finding marks one passage that an editorial review flagged, with its kind, rationale, and decision.
---

`editorial-finding` wraps a passage that an editorial review flagged. Diagnose tooling writes these blocks so a human or an agent can read the finding beside the text it is about, and a later pass can act on the `decision`.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `id` | `finding-` plus 16 lowercase hex characters (required) | none |
| `kind` | any non-empty text, such as `clarity` or `redundancy` (required) | none |
| `rationale` | any text | none |
| `decision` | `skip`, `rewrite`, `delete`, `keep`, `add` | none |
| `group` | any text; findings with the same group belong together | none |

The `id` becomes the HTML id, and `kind`, `decision`, and `group` are exposed as `data-` attributes for tooling.

## A finding with every attribute

:::example
```markus
:::editorial-finding{id="finding-0123456789abcdef" kind="clarity" rationale="Sentence is long" decision="rewrite" group="intro"}
The sentence under review, which goes on for rather longer than it needs to before reaching its point.
:::
```
:::

## Only the required attributes

:::example
```markus
:::editorial-finding{id="finding-00000000000000aa" kind="redundancy"}
This paragraph repeats the one above it.
:::
```
:::

## A finding with no passage

A finding can be empty, for example when the decision is to `add` something that is missing.

:::example
```markus
:::editorial-finding{id="finding-00000000000000bb" kind="missing-context" rationale="Define the acronym on first use" decision="add"}
:::
```
:::

## Invalid ids

The id format is checked, so a finding cannot silently collide with an ordinary heading or element id.

```md
:::editorial-finding{id="intro" kind="clarity"}
Fails: id must match finding-[16 lowercase hex chars].
:::
```
