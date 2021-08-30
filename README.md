# Introduction 
This is the best Reddit clone you'll ever see.

# Run
### Backend
Install [Neo4j](https://neo4j.com/download/), [MongoDB](https://www.mongodb.com/try/download/community) and [Redis](https://redis.io/download).

Install [poetry](https://python-poetry.org/docs/#installation) and run `poetry install` from the `backend` directory (where the `pyproject.toml` file is located).

Copy the contents of the `dot_env_example` to a new file called `.env` in the same directory and adjust credentials for production DB.

To run, execute `poetry run app/main.py` from the `backend` directory.

From the `backend` directory, run `poetry run scripts/dummy_data.py` with the `fill` argument to fill the databases with dummy data, with the `clear` argument to clear all data, or with `-h` for more information.

# Test
### Backend
Adjust credentials for testing DB in `.env`. 

Run `scripts/test.sh` to run all tests including a coverage report.

# Develop
### Backend
To resolve the modules correctly in your IDE, the `backend` directory needs to be in your `PYTHONPATH` (e.g. [instructions for PyCharm](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-reloading-interpreter-paths.html)).

For logging Cypher queries, set environment variable `NEOMODEL_CYPHER_DEBUG=1`.

For code linting, run `scripts/lint.sh` from the `backend` directory.

Before commiting, run `scripts/format.sh` from the `backend` directory.
It performs automatic code formatting, import sorting and removes unused imports.
