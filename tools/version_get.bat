@echo off
REM Print the release version (pyproject.toml [project] version).
uv run python "%~dp0release\version_number.py" get
set "VERSION_SCRIPT_EXIT_CODE=%ERRORLEVEL%"
exit /b %VERSION_SCRIPT_EXIT_CODE%
