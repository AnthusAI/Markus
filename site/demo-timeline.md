---
title: Timeline
description: timeline and timeline-event.
theme: catppuccin
---

# Timeline

A timeline is a chronological sequence. `timeline` may contain only `timeline-event` blocks.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| timeline `label` | any text; accessible name | none |
| event `date` | any text | none |
| event `time` | any text | none |
| event `title` | any text | none |
| event `icon` | icon name or text, as for cards | none |

### Dates and titles

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

:::details{summary="Markus source" open=true}
```md
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

:::timeline
:::timeline-event{date="2026-09-04" time="09:00" title="Kickoff"}
Date and time together.
:::

:::timeline-event{date="2026-09-04" time="14:30" title="Review"}
Same day, later.
:::
:::

:::details{summary="Markus source" open=true}
```md
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

:::details{summary="Markus source" open=true}
```md
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

:::timeline
:::timeline-event{date="2026"}
An event with just a date and a body.
:::

:::timeline-event{date="2027"}
Another.
:::
:::

:::details{summary="Markus source" open=true}
```md
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

:::timeline
:::timeline-event{title="Step one"}
No date.
:::

:::timeline-event{title="Step two"}
Still no date.
:::
:::

:::details{summary="Markus source" open=true}
```md
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
