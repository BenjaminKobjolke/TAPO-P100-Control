import pytest

from tapo_control.command import CommandError, PlugAction, PlugCommand, parse_args


def test_parses_valid_command() -> None:
    assert parse_args(["me@x.com", "pw", "192.168.10.82", "on"]) == PlugCommand(
        "me@x.com", "pw", "192.168.10.82", PlugAction.ON
    )


def test_strips_single_quotes_from_password() -> None:
    assert parse_args(["u", "'p w'", "10.0.0.1", "off"]).password == "p w"


def test_keeps_lone_quote_password() -> None:
    assert parse_args(["u", "'", "10.0.0.1", "off"]).password == "'"


@pytest.mark.parametrize("args", [[], ["u", "p", "10.0.0.1"], ["u", "p", "10.0.0.1", "on", "x"]])
def test_rejects_wrong_arg_count(args: list[str]) -> None:
    with pytest.raises(CommandError, match="usage"):
        parse_args(args)


def test_rejects_invalid_ip() -> None:
    with pytest.raises(CommandError, match='Invalid IP "plug.local"'):
        parse_args(["u", "p", "plug.local", "on"])


def test_rejects_invalid_action() -> None:
    with pytest.raises(CommandError, match='Invalid action "toggle"'):
        parse_args(["u", "p", "10.0.0.1", "toggle"])
