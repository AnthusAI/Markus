---
title: Diagram
description: diagram, node, row and link, flow diagrams written as Markdown and rendered as accessible HTML.
---

A diagram is a vertical flow of boxes. `node` is a box with a title and a Markdown body, `row` places nodes side by side (stacked on narrow screens), and `link` is the arrow between two items. It renders as an ordered list with plain HTML and CSS: no script and no image, so it reads correctly with a screen reader.

## Attributes

| Directive | Attribute | Values | Default |
| --- | --- | --- | --- |
| `diagram` | `title` | any text | `Diagram` for assistive technology |
| `node` | `title` | any text (required) |  |
| `node` | `tone` | `neutral`, `human`, `agent`, `risk`, `ok` | `neutral` |
| `link` | `label` | text for the downward arrow | none |
| `link` | `back` | text for an upward arrow | none |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

`tone` is a meaning, never a color: the theme chooses the color. A `link` is a leaf (`::link`) and must sit between two nodes or rows. Prose after the last node or row becomes the caption; prose anywhere else is an error.

## A loop with a feedback arrow

:::example
```markus
:::diagram{title="The Cybernetic Loop"}
:::node{title="Engine" tone="agent"}
LLM generation. Fast, prolific, tireless, with no opinion about whether the output is correct.
:::
::link{label="output" back="correction"}
:::node{title="Governor" tone="human"}
Specs, tests, CI gates, telemetry. Slow, opinionated; measures the output against intent.
:::
Skip the loop and it stops being cybernetic: it is just an Engine running open, *vibe coding*.
:::
```
:::

## Side by side

:::example
```markus
:::diagram{title="Two Minds, Two Systems"}
:::row
:::node{title="System 1" tone="agent"}
Fast, intuitive, pattern-matching, with no verification.

Externalized as **Vibe Coding (LLMs)**, the Engine.
:::
:::node{title="System 2" tone="human"}
Slow, deliberate, logical, effortful.

Externalized as **Engineering Discipline (BDD/TDD)**, the Governor.
:::
:::
:::
```
:::

## Three nodes in a row

:::example
```markus
:::diagram{title="Where the LLM Sits"}
:::row
:::node{title="Source"}
Prompt injection triggers a flaw downstream.

`attacker -> (LLM) -> victim component`
:::
:::node{title="Actuator"}
The LLM's own reasoning bridges the path.

`attacker -> (LLM) -> downstream system`
:::
:::node{title="Target" tone="risk"}
The model's own alignment is what breaks.

`attacker -> [(LLM)]`
:::
:::
:::
```
:::

## A hierarchy with rows and links

:::example
```markus
:::diagram{title="One supervised software team"}
:::node{title="Human" tone="human"}
:::
::link{label="sets direction and checks outcomes"}
:::node{title="Software Director" tone="agent"}
:::
::link{label="assigns and reviews work"}
:::row
:::node{title="Coding agent" tone="agent"}
:::
:::node{title="Coding agent" tone="agent"}
:::
:::node{title="Coding agent" tone="agent"}
:::
:::node{title="Coding agent" tone="agent"}
:::
:::
The human sets direction. The Software Director handles the day-to-day loop.
:::
```
:::

## Tones

:::example
```markus
:::diagram{title="Tones"}
:::row
:::node{title="neutral" tone="neutral"}
The default.
:::
:::node{title="human" tone="human"}
People and their judgment.
:::
:::node{title="agent" tone="agent"}
Models and automation.
:::
:::node{title="risk" tone="risk"}
Where things break.
:::
:::node{title="ok" tone="ok"}
Verified and healthy.
:::
:::
:::
```
:::
