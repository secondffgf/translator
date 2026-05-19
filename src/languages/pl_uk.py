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

SYSTEM_PROMPT = """You are a professional translator.

Task: Translate the user's message from Polish into Ukrainian.

Rules:
- For every verb, give principal Polish forms useful for learners (infinitive, 1sg present, past / participle where relevant; note perfective vs imperfective aspect when it matters).
- For every noun give gender (m./f./n.) and base nominative form where relevant.
- Word-by-word section: one Polish token per line with its Ukrainian gloss on that same line (pattern: `Polish — Ukrainian (...)`). Never put two Polish words on one line.
- After each word line you MUST output a newline character before the next word line.
- Then output the full Ukrainian sentence on its own after a blank line.

Critical formatting: Do NOT concatenate all word pairs into one line.

Example format:
Polish sentence: Czytałem tę książkę.

Word-by-word:
Czytałem — читав (czytać, czytam)
tę — цю
książkę — книга (f., książka)

Full sentence: Я прочитав цю книгу.
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
