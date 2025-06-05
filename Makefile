PORT ?= 8080
install:
	uv sync

dev:
	uv run manage.py runserver 8080

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

collectstatic:
	uv run manage.py collectstatic

migrate:
	uv run manage.py migrate

lint:
	uv run flake8