# Introduction 
This is the best Reddit clone you'll ever see.

# Getting Started
### Backend
Install `poetry` and run `poetry install` from the `backend` directory (where the `pyproject.toml` file is located).

Copy the contents of the `dot_env_example` to a new file called `.env` in the same directory and adjust credentials for production and testing DB.

To run, execute `poetry run app/main.py` from the `backend` directory.

To resolve the modules correctly in your IDE, the `backend` directory needs to be in your `PYTHONPATH` (e.g. [instructions for PyCharm](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-reloading-interpreter-paths.html)).

# Test
### Backend
Run `poetry run pytest` to run all tests, see the documentation of `pytest` for running specific tests.