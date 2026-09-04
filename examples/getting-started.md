# Getting started with Markus

Markus is GitHub Flavored Markdown plus colon-fenced directives that name
layout *intent* rather than CSS.

:::pull-quote{attribution="Engineering principle" tone="primary"}
The best system is often the one whose failure modes you can explain.
:::

:::feature-grid{columns=3}
:::feature-card{icon="bolt"}
## Low latency

Keep common interactions local to minimize round trips.
:::

:::feature-card{icon="lock"}
## Private by default

Do not transmit user data unless the task requires it.
:::

:::feature-card{icon="gauge"}
## Measurable cost

Track tokens, watts, requests, and time-to-result.
:::
:::

:::two-up{ratio="1:1" align="start"}
:::column
## What changes

- A local model lowers marginal request cost
- Deployment becomes a systems problem
:::

:::column
## What remains

- Evaluation
- Retrieval quality
- UX
- Observability
:::
:::

:::callout{kind="note" title="Editorial guidance"}
Use `two-up` to express a conceptual pairing, not merely because two
paragraphs happen to fit beside each other.
:::
