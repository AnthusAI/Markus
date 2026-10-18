---
title: Metric
description: metric, the leaf directive for key figures.
theme: catppuccin
---

# Metric

A metric is a single key fact. It is a leaf directive: two colons, no body.

[All features](features.html)

## Attributes

| Attribute | Values | Default |
| --- | --- | --- |
| `value` | any text (required) |  |
| `unit` | any text | none |
| `label` | any text | `Metric` |
| `delta` | any text; sign picks the direction | none |

### Value only

The label falls back to `Metric`.

::metric{value="42"}

:::details{summary="Markus source" open=true}
```md
::metric{value="42"}
```
:::

### Value and label

::metric{value="99.95%" label="Uptime"}

:::details{summary="Markus source" open=true}
```md
::metric{value="99.95%" label="Uptime"}
```
:::

### With unit

::metric{value="12" unit="ms" label="p95 latency"}

:::details{summary="Markus source" open=true}
```md
::metric{value="12" unit="ms" label="p95 latency"}
```
:::

## Delta direction

The delta text decides the direction: a leading `-` is down, a leading `+` is up, anything else is flat.

### Negative delta

::metric{value="12" unit="ms" label="p95 latency" delta="-38%"}

:::details{summary="Markus source" open=true}
```md
::metric{value="12" unit="ms" label="p95 latency" delta="-38%"}
```
:::

### Positive delta

::metric{value="4.2" unit="k" label="Requests per second" delta="+12%"}

:::details{summary="Markus source" open=true}
```md
::metric{value="4.2" unit="k" label="Requests per second" delta="+12%"}
```
:::

### Neutral delta

::metric{value="7" label="Open issues" delta="0%"}

:::details{summary="Markus source" open=true}
```md
::metric{value="7" label="Open issues" delta="0%"}
```
:::

### Several in a row

Metrics stack in the document flow; wrap them in a `card-grid` for a dashboard row.

::metric{value="12" unit="ms" label="Latency" delta="-38%"}

::metric{value="99.95%" label="Uptime" delta="+0.02%"}

::metric{value="3" label="Regions"}

:::details{summary="Markus source" open=true}
```md
::metric{value="12" unit="ms" label="Latency" delta="-38%"}

::metric{value="99.95%" label="Uptime" delta="+0.02%"}

::metric{value="3" label="Regions"}
```
:::

### Metrics in cards

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

:::details{summary="Markus source" open=true}
```md
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
