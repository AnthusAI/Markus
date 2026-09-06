"""Step definitions for Markus behavior specs."""

from __future__ import annotations

import io
import json
import os
import re
import shlex
from contextlib import redirect_stderr, redirect_stdout

from behave import given, then, when

from markusmd.api import convert, parse, parse_document
from markusmd.ast import Directive, MarkdownBlock
from markusmd.cli import main
from markusmd.errors import MarkusError
from markusmd.sitebuild import build_site


@given("the Markus source:")
def given_source(context):
    context.source = context.text or ""


@given('a Markus file "{name}" with:')
def given_file(context, name):
    path = context.work_dir / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(context.text or "", encoding="utf-8")


@given("the bundled Markus site sources")
def given_site_sources(context):
    context.site_source = context.repo_root / "site"


@when("I convert the source to an HTML fragment")
def when_convert(context):
    try:
        context.html = convert(context.source, include_css=False, full_document=False)
        context.convert_failed = False
        context.error = None
    except MarkusError as exc:
        context.convert_failed = True
        context.error = exc
        context.html = ""


@when("I convert the source to a full HTML document")
def when_convert_full(context):
    try:
        context.html = convert(context.source, include_css=True, full_document=True)
        context.convert_failed = False
        context.error = None
    except MarkusError as exc:
        context.convert_failed = True
        context.error = exc
        context.html = ""


@when('I convert the source to an HTML fragment with theme "{theme}"')
def when_convert_theme(context, theme):
    try:
        context.html = convert(context.source, theme=theme, include_css=False, full_document=False)
        context.convert_failed = False
        context.error = None
    except MarkusError as exc:
        context.convert_failed = True
        context.error = exc
        context.html = ""


@when("I parse the source")
def when_parse(context):
    try:
        context.document = parse(context.source)
        context.convert_failed = False
        context.error = None
    except MarkusError as exc:
        context.convert_failed = True
        context.error = exc
        context.document = None


@when("I parse the source into the document IR")
def when_parse_ir(context):
    context.ir = parse_document(context.source)


@when("I parse the source into the document IR with html allowed")
def when_parse_ir_html(context):
    context.ir = parse_document(context.source, allow_html=True)


@when('I run "{command}"')
def when_run(context, command):
    args = shlex.split(command)
    if args and args[0] == "markus":
        args = args[1:]
    stdout = io.StringIO()
    stderr = io.StringIO()
    previous = os.getcwd()
    os.chdir(context.work_dir)
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            context.exit_code = main(args)
    finally:
        os.chdir(previous)
    context.stdout = stdout.getvalue()
    context.stderr = stderr.getvalue()


@when("I build the demo site")
def when_build_site(context):
    context.site_dir = build_site(context.site_source, context.work_dir / "_site")


@then("conversion should succeed")
def then_convert_ok(context):
    assert not context.convert_failed, context.error


@then("conversion should fail")
def then_convert_fail(context):
    assert context.convert_failed, "expected conversion to fail"


@then('the error should contain "{snippet}"')
def then_error_contains(context, snippet):
    assert context.error is not None, "no error captured"
    assert snippet in str(context.error), str(context.error)


@then("the error should mention line {line:d}")
def then_error_line(context, line):
    assert context.error is not None
    assert context.error.line == line, context.error.line


@then('the HTML should contain "{snippet}"')
def then_html_contains(context, snippet):
    assert not context.convert_failed, context.error
    assert snippet in context.html, context.html


@then('the HTML should not contain "{snippet}"')
def then_html_not_contains(context, snippet):
    assert not context.convert_failed, context.error
    assert snippet not in context.html, context.html


@then('the HTML should contain a "{tag}" with class "{cls}"')
def then_tag_class(context, tag, cls):
    assert not context.convert_failed, context.error
    pattern = rf"<{tag}\b[^>]*class=\"[^\"]*{re.escape(cls)}"
    assert re.search(pattern, context.html), context.html


@then('the HTML should contain three "{tag}" elements with class "{cls}"')
def then_three_tags(context, tag, cls):
    assert not context.convert_failed, context.error
    count = len(re.findall(rf"<{tag}\b[^>]*class=\"[^\"]*{re.escape(cls)}", context.html))
    assert count == 3, f"expected 3, found {count} in {context.html}"


@then('the HTML should contain struck text "{text}"')
def then_struck(context, text):
    assert not context.convert_failed, context.error
    assert (
        f"<s>{text}</s>" in context.html
        or f"<del>{text}</del>" in context.html
        or f"<strike>{text}</strike>" in context.html
    ), context.html


@then('the HTML should contain a link to "{url}"')
def then_link(context, url):
    assert not context.convert_failed, context.error
    assert f'href="{url}"' in context.html, context.html


