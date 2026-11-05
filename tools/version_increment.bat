@echo off
REM Bump the last version segment in pyproject.toml (0.1.0 -> 0.1.1) and print it.
uv run python "%~dp0release\version_number.py" increment
set "VERSION_SCRIPT_EXIT_CODE=%ERRORLEVEL%"
exit /b %VERSION_SCRIPT_EXIT_CODE%
