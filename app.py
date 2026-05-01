"""Streamlit UI: translate via local Ollama; language pair from ``APP_LANGUAGE`` or ``--lang``."""

from __future__ import annotations

import os

import ollama
import streamlit as st

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

model = st.sidebar.text_input("Ollama model name", value=DEFAULT_MODEL, help="Must match `ollama list` on this machine.")
default_host = os.environ.get("OLLAMA_HOST", "")
host = st.sidebar.text_input(
    "Ollama API URL (optional)",
    value=default_host,
    placeholder="http://192.168.0.111:11434",
    help="Base URL of the Ollama API (same machine or remote). Set OLLAMA_HOST or edit here.",
)
st.sidebar.caption(f"Language pair: **{LANG.code}** (`APP_LANGUAGE` or `--lang`)")

source = st.text_area(
    LANG.source_label,
    height=180,
    placeholder=LANG.source_placeholder,
    key="source_text",
)


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


if st.button(LANG.translate_button, type="primary", disabled=not source.strip()):
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

st.sidebar.markdown("---")
