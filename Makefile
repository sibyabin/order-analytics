# .ONESHELL:
.PHONY: install activate fmt lint test run build docs clean

# Configuration
VENV = venv
PROJECT = order_analytics

# set the project variables to the current directory
export PROJECT_HOME := $(CURDIR)/order_analytics
# export DATABASE_PATH := $(PROJECT_HOME)/database
# export SQL_PATH := $(PROJECT_HOME)/sqls
# export FILES_PATH := $(PROJECT_HOME)/files

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

help:             				## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

print:             				## print the configs
	@echo PROJECT_HOME = $(PROJECT_HOME)

install: requirements-test.txt			## Virtual environment setup
	@echo "Going to setup environment"
	python -m venv $(VENV) && . $(CMD) && $(PYTHON) -m pip install --upgrade pip setuptools
	$(PIP) install -r requirements-test.txt
	$(ENV_PREFIX)/pip install -e .[test]
	@echo "Setup completed"

activate: install
	@echo "Going to activate environment"
	. $(CMD)

fmt:              				## Format code using black & isort.
	$(ENV_PREFIX)/isort $(PROJECT)/
	$(ENV_PREFIX)/black -l 100 $(PROJECT)/
	$(ENV_PREFIX)/black -l 100 tests/

lint:             				## Run linters.
	$(ENV_PREFIX)/flake8 $(PROJECT)/
	$(ENV_PREFIX)/black -l 120 --check $(PROJECT)/
	$(ENV_PREFIX)/black -l 120 --check tests/
	$(ENV_PREFIX)/mypy --ignore-missing-imports $(PROJECT)/

test: lint        				## Run tests and generate coverage.
	$(ENV_PREFIX)/pytest -v --cov-config .coveragerc --cov=$(PROJECT) -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)/coverage xml
	$(ENV_PREFIX)/coverage html

run: activate     				## Run app.
	@echo "Going to run scripts"
	$(PYTHON) $(PROJECT)/main.py
	@echo "Script run completed"

build: activate   				## Build package.
	@echo "Going to build packages"
	$(PYTHON) setup.py sdist bdist_wheel | tee logs/build.log
	@echo "Package build completed"

clean:            				## Clean unused files.
	@echo "Going to clean directories"
	rm -rf $(VENV)
	rm -rf build dist *.egg-info
	rm -rf site
	rm -rf logs
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete


docs:            				## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)/mkdocs build
