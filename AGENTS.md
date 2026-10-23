# AGENTS.md: Markus

Operating manual for any agent or person working in this repository, whatever the tool. Read [README.md](README.md) first (what this is, where it runs, how a change ships). Engine-level rules for Papyrus sites live in the Papyrus [AGENTS.md](https://github.com/AnthusAI/Papyrus/blob/main/AGENTS.md); this file does not repeat them. Papyrus docs index: [docs/README.md](https://github.com/AnthusAI/Papyrus/blob/main/docs/README.md).

## What this project is

Markus is GitHub-flavored Markdown with a small vocabulary of semantic layout directives. Authors encode intent in colon-fenced blocks; the renderer turns that into accessible HTML and CSS. The PyPI package is **`anthus-markus`**, imported as `markusmd`, with the CLI `markus`. This repository is also the source of the documentation site at [markus.anth.us](https://markus.anth.us/), which Papyrus builds. Markus is the content language of every Papyrus site; Papyrus pins a supported Markus range (`>=0.7.0,<1.0.0` today), so a breaking change here needs a Papyrus change first.

## Map of the parts

| Part | Where | Docs |
| --- | --- | --- |
| Parser, AST, validation, renderer, themes, CLI | `src/markusmd/` (`parse.py`, `blocks.py`, `render.py`, `registry.py`, `themes.py`, `cli.py`, `sitebuild.py`, ...) | [docs/LANGUAGE.md](docs/LANGUAGE.md), `CHANGELOG.md` |
| Behaviour contract | `features/*.feature` (Gherkin), steps in `features/steps/` | `behave.ini` |
| Documentation site content | `site/*.md` (one page per file) and `site/site.css` | [Papyrus static docs sites](https://github.com/AnthusAI/Papyrus/blob/main/docs/building-a-papyrus-static-site.md) (the "Documentation sites" paragraph) |
| Documentation site build | `docsite/build_site.py`: sidebar `NAVIGATION` (every page under `site/` must appear exactly once), banner, theme picker, Anthus footer, GA4 and consent (`GA_MEASUREMENT_ID`, `PRIVACY_POLICY_URL`), `SITE_URL`, custom domain `markus.anth.us`. `docsite/requirements.txt` holds the Papyrus pin and installs this checkout. `docsite/social-preview.html` makes the share image. | same Papyrus guide |
| The library's own demo builder | `markus site site --out _site` (`make site`), `src/markusmd/sitebuild.py`, covered by `features/site.feature`. It is not what is deployed. | `Makefile` |
| Agent-readable output | Papyrus writes a `.md` twin per page, `/llms.txt`, `/llms-full.txt`, `sitemap.xml` and page actions (copy, open in ChatGPT, Claude or Perplexity) for the docs site | [agent-readable-sites](https://github.com/AnthusAI/Papyrus/blob/main/docs/agent-readable-sites.md) |
| GA4 and consent | `docsite/build_site.py`; Papyrus emits Consent Mode v2 defaults, the banner, the "Cookie settings" link and the events | [site-hosting, Consent Mode v2](https://github.com/AnthusAI/Papyrus/blob/main/docs/site-hosting.md) |
| CI, Pages, release, PyPI | `.github/workflows/ci.yml`, `pages.yml`, `semantic-release.yml`, `publish-pypi.yml` | README |
| Board | Kanbus project key `kanbus` (`.kanbus.yml`, `project/`); workflow in `CONTRIBUTING_AGENT.template.md` | |

Papyrus features this repository does not use: the CMS and newsroom backend, Amplify, S3 and CloudFront hosting, reader steering, the newsletter plugin, monitoring and the Cyclotron router, procedures, the knowledge run, automations and review requests. The docs site is a static Papyrus "documentation site" (the `docs_site` builder, not the standard front end with `web/projection.json`); GitHub Pages hosts it.

## Common tasks

**Set up**: `python -m pip install -e ".[dev]"` in a virtual environment.

**Run the tests**: `ruff check src features` and `behave` (the same as CI; `make lint`, `make test`). Both must pass before you push.

**Build the docs site locally**:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r docsite/requirements.txt
python docsite/build_site.py --out _site
```

Run it inside the virtual environment: Papyrus calls `markus --version` from `PATH` and fails the build on a different or old `markus` (for example `got '0.5.1'`).

**Add a docs page**: create `site/<name>.md` and list it in `NAVIGATION` in `docsite/build_site.py`; the build fails if a page is missing from the navigation. Add or extend the Gherkin feature if the page documents new behaviour.

**Add or change a directive**: write the scenario in `features/` first, then the step definitions in `features/steps/`, then the code in `src/markusmd/`. Unknown directive names and attributes must keep failing validation. Document it in `docs/LANGUAGE.md` and a `site/demo-*.md` page.

**Bump the Papyrus pin for the docs site**: change `papyrus-newsroom[markus]==X.Y.Z` in `docsite/requirements.txt` (check the release exists with `pip index versions papyrus-newsroom`), build locally in a fresh virtual environment, and open a `docs:` pull request (no library release). The pin is `5.28.0`; the latest engine release at the time of writing is `5.32.0`.

**Deploy the site**: merge to `main`. `GitHub Pages` builds and deploys it (`workflow_dispatch` can re-run it). There is no AWS step. After a merge check `https://markus.anth.us/` returns 200. Only DNS touches AWS (the `markus` CNAME in the `anth.us` zone, `papyrus-production`).

**Release the library**: automatic. A `feat:` or `fix:` commit reaching `main` makes `Semantic Release` tag `vX.Y.Z` and update `CHANGELOG.md`, and `Publish to PyPI` uploads it through PyPI trusted publishing (the `pypi` environment, OIDC; there is no PyPI token in the repository). Releases above `0.x` are blocked. Do not hand-tag.

**Start a new Papyrus docs or static site**: [building-a-papyrus-static-site](https://github.com/AnthusAI/Papyrus/blob/main/docs/building-a-papyrus-static-site.md) and [site-hosting](https://github.com/AnthusAI/Papyrus/blob/main/docs/site-hosting.md).

## Git workflow

This repository is its own git repository; never commit Markus into a parent checkout.

- Open pull requests against **`main`** and merge them when CI is green; merge commits are the norm here. The earlier guidance to use `develop` as the integration branch is out of date: `develop` is 18 commits behind `main` and holds only three Kanbus chore commits that are not in `main`. Do not use it. Recent changes (Papyrus pins, Contact link, GA4) all went to `main`.
- `main` is the release and Pages branch. `feat:` and `fix:` commits there publish a release; use `docs:`, `chore:`, `refactor:` or `test:` for changes that must not.
- Conventional commits. Never force-push `main`. Do not park finished work on long-lived feature branches.
- Shared checkouts: never switch branches and never `git stash`. Use `git worktree add` or a fresh clone.

## Hard rules

- Behaviour changes start in `features/` (Gherkin, narrative and complete). Unit tests alone are not enough.
- Validation is not a security control. Static output is built from repo-committed Markdown with `--allow-html` off; never add that flag to a build (Papyrus refuses it).
- Secrets: none belong in this repository; Actions use the built-in `GITHUB_TOKEN` and PyPI trusted publishing. Anything new goes in SSM Parameter Store as SecureString or GitHub encrypted secrets, never in files.
- No real email addresses in the repository or in pages; use placeholders and the `https://anth.us/engage/` form for contact.
- The site's "Contact us" link must keep going to `https://anth.us/engage/?solution=Markus&cta=contact`.
- If this site ever gains a CMS backend, the engine rules apply: never run `papyrus ops content project --reconcile` without the deployed plugin list, never use `--allow-deletions`, take the projection lease. Today nothing is projected.
- Do not read or write `project/` Kanbus data directly except the wiki pages under `project/wiki/*.md`; use `KANBUS_REALTIME_BROKER=off kbs ...`. Stories go open, in_progress, blocked or closed. Human review is never a story state; use review requests.
- Wording: never write "desk"; say "section" or the role. Attribution is "AI". Use "Account", not "Organization", for the shared directory tenant.
- GA4 follows the anth.us standard: Consent Mode v2 with the banner and a Cookie settings link. Do not turn on `analytics_only` here.

## Ownership and coordination

- Ryan owns the project. Papyrus owns the docs-site builder; ask the Papyrus session before relying on a new builder option, and tell it before changing how this site is built or deployed.
- A Markus release changes what every Papyrus site can render: confirm the Papyrus supported range (`security.py` in `papyrus_content/markus_renderer`) before a breaking change.
- Never touch Anth.us from here.

## Current state (2026-10-23)

- Live: `https://markus.anth.us/` (200), `/llms.txt`, `/llms-full.txt`, `/sitemap.xml` (200); GA4 and the consent banner are in the pages; the Contact link points at the Anthus engage page. Latest release `0.14.0` (PyPI and GitHub, 2026-10-22). CI: 261 scenarios pass locally.
- The docs site pins Papyrus `5.28.0`, one release behind the other Papyrus sites.
- Known gaps: `docs/LANGUAGE.md` and the feature index are the references; nothing in this repository tracks planned directives, so use the Kanbus board. The `site/` pages and `docsite/build_site.py` navigation must be kept in step by hand.

## Where the docs live

[README.md](README.md), [docs/LANGUAGE.md](docs/LANGUAGE.md), `CHANGELOG.md`, the live feature index at [markus.anth.us/articles/features.html](https://markus.anth.us/articles/features.html), and the [Papyrus docs index](https://github.com/AnthusAI/Papyrus/blob/main/docs/README.md).
