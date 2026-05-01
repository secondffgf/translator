"""Streamlit UI: German → Ukrainian translation via local Ollama."""

from __future__ import annotations

import os
import re

import ollama
import streamlit as st

DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "translategemma")
SYSTEM_PROMPT = """You are a professional translator.

Task: Translate the user's message from German into Ukrainian.

Rules:
- For every verb, give three conjugation forms: infinitive, Präteritum, and past participle with auxiliary.
- For every noun give gender and article where relevant.
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


def _connection_unreachable_hint(exc: BaseException) -> str | None:
    """Return a short hint for common 'cannot reach Ollama' errors (e.g. errno 113)."""
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


def normalize_german_ukrainian_lines(text: str) -> str:
    """One German–Ukrainian pair per line: insert newlines before each new `… — …` pair."""
    if not text.strip():
        return text
    # German token (allow hyphen compounds); dash may be em dash or ASCII hyphen
    german_token = r"[A-Za-zäöüÄÖÜß]+(?:-[A-Za-zäöüÄÖÜß]+)?"
    dash = r"[—\-]"
    # Space(s) before the next pair: German token, optional spaces, dash, spaces (start of Ukrainian)
    new_pair = re.compile(rf"(?<!\n)\s+(?={german_token}\s*{dash}\s)")
    out = new_pair.sub("\n", text)
    return re.sub(r"\n{3,}", "\n\n", out)


def translate_stream(client: ollama.Client, model: str, german_text: str):
    stream = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": german_text},
        ],
        stream=True,
    )
    for chunk in stream:
        content = chunk.get("message", {}).get("content")
        if content:
            yield content


st.set_page_config(page_title="DE → UK (Ollama)", page_icon="🌐", layout="centered")
st.title("German → Ukrainian")
st.caption("Powered by Ollama.")

model = st.sidebar.text_input("Ollama model name", value=DEFAULT_MODEL, help="Must match `ollama list` on this machine.")
default_host = os.environ.get("OLLAMA_HOST", "")
host = st.sidebar.text_input(
    "Ollama API URL (optional)",
    value=default_host,
    placeholder="http://192.168.0.111:11434",
    help="Base URL of the Ollama API (same machine or remote). Set OLLAMA_HOST or edit here.",
)

german = st.text_area("German text", height=180, placeholder="Guten Tag, wie geht es Ihnen?")

if st.button("Translate to Ukrainian", type="primary", disabled=not german.strip()):
    try:
        client = _ollama_client(host)
        output_box = st.empty()
        buffer = ""
        for chunk in translate_stream(client, model, german.strip()):
            buffer += chunk
            # st.text preserves newlines; formatter splits glued "Word — … word — …" onto separate lines
            output_box.text(normalize_german_ukrainian_lines(buffer))
        if not buffer.strip():
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

st.sidebar.markdown("---")
