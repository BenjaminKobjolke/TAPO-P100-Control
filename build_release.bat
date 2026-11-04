@echo off
cd /d "%~dp0"
uv run --with pyinstaller pyinstaller --onefile --name tapo src\tapo.py
exit /b %ERRORLEVEL%
