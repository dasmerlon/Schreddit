#!/usr/bin/env bash

set -e
set -x

# sort imports one per line, so autoflake can remove unused imports
poetry run isort app --force-single-line-imports

# remove unused imports
poetry run autoflake --remove-all-unused-imports --recursive --in-place app --exclude=__init__.py

# format code
poetry run black app

# sort imports
poetry run isort app
