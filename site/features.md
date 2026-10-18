---
title: Feature index
description: Every Markus directive and Markdown feature, each with a page of examples.
---

Every directive in the Markus registry and every Markdown feature it renders has a page here. Each page lists the attributes, then shows every variant as Markus source beside the result it renders. On narrow screens the source sits above the preview.

Markus ships with 22 themes. Pick one from the **Theme** menu at the top of any page to see every example on the site re-rendered in it; **Markus** is the default and follows your light or dark setting. Apply a theme to your own pages with `theme:` in front matter or `markus convert --theme NAME`.

## Directives

| Directive | Kind | Page |
| --- | --- | --- |
| `callout` | container | [Callouts and asides](demo-callouts.html) |
| `note`, `tip`, `warning`, `caution` | container aliases | [Callouts and asides](demo-callouts.html) |
| `aside` | container | [Callouts and asides](demo-callouts.html) |
| `pull-quote` | container | [Pull quote](demo-pull-quote.html) |
| `details` | container | [Details](demo-details.html) |
| `editorial-finding` | container | [Editorial finding](demo-editorial-finding.html) |
| `example` | container | [Example](demo-example.html) |
| `card-grid`, `feature-grid` | container | [Card grid and cards](demo-cards.html) |
| `card`, `feature-card` | container | [Card grid and cards](demo-cards.html) |
| `two-up`, `column` | container | [Two-up and columns](demo-two-up.html) |
| `tabs`, `tab` | container | [Tabs](demo-tabs.html) |
| `figure` | container | [Figure and video](demo-media.html) |
| `video` | leaf | [Figure and video](demo-media.html) |
| `metric` | leaf | [Metric](demo-metric.html) |
| `bar-chart` | container | [Bar chart](demo-bar-chart.html) |
| `step-list`, `step` | container | [Step list](demo-steps.html) |
| `timeline`, `timeline-event` | container | [Timeline](demo-timeline.html) |
| `conversation`, `message-group`, `message` | container | [Conversation](demo-conversation.html) |
| `diagram`, `row`, `node` | container | [Diagram](demo-diagram.html) |
| `link` | leaf | [Diagram](demo-diagram.html) |

## Language

| Feature | Page |
| --- | --- |
| Front matter, container and leaf syntax, attributes, ids, nesting, validation | [Syntax and metadata](demo-syntax.html) |
| Headings, emphasis, links, images, lists, task lists, tables, code, quotes, alerts, breaks | [GitHub Flavored Markdown](gfm-features.html) |
| `==text==` highlights | [Highlight](demo-highlight.html) |
| Generated heading ids and `{#custom-id}` | [Heading anchors](demo-heading-anchors.html) |
| Alignment, wrapping, numeric columns, scrolling, captions | [Tables](demo-tables.html) |

## Elsewhere

- [Get started](getting-started.html): install, the command line, and the Python API.
- [Gallery](gallery.html): every directive on one page.
- [Markus and GFM](gfm.html): the Markdown baseline Markus keeps on purpose.
