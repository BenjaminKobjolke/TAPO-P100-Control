# TAPO P100 Control

Switch a TP-Link Tapo P100 smart plug on or off from the command line.
Uses [almottier/TapoP100](https://github.com/almottier/TapoP100) (fork of fishbigger/TapoP100).

Enable "Third-Party Compatibility" in the Tapo app, otherwise the plug rejects the login.

# Use

## Exe from release
> tapo.exe TAPO_USERNAME TAPO_PASSWORD IP on|off

### Examples
> tapo.exe test@test.com 12345 192.168.10.82 off

> tapo.exe test@test.com 12345 192.168.10.82 on

## From source
Run `install.bat` once first (see [Install](#install)), then from the project root:

> start.bat TAPO_USERNAME TAPO_PASSWORD IP on|off

In PowerShell, prefix it with `.\`:

> .\start.bat TAPO_USERNAME TAPO_PASSWORD IP on|off

or

> uv run python src/tapo.py TAPO_USERNAME TAPO_PASSWORD IP on|off

Exit code is `0` on success and `1` on invalid input or when the plug cannot be switched.

# Develop

## Requirements
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (installs Python 3.11/3.12 itself)
- git (the PyP100 dependency is installed from GitHub)

## Install
> install.bat

Runs `uv sync --all-extras` and the test suite.

## Update dependencies
> update.bat

Runs `uv lock --upgrade`, `uv sync`, ruff, mypy and the tests. Commit `uv.lock` afterwards.

## Tests and checks
- `tools\run_tests.bat` — unit tests (`tests/unit`)
- `tools\run_integration_tests.bat` — integration tests (`tests/integration`, runs the real script, no network)
- `uv run ruff check src tests`, `uv run ruff format src tests`, `uv run mypy src/`

## Build exe
> build_release.bat

Runs PyInstaller through `uv run --with pyinstaller`; the exe is written to `dist/tapo.exe`.
