"""Command-line interface for Markus."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from markusmd import __version__
from markusmd.api import convert, parse
from markusmd.errors import MarkusError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="markus",
        description="Convert Markus (GFM + semantic directives) to HTML.",
    )
    parser.add_argument("--version", action="version", version=f"markus {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    convert_p = sub.add_parser("convert", help="Render a Markus file to HTML")
    convert_p.add_argument("source", help="Markus file, or - for stdin")
    convert_p.add_argument("-o", "--output", help="Write HTML to this file instead of stdout")
    convert_p.add_argument("--fragment", action="store_true", help="Emit the article only")
    convert_p.add_argument("--no-css", action="store_true", help="Do not inline Markus CSS")
    convert_p.add_argument(
        "--allow-html",
        action="store_true",
        help="Pass through raw HTML in Markdown",
    )
    convert_p.add_argument(
        "--theme",
        help="Apply a visual theme (e.g. hackerman)",
    )

    ast_p = sub.add_parser("ast", help="Print the validated document AST as JSON")
    ast_p.add_argument("source", help="Markus file, or - for stdin")

    validate_p = sub.add_parser("validate", help="Validate Markus source and exit")
    validate_p.add_argument("source", help="Markus file, or - for stdin")

    preview_p = sub.add_parser("preview", help="Live editor for Markus source")
    preview_p.add_argument("source", nargs="?", help="Optional file to load in the editor")
    preview_p.add_argument("--host", default="127.0.0.1")
    preview_p.add_argument("--port", type=int, default=43147)

    site_p = sub.add_parser("site", help="Build the static GitHub Pages demo")
    site_p.add_argument(
        "source_dir",
        nargs="?",
        default="site",
        help="Directory of Markus pages (default: site/)",
    )
    site_p.add_argument("-o", "--out", default="_site", help="Output directory")
    site_p.add_argument("--serve", action="store_true", help="Serve the built site")
    site_p.add_argument("--host", default="127.0.0.1")
    site_p.add_argument("--port", type=int, default=43147)

    args = parser.parse_args(argv)
    try:
        if args.command == "convert":
            return _cmd_convert(args)
        if args.command == "ast":
            return _cmd_ast(args)
        if args.command == "validate":
            return _cmd_validate(args)
        if args.command == "preview":
            from markusmd.preview import serve_preview

            serve_preview(host=args.host, port=args.port, initial=_read_optional(args.source))
            return 0
        if args.command == "site":
            from markusmd.sitebuild import build_site, serve_directory

            dest = build_site(Path(args.source_dir), Path(args.out))
            if args.serve:
                serve_directory(dest, host=args.host, port=args.port)
            else:
                print(dest)
            return 0
    except MarkusError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 1


def _read(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def _read_optional(path: str | None) -> str:
    if not path:
        return ""
    return _read(path)


def _cmd_convert(args: argparse.Namespace) -> int:
    html = convert(
        _read(args.source),
        allow_html=args.allow_html,
        include_css=not args.no_css,
        full_document=not args.fragment,
        theme=args.theme,
    )
    if args.output:
        Path(args.output).write_text(html, encoding="utf-8")
    else:
        sys.stdout.write(html)
        if not html.endswith("\n"):
            sys.stdout.write("\n")
    return 0


def _cmd_ast(args: argparse.Namespace) -> int:
    document = parse(_read(args.source))
    json.dump(document.to_dict(), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    parse(_read(args.source))
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
