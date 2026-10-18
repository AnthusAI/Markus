---
title: Metric
description: metric, the leaf directive for key figures.
---

A metric is a single key fact. It is a leaf directive: two colons, no body.

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `value` | any text (required) |  |
| `unit` | any text | none |
| `label` | any text | `Metric` |
| `delta` | any text; sign picks the direction | none |

Every directive also accepts `id`, which becomes the HTML id; see [Syntax and metadata](demo-syntax.html#element-id).

### Value only

The label falls back to `Metric`.

:::example
```markus
::metric{value="42"}
```
:::

### Value and label

:::example
```markus
::metric{value="99.95%" label="Uptime"}
```
:::

### With unit

:::example
```markus
::metric{value="12" unit="ms" label="p95 latency"}
```
:::

## Delta direction

The delta text decides the direction: a leading `-` is down, a leading `+` is up, anything else is flat.

### Negative delta

:::example
```markus
::metric{value="12" unit="ms" label="p95 latency" delta="-38%"}
```
:::

### Positive delta

:::example
```markus
::metric{value="4.2" unit="k" label="Requests per second" delta="+12%"}
```
:::

### Neutral delta

:::example
```markus
::metric{value="7" label="Open issues" delta="0%"}
```
:::

### Several in a row

Metrics stack in the document flow; wrap them in a `card-grid` for a dashboard row.

:::example
```markus
::metric{value="12" unit="ms" label="Latency" delta="-38%"}

::metric{value="99.95%" label="Uptime" delta="+0.02%"}

::metric{value="3" label="Regions"}
```
:::

### Metrics in cards

:::example{layout="stacked"}
```markus
:::card-grid{columns=3 label="Dashboard"}
:::card{title="Speed"}
::metric{value="12" unit="ms" label="p95" delta="-38%"}
:::

:::card{title="Uptime"}
::metric{value="99.95%" label="30 days" delta="+0.02%"}
:::

:::card{title="Regions"}
::metric{value="3" label="Live"}
:::
:::
```
:::
