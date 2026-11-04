from unittest.mock import MagicMock, call

import pytest
from PyP100 import PyP100

from tapo_control.command import PlugAction, PlugCommand
from tapo_control.plug import PlugError, switch_plug


def make_factory(plug: MagicMock) -> MagicMock:
    return MagicMock(return_value=plug)


@pytest.mark.parametrize(
    ("action", "method"), [(PlugAction.ON, "turnOn"), (PlugAction.OFF, "turnOff")]
)
def test_logs_in_then_switches(action: PlugAction, method: str) -> None:
    plug = MagicMock(spec=PyP100.P100)
    factory = make_factory(plug)

    switch_plug(PlugCommand("u", "p", "10.0.0.1", action), factory)

    factory.assert_called_once_with("10.0.0.1", "u", "p")
    assert plug.method_calls == [call.handshake(), call.login(), getattr(call, method)()]


def test_wraps_failure_with_hint() -> None:
    plug = MagicMock(spec=PyP100.P100)
    plug.login.side_effect = Exception("bad credentials")

    with pytest.raises(PlugError, match="Failed to switch plug 10.0.0.1 off: bad credentials"):
        switch_plug(PlugCommand("u", "p", "10.0.0.1", PlugAction.OFF), make_factory(plug))
