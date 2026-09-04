# AGENTS.md

## What this project is

Markus is GitHub-flavored Markdown with a small vocabulary of semantic layout
directives. Authors encode intent in colon-fenced blocks; the renderer turns
that into accessible HTML and CSS.

The PyPI package is **`anthus-markus`**. Import as `markusmd`. The CLI is
`markus`.

The demo site lives at [anthusai.github.io/Markus/](https://anthusai.github.io/Markus/).

## Behavior-driven design

Markus is behavior-driven. Gherkin features in `features/` are the contract
for parsing, validation, rendering, and the CLI.

- Behavior changes start in `features/`.
- Implement step definitions in `features/steps/`, then production code in
  `src/markusmd/`.
- Run `behave` and `ruff check src features` before pushing.

## Git

This repository is its own git repo. Do not commit Markus into the parent
`~/Projects` checkout.

`develop` is the continuous-integration branch. Merge accepted, green work
there as soon as it is ready. Do not park completed work on long-lived
feature branches waiting for `main`.

`main` is the release branch. Semantic-release runs only from `main`.
Do not treat a merge to `develop` as a release. The release workflow is
local to this repo and authenticates with `GITHUB_TOKEN`.

Open pull requests against `develop`. Merge them there as soon as review is
addressed and CI is green. Do not park completed work on feature branches.
Promote `develop` to `main` when you intend a release, not as the daily
integration path.

## Semantic release

Releases are automated from conventional commits on `main`:

| Commit prefix | Release bump |
| --- | --- |
| `fix:` | patch |
| `feat:` | minor |
| `chore:`, `docs:`, `refactor:`, `test:` | no release (unless breaking) |

Release notes land in `CHANGELOG.md`. Tags use the `v{version}` format.
While the project is pre-1.0, the workflow blocks accidental `1.x` releases.

PyPI publishing uses `PYPI_TOKEN` in repository secrets. Until that secret is
set, release tagging and changelog updates still run; the explicit twine upload
step is skipped with a warning.
