"""Public exceptions for Markus parse and validation failures."""

from __future__ import annotations


class MarkusError(Exception):
    """Base error for Markus source that cannot be parsed or rendered."""

    def __init__(self, message: str, line: int | None = None) -> None:
        self.line = line
        if line is not None:
            super().__init__(f"line {line}: {message}")
        else:
            super().__init__(message)


class MarkusSyntaxError(MarkusError):
    """The source is not valid Markus (unclosed fence, bad attributes, etc.)."""


class MarkusValidationError(MarkusError):
    """A directive name, attribute, or nesting rule failed validation."""


class MarkusSerializationError(MarkusError):
    """A parsed value cannot be represented in the Markus document IR.

    Raised when front matter (or other IR data) contains a Python value that
    the IR's JSON-typed-scalars-only contract does not cover and that has no
    safe, lossless normalization (e.g. a YAML `!!set` or `!!binary` value).
    See `markusmd.ast._to_json_safe` for the values that *are* normalized
    (dates, datetimes, times) versus those that raise this error.
    """
