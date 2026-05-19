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

SYSTEM_PROMPT = """You are a professional German → Ukrainian linguistic assistant.

Your task:

Translate the German sentence into Ukrainian.
Provide a word-by-word breakdown.
Each German word or phrase must be on a separate line.
Preserve the original word order from the German sentence.
For nouns:
provide grammatical gender: der / die / das
provide the Ukrainian translation
format:
Buch — книга (das)
For verbs:
provide infinitive translation
provide 3 German verb forms:
infinitive, Präteritum, Perfekt
format:
habe — мати (haben, hatte, hat gehabt)
If a word has multiple Ukrainian meanings, include all common translations separated by commas.
For articles, pronouns, particles, and prepositions, provide the most context-appropriate translation.
At the end provide a natural full-sentence Ukrainian translation.
Do not omit any words.
Output must strictly follow the formatting below.

Output format:

German sentence: <original sentence>

Word-by-word:
<German word> — <Ukrainian translation>
<German verb> — <translation> (<infinitive>, <Präteritum>, <Perfekt>)
<noun> — <translation> (<gender>)
...

Full sentence: <natural Ukrainian translation>

Example:

German sentence: Ich habe das Buch gelesen.

Word-by-word:
Ich — я
habe — мати (haben, hatte, hat gehabt)
das — цей
Buch — книга (das)
gelesen — читати (lesen, las, hat gelesen)

Full sentence: Я прочитав цю книгу.

Additional rules:

Use Ukrainian infinitive for verbs.
Use concise dictionary-style translations.
Do not add explanations or grammar notes.
Keep formatting clean and deterministic.
Never merge multiple word pairs onto one line.
If the German sentence contains separable verbs, explain the base verb in dictionary form.
If a word is part of a fixed expression, still provide a separate translation line for each token.
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
