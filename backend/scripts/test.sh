#!/usr/bin/env bash

set -e
set -x

poetry run pytest --cov-report=term-missing --cov=app app/tests
