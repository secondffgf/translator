"""Ukrainian → French: prompt and UI strings."""

from __future__ import annotations

from languages.profile import LanguagePair

CODE = "uk-fr"

SPECIAL_CHARACTERS = (
    "і",
    "ї",
    "є",
    "ґ",
    "І",
    "Ї",
    "Є",
    "Ґ",
    "'",
    "’",
)

SYSTEM_PROMPT = """Ukrainian → French assistant. Word-by-word rows in source order, then natural full French (JSON per schema).

Per token:
- Verbs: French gloss; explanation = infinitive, present 1sg if helpful, participle / auxiliary.
- Nouns: gloss; explanation = gender (le/la) and base form.
- Multiple senses: comma in translation.

Rules: one Ukrainian token per row; concise dictionary French; no prose beyond explanation.
"""


PAIR = LanguagePair(
    code=CODE,
    system_prompt=SYSTEM_PROMPT,
    page_title="UK → FR (Ollama)",
    heading="Ukrainian → French",
    caption="Powered by Ollama.",
    source_label="Ukrainian text",
    source_placeholder="Привіт, як справи?",
    translate_button="Translate to French",
    translation_heading="Translation",
    special_characters=SPECIAL_CHARACTERS,
)
