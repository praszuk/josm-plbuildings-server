.PHONY: install black black-check isort isort-check format format-check dprod-run drun clean dclean update

SHELL := /bin/bash
VENV=.venv
PYTHON=$(VENV)/bin/python
PROJECT_DIR=$(shell pwd)
APP_DIR=backend


install:
	virtualenv -p python3 $(VENV)
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install -r requirements/requirements-dev.txt
	if [ -d ".git" ]; then $(PYTHON) -m pre_commit install; fi

isort:
	$(PYTHON) -m isort $(APP_DIR)

isort-check:
	$(PYTHON) -m isort --check --diff $(APP_DIR)

black-check:
	$(PYTHON) -m black --check --diff $(APP_DIR)

black:
	$(PYTHON) -m black $(APP_DIR)

format: isort black

format-check: isort-check black-check

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