@then('the HTML should contain an attribute {name} of "{value}"')
def then_attr(context, name, value):
    assert not context.convert_failed, context.error
    assert f'{name}="{value}"' in context.html, context.html


@then('the front matter key "{key}" should be "{value}"')
def then_front_matter(context, key, value):
    assert context.document is not None
    assert str(context.document.front_matter.get(key)) == value, context.document.front_matter


@then("the document should have empty front matter")
def then_empty_front_matter(context):
    assert context.document is not None
    assert context.document.front_matter == {}


@then('the document should contain markdown starting with "{prefix}"')
def then_markdown_prefix(context, prefix):
    blocks = [node for node in context.document.children if isinstance(node, MarkdownBlock)]
    assert blocks, context.document
    assert blocks[0].source.lstrip().startswith(prefix), blocks[0].source


@then('the directive "{name}" should have attribute "{key}" equal to "{value}"')
def then_directive_attr(context, name, key, value):
    directive = _find_directive(context.document.children, name)
    assert directive is not None, f"no directive named {name}"
    actual = directive.attributes.get(key)
    assert str(actual) == value, directive.attributes


@then("the command should succeed")
def then_cmd_ok(context):
    assert context.exit_code == 0, context.stderr


@then("the command should fail")
def then_cmd_fail(context):
    assert context.exit_code != 0


@then('stdout should contain "{snippet}"')
def then_stdout(context, snippet):
    assert snippet in context.stdout, context.stdout


@then('stdout should not contain "{snippet}"')
def then_stdout_not_contains(context, snippet):
    assert snippet not in context.stdout, context.stdout


@then('stderr should contain "{snippet}"')
def then_stderr(context, snippet):
    assert snippet in context.stderr, context.stderr


@then('the site should include "{relative}"')
def then_site_includes(context, relative):
    path = context.site_dir / relative
    assert path.exists(), f"missing {path}"


@then('"{page}" should contain "{snippet}"')
def then_page_contains(context, page, snippet):
    text = (context.site_dir / page).read_text(encoding="utf-8")
    assert snippet in text, text


@then("the document IR schema_version should be {version:d}")
def then_ir_schema_version(context, version):
    assert context.ir["schema_version"] == version, context.ir["schema_version"]


@then('the document IR child {index:d} type should be "{expected}"')
def then_ir_child_type(context, index, expected):
    child = context.ir["children"][index]
    assert child["type"] == expected, child


@then('the document IR child {index:d} field "{field}" should equal {value}')
def then_ir_child_field(context, index, field, value):
    child = context.ir["children"][index]
    expected = json.loads(value)
    assert child[field] == expected, (field, child.get(field), expected)


@then('the document IR child {index:d} should have {count:d} "{field}" entries')
def then_ir_child_count(context, index, count, field):
    child = context.ir["children"][index]
    assert len(child[field]) == count, child[field]


@then('the document IR child {index:d} item {item:d} checked should be {value}')
def then_ir_child_item_checked(context, index, item, value):
    child = context.ir["children"][index]
    expected = json.loads(value)
    actual = child["items"][item]["checked"]
    assert actual == expected, (actual, expected)


@then('the document IR child {index:d} inline text should be "{expected}"')
def then_ir_child_inline_text(context, index, expected):
    child = context.ir["children"][index]
    assert _flatten_inline_text(child["inline"]) == expected, child["inline"]


@then("the document IR children types should be:")
def then_ir_children_types(context):
    actual = [child["type"] for child in context.ir["children"]]
    expected = [row["type"] for row in context.table]
    assert actual == expected, actual


@then("the ast JSON output children types should be:")
def then_ast_json_children_types(context):
    doc = json.loads(context.stdout)
    actual = [child["type"] for child in doc["children"]]
    expected = [row["type"] for row in context.table]
    assert actual == expected, actual


@then("the ast JSON output schema_version should be {version:d}")
def then_ast_json_schema_version(context, version):
    doc = json.loads(context.stdout)
    assert doc["schema_version"] == version, doc["schema_version"]


def _flatten_inline_text(inline_nodes) -> str:
    parts = []
    for node in inline_nodes:
        if node["type"] == "text":
            parts.append(node["text"])
        elif "children" in node:
            parts.append(_flatten_inline_text(node["children"]))
        elif node["type"] == "soft_break" or node["type"] == "hard_break":
            parts.append("\n")
    return "".join(parts)


def _find_directive(nodes, name):
    for node in nodes:
        if isinstance(node, Directive):
            if node.name == name:
                return node
            found = _find_directive(node.children, name)
            if found:
                return found
    return None
