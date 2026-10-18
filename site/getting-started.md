---
title: Get started
description: Install Markus, convert a page, and use it from Python.
---

Markus is GitHub Flavored Markdown with a small vocabulary for layout intent. You write Markdown; where Markdown cannot say what you mean, you add a colon-fenced directive.

## Install

Markus needs Python 3.10 or newer. The package is `anthus-markus`, the module is `markusmd`, and the command is `markus`.

```bash
pip install anthus-markus
```

## Write a page

Save this as `page.md`. The preview beside it is what Markus renders.

:::example
```markus
---
title: Release notes
description: What changed this week.
---

We shipped **three** improvements.

:::callout{kind="tip" title="Upgrade now"}
Every change is backward compatible.
:::

::metric{value="38" unit="%" label="Faster builds" delta="-38%"}
```
:::

## Convert it

```bash
markus convert page.md -o page.html
```

`convert` writes a complete HTML document with Markus's stylesheet inlined. Useful options:

| Option | Effect |
| --- | --- |
| `--fragment` | Emit only the `<article>`, for embedding in your own template |
| `--no-css` | Leave the stylesheet out and link your own |
| `--theme NAME` | Apply a named theme |
| `--minify-css` | Minify the inlined stylesheet |
| `-o FILE` | Write to a file instead of stdout; use `-` as the source to read stdin |

## Check it

```bash
markus validate page.md
markus ast page.md
```

`validate` reports the first unknown directive, unknown attribute, or misplaced child with its line number. `ast` prints the validated document as JSON: front matter and an ordered list of directive and Markdown block nodes.

## Edit with a live preview

```bash
markus preview page.md
```

`preview` opens a local editor with the rendered page beside the source.

## Use it from Python

```python
from markusmd import convert, parse, parse_document

html = convert(open("page.md", encoding="utf-8").read())
fragment = convert(source, full_document=False, include_css=False)

document = parse(source)           # validated AST: Document, Directive, MarkdownBlock
tree = parse_document(source)      # the same structure as plain JSON-ready data
```

Invalid source raises `MarkusSyntaxError` or `MarkusValidationError`, both subclasses of `MarkusError`, each with a `line` attribute.

## Where to next

- [Syntax and metadata](demo-syntax.html) covers the rules every directive shares.
- The [feature index](features.html) lists every directive with its page.
