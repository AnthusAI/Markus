---
title: GitHub Flavored Markdown in Markus
description: The GFM baseline Markus keeps on purpose.
---

# GitHub Flavored Markdown

Markus starts from CommonMark plus the GFM extensions people already use in pull requests and README files. Directives wrap this baseline; they do not replace it.

## Emphasis, links, and code

Markus is **deliberately small**. It is also *deliberately boring* about inline syntax: `inline code`, ~~struck text~~, and [standard links](https://github.github.com/gfm/).

```python
from markusmd import convert

html = convert("# Hello from Markus\n")
```

Autolinks such as https://github.com/AnthusAI/Markus should light up without extra markup.

## Lists and tasks

- Colon fences nest
- YAML front matter is optional
- Raw HTML is off unless you pass `--allow-html`

1. Parse
2. Validate against the registry
3. Render semantic HTML

- [x] Tables
- [x] Strikethrough
- [x] Task lists
- [ ] Inventing a new emphasis sigil

## Tables

| Put in the document | Put in the theme |
| --- | --- |
| “This is a pull quote” | Float, type, quotation marks |
| “These are peer cards” | Responsive columns |
| “These are two views” | Split vs stack |
| “This is supplemental” | Disclosure, print hiding |

## Quotes and GFM alerts

> Ordinary blockquotes remain blockquotes.

> [!NOTE]
> GitHub-style alerts still parse as GFM. Prefer `:::callout` when you want Markus’s registry, attributes, and HTML.

:::callout{kind="tip" title="When to use a directive"}
If you need a validated attribute, nested layout, or a stable HTML contract across HTML/PDF/email, use a Markus directive. If you need a paragraph, use a paragraph.
:::
