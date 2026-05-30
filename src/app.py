"""Streamlit UI: translate via local Ollama; language pair from ``APP_LANGUAGE`` or ``--lang``."""

from __future__ import annotations

import os
import time

import ollama
import streamlit as st
from pydantic import ValidationError

from languages import load_language
from llm_response import parse_translation_json, with_token_usage
from settings import get_language_code
from util import (
    check_ollama_available,
    completion_field,
    connection_unreachable_hint,
    fetch_translation_completion,
    format_elapsed_seconds,
    format_token_usage,
    maybe_focus_source_textarea,
    ollama_client,
    render_special_character_buttons,
)

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
if "translation_response" not in st.session_state:
    st.session_state.translation_response = None
if "translation_elapsed_seconds" not in st.session_state:
    st.session_state.translation_elapsed_seconds = None

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

render_special_character_buttons(LANG)

if st.button(
    LANG.translate_button,
    type="primary",
    disabled=not source.strip() or not api_ok,
    help=None if api_ok else "Connect to Ollama first (check API URL and server).",
):
    st.session_state["_focus_source_textarea"] = True
    st.session_state["_translation_started_at"] = time.perf_counter()
    raw_content = ""
    try:
        client = ollama_client(host)
        with st.spinner("Translating…"):
            raw_content, resp_obj = fetch_translation_completion(
                client,
                model,
                source.strip(),
                system_prompt=LANG.system_prompt,
            )
        if not raw_content:
            st.session_state.pop("_translation_started_at", None)
            st.warning("Model returned no text. Check the model name and that Ollama is running.")
        else:
            payload = parse_translation_json(raw_content)
            prompt_tokens = int(completion_field(resp_obj, "prompt_eval_count") or 0)
            completion_tokens = int(completion_field(resp_obj, "eval_count") or 0)
            st.session_state.translation_response = with_token_usage(
                payload,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
            st.session_state["_clear_source_after_translate"] = True
            st.rerun()
    except ValidationError as e:
        st.session_state.pop("_translation_started_at", None)
        st.error(f"Model output did not match the expected JSON shape: {e}")
        if raw_content.strip():
            with st.expander("Raw model output"):
                st.code(raw_content)
    except ollama.ResponseError as e:
        st.session_state.pop("_translation_started_at", None)
        st.error(f"Ollama error: {e}")
    except ConnectionError as e:
        st.session_state.pop("_translation_started_at", None)
        st.error(f"Cannot reach Ollama: {e}. Is the server running?")
    except Exception as e:  # noqa: BLE001 — show user-facing errors in UI
        st.session_state.pop("_translation_started_at", None)
        hint = connection_unreachable_hint(e)
        if hint:
            st.error(f"{e}\n\n{hint}")
        else:
            st.error(str(e))

if st.session_state.translation_response:
    started_at = st.session_state.pop("_translation_started_at", None)
    if started_at is not None:
        st.session_state.translation_elapsed_seconds = time.perf_counter() - started_at
    tr = st.session_state.translation_response
    st.subheader(LANG.translation_heading)
    st.markdown(f"**Original phrase:** {tr.original_phrase}")
    st.markdown("**Words:**")
    for w in tr.words:
        row = f"- **{w.word}** — {w.translation}"
        if w.explanation:
            row += f" — _{w.explanation}_"
        st.markdown(row)
    st.markdown(f"**Full phrase translation:** {tr.full_phrase_translation}")
    token_line = format_token_usage(tr)
    if token_line:
        st.caption(token_line)
    elapsed_line = format_elapsed_seconds(st.session_state.translation_elapsed_seconds)
    if elapsed_line:
        st.caption(elapsed_line)

maybe_focus_source_textarea()

st.sidebar.markdown("---")
