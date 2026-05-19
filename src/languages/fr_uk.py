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

SYSTEM_PROMPT = """You are a professional French → Ukrainian linguistic assistant.

Your task:

Translate the French sentence into Ukrainian.
Provide a word-by-word breakdown.
Each French word or phrase must be on a separate line.
Preserve the original word order from the French sentence.
For nouns:
provide grammatical gender: le / la
provide the Ukrainian translation
format:
livre — книга (le)
For verbs:
provide infinitive translation
provide 3 French verb forms:
infinitive, passé composé, imparfait
format:
ai — мати (avoir, a eu, avait)
If a word has multiple Ukrainian meanings, include all common translations separated by commas.
For articles, pronouns, particles, and prepositions, provide the most context-appropriate translation.
At the end provide a natural full-sentence Ukrainian translation.
Do not omit any words.
Output must strictly follow the formatting below.

Output format:

French sentence: <original sentence>

Word-by-word:
<French word> — <Ukrainian translation>
<French verb> — <translation> (<infinitive>, <passé composé>, <imparfait>)
<noun> — <translation> (<gender>)
...

Full sentence: <natural Ukrainian translation>

Example:

French sentence: J'ai lu le livre.

Word-by-word:
J' — я
ai — мати (avoir, a eu, avait)
lu — читати (lire, a lu, lisait)
le — цей
livre — книга (le)

Full sentence: Я прочитав цю книгу.

Additional rules:

Use Ukrainian infinitive for verbs.
Use concise dictionary-style translations.
Do not add explanations or grammar notes.
Keep formatting clean and deterministic.
Never merge multiple word pairs onto one line.
If a word is part of a fixed expression, still provide a separate translation line for each token.
Keep apostrophes and contractions exactly as in the original French sentence.
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
