# Introduction
This is Schreddit, a Reddit clone.

There is a deployed version of the clone available [here](https://kind-sea-014761903.azurestaticapps.net/), but a local installation is recommended.

# Run
### Backend
Install [Neo4j](https://neo4j.com/download/), the [Neo4j APOC Core library](https://neo4j.com/labs/apoc/4.3/installation/), [MongoDB](https://www.mongodb.com/try/download/community) and [Redis](https://redis.io/download).

Install [poetry](https://python-poetry.org/docs/#installation) and run `poetry install` from the `backend` directory (where the `pyproject.toml` file is located) to install the required dependencies.

Copy the contents of the `dot_env_example` to a new file called `.env` in the same directory and adjust credentials for production DB.

To run, execute `poetry run app/main.py` from the `backend` directory.
The API documentation will be available via http://localhost:8000/docs.

From the `backend` directory, run `poetry run scripts/dummy_data.py` with the `fill` argument to fill the databases with dummy data, with the `clear` argument to clear all data, or with `-h` for more information on configuration parameters.

### Frontend
Install [Node.js](https://nodejs.org/en/download/) and run `npm install` from the `frontend/schreddit-ui` directory (where the `package.json` file is located) to install the required dependencies.

To run, execute `npm start` from the `frontend/schreddit-ui` directory.
The app will be available via http://localhost:3000.

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
