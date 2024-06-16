# .ONESHELL:
.PHONY: setup activate fmt lint test run build docs clean

# Configuration
VENV = venv
PROJECT = order_analytics

ifeq ($(shell uname), Linux)
	ENV_PREFIX = $(VENV)/bin
	CMD = source $(VENV)/bin/activate
else
	ENV_PREFIX = $(VENV)/Scripts
	CMD = $(VENV)/Scripts/activate
endif
PIP = $(ENV_PREFIX)/pip3
PYTHON = $(ENV_PREFIX)/python

#Default target
# all: help setup activate fmt lint test run build docs

help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

setup: requirements-test.txt
	@echo "Going to setup environment"
	python -m venv $(VENV) && . $(CMD) && $(PIP) install -r requirements-test.txt
	$(PYTHON) -m pip install --upgrade pip setuptools 
	@echo "Setup completed"

activate: setup
	@echo "Going to activate environment"
	. $(CMD)

fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)/isort $(PROJECT)/
	$(ENV_PREFIX)/black -l 79 $(PROJECT)/
	$(ENV_PREFIX)/black -l 79 tests/

lint:             ## Run linters.
	$(ENV_PREFIX)/flake8 $(PROJECT)/
	$(ENV_PREFIX)/black -l 79 --check $(PROJECT)/
	$(ENV_PREFIX)/black -l 79 --check tests/
	$(ENV_PREFIX)/mypy --ignore-missing-imports $(PROJECT)/

test: lint        ## Run tests and generate coverage.
	$(ENV_PREFIX)/pytest -v --cov-config .coveragerc --cov=$(PROJECT) -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)/coverage xml
	$(ENV_PREFIX)/coverage html

run: activate     ## Run app.
	@echo "Going to run scripts"
	$(PYTHON) $(PROJECT)/main.py
	@echo "Script run completed"

build: activate   ## Build package.
	@echo "Going to build packages"
	$(PYTHON) setup.py sdist bdist_wheel | tee logs/build.log
	@echo "Package build completed"

clean:            ## Clean unused files.
	@echo "Going to clean directories"
	rm -rf $(VENV)
	rm -rf build dist *.egg-info
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete


docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)/mkdocs build
	URL="site/index.html"; xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL || open $$URL
