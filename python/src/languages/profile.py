"""Language pair configuration (prompt + UI)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguagePair:
    """One pair (source → target) with its own system prompt and labels."""

    code: str
    system_prompt: str
    page_title: str
    heading: str
    caption: str
    source_label: str
    source_placeholder: str
    translate_button: str
    translation_heading: str
    special_characters: tuple[str, ...]
