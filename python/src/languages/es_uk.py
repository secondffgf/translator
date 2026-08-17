"""Spanish → Ukrainian: prompt and UI strings."""

from __future__ import annotations

from languages.profile import LanguagePair

CODE = "es-uk"

SPECIAL_CHARACTERS = (
    "á",
    "é",
    "í",
    "ó",
    "ú",
    "ñ",
    "ü",
    "Á",
    "É",
    "Í",
    "Ó",
    "Ú",
    "Ñ",
    "Ü",
    "¿",
    "¡",
)

SYSTEM_PROMPT = """You are a professional translator.

Task: Translate the user's message from Spanish into Ukrainian.

Rules:
- For every verb, give principal Spanish forms useful for learners (infinitive, gerund, past participle / compound tenses where relevant).
- For every noun give gender (el/la) where relevant.
- If a word has more than one common or valid Ukrainian translation (different senses, register, or phrasing), give two or three glosses on that same line, separated by " / " (e.g. `banco — банк / лавка`). When there is only one good gloss, keep a single Ukrainian equivalent.
- Word-by-word section: one Spanish token per line with its Ukrainian gloss on that same line (pattern: `Spanish — Ukrainian (...)`). Never put two Spanish words on one line.
- After each word line you MUST output a newline character before the next word line.
- Then output the full Ukrainian sentence on its own after a blank line.

Critical formatting: Do NOT concatenate all word pairs into one line.

Example format:
Spanish sentence: He leído el libro.

Word-by-word:
He — я (haber: he, has, ha…)
leído — читати (leer, leído)
el — цей / книга (артикул)
libro — книга (m., el libro)

Full sentence: Я прочитав цю книгу.
"""


PAIR = LanguagePair(
    code=CODE,
    system_prompt=SYSTEM_PROMPT,
    page_title="ES → UK (Ollama)",
    heading="Spanish → Ukrainian",
    caption="Powered by Ollama.",
    source_label="Spanish text",
    source_placeholder="Hola, ¿cómo está usted?",
    translate_button="Translate to Ukrainian",
    translation_heading="Translation",
    special_characters=SPECIAL_CHARACTERS,
)
