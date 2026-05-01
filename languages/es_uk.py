"""Spanish → Ukrainian: prompt, UI strings, and word-pair line normalization."""

from __future__ import annotations

import re

from languages.profile import LanguagePair

CODE = "es-uk"

# Latin letters used in Spanish (no ß); includes accented vowels and ñ.
_ES_CHAR = r"A-Za-záéíóúÁÉÍÓÚñÑüÜ"

SYSTEM_PROMPT = """You are a professional translator.

Task: Translate the user's message from Spanish into Ukrainian.

Rules:
- For every verb, give principal Spanish forms useful for learners (infinitive, gerund, past participle / compound tenses where relevant).
- For every noun give gender (el/la) where relevant.
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


def normalize_output(text: str) -> str:
    """One Spanish–Ukrainian pair per line when the model glued pairs on one line."""
    if not text.strip():
        return text
    es_token = (
        rf"[{_ES_CHAR}]+(?:['’][{_ES_CHAR}]+)?"
        rf"(?:-[{_ES_CHAR}]+)?"
    )
    dash = r"[—\-]"
    new_pair = re.compile(rf"(?<!\n)\s+(?={es_token}\s*{dash}\s)")
    out = new_pair.sub("\n", text)
    return re.sub(r"\n{3,}", "\n\n", out)


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
    normalize_output=normalize_output,
)
