.PHONY: build up up-build down logs dev lint

IMAGE ?= nextjs-hello
PORT ?= 3000

build:
	docker build -t $(IMAGE) .

up:
	docker compose up

up-build:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

dev:
	npm run dev

lint:
	npm run lint
