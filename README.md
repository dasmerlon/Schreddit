# Introduction 
This is the best Reddit clone you'll ever see.

# Run
### Backend
Install `poetry` and run `poetry install` from the `backend` directory (where the `pyproject.toml` file is located).

Copy the contents of the `dot_env_example` to a new file called `.env` in the same directory and adjust credentials for production and testing DB.

To run, execute `poetry run app/main.py` from the `backend` directory.

To resolve the modules correctly in your IDE, the `backend` directory needs to be in your `PYTHONPATH` (e.g. [instructions for PyCharm](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-reloading-interpreter-paths.html)).

# Test
### Backend
Run `scripts/test.sh` to run all tests including a coverage report.

# Develop
### Backend
For code linting run `scripts/lint.sh` from the `backend` directory.

Before commiting, run `scripts/format.sh` from the `backend` directory
It does automatic code formatting, import sorting, and removes unused imports.
