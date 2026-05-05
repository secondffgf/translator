"""Streamlit UI: translate via local Ollama; language pair from ``APP_LANGUAGE`` or ``--lang``."""

from __future__ import annotations

import os

import ollama
import streamlit as st
import streamlit.components.v1 as components

from languages import load_language
from settings import get_language_code

DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "translategemma")

try:
    LANG = load_language(get_language_code())
except ValueError as e:
    st.set_page_config(page_title="translategemma", layout="centered")
    st.error(str(e))
    st.stop()

st.set_page_config(page_title=LANG.page_title, page_icon="🌐", layout="centered")
st.title(LANG.heading)
st.caption(LANG.caption)

if "source_text" not in st.session_state:
    st.session_state.source_text = ""
if "translation_output" not in st.session_state:
    st.session_state.translation_output = None

if st.session_state.pop("_clear_source_after_translate", False):
    st.session_state.source_text = ""


_FOCUS_SOURCE_TEXTAREA = """
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


def _maybe_focus_source_textarea() -> None:
    if st.session_state.pop("_focus_source_textarea", False):
        components.html(_FOCUS_SOURCE_TEXTAREA, height=0)


def _render_special_character_buttons() -> None:
    """Append-on-click buttons for non-ASCII letters; refocus source textarea after each click."""
    chars = LANG.special_characters
    if not chars:
        return
    st.caption(
        "Special characters in this language — click a button to append it to the text above:"
    )
    cols_per_row = 10
    for row_start in range(0, len(chars), cols_per_row):
        chunk = chars[row_start : row_start + cols_per_row]
        cols = st.columns(len(chunk))
        for i, ch in enumerate(chunk):
            idx = row_start + i
            with cols[i]:
                if st.button(
                    ch,
                    key=f"spec_char_{LANG.code}_{idx}",
                    use_container_width=True,
                ):
                    st.session_state["_pending_source_append"] = ch
                    st.rerun()


def _connection_unreachable_hint(exc: BaseException) -> str | None:
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
        return _connection_unreachable_hint(cause)
    return None


def _ollama_client(host: str) -> ollama.Client:
    h = (host or "").strip()
    return ollama.Client(host=h) if h else ollama.Client()


def _parse_installed_model_names(list_response: object) -> list[str]:
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


def _model_installed(installed: list[str], requested: str) -> bool:
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
        client = _ollama_client(host)
        resp = client.list()
        names = _parse_installed_model_names(resp)
    except Exception as e:  # noqa: BLE001 — health probe
        h = (host or "").strip() or "(default)"
        return False, False, f"Cannot reach Ollama at **{h}**: {e}"

    h = (host or "").strip() or "default host"
    if not model.strip():
        return True, False, f"Ollama API OK (**{h}**). Enter a model name."
    if _model_installed(names, model):
        return True, True, f"Ollama API OK (**{h}**), model **`{model.strip()}`** is available."
    return True, False, (
        f"Ollama API OK (**{h}**), but model **`{model.strip()}`** was not found in "
        f"`ollama list` ({len(names)} model(s) on server). Pull it or adjust the name."
    )


def translate_stream(client: ollama.Client, model: str, source_text: str):
    stream = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": LANG.system_prompt},
            {"role": "user", "content": source_text},
        ],
        stream=True,
    )
    for chunk in stream:
        content = chunk.get("message", {}).get("content")
        if content:
            yield content


model = st.sidebar.text_input("Ollama model name", value=DEFAULT_MODEL, help="Must match `ollama list` on this machine.")
default_host = os.environ.get("OLLAMA_HOST", "")
host = st.sidebar.text_input(
    "Ollama API URL (optional)",
    value=default_host,
    placeholder="http://192.168.0.111:11434",
    help="Base URL of the Ollama API (same machine or remote). Set OLLAMA_HOST or edit here.",
)

api_ok, model_ok, health_msg = check_ollama_available(host, model)
if api_ok and model_ok:
    st.sidebar.success(health_msg)
elif api_ok:
    st.sidebar.warning(health_msg)
else:
    st.sidebar.error(health_msg)

st.sidebar.caption(f"Language pair: **{LANG.code}** (`APP_LANGUAGE` or `--lang`)")

# Apply character-append from special-buttons *before* instantiating the text_area widget
# (Streamlit forbids mutating session_state[key] after the widget with that key is created).
_pending_char = st.session_state.pop("_pending_source_append", None)
if _pending_char is not None:
    st.session_state.source_text = (st.session_state.get("source_text") or "") + _pending_char
    st.session_state["_focus_source_textarea"] = True

source = st.text_area(
    LANG.source_label,
    height=180,
    placeholder=LANG.source_placeholder,
    key="source_text",
)

_render_special_character_buttons()

if st.button(
    LANG.translate_button,
    type="primary",
    disabled=not source.strip() or not api_ok,
    help=None if api_ok else "Connect to Ollama first (check API URL and server).",
):
    st.session_state["_focus_source_textarea"] = True
    try:
        client = _ollama_client(host)
        output_box = st.empty()
        buffer = ""
        norm = LANG.normalize_output
        for chunk in translate_stream(client, model, source.strip()):
            buffer += chunk
            output_box.text(norm(buffer))
        if buffer.strip():
            st.session_state.translation_output = norm(buffer)
            st.session_state["_clear_source_after_translate"] = True
            st.rerun()
        else:
            st.warning("Model returned no text. Check the model name and that Ollama is running.")
    except ollama.ResponseError as e:
        st.error(f"Ollama error: {e}")
    except ConnectionError as e:
        st.error(f"Cannot reach Ollama: {e}. Is the server running?")
    except Exception as e:  # noqa: BLE001 — show user-facing errors in UI
        hint = _connection_unreachable_hint(e)
        if hint:
            st.error(f"{e}\n\n{hint}")
        else:
            st.error(str(e))

if st.session_state.translation_output:
    st.subheader(LANG.translation_heading)
    st.text(st.session_state.translation_output)

_maybe_focus_source_textarea()

st.sidebar.markdown("---")
