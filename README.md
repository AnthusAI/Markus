# Markus

**GitHub-flavored Markdown with a small vocabulary for layout intent.**

Markus keeps Markdown as the content language, then adds colon-fenced
directives for the things GFM cannot say: *this is a pull quote*, *these
items are peer cards*, *these two views belong together*. Authors encode
meaning. The renderer turns that meaning into accessible HTML and responsive
CSS — or, later, print, EPUB, or email.

## Install

```bash
pip install anthus-markus
```

Python 3.10 or newer.

## Convert a page

```bash
markus convert examples/getting-started.md -o page.html
markus validate examples/getting-started.md
markus ast examples/getting-started.md
```

Python API:

```python
from markusmd import convert

html = convert(open("page.md", encoding="utf-8").read())
```

## Directives

```md
:::pull-quote{attribution="Engineering principle" tone="primary"}
The best system is often the one whose failure modes you can explain.
:::

:::feature-grid{columns=3}
:::feature-card{icon="bolt"}
## Low latency
Keep common interactions local.
:::
:::
```

The 0.1 vocabulary:

| Directive | Intent |
| --- | --- |
| `callout` (`note`, `warning`, `tip`, `caution`) | Status or editorial note |
| `pull-quote` | Editorial quotation |
| `card-grid` / `card` | Peer items |
| `two-up` / `column` | A conceptual pair |
| `figure` | Media with caption and credit |
| `details` | Progressive disclosure |
| `aside` | Supporting, non-linear material |
| `metric` | A labeled fact (`::metric{...}`) |

Unknown names and unknown attributes fail validation. That is intentional:
Markus must not decay into an untyped CSS API. See
[docs/LANGUAGE.md](docs/LANGUAGE.md) for the full contract.

## Demo site

**[anthusai.github.io/Markus/](https://anthusai.github.io/Markus/)** — written in
Markus and built by Markus.

To run the same site locally:

```bash
pip install -e ".[dev]"
markus site site --out _site --serve --port 43147
```

## Preview locally

```bash
markus preview examples/getting-started.md
```

## Development

```bash
pip install -e ".[dev]"
behave          # Gherkin behavior specs
ruff check src features
python -m build
```

## License

MIT © Anthus AI Solutions
