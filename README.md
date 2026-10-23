# Markus

**GitHub-flavored Markdown with a small vocabulary for layout intent.**

Markus keeps Markdown as the content language, then adds colon-fenced
directives for the things GFM cannot say: *this is a pull quote*, *these
items are peer cards*, *these two views belong together*. Authors encode
meaning. The renderer turns that meaning into accessible HTML and responsive
CSS — or, later, print, EPUB, or email.

## What this repository is

Two things live here. The **library** is `anthus-markus` on PyPI (import `markusmd`, CLI `markus`), in `src/markusmd/`, specified by Gherkin features in `features/`. The **documentation site** is `site/` (Markus pages and `site.css`) plus `docsite/build_site.py` (navigation, banner, theme picker, Anthus footer, GA4).

How it relates to the rest of the platform: [Papyrus](https://github.com/AnthusAI/Papyrus) uses Markus as the content language of its sites and renders this documentation site (the build imports `papyrus_content.markus_renderer`). The sister Papyrus sites are Anth.us, Pilobol.us, Threat Intelligence, Tactus and p.apyr.us. Cyclotron, Prospectus, Biblicus and Tactus are separate projects; this repository does not depend on them.

## Where it runs

| Thing | Value |
| --- | --- |
| Library | PyPI project `anthus-markus` (latest release `0.14.0`), published by GitHub Actions with trusted publishing |
| Documentation site | `https://markus.anth.us/` on GitHub Pages, deployed from `main` by `.github/workflows/pages.yml` (Pages source: GitHub Actions workflow, HTTPS enforced). No AWS resources serve it; the only AWS part is DNS: `markus` is a CNAME to `anthusai.github.io` in the `anth.us` hosted zone of the `papyrus-production` account (`712236451410`). |
| Papyrus pin for the site | `papyrus-newsroom[markus]==5.28.0` in `docsite/requirements.txt` |
| Analytics | Google Analytics 4 (`G-31SC26SDGX`) with Consent Mode v2 and a cookie banner, emitted by Papyrus; privacy link `https://anth.us/privacy/`. The footer "Contact us" link goes to `https://anth.us/engage/?solution=Markus&cta=contact`. |

## How a change reaches production

1. Branch from `main` and open a pull request to `main` (see [AGENTS.md](AGENTS.md) for why `main` and not `develop`).
2. `CI` (`.github/workflows/ci.yml`) runs `ruff check src features` and `behave` on Python 3.10 to 3.13.
3. A push to `main` runs `GitHub Pages` (builds with `docsite/build_site.py`, deploys to Pages) and, after CI succeeds, `Semantic Release`. `fix:` releases a patch and `feat:` a minor version; `docs:`, `chore:`, `refactor:` and `test:` release nothing. A release tags `vX.Y.Z`, updates `CHANGELOG.md` and `Publish to PyPI` uploads it. While pre-1.0 the workflow refuses any `1.x` release.
4. To take a newer Papyrus for the site, change the pin in `docsite/requirements.txt` (a `docs:` commit, so nothing is released), check the local build, and merge.

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

The core vocabulary. The [feature index](https://anthusai.github.io/Markus/articles/features.html) documents every directive, with source and preview side by side.

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
| `example` | Markus source beside its rendered preview, for documentation |

Unknown names and unknown attributes fail validation. That is intentional:
Markus must not decay into an untyped CSS API. See
[docs/LANGUAGE.md](docs/LANGUAGE.md) for the full contract.

## Documentation site

**[markus.anth.us](https://markus.anth.us/)** is the documentation and demo site. It is written in Markus (`site/`) and built by [Papyrus](https://github.com/AnthusAI/Papyrus) with `docsite/build_site.py`. The older address [anthusai.github.io/Markus/](https://anthusai.github.io/Markus/) is the same GitHub Pages deployment under the repository's default host.

To build the same site locally, use a virtual environment: Papyrus runs `markus --version` from `PATH` to check the version, so a different `markus` earlier on `PATH` makes the build fail.

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r docsite/requirements.txt     # Papyrus (pinned) and this checkout of Markus
python docsite/build_site.py --out _site    # 27 pages
python -m http.server --directory _site 8000
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

## More

[AGENTS.md](AGENTS.md) is the operating manual for agents and people. The language contract is [docs/LANGUAGE.md](docs/LANGUAGE.md); the Papyrus documentation index is [docs/README.md](https://github.com/AnthusAI/Papyrus/blob/main/docs/README.md).

## License

MIT © Anthus AI Solutions
