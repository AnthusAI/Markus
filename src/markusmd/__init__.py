"""Markus: GitHub-flavored Markdown with semantic layout directives."""

from markusmd.api import convert, parse, parse_document, render
from markusmd.ast import Directive, Document, MarkdownBlock, Node
from markusmd.blocks import IR_SCHEMA_VERSION
from markusmd.errors import MarkusError, MarkusSyntaxError, MarkusValidationError
from markusmd.registry import Registry
from markusmd.render import minify_css

__version__ = "0.1.0"

__all__ = [
    "IR_SCHEMA_VERSION",
    "Directive",
    "Document",
    "MarkdownBlock",
    "MarkusError",
    "MarkusSyntaxError",
    "MarkusValidationError",
    "Node",
    "Registry",
    "__version__",
    "convert",
    "minify_css",
    "parse",
    "parse_document",
    "render",
]
