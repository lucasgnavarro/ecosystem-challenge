.PHONY: build \
init-venv \
test \
server \
run

.DEFAULT_GOAL := help

# FOR python requirements
VENV_FOLDER ?= .venv
REQUIREMENTS_FILE ?= dev-requirements.txt

help:
	@echo "    build"
	@echo "        Build docker image."
	@echo "    init-venv"
	@echo "        Initialize python virtual environment."
	@echo "    test"
	@echo "        Run Tests"
	@echo "    serve"
	@echo "        Start local web server"

build:
	@docker build . -t ecosystem-challenge_app

init-venv:
	@python3 -m venv $(VENV_FOLDER)
	@make update-venv

update-venv:
	@( \
		. $(VENV_FOLDER)/bin/activate; \
		pip install --upgrade setuptools pip; \
		pip install -r $(REQUIREMENTS_FILE); \
		pre-commit install; \
	)

test:
	@pytest --cov-report term --cov-report html --cov=app -s

server:
	@uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

run:
	@docker-compose up
