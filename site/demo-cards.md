---
title: Card grid and cards
description: card-grid, card, feature-grid, and feature-card.
theme: catppuccin
---

# Card grid and cards

A card grid holds peer items that should read as a set. `card-grid` may contain only `card`; `feature-grid` and `feature-card` are aliases for the same blocks.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| grid `label` | any text; accessible name | `Related items` |
| grid `columns` | 1 to 6 | theme decides |
| card `icon` | `bolt`, `lock`, `gauge`, `eye`, `brain`, `quote`, `grid`, `scale`, `book`, or any text | none |
| card `title` | any text | none |
| card `span` | 1 to 6, or `full` | 1 |

### Basic grid

`label` is the accessible name of the grid and is not shown.

:::card-grid{label="Three ideas"}
:::card{title="One"}
First peer item.
:::

:::card{title="Two"}
Second peer item.
:::

:::card{title="Three"}
Third peer item.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::card-grid{label="Three ideas"}
:::card{title="One"}
First peer item.
:::

:::card{title="Two"}
Second peer item.
:::

:::card{title="Three"}
Third peer item.
:::
:::
```
:::

## Columns

`columns` is a hint from 1 to 6. The theme collapses columns on small screens.

### columns=2

:::card-grid{columns=2 label="2 columns"}
:::card{title="A"}
Body.
:::

:::card{title="B"}
Body.
:::

:::card{title="C"}
Body.
:::

:::card{title="D"}
Body.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::card-grid{columns=2 label="2 columns"}
:::card{title="A"}
Body.
:::

:::card{title="B"}
Body.
:::

:::card{title="C"}
Body.
:::

:::card{title="D"}
Body.
:::
:::
```
:::

### columns=4

:::card-grid{columns=4 label="4 columns"}
:::card{title="A"}
Body.
:::

:::card{title="B"}
Body.
:::

:::card{title="C"}
Body.
:::

:::card{title="D"}
Body.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::card-grid{columns=4 label="4 columns"}
:::card{title="A"}
Body.
:::

:::card{title="B"}
Body.
:::

:::card{title="C"}
Body.
:::

:::card{title="D"}
Body.
:::
:::
```
:::

## Card attributes

### Icon

Nine icon names map to a mark. Any other value is shown as the text you wrote, so a single character also works.

:::card-grid{columns=3 label="Icons"}
:::card{icon="bolt" title="bolt"}
Named icon.
:::

:::card{icon="lock" title="lock"}
Named icon.
:::

:::card{icon="gauge" title="gauge"}
Named icon.
:::

:::card{icon="eye" title="eye"}
Named icon.
:::

:::card{icon="brain" title="brain"}
Named icon.
:::

:::card{icon="quote" title="quote"}
Named icon.
:::

:::card{icon="grid" title="grid"}
Named icon.
:::

:::card{icon="scale" title="scale"}
Named icon.
:::

:::card{icon="book" title="book"}
Named icon.
:::

:::card{icon="rocket" title="rocket"}
An unknown icon name is rendered as literal text.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::card-grid{columns=3 label="Icons"}
:::card{icon="bolt" title="bolt"}
Named icon.
:::

:::card{icon="lock" title="lock"}
Named icon.
:::

:::card{icon="gauge" title="gauge"}
Named icon.
:::

:::card{icon="eye" title="eye"}
Named icon.
:::

:::card{icon="brain" title="brain"}
Named icon.
:::

:::card{icon="quote" title="quote"}
Named icon.
:::

:::card{icon="grid" title="grid"}
Named icon.
:::

:::card{icon="scale" title="scale"}
Named icon.
:::

:::card{icon="book" title="book"}
Named icon.
:::

:::card{icon="rocket" title="rocket"}
An unknown icon name is rendered as literal text.
:::
:::
```
:::

### Title in the attribute or a heading in the body

:::card-grid{columns=2 label="Titles"}
:::card{title="Attribute title"}
The title came from the `title` attribute.
:::

:::card
### Body heading

The title came from a Markdown heading in the body.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::card-grid{columns=2 label="Titles"}
:::card{title="Attribute title"}
The title came from the `title` attribute.
:::

:::card
### Body heading

The title came from a Markdown heading in the body.
:::
:::
```
:::

### Span

`span` is 1 to 6 or `full`.

:::card-grid{columns=3 label="Spans"}
:::card{span=1 title="span=1"}
One column.
:::

:::card{span=2 title="span=2"}
Two columns.
:::

:::card{span=3 title="span=3"}
Three columns.
:::

:::card{span=full title="span=full"}
Every column.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::card-grid{columns=3 label="Spans"}
:::card{span=1 title="span=1"}
One column.
:::

:::card{span=2 title="span=2"}
Two columns.
:::

:::card{span=3 title="span=3"}
Three columns.
:::

:::card{span=full title="span=full"}
Every column.
:::
:::
```
:::

### Rich body

:::card-grid{columns=2 label="Rich"}
:::card{icon="book" title="Lists"}
- one
- two
:::

:::card{icon="lock" title="Code"}
```python
print("hello")
```
:::
:::

:::details{summary="Markus source" open=true}
````md
:::card-grid{columns=2 label="Rich"}
:::card{icon="book" title="Lists"}
- one
- two
:::

:::card{icon="lock" title="Code"}
```python
print("hello")
```
:::
:::
````
:::

## Aliases: feature-grid and feature-card

### feature-grid with feature-card

:::feature-grid{columns=3 label="Features"}
:::feature-card{icon="bolt"}
## Fast

An alias of card.
:::

:::feature-card{icon="lock"}
## Private

An alias of card.
:::

:::feature-card{icon="eye"}
## Clear

An alias of card.
:::
:::

:::details{summary="Markus source" open=true}
```md
:::feature-grid{columns=3 label="Features"}
:::feature-card{icon="bolt"}
## Fast

An alias of card.
:::

:::feature-card{icon="lock"}
## Private

An alias of card.
:::

:::feature-card{icon="eye"}
## Clear

An alias of card.
:::
:::
```
:::
