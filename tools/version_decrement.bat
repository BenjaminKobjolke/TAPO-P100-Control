@echo off
REM Roll the last version segment in pyproject.toml back by one and print it.
uv run python "%~dp0release\version_number.py" decrement
set "VERSION_SCRIPT_EXIT_CODE=%ERRORLEVEL%"
exit /b %VERSION_SCRIPT_EXIT_CODE%
