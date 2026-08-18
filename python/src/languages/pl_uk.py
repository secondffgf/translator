"""Polish → Ukrainian: prompt and UI strings."""

from __future__ import annotations

from languages.profile import LanguagePair

CODE = "pl-uk"

SPECIAL_CHARACTERS = (
    "ą",
    "ć",
    "ę",
    "ł",
    "ń",
    "ó",
    "ś",
    "ź",
    "ż",
    "Ą",
    "Ć",
    "Ę",
    "Ł",
    "Ń",
    "Ó",
    "Ś",
    "Ź",
    "Ż",
)

SYSTEM_PROMPT = """Polish → Ukrainian assistant. Word-by-word rows in source order, then natural full Ukrainian (JSON per schema).

Per token:
- Verbs: Ukrainian gloss; explanation = infinitive, 1sg present, past; note perfective/imperfective when relevant.
- Nouns: gloss; explanation = gender (m./f./n.) and nominative base.
- Multiple senses: comma in translation.

Rules: one Polish token per row; concise dictionary Ukrainian; no prose beyond explanation.
"""


PAIR = LanguagePair(
    code=CODE,
    system_prompt=SYSTEM_PROMPT,
    page_title="PL → UK (Ollama)",
    heading="Polish → Ukrainian",
    caption="Powered by Ollama.",
    source_label="Polish text",
    source_placeholder="Dzień dobry, jak się Pan ma?",
    translate_button="Translate to Ukrainian",
    translation_heading="Translation",
    special_characters=SPECIAL_CHARACTERS,
)
