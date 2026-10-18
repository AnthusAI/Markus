---
title: Markdown for layout intent
description: GitHub-flavored Markdown with a small, semantic vocabulary for layout.
authors:
  - Anthus AI Solutions
date: 2026-09-04
---

Markus keeps [GitHub Flavored Markdown](gfm.html) as the content language, then adds a handful of colon-fenced directives for the things Markdown was never meant to say: *this is a pull quote*, *these are peer cards*, *these two ideas belong beside each other*.

The source stays diffable. The renderer decides whether that pairing becomes two columns, a stacked phone layout, or a print spread.

:::pull-quote{attribution="Markus design principle" tone="primary"}
Encode intent in the document. Leave grid tracks, type ramps, and hover states to the theme.
:::

:::callout{kind="note" title="What Markus is not"}
It is not a visual programming language. There is no `margin`, no `font-size`, and no `grid-template-columns` in the authoring API. Unknown attributes are errors, on purpose.
:::

## Write this, get this

Every example in these docs shows the Markus source beside what it renders. This one is a callout and a metric inside a two-up pair.

:::example{layout="stacked"}
```markus
:::two-up{ratio="2:1"}
:::column
### Ship the smaller model

It answers 94% of support questions on its own, at a tenth of the cost.

:::tip
Route the rest to the large model.
:::
:::

:::column
::metric{value="0.1" unit="x" label="Cost per answer" delta="-90%"}
:::
:::
```
:::

[Get started](getting-started.html) to install Markus, or browse the [feature index](features.html) for every directive and Markdown feature.

## A vocabulary small enough to remember

:::feature-grid{columns=3 label="Core layout blocks"}
:::feature-card{icon="quote"}
## Pull quote

An editorial quotation with optional attribution, tone, and alignment.
:::

:::feature-card{icon="grid"}
## Card grid

Peer ideas that should read as a set, not a numbered list pretending to be a layout.
:::

:::feature-card{icon="scale"}
## Two-up

A conceptual pairing: contrast, before/after, claim and caveat.
:::
:::

:::two-up{ratio="1:1" align="start"}
:::column
## What belongs in the source

- The kind of block you mean
- A short, validated attribute set
- Nested Markdown, including other directives
- Document metadata in YAML front matter
:::

:::column
## What belongs in the theme

- Column counts that collapse on small screens
- Typography and color
- Print, EPUB, or email fallbacks
- Component-level accessibility rules
:::
:::

## Ratios on a three-column track

`two-up` ratios count parts across three columns: `2:1` is two parts plus one; `1:2` is one plus two. Blocks outside `two-up` span the full width.

:::two-up{ratio="2:1"}
:::column
### Primary (2 parts)

The narrative, claim, or longer explanation belongs in the wider column.
:::

:::column
### Aside (1 part)

Metadata, a caveat, or a short counterpoint.
:::
:::

:::two-up{ratio="1:2"}
:::column
### Lead (1 part)

A label, qualifier, or setup line.
:::

:::column
### Body (2 parts)

Material that should dominate when the second column carries the weight.
:::
:::

:::card-grid{columns=3 label="Spanning the track"}
:::card{span=full}
### Full width (all three columns)

Outside `two-up`, ordinary blocks span the entire track. Inside a `card-grid`, set `span=full` on a card to do the same.
:::
:::

## Metrics as first-class facts

Leaf directives cover facts that should be extractable later, not just styled.

:::card-grid{columns=3 label="Example metrics"}
:::card
::metric{value="0" label="CSS properties in the authoring API"}
:::

:::card
::metric{value="GFM" label="Markdown baseline"}
:::

:::card
::metric{value="MIT" label="License"}
:::
:::

:::figure{src="assets/pipeline.svg" alt="Pipeline from Markus source through a parser and a validating registry to semantic HTML" caption="Parse, validate, then render. Never regex-replace a directive after the fact."}
:::

## Structured procedures

:::step-list
:::step
### 1. Encode intent in source
Author content in GFM, wrapping layouts in colon-fenced directives.
:::

:::step
### 2. Validate against strict schemas
Markus checks directives and attributes at compile time, rejecting rogue CSS.
:::

:::step
### 3. Render accessible HTML
Output semantic markup ready for static hosting, responsive themes, or print.
:::
:::

## Multi-platform instructions

:::tabs{label="Install instructions"}
:::tab{label="pip"}
Install into the current environment:

```bash
pip install anthus-markus
```
:::

:::tab{label="pipx"}
Install the `markus` command in its own environment:

```bash
pipx install anthus-markus
```
:::

:::tab{label="uv"}
Add Markus to a uv project:

```bash
uv add anthus-markus
```
:::
:::

## Project timeline

:::timeline{label="Development milestones"}
:::timeline-event{date="2026-08-01" title="Initial Concept"}
Markus originated as a strict semantic layer for technical publishing.
:::

:::timeline-event{date="2026-08-15" title="Core AST & Validation"}
Implemented the markdown-it directive parser, Pydantic attribute validation, and early theme support.
:::

:::timeline-event{date="2026-09-04" title="Rich Directives & Themes"}
Added tabs, step lists, timelines, and 20+ accessible color palettes.
:::

:::timeline-event{date="2026-10-18" title="Conversations, diagrams, and examples"}
Added conversation transcripts, flow diagrams, bar charts, highlights, heading anchors, and side-by-side source examples.
:::
:::

:::details{summary="Why not raw HTML?"}
Raw HTML is a compatibility hatch, not the authoring API. It names CSS classes, invites sanitizer fights, and cannot tell a renderer whether three boxes are a comparison, a feature set, or leftover layout. Markus keeps a registry: unknown names fail in CI instead of silently becoming untyped markup.
:::

:::aside{title="Try it"}
Install the Python module with `pip install anthus-markus`, then run `markus convert page.md`. The [gallery](gallery.html) renders every directive on one page. `markus preview` opens a live editor.
:::
