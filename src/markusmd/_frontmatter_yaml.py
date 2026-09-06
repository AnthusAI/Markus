"""A `yaml.SafeLoader` variant with YAML 1.1 sexagesimal literals disabled.

PyYAML implements YAML 1.1, where a bare ``HH:MM:SS`` (or ``HH:MM:SS.fff``)
scalar is a *sexagesimal* int/float literal -- ``13:30:00`` resolves to the
int ``48600`` (``13*3600 + 30*60``), not a time of day. YAML 1.2 dropped
sexagesimals from the core schema entirely, but this project intentionally
does not adopt a full YAML 1.2 loader (see module docstring below for why);
instead this module patches PyYAML's implicit resolvers to remove *only* the
sexagesimal alternative from the int and float tags, leaving every other
PyYAML 1.1-ism (octal ``0755``, ``yes``/``no``/``on``/``off`` booleans, plain
decimal/hex/binary ints, plain floats, timestamps) exactly as authors already
know them.

Why not switch to a YAML 1.2 core-schema loader (e.g. `ruamel.yaml` in 1.2
mode) instead: that schema also drops YAML 1.1's ``yes``/``no``/``on``/``off``/
``y``/``n`` boolean forms (only ``true``/``True``/``TRUE``/``false``/
``False``/``FALSE`` remain booleans) and its octal syntax (``0755`` is a
*string* in 1.2 core schema; only ``0o755`` is the octal int). Front matter
that already relies on either of those forms
would silently change type -- trading one silent-coercion bug for another,
just less likely to be hit today. It would also add a new runtime dependency
for a fix that PyYAML's own public resolver API can express directly. So this
module keeps PyYAML and narrows exactly the one pattern that is wrong.
"""

from __future__ import annotations

import re

import yaml

# PyYAML's stock patterns (yaml.resolver.Resolver), reproduced with the
# sexagesimal alternative (`...(?::[0-5]?[0-9])+...`) removed. Everything
# else -- binary, octal, decimal, hex ints; plain floats, inf, nan -- is
# copied verbatim so behavior for every other scalar shape is unchanged.
_INT_RE = re.compile(
    r"""^(?:[-+]?0b[0-1_]+
        |[-+]?0[0-7_]+
        |[-+]?(?:0|[1-9][0-9_]*)
        |[-+]?0x[0-9a-fA-F_]+)$""",
    re.VERBOSE,
)

_FLOAT_RE = re.compile(
    r"""^(?:[-+]?(?:[0-9][0-9_]*)\.[0-9_]*(?:[eE][-+][0-9]+)?
        |\.[0-9][0-9_]*(?:[eE][-+][0-9]+)?
        |[-+]?\.(?:inf|Inf|INF)
        |\.(?:nan|NaN|NAN))$""",
    re.VERBOSE,
)


class FrontMatterLoader(yaml.SafeLoader):
    """`yaml.SafeLoader` without YAML 1.1 sexagesimal int/float literals.

    A bare ``HH:MM:SS`` scalar (e.g. a publication time in front matter)
    stays the string ``"13:30:00"`` instead of silently becoming the
    sexagesimal integer ``48600``. Every other PyYAML 1.1 resolution rule
    (octals, ``yes``/``no`` booleans, timestamps, plain ints/floats) is
    untouched.
    """


def _first_chars(tag: str) -> list[str]:
    """Return the first-character keys PyYAML registers `tag`'s resolver under."""
    return [
        ch
        for ch, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
        if any(candidate_tag == tag for candidate_tag, _ in resolvers)
    ]


def _replace_implicit_resolver(loader: type[yaml.SafeLoader], tag: str, regexp: re.Pattern) -> None:
    """Replace all of `tag`'s implicit-resolver entries on `loader` with `regexp`.

    `yaml.resolver.BaseResolver.add_implicit_resolver` only *appends*; it has
    no way to remove or replace an existing pattern for a tag. To narrow an
    existing rule (rather than add a new, competing one) we have to rebuild
    the per-first-character resolver lists ourselves, substituting the new
    pattern anywhere the old tag appears and leaving every other tag's
    entries (bool, timestamp, merge, null, ...) untouched.
    """
    # Rebuild from whatever `loader` already has (its own dict if a previous
    # call to this function has already run, else the inherited base dict)
    # so repeated calls -- once per tag -- compose instead of clobbering
    # each other's edits.
    base = loader.__dict__.get("yaml_implicit_resolvers", yaml.SafeLoader.yaml_implicit_resolvers)
    implicit_resolvers = {ch: list(resolvers) for ch, resolvers in base.items()}
    for ch in _first_chars(tag):
        implicit_resolvers[ch] = [
            (candidate_tag, regexp) if candidate_tag == tag else (candidate_tag, candidate_re)
            for candidate_tag, candidate_re in implicit_resolvers[ch]
        ]
    loader.yaml_implicit_resolvers = implicit_resolvers


_replace_implicit_resolver(FrontMatterLoader, "tag:yaml.org,2002:int", _INT_RE)
_replace_implicit_resolver(FrontMatterLoader, "tag:yaml.org,2002:float", _FLOAT_RE)
