"""tools/release/version_number.py: semver patch bump of pyproject.toml [project] version."""

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "tools" / "release" / "version_number.py"


def _load() -> ModuleType:
    # tools/ is not a package on pythonpath, so load the script by path
    spec = importlib.util.spec_from_file_location("version_number", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def pyproject(tmp_path: Path) -> Path:
    path = tmp_path / "pyproject.toml"
    path.write_bytes(
        b'[project]\r\nname = "x"\r\nversion = "0.1.9"\r\n\r\n[tool.x]\r\nversion = "9"\r\n'
    )
    return path


def test_get_reads_project_version(pyproject: Path) -> None:
    assert _load().read_version(pyproject) == "0.1.9"


def test_increment_then_decrement_round_trips(pyproject: Path) -> None:
    vn = _load()
    original = pyproject.read_bytes()
    assert vn.shift_patch(1, pyproject) == "0.1.10"
    assert b'version = "0.1.10"\r\n' in pyproject.read_bytes()
    assert b'version = "9"' in pyproject.read_bytes()
    assert vn.shift_patch(-1, pyproject) == "0.1.9"
    assert pyproject.read_bytes() == original


def test_decrement_below_zero_fails(tmp_path: Path) -> None:
    path = tmp_path / "pyproject.toml"
    path.write_text('[project]\nversion = "0.1.0"\n', encoding="utf-8")
    with pytest.raises(ValueError):
        _load().shift_patch(-1, path)
