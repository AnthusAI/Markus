"""Behave environment for Markus behavior specs."""

from __future__ import annotations

import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def before_all(context):
    context.repo_root = ROOT


def before_scenario(context, scenario):
    context.source = ""
    context.html = ""
    context.document = None
    context.error = None
    context.convert_failed = False
    context.exit_code = None
    context.stdout = ""
    context.stderr = ""
    context.site_dir = None
    context.work_dir_obj = tempfile.TemporaryDirectory(prefix="markus_behave_")
    context.work_dir = Path(context.work_dir_obj.name)


def after_scenario(context, scenario):
    if getattr(context, "work_dir_obj", None):
        context.work_dir_obj.cleanup()
