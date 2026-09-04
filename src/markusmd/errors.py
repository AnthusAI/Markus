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
