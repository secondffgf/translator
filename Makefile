.PHONY: up-de up-es up-fr up-pl down logs ollama-check

OLLAMA_HOST ?= http://192.168.0.111:11434

up-de:
	APP_LANGUAGE=de-uk docker compose up --build

up-es:
	APP_LANGUAGE=es-uk docker compose up --build

up-fr:
	APP_LANGUAGE=fr-uk docker compose up --build

up-pl:
	APP_LANGUAGE=pl-uk docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

ollama-check:
	@host="$(OLLAMA_HOST)"; host="$${host%/}"; \
	echo "Checking Ollama at $$host/api/tags"; \
	curl -fsS --connect-timeout 3 "$$host/api/tags" >/dev/null && \
	echo "OK: Ollama is reachable at $$host" || \
	(echo "ERROR: Cannot reach Ollama at $$host"; exit 1)
