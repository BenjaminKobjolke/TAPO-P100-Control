"""Run the real entry script in a subprocess (no network: only failing-validation paths)."""

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "src" / "tapo.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, timeout=60
    )


@pytest.mark.parametrize(
    ("args", "message"),
    [
        ((), "usage: tapo USERNAME PASSWORD IP on|off"),
        (("u", "p", "300.1.1.1", "on"), 'Invalid IP "300.1.1.1"'),
        (("u", "p", "10.0.0.1", "toggle"), 'Invalid action "toggle"'),
    ],
)
def test_invalid_input_exits_one_with_message(args: tuple[str, ...], message: str) -> None:
    result = run_cli(*args)
    assert result.returncode == 1
    assert message in result.stderr
    assert "Traceback" not in result.stderr
