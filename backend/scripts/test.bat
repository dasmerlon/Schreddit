@echo off
echo start testing..

call poetry run pytest --cov-report=term-missing --cov=app app/tests