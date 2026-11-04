"""Talk to the plug through PyP100."""

from collections.abc import Callable
from typing import Any

from PyP100 import PyP100

from tapo_control.command import PlugAction, PlugCommand
from tapo_control.constants import SWITCH_FAILED

PlugFactory = Callable[[str, str, str], Any]
DEFAULT_PLUG_FACTORY: PlugFactory = PyP100.P100


class PlugError(RuntimeError):
    """Raised when the plug could not be switched."""


def switch_plug(command: PlugCommand, plug_factory: PlugFactory = DEFAULT_PLUG_FACTORY) -> None:
    """Log in to the plug and turn it on or off."""
    try:
        plug = plug_factory(command.ip, command.username, command.password)
        plug.handshake()
        plug.login()
        if command.action is PlugAction.ON:
            plug.turnOn()
        else:
            plug.turnOff()
    except Exception as e:  # PyP100 raises bare Exception and requests errors
        raise PlugError(SWITCH_FAILED.format(ip=command.ip, action=command.action, error=e)) from e
