"""French → Ukrainian: prompt and UI strings."""

from __future__ import annotations

from languages.profile import LanguagePair

CODE = "fr-uk"

SPECIAL_CHARACTERS = (
    "à",
    "â",
    "ä",
    "ç",
    "é",
    "è",
    "ê",
    "ë",
    "î",
    "ï",
    "ô",
    "ö",
    "ù",
    "û",
    "ü",
    "ÿ",
    "œ",
    "æ",
    "À",
    "Â",
    "Ä",
    "Ç",
    "É",
    "È",
    "Ê",
    "Ë",
    "Î",
    "Ï",
    "Ô",
    "Ö",
    "Ù",
    "Û",
    "Ü",
    "Ÿ",
    "Œ",
    "Æ",
)

SYSTEM_PROMPT = """French → Ukrainian assistant. Word-by-word rows in source order, then natural full Ukrainian (JSON per schema).

Per token:
- Nouns: Ukrainian gloss; explanation = gender (le/la).
- Verbs: Ukrainian infinitive; explanation = French infinitive, passé composé, imparfait.
- Other words: context gloss; comma-separate common senses.

Rules: one French token per row; preserve apostrophes/contractions; concise dictionary Ukrainian; no prose beyond explanation.
"""


PAIR = LanguagePair(
    code=CODE,
    system_prompt=SYSTEM_PROMPT,
    page_title="FR → UK (Ollama)",
    heading="French → Ukrainian",
    caption="Powered by Ollama.",
    source_label="French text",
    source_placeholder="Bonjour, comment allez-vous ?",
    translate_button="Translate to Ukrainian",
    translation_heading="Translation",
    special_characters=SPECIAL_CHARACTERS,
)
