"""English → French: example second pair (extend the same pattern for new languages)."""

from __future__ import annotations

from languages.profile import LanguagePair

CODE = "en-fr"

SYSTEM_PROMPT = """You are a professional translator.

Task: Translate the user's message from English into French.

Rules:
- Preserve tone (formal/informal) when clear from the English.
- Use natural, idiomatic French.
- If the user asks for word-by-word help, put one English token per line with French gloss using the pattern `English — French`.
- Otherwise output only the French translation with no preamble.

Example (word-by-word mode):
Hello — Bonjour
world — monde

Full sentence: Bonjour le monde.
"""


def normalize_output(text: str) -> str:
    """Optional: add pair-aware formatting later; pass through for now."""
    return text


PAIR = LanguagePair(
    code=CODE,
    system_prompt=SYSTEM_PROMPT,
    page_title="EN → FR (Ollama)",
    heading="English → French",
    caption="Powered by Ollama.",
    source_label="English text",
    source_placeholder="Hello, how are you?",
    translate_button="Translate to French",
    translation_heading="Translation",
    normalize_output=normalize_output,
)
