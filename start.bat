@echo off
uv run python "%~dp0src\tapo.py" %*
exit /b %ERRORLEVEL%
