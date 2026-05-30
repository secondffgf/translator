"""Ollama probes, translation fetch, Streamlit widgets shared by ``app.py``."""

from __future__ import annotations

import os

import ollama
import streamlit as st

from languages.profile import LanguagePair
from llm_response import (
    STRUCTURED_JSON_SYSTEM_SUPPLEMENT,
    TranslationLLMResponse,
    translation_llm_json_schema,
)

FOCUS_SOURCE_TEXTAREA_SCRIPT = """
<script>
(function () {
  const doc = window.parent.document;
  let ta = doc.querySelector("section.main textarea");
  if (!ta) {
    ta = doc.querySelector('[data-testid="stAppViewContainer"] textarea');
  }
  if (!ta) {
    ta = doc.querySelector("textarea");
  }
  if (ta) {
    ta.focus();
    const n = ta.value.length;
    ta.setSelectionRange(n, n);
  }
})();
</script>
"""


def maybe_focus_source_textarea() -> None:
    if st.session_state.pop("_focus_source_textarea", False):
        st.iframe(FOCUS_SOURCE_TEXTAREA_SCRIPT, height=1, tab_index=-1)


SPECIAL_CHAR_BUTTON_CSS = """
<style>
section[data-testid="stSidebar"] .tg-spec-char-host ~ div[data-testid="stHorizontalBlock"] button {
    width: 100%;
}
</style>
<div class="tg-spec-char-host" aria-hidden="true"></div>
"""

COLS_PER_ROW = 5


def render_special_character_buttons(lang: LanguagePair) -> None:
    """Append-on-click buttons for non-ASCII letters; refocus source textarea after each click."""
    chars = lang.special_characters
    if not chars:
        return
    st.sidebar.markdown("---")
    st.sidebar.markdown(SPECIAL_CHAR_BUTTON_CSS, unsafe_allow_html=True)
    st.sidebar.caption("Special characters — click to append to the source text:")
    for row_start in range(0, len(chars), COLS_PER_ROW):
        chunk = chars[row_start : row_start + COLS_PER_ROW]
        cols = st.sidebar.columns(COLS_PER_ROW)
        for col_idx, ch in enumerate(chunk):
            idx = row_start + col_idx
            with cols[col_idx]:
                if st.button(
                    ch,
                    key=f"spec_char_{lang.code}_{idx}",
                    use_container_width=True,
                ):
                    st.session_state["_pending_source_append"] = ch
                    st.rerun()


def connection_unreachable_hint(exc: BaseException) -> str | None:
    errno = getattr(exc, "errno", None)
    text = str(exc).lower()
    if errno == 113 or "no route to host" in text or "[errno 113]" in text:
        return (
            "**No route to host** — this machine cannot reach that IP on the network. "
            "Check: IP is correct (home LAN is often **192.168.**… not **192.186.**…), "
            "both PCs are on the same LAN (no guest isolation), "
            "firewall on the Ollama host allows **TCP 11434**, "
            "and Ollama is bound to **0.0.0.0** (e.g. `OLLAMA_HOST=0.0.0.0:11434`). "
            "From this machine, try: `curl -sS http://<ip>:11434/api/tags`."
        )
    cause = exc.__cause__ or exc.__context__
    if cause is not None and cause is not exc:
        return connection_unreachable_hint(cause)
    return None


def ollama_client(host: str) -> ollama.Client:
    h = (host or "").strip()
    return ollama.Client(host=h) if h else ollama.Client()


def parse_installed_model_names(list_response: object) -> list[str]:
    names: list[str] = []
    raw: object | None = None
    if isinstance(list_response, dict):
        raw = list_response.get("models")
    elif list_response is not None:
        raw = getattr(list_response, "models", None)
    if not raw:
        return names
    for item in raw:
        if isinstance(item, dict):
            n = item.get("model") or item.get("name") or ""
        else:
            n = getattr(item, "model", None) or getattr(item, "name", None) or ""
        n = str(n).strip()
        if n:
            names.append(n)
    return names


def completion_field(resp: object, key: str, default: object = None) -> object:
    if isinstance(resp, dict):
        return resp.get(key, default)
    return getattr(resp, key, default)


def format_token_usage(resp: TranslationLLMResponse | None) -> str | None:
    if resp is None or resp.token_usage is None:
        return None
    u = resp.token_usage
    if u.prompt_tokens == 0 and u.completion_tokens == 0:
        return None
    return (
        f"Tokens consumed: **{u.prompt_tokens}** prompt + **{u.completion_tokens}** generated "
        f"= **{u.total_tokens}** total"
    )


def format_elapsed_seconds(seconds: float | None) -> str | None:
    if seconds is None or seconds < 0:
        return None
    if seconds >= 60:
        minutes = int(seconds // 60)
        remainder = seconds % 60
        return f"Time taken: **{minutes}m {remainder:.1f}s**"
    return f"Time taken: **{seconds:.1f} s**"


def model_installed(installed: list[str], requested: str) -> bool:
    r = (requested or "").strip()
    if not r:
        return False
    if r in installed:
        return True
    return any(
        n == r or n.startswith(r + ":") or (":" not in r and n.split(":", 1)[0] == r)
        for n in installed
    )


def check_ollama_available(host: str, model: str) -> tuple[bool, bool, str]:
    """Return (api_reachable, model_installed, sidebar_message)."""
    try:
        client = ollama_client(host)
        resp = client.list()
        names = parse_installed_model_names(resp)
    except Exception as e:  # noqa: BLE001 — health probe
        h = (host or "").strip() or "(default)"
        return False, False, f"Cannot reach Ollama at **{h}**: {e}"

    h = (host or "").strip() or "default host"
    if not model.strip():
        return True, False, f"Ollama API OK (**{h}**). Enter a model name."
    if model_installed(names, model):
        return True, True, f"Ollama API OK (**{h}**), model **`{model.strip()}`** is available."
    return True, False, (
        f"Ollama API OK (**{h}**), but model **`{model.strip()}`** was not found in "
        f"`ollama list` ({len(names)} model(s) on server). Pull it or adjust the name."
    )


def ollama_num_ctx() -> int:
    """Context window for ``client.chat`` (``options.num_ctx``); default 64k tokens."""
    raw = (os.environ.get("OLLAMA_NUM_CTX") or "65536").strip()
    try:
        return int(raw)
    except ValueError:
        return 65536


def fetch_translation_completion(
    client: ollama.Client,
    model: str,
    source_text: str,
    *,
    system_prompt: str,
) -> tuple[str, object]:
    """Run one chat completion with JSON schema; return assistant text and raw API response."""
    resp = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": STRUCTURED_JSON_SYSTEM_SUPPLEMENT},
            {"role": "user", "content": source_text},
        ],
        stream=False,
        format=translation_llm_json_schema(),
        options={"num_ctx": ollama_num_ctx()},
    )
    message = completion_field(resp, "message") or {}
    raw_content = (
        message.get("content")
        if isinstance(message, dict)
        else getattr(message, "content", None)
    )
    return ((raw_content or "").strip(), resp)
