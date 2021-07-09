@echo off 
echo start formatting..

:: sort imports one per line, so autoflake can remove unused imports
call poetry run isort app --force-single-line-imports

:: remove unused imports
call poetry run autoflake --remove-all-unused-imports --recursive --in-place app --exclude=__init__.py

:: format code
call poetry run black app

:: sort imports
call poetry run isort app