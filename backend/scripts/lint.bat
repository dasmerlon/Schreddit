@echo off
echo start linting..

call poetry run black app --check
call poetry run isort --check-only app
call poetry run flake8