"""French → Ukrainian: prompt, UI strings, and word-pair line normalization."""

from __future__ import annotations

import re

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

_FR_CHAR = r"A-Za-zÀÂÄÇÉÈÊËÎÏÔÖÙÛÜàâäçéèêëîïôöùûüÿŒœÆæ"

SYSTEM_PROMPT = """You are a professional translator.

Task: Translate the user's message from French into Ukrainian.

Rules:
- For every verb, give principal French forms useful for learners (infinitive, present 1sg if helpful, past participle / auxiliary where relevant).
- For every noun give gender (le/la) where relevant.
- If a word has more than one common or valid Ukrainian translation (different senses, register, or phrasing), give two or three glosses on that same line, separated by " / " (e.g. `vol — політ / крадіжка`). When there is only one good gloss, keep a single Ukrainian equivalent.
- Word-by-word section: one French token per line with its Ukrainian gloss on that same line (pattern: `French — Ukrainian (...)`). Never put two French words on one line.
- After each word line you MUST output a newline character before the next word line.
- Then output the full Ukrainian sentence on its own after a blank line.

Critical formatting: Do NOT concatenate all word pairs into one line.

Example format:
French sentence: J'ai lu le livre.

Word-by-word:
J'ai — я прочитав / маю (avoir: ai, as, a…)
lu — читати (lire, lu)
le — цей
livre — книга (m., le)

Full sentence: Я прочитав цю книгу.
"""


def normalize_output(text: str) -> str:
    """One French–Ukrainian pair per line when the model glued pairs on one line."""
    if not text.strip():
        return text
    fr_token = (
        rf"[{_FR_CHAR}]+(?:['’][{_FR_CHAR}]+)?"
        rf"(?:-[{_FR_CHAR}]+)?"
    )
    dash = r"[—\-]"
    new_pair = re.compile(rf"(?<!\n)\s+(?={fr_token}\s*{dash}\s)")
    out = new_pair.sub("\n", text)
    return re.sub(r"\n{3,}", "\n\n", out)


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
    normalize_output=normalize_output,
)
