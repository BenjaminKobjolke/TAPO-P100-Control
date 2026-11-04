@echo off
REM Build dist\tapo.exe; release_notes\ is bundled into the exe (PyInstaller --add-data).
cd /d "%~dp0.."
uv run --with pyinstaller pyinstaller --onefile --name tapo --add-data "release_notes;release_notes" src\tapo.py
exit /b %ERRORLEVEL%
