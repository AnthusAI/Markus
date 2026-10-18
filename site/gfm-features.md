---
title: GFM feature demos
description: Every GitHub Flavored Markdown feature Markus renders.
theme: catppuccin
---

# GFM feature demos

Markus renders CommonMark plus the GFM extensions with markdown-it. Each section shows the rendered result, then the source.

[All features](features.html)

## Headings

# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

:::details{summary="Markdown source" open=true}
```md
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
```
:::

## Emphasis, strong, strikethrough, inline code

*Italic*, **bold**, ***both***, ~~struck~~, and `inline code`.

:::details{summary="Markdown source" open=true}
```md
*Italic*, **bold**, ***both***, ~~struck~~, and `inline code`.
```
:::

## Links and autolinks

An [inline link](https://github.github.com/gfm/), a [link with a title](https://example.com "Example title"), a [reference link][ref], and a bare URL https://github.com/AnthusAI/Markus that becomes a link.

[ref]: https://example.com

:::details{summary="Markdown source" open=true}
```md
An [inline link](https://github.github.com/gfm/), a [link with a title](https://example.com "Example title"), a [reference link][ref], and a bare URL https://github.com/AnthusAI/Markus that becomes a link.

[ref]: https://example.com
```
:::

## Images

![Markus pipeline](assets/pipeline.svg)

:::details{summary="Markdown source" open=true}
```md
![Markus pipeline](assets/pipeline.svg)
```
:::

## Bullet lists, nested

- Parse
- Validate
  - Attributes
  - Nesting
- Render

:::details{summary="Markdown source" open=true}
```md
- Parse
- Validate
  - Attributes
  - Nesting
- Render
```
:::

## Ordered lists

1. Parse
2. Validate
3. Render

Starting elsewhere:

5. Five
6. Six

:::details{summary="Markdown source" open=true}
```md
1. Parse
2. Validate
3. Render

Starting elsewhere:

5. Five
6. Six
```
:::

## Task lists

- [x] Tables
- [x] Strikethrough
- [ ] Something still to do

:::details{summary="Markdown source" open=true}
```md
- [x] Tables
- [x] Strikethrough
- [ ] Something still to do
```
:::

## Tables with alignment

| Left | Center | Right |
| :--- | :---: | ---: |
| a | b | c |
| longer | cell | 12 |

:::details{summary="Markdown source" open=true}
```md
| Left | Center | Right |
| :--- | :---: | ---: |
| a | b | c |
| longer | cell | 12 |
```
:::

## Fenced code with a language

```python
from markusmd import convert

html = convert("# Hello\n")
```

:::details{summary="Markdown source" open=true}
````md
```python
from markusmd import convert

html = convert("# Hello\n")
```
````
:::

## Indented code

    four spaces
    make a code block

:::details{summary="Markdown source" open=true}
```md
    four spaces
    make a code block
```
:::

## Blockquotes

> A quote.
>
> > A nested quote.

:::details{summary="Markdown source" open=true}
```md
> A quote.
>
> > A nested quote.
```
:::

## GFM alerts

> [!NOTE]
> A note alert.

> [!WARNING]
> A warning alert.

:::details{summary="Markdown source" open=true}
```md
> [!NOTE]
> A note alert.

> [!WARNING]
> A warning alert.
```
:::

## Thematic break

Above

---

Below

:::details{summary="Markdown source" open=true}
```md
Above

---

Below
```
:::

## Hard and soft line breaks

A soft break
continues the line.

A hard break ends with two spaces  
or a backslash\
and starts a new line.

:::details{summary="Markdown source" open=true}
```md
A soft break
continues the line.

A hard break ends with two spaces  
or a backslash\
and starts a new line.
```
:::

## Typographer

"Smart quotes", it's, an ellipsis..., and a dash -- or --- are typeset.

:::details{summary="Markdown source" open=true}
```md
"Smart quotes", it's, an ellipsis..., and a dash -- or --- are typeset.
```
:::

## Escapes

\*not italic\*, \`not code\`, and \# not a heading.

:::details{summary="Markdown source" open=true}
```md
\*not italic\*, \`not code\`, and \# not a heading.
```
:::

## Raw HTML

Raw HTML is off unless you pass `--allow-html`. This site does not enable it, so an HTML tag in source is shown as text:

<kbd>Ctrl</kbd>
