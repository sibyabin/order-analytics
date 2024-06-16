# Order-Analytics
`order-analytics` is a data engineering solution project for ABC Musical Instruments LTD, UK. The project caters to the order data analytics requirement using python and sqllite.

## Project deliverables 
- Datamodel
- ETL Processing 
- Documentation

# How to Run locally ?

## Pre-Requisites
- Python 3
- [Make ](https://gnuwin32.sourceforge.net/packages/make.htm)


## Setting up your own virtual environment

Run `make virtualenv` to create a virtual environment.
then activate it with `source .venv/bin/activate`.

## Run the tests to ensure everything is working

Run `make test` to run the tests.

## Format the code

Run `make fmt` to format the code.

## Run the linter

Run `make lint` to run the linter.

## Test your changes

Run `make test` to run the tests.

## Build the docs locally

Run `make docs` to build the docs.Ensure your new changes are documented.

## Makefile utilities

This project comes with a `Makefile` that contains a number of useful utility.

```bash 
❯ make
Usage: make <target>

Targets:
help:             ## Show the help.
fmt:              ## Format code using black & isort.
lint:             ## Run pep8, black, mypy linters.
test              ## Run tests and generate coverage report.
run:              ## Run the project.
build:            ## Build package.
clean:            ## Clean unused files.
docs:             ## Build the documentation.

```
