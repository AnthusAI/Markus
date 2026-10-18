# Changelog

## 0.6.0

New syntax:

- `bar-chart` directive: labeled horizontal bars from a GFM table.
- `conversation`, `message-group`, and `message` directives for role-labeled
  transcripts.
- `diagram`, `node`, `row`, and `link` directives for vertical flows of boxes
  and arrows.
- `==highlight==` inline marks.
- Heading ids and `{#id}` anchors: a heading ending in `{#custom-id}` chooses
  its own id, and explicit ids are reserved across the whole document.
- Multi-line attribute blocks for leaf and container directives: the opening
  `{` stays on the directive line and the block ends at the first `}` outside
  quotes. Backslash escapes a quote inside a quoted value. An unterminated
  block is a syntax error at the directive's first line.

Rendering:

- GFM tables are wrapped in a horizontal scroll container and restyled.
- New demo pages for each directive and for GFM, with a feature index at
  `features.html`.

Behavior change:

- Every rendered heading now carries an `id` attribute. Existing output that
  assumed id-less headings (snapshots, CSS selectors, exact-HTML tests) will
  differ.

## 0.1.0

- Initial Markus language: GFM baseline, YAML front matter, and a small
  semantic directive registry.
- HTML renderer with bundled CSS.
- `markus` CLI: `convert`, `ast`, `validate`, `preview`, `site`.
- GitHub Pages demo generated from Markus sources in `site/`.
