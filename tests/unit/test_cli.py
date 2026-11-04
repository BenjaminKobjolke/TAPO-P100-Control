from unittest.mock import MagicMock, patch

from PyP100 import PyP100

from tapo_control.app_logger import AppLogger
from tapo_control.cli import main


def test_returns_zero_on_success() -> None:
    plug = MagicMock(spec=PyP100.P100)
    assert main(["u", "p", "10.0.0.1", "on"], MagicMock(return_value=plug)) == 0
    plug.turnOn.assert_called_once_with()


@patch("tapo_control.cli.AppLogger", spec=AppLogger)
def test_reports_invalid_args_and_returns_one(logger_cls: MagicMock) -> None:
    factory = MagicMock()
    assert main(["u", "p", "nope", "on"], factory) == 1
    factory.assert_not_called()
    assert 'Invalid IP "nope"' in logger_cls.return_value.error.call_args.args[0]


@patch("tapo_control.cli.AppLogger", spec=AppLogger)
def test_reports_plug_failure_and_returns_one(logger_cls: MagicMock) -> None:
    factory = MagicMock(side_effect=Exception("timeout"))
    assert main(["u", "p", "10.0.0.1", "off"], factory) == 1
    assert "Third-Party Compatibility" in logger_cls.return_value.error.call_args.args[0]
