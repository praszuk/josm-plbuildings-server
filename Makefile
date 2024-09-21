.PHONY: install format format-check lint lint-check dprod-run drun clean dclean update

SHELL := /bin/bash
VENV=.venv
PYTHON=$(VENV)/bin/python
PROJECT_DIR=$(shell pwd)
APP_DIR=backend


install:
	virtualenv -p python3 $(VENV)
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install -r requirements/requirements-dev.txt
	$(PYTHON) -m pip install -r requirements/requirements.txt
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit install; fi

format:
	$(PYTHON) -m ruff format $(APP_DIR)

format-check:
	$(PYTHON) -m ruff format --diff $(APP_DIR)

lint:
	$(PYTHON) -m ruff check $(APP_DIR)

lint-check:
	$(PYTHON) -m ruff check --diff $(APP_DIR)

drun:
	docker compose -f docker-compose-dev.yml up

dprod-run:
	docker compose -f docker-compose-prod.yml up

dclean:
	docker compose -f docker-compose-dev.yml down
	docker compose -f docker-compose-prod.yml down

clean: dclean
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit uninstall; fi
	rm -rf  __pycache__ $(VENV)

update:
	for filename in requirements/*.in; do pur -r $$filename; done
	pip-compile-multi