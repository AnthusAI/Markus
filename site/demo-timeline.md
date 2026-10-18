---
title: Timeline
description: timeline and timeline-event.
---

A timeline is a chronological sequence. `timeline` may contain only `timeline-event` blocks.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| timeline `label` | any text; accessible name | none |
| event `date` | any text | none |
| event `time` | any text | none |
| event `title` | any text | none |
| event `icon` | icon name or text, as for cards | none |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

### Dates and titles

:::example
```markus
:::timeline{label="Release history"}
:::timeline-event{date="2026-06-01" title="Prototype"}
First working parser.
:::

:::timeline-event{date="2026-08-15" title="Registry"}
Strict attribute schemas.
:::

:::timeline-event{date="2026-09-04" title="Site builder"}
The demo site.
:::
:::
```
:::

### With time

:::example
```markus
:::timeline
:::timeline-event{date="2026-09-04" time="09:00" title="Kickoff"}
Date and time together.
:::

:::timeline-event{date="2026-09-04" time="14:30" title="Review"}
Same day, later.
:::
:::
```
:::

### With icons

:::example
```markus
:::timeline{label="Journey"}
:::timeline-event{date="Q1" title="Idea" icon="brain"}
Brain icon.
:::

:::timeline-event{date="Q2" title="Build" icon="bolt"}
Bolt icon.
:::

:::timeline-event{date="Q3" title="Ship" icon="book"}
Book icon.
:::
:::
```
:::

### Date only, no title

:::example
```markus
:::timeline
:::timeline-event{date="2026"}
An event with just a date and a body.
:::

:::timeline-event{date="2027"}
Another.
:::
:::
```
:::

### Title only, no date

:::example
```markus
:::timeline
:::timeline-event{title="Step one"}
No date.
:::

:::timeline-event{title="Step two"}
Still no date.
:::
:::
```
:::
