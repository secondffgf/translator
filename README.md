# translategemma

Small **Streamlit** app that takes **German** text and translates it to **Ukrainian** using a local **[Ollama](https://ollama.com/)** model (default name: `translategemma`).

## Prerequisites

- [Ollama](https://ollama.com/) with your translation model pulled on the machine that runs it (`ollama list` there).
- Python 3.12+ **or** Docker with Compose.

## Language pairs

Prompts and UI strings live under **`src/languages/`**. Each pair defines `PAIR` in its module (e.g. **`src/languages/de_uk.py`**, **`src/languages/es_uk.py`**, **`src/languages/fr_uk.py`**, **`src/languages/pl_uk.py`**). Register new pairs in **`src/languages/__init__.py`** (`_REGISTRY`).

Choose the pair **without editing code**:

- **Environment:** `APP_LANGUAGE=de-uk`, `es-uk`, `fr-uk`, or `pl-uk`
- **CLI (after `--`):**  
  `PYTHONPATH=src streamlit run src/app.py -- --lang es-uk`  
  Docker image CMD can append `-- --lang es-uk` if you prefer flags over env.

Default is **`de-uk`**.

## Run with Docker (recommended)

From this directory:

```bash
docker compose up --build
```

Pick the **language pair** without editing YAML (default **`de-uk`**):

```bash
APP_LANGUAGE=es-uk docker compose up --build
APP_LANGUAGE=fr-uk docker compose up --build
APP_LANGUAGE=pl-uk docker compose up --build
```

Or put **`APP_LANGUAGE=es-uk`** in a **`.env`** file next to `docker-compose.yml` (Compose reads it automatically).

Open **http://localhost:8501**.

Ollama is expected on **another machine**. Compose defaults:

- `OLLAMA_HOST=http://192.168.0.111:11434` (edit `docker-compose.yml` if your Ollama host differs)
- `OLLAMA_MODEL=translategemma:12b`
- `APP_LANGUAGE` — **`${APP_LANGUAGE:-de-uk}`** in Compose; override as above
- **`network_mode: host`** (Linux) so the container uses the **same routing as your PC** and can reach `192.168.*` addresses. Without this, Docker’s bridge network sometimes cannot reach the LAN even when `curl` on the host works (VPN / split routing → errno 113).

**Docker Desktop (Mac/Windows):** host networking is limited or unsupported; if the container still cannot reach Ollama, run the app on the host: `PYTHONPATH=src streamlit run src/app.py`.

On the **Ollama machine**, the API must accept connections from your network (not only `127.0.0.1`), for example:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

## On Mac
1. for each environment variable, call launchctl setenv
```bash
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
export OLLAMA_HOST="0.0.0.0:11434"
```
2. restart Ollama application

3. run translate llm
```bash
 ollama run translategemma:12b
```

Also open **TCP port 11434** (or your port) in that machine’s firewall so this PC can reach it.

If your LAN uses **`192.168.x.x`**, your address might be `192.168.0.111` instead of `192.186.x.x` — update the URL accordingly.

### Docker without Compose (Linux — same idea as Compose)

Use **host networking** so outbound routes match the host (needed for LAN IPs with many VPN/setups):

```bash
docker build -t translategemma-ui .
docker run --rm --network host \
  -e OLLAMA_HOST=http://192.168.0.111:11434 \
  -e OLLAMA_MODEL=translategemma:12b \
  translategemma-ui
```

Open **http://localhost:8501**. Without `--network host`, use port mapping `-p 8501:8501` only if your setup reaches Ollama from the bridge network.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=src streamlit run src/app.py
```

Or use the `Makefile` shortcuts:

```bash
make up-es    # docker compose with APP_LANGUAGE=es-uk
```

Ollama’s default API (`http://127.0.0.1:11434`) is used if you leave the **Ollama API URL** field empty in the sidebar.

## Troubleshooting: `[Errno 113] No route to host`

That error means **this computer cannot send packets to the IP you configured** (routing / wrong address / blocked path), not “Ollama returned HTTP 500”.

1. **Confirm the IP** — Typing **`192.186`** instead of **`192.168`** is a common mistake. On the Ollama PC run `ip a` / `ifconfig` (or check the router’s DHCP list) and set `OLLAMA_HOST` / the sidebar URL to that address, e.g. `http://192.168.0.111:11434`.
2. **Reachability** — From the machine running Streamlit (or from inside the container host), run:  
   `curl -sS --connect-timeout 3 http://<ollama-ip>:11434/api/tags`  
   If that fails, fix the network before the app will work.
3. **Ollama binds to all interfaces** — On the Ollama host use `OLLAMA_HOST=0.0.0.0:11434` so it listens on the LAN, not only `127.0.0.1`.
4. **Firewall** — Allow **TCP 11434** inbound on the Ollama machine (ufw, Windows Defender Firewall, etc.).
5. **Wi‑Fi guest / AP isolation** — Some routers block client-to-client traffic; use the main LAN or wired connection.
6. **Docker bridge vs host** — If `curl` on the host works to `192.168.*` but the **container** gets errno 113, use **`network_mode: host`** in Compose (already set in this repo on Linux) or `docker run --network host`.

## Configuration

| Variable / UI field | Meaning |
| --- | --- |
| `OLLAMA_MODEL` | Default model name in the sidebar (default: `translategemma`). |
| `OLLAMA_HOST` | Full base URL for the Ollama API (e.g. `http://192.168.0.111:11434`). Also editable in the sidebar. |
| `APP_LANGUAGE` | Language pair code: `de-uk`, `es-uk`, `fr-uk`, `pl-uk`, … (must exist in `src/languages/__init__.py`). |

## Project layout

- `src/util.py` — Ollama health checks, structured chat fetch, connection hints, Streamlit helpers.
- `src/llm_response.py` — Pydantic models for structured translation JSON.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — image build (`PYTHONPATH=/app/src`) and `streamlit run src/app.py`.
- `docker-compose.yml` — **`network_mode: host`** (Linux), **8501**, remote Ollama URL, **`APP_LANGUAGE`**.
- `src/languages/` — one module per pair (`de_uk.py`, `es_uk.py`, `pl_uk.py`, …): **system prompt**, UI labels, optional **`normalize_output`**.
- `src/settings.py` — resolves **`APP_LANGUAGE`** or **`--lang`** / **`--language`**.
