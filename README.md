# Order-Analytics

`order-analytics` is a data engineering project for ABC Musical Instruments LTD, UK. The project caters to the order data analytics requirements using python and sqlite.

## Table of Contents
- [Design Decisions](#design-decisions)
- [Pre-requisites](#pre-requisites)
- [Project deliverables](#project-deliverables)
- [Project Structure](#project-structure)
- [How to setup the project locally](#how-to-setup-the-project-locally)
- [How to run the script locally?](#how-to-run-the-script-locally)
- [How to run the tests locally?](#how-to-run-the-tests-locally)
- [Project Links](#project-links)
- [TODO](#todo)
- [Using Makefile - Options available](#using-makefile---options-available)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Other useful commands](#other-useful-commands)
- [Author](#author)

## Design Decisions
| Item | Decision |
| ------ | ------ |
| ORM tools or native approach to interact with databases | Chosen native approach as being a DWH, we may have to version control even the DDL's. Using an ORM gives less flexibility to move to a database deployment tools like flyway or dbdeploy or sqitch |
|||
|||

## Pre-requisites
- Python 3.9
- Make utility. **THIS IS OPTIONAL**. Please check [Make ](https://gnuwin32.sourceforge.net/packages/make.htm) for installation in windows.

## Project deliverables

- Datamodel
- ETL Specification Document
- Python ETL Code
- Documentation

### Data model diagrams
![orders mart](docs/assets/orders_mart.svg)

## Project Structure

```
.
├── docs
│   ├── assets
│   │   └── orders_mart.svg
│   ├── index.md
│   └── shared
│       └── Requirement.docx
├── LICENSE
├── Makefile
├── mkdocs.yml
├── order_analytics
│   ├── config
│   │   └── config.ini
│   ├── core
│   │   ├── commons
│   │   │   ├── batch.py
│   │   │   ├── config.py
│   │   │   ├── db.py
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── utils.py
│   │   └── __init__.py
│   ├── database
│   │   └── orders.db
│   ├── files
│   │   ├── orders.csv
│   │   ├── orders_test_1.csv
│   │   └── orders_test_2.csv
│   ├── __init__.py
│   ├── main.py
│   ├── sqls
│   │   ├── ddls
│   │   │   ├── batch_information.sql
│   │   │   ├── currency_dim.sql
│   │   │   ├── customer_dim.sql
│   │   │   ├── date_dim.sql
│   │   │   ├── order_line_fact.sql
│   │   │   ├── product_dim.sql
│   │   │   └── stg_orders.sql
│   │   └── transformations
│   │       ├── currency_dim.sql
│   │       ├── customer_dim.sql
│   │       ├── order_line_fact.sql
│   │       └── product_dim.sql
│   └── VERSION
├── README.md
├── requirements-test.txt
├── requirements.txt
├── setup.py
└── tests
    ├── db_test.py
    └── main_test.py


```

## How to setup the project locally?

- ##### Clone the `order-analytics` github project repository

```bash
git clone https://github.com/sibyabin/order-analytics.git
```

- ##### Change the directory to the app folder

```bash
cd order_analytics
```

- ##### Create a virtual environment

```bash
python -m venv venv
```

- ##### Activate virtual environment (Note: please use commands according to your machines OS)

```bash
source venv/bin/activate (for linux)  or  . venv/Scripts/activate  (for windows)
```

- ##### Upgrade pip

```bash
python  -m pip install --upgrade pip
```

- ##### Install requirements

```bash
pip install -r requirements-test.txt

pip install -e .
```

## How to run the script locally?

The script accepts two paramters:

**-e or --environment** : Use **dev** as value

**-f or --filename** : Use any file placed within **order_analytics/files** folder. You can load your own files by copying the file to the mentioend directory and then passign the correct
filename to the -f option while triggering the script

```bash
export PROJECT_HOME=your/path/to/order_analytics
python order_analytics/main.py -e dev -f orders_test_1.csv
```

## Screencast
https://1drv.ms/f/s!Ag168Up5vNdNhMlMX_UOdPdjHTAVjQ?e=zvkcmK 

## How to run the tests locally?

Run pytest in the terminal and you should see the default tests written are getting executed and the coverage files are getting generated

```bash
pytest
```

```bash

$ pytest
============================= test session starts =============================
platform win32 -- Python 3.9.1, pytest-8.2.2, pluggy-1.5.0
rootdir: E:\repo\order-analytics
plugins: cov-5.0.0
collected 3 items

tests\db_test.py ..                                                      [ 66%]
tests\main_test.py .                                                     [100%]

============================== 3 passed in 1.01s ==============================
(venv)
```

## Project Links

| Item | Description |
| ------ | ------ |
| Project Board | [Project Board](https://github.com/users/sibyabin/projects/3/views/1?layout=board) |
| Issues | [Issues](https://github.com/sibyabin/order-analytics/issues) |
| Mapping Document | |


## TODO

- Exception tables
- Batch status dashboard

------

## Using Makefile - Options available

This project comes with a `Makefile` that contains a number of target options to simplify the different activities using short commands.

```bash
❯ make
Usage: make <target>

Targets:
install           ## Virtual environment setup
test              ## Run tests and generate coverage report.
run               ## Run the project.
clean             ## Clean unused files.

fmt               ## Format code using black & isort.
lint              ## Run pep8, black, mypy linters.
build             ## Build package.
docs              ## Build the documentation.
```

### Setting up your own virtual environment

Run `make install` to create a virtual environment `venv` locally and then install all the package requirements to it.

```bash
$ make setup
Going to setup environment
python -m venv venv && . venv/Scripts/activate && venv/Scripts/python -m pip install --upgrade pip setuptools
Collecting pip
  Using cached pip-24.0-py3-none-any.whl (2.1 MB)
Collecting setuptools
  Using cached setuptools-70.0.0-py3-none-any.whl (863 kB)
Installing collected packages: pip, setuptools
  Attempting uninstall: pip
    Found existing installation: pip 20.2.3
    Uninstalling pip-20.2.3:
      Successfully uninstalled pip-20.2.3
  Attempting uninstall: setuptools
    Found existing installation: setuptools 49.2.1
    Uninstalling setuptools-49.2.1:
      Successfully uninstalled setuptools-49.2.1
Successfully installed pip-24.0 setuptools-70.0.0
venv/Scripts/pip3 install -r requirements-test.txt
Collecting pytest (from -r requirements-test.txt (line 1))
  Downloading pytest-8.2.2-py3-none-any.whl.metadata (7.6 kB)

.........................................................
.........................................................

Using cached idna-3.7-py3-none-any.whl (66 kB)
Using cached urllib3-2.2.1-py3-none-any.whl (121 kB)
Installing collected packages: urllib3, idna, charset-normalizer, certifi, requests, order-analytics
  Running setup.py develop for order-analytics
Successfully installed certifi-2024.6.2 charset-normalizer-3.3.2 idna-3.7 order-analytics-0.1.0 requests-2.32.3 urllib3-2.2.1
Setup completed
```

### Run the tests to ensure everything is working locally

Run `make test` to run the tests.

### Run the code

Run `make run` to run the code. This will

- Create databases and tables (if not exists already)
- Load data to staging
- Load data from staging to mart tables
- Store exception records to exception schema tables

### Cleaning the project

`make clean` will remove

- logs
- site directory
- build packages
- virtual environment etc.

## Other useful commands

| Command | Description |
| ------ | ------ |
| `make fmt` | To format the code |
| `make lint` | To run the linter |
| `make docs` | To build the docs.|

## Pre-commit Hooks

Use the pre-commit hooks defined in the project to fix format issues.

```bash
pre-commit install

pre-commit run
```

## Author

- [Siby Abin Thomas](https://www.github.com/sibyabin)
