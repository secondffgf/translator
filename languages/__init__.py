"""Load a ``LanguagePair`` by code (see ``languages.de_uk``, ``languages.en_fr``, …)."""

from __future__ import annotations

from importlib import import_module

from languages.profile import LanguagePair

_REGISTRY: dict[str, str] = {
    "de-uk": "languages.de_uk",
    "en-fr": "languages.en_fr",
}


def list_language_codes() -> list[str]:
    return sorted(_REGISTRY.keys())


def load_language(code: str) -> LanguagePair:
    key = (code or "").strip().lower()
    if key not in _REGISTRY:
        raise ValueError(
            f"Unknown language pair {code!r}. "
            f"Use one of: {', '.join(list_language_codes())}"
        )
    mod = import_module(_REGISTRY[key])
    pair = getattr(mod, "PAIR", None)
    if pair is None:
        raise ValueError(f"Module {_REGISTRY[key]} must define PAIR: LanguagePair")
    return pair
