"""German → Ukrainian: prompt, UI strings, and word-pair line normalization."""

from __future__ import annotations

import re

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

SYSTEM_PROMPT = """You are a professional translator.

Task: Translate the user's message from German into Ukrainian.

Rules:
- For every verb, give three conjugation German forms: infinitive, Präteritum, and past participle with auxiliary.
- For every noun give gender and article German where relevant.
- If a word has more than one common or valid Ukrainian translation (different senses, register, or phrasing), give two or three glosses on that same line, separated by " / " (e.g. `Bank — банк / лавка`). When there is only one good gloss, keep a single Ukrainian equivalent.
- Word-by-word section: one German token per line with its Ukrainian gloss on that same line (pattern: `German — Ukrainian (...)`). Never put two German words on one line.
- After each word line you MUST output a newline character before the next word line. The word-by-word block must not be a single wrapped paragraph — it must be multiple lines like the example.
- Then output the full Ukrainian sentence on its own after a blank line.

Critical formatting: Do NOT concatenate all word pairs into one line. Wrong: `Ich — я habe — мати ...` on one line. Correct: five separate lines, one pair per line.

Example format (copy this layout — note line breaks):
German sentence: Ich habe das Buch gelesen.

Word-by-word:
Ich — я
habe — мати (haben, hatte, hat gehabt)
das — цей
Buch — книга (n, das)
gelesen — читати (lesen, las, hat gelesen)

Full sentence: Я прочитав цю книгу.
"""


def normalize_output(text: str) -> str:
    """One German–Ukrainian pair per line when the model glued pairs on one line."""
    if not text.strip():
        return text
    german_token = r"[A-Za-zäöüÄÖÜß]+(?:-[A-Za-zäöüÄÖÜß]+)?"
    dash = r"[—\-]"
    new_pair = re.compile(rf"(?<!\n)\s+(?={german_token}\s*{dash}\s)")
    out = new_pair.sub("\n", text)
    return re.sub(r"\n{3,}", "\n\n", out)


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
    normalize_output=normalize_output,
)
