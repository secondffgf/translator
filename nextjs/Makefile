.PHONY: build up up-build down logs dev lint clean rebuild

IMAGE ?= nextjs-hello
PORT ?= 3000
NPM_CONFIG_USERCONFIG := $(CURDIR)/.npmrc
NPM_CONFIG_REGISTRY := https://registry.npmjs.org/

build:
	docker build -t $(IMAGE) .

up:
	docker compose up

up-build:
	docker compose up --build

down:
	docker compose down

clean:
	docker compose down --rmi local --remove-orphans

rebuild:
	docker compose down --rmi local --remove-orphans
	docker compose build --no-cache
	docker compose up --build

logs:
	docker compose logs -f

dev:
	NPM_CONFIG_USERCONFIG=$(NPM_CONFIG_USERCONFIG) NPM_CONFIG_REGISTRY=$(NPM_CONFIG_REGISTRY) npm run dev

lint:
	NPM_CONFIG_USERCONFIG=$(NPM_CONFIG_USERCONFIG) NPM_CONFIG_REGISTRY=$(NPM_CONFIG_REGISTRY) npm run lint
