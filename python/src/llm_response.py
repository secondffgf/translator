"""Pydantic models for structured translation output from Ollama."""

from __future__ import annotations

import copy
import re

from pydantic import BaseModel, Field


class TokenUsage(BaseModel):
    """Token counts from Ollama (`prompt_eval_count`, `eval_count`)."""

    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class WordTranslation(BaseModel):
    """One source token aligned with its target gloss and optional note."""

    word: str = Field(description="Source word or phrase in original order.")
    translation: str = Field(description="Target-language translation or gloss.")
    explanation: str | None = Field(
        default=None,
        description="Optional grammar, gender, tense, register, or multi-sense note.",
    )


class TranslationLLMResponse(BaseModel):
    """Structured translation from the assistant JSON plus optional usage (filled client-side)."""

    original_phrase: str = Field(description="Verbatim source sentence.")
    words: list[WordTranslation] = Field(description="Word-by-word rows in original order.")
    full_phrase_translation: str = Field(description="Natural translation of the whole sentence.")
    token_usage: TokenUsage | None = Field(
        default=None,
        description="Set by the app from Ollama metadata; omit from the model JSON.",
    )


STRUCTURED_JSON_SYSTEM_SUPPLEMENT = """\
Your reply MUST be a single JSON object only — no markdown fences and no text before or after.
Use exactly these keys:
- "original_phrase": string (the source sentence as given by the user)
- "words": array of objects, each with "word", "translation", and optionally "explanation" (string or null)
- "full_phrase_translation": string (fluent translation of the whole sentence)

Do not include "token_usage"; the client fills it from API metadata.

Apply every linguistic rule from the instructions above; express the result only through this JSON.
"""


def translation_llm_json_schema() -> dict:
    """JSON Schema for Ollama ``format`: translation fields only (no ``token_usage``)."""
    schema = copy.deepcopy(TranslationLLMResponse.model_json_schema())
    props = dict(schema.get("properties") or {})
    props.pop("token_usage", None)
    schema["properties"] = props
    req = [r for r in (schema.get("required") or []) if r != "token_usage"]
    if req:
        schema["required"] = req
    elif "required" in schema:
        del schema["required"]
    return schema


def _strip_json_fence(raw: str) -> str:
    text = raw.strip()
    m = re.match(
        r"^```(?:json)?\s*\n?(.*?)\n?```\s*$",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if m:
        return m.group(1).strip()
    return text


def parse_translation_json(raw: str) -> TranslationLLMResponse:
    """Parse assistant message JSON into ``TranslationLLMResponse`` (``token_usage`` defaults to None)."""
    return TranslationLLMResponse.model_validate_json(_strip_json_fence(raw))


def with_token_usage(
    resp: TranslationLLMResponse,
    *,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
) -> TranslationLLMResponse:
    """Return a copy with ``token_usage`` set from Ollama counts."""
    usage: TokenUsage | None = None
    if prompt_tokens or completion_tokens:
        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )
    return resp.model_copy(update={"token_usage": usage})


def format_translation_plain(tr: TranslationLLMResponse) -> str:
    """Plain-text rendering (e.g. logs or copy-paste)."""
    lines = [f"Original phrase: {tr.original_phrase}", "", "Word-by-word:"]
    for w in tr.words:
        row = f"{w.word} — {w.translation}"
        if w.explanation:
            row += f" ({w.explanation})"
        lines.append(row)
    lines.extend(["", f"Full phrase: {tr.full_phrase_translation}"])
    return "\n".join(lines)
