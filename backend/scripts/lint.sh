#!/usr/bin/env bash

set -x

# dry run of format.sh, using flake8 instead of autoflake
poetry run black app --check
poetry run isort --check-only app
poetry run flake8
