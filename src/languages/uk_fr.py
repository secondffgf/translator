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

SYSTEM_PROMPT = """You are a professional translator.

Task: Translate the user's message from Ukrainian into French.

Rules:
- For every verb, give principal French forms useful for learners (infinitive, present 1sg if helpful, past participle / auxiliary where relevant).
- For every noun give gender (le/la) where relevant.
- Word-by-word section: one Ukrainian token per line with its French gloss on that same line (pattern: `Ukrainian — French (...)`). Never put two Ukrainian words on one line.
- After each word line you MUST output a newline character before the next word line.
- Then output the full French sentence on its own after a blank line.

Critical formatting: Do NOT concatenate all word pairs into one line.

Example format:
Ukrainian sentence: Я прочитав цю книгу.

Word-by-word:
Я — je (pron.)
прочитав — j'ai lu (lire, lu)
цю — cette (f.)
книгу — livre (m., le livre)

Full sentence: J'ai lu ce livre.
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
