"""German → Ukrainian: prompt and UI strings."""

from __future__ import annotations

from languages.profile import LanguagePair

CODE = "de-uk"

# Letters beyond US ASCII — for copy-paste when only an English keyboard is configured.
SPECIAL_CHARACTERS = (
    "ä",
    "ö",
    "ü",
    "ß",
    "Ä",
    "Ö",
    "Ü",
)

SYSTEM_PROMPT = """German → Ukrainian assistant. Word-by-word rows in source order, then natural full Ukrainian (JSON per schema).

Per token:
- Nouns: Ukrainian gloss; explanation = gender (der/die/das).
- Verbs: Ukrainian infinitive; explanation = German infinitive, Präteritum, Perfekt (e.g. haben, hatte, hat gehabt).
- Other words: context gloss; comma-separate common senses.

Rules: one German token per row; omit nothing; concise dictionary Ukrainian; no prose beyond explanation.
Prefixed verbs stay one token (be-, er-, ver-, zer-, emp-, ent-, miss-, wider-, lexical ein-: einreden, einschlafen, einleiten — never ein + verb).
Separable verbs: dictionary base in explanation.

Examples: habe — мати (haben, hatte, hat gehabt); einschlafen — засинати (einschlafen, schlief ein, ist eingeschlafen).
"""


PAIR = LanguagePair(
    code=CODE,
    system_prompt=SYSTEM_PROMPT,
    page_title="DE → UK (Ollama)",
    heading="German → Ukrainian",
    caption="Powered by Ollama.",
    source_label="German text",
    source_placeholder="Guten Tag, wie geht es Ihnen?",
    translate_button="Translate to Ukrainian",
    translation_heading="Translation",
    special_characters=SPECIAL_CHARACTERS,
)
