"""Language selection: ``--lang`` / ``--language`` after ``--``, or ``APP_LANGUAGE`` env."""

from __future__ import annotations

import os
import sys


def language_code_from_argv() -> str | None:
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg in ("--lang", "--language") and i + 1 < len(args):
            return args[i + 1].strip()
    return None


def get_language_code() -> str:
    return language_code_from_argv() or os.environ.get("APP_LANGUAGE", "de-uk")
