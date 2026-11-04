"""Parse and validate the command-line arguments into a typed command."""

import ipaddress
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from tapo_control.constants import ARG_COUNT, INVALID_ACTION, INVALID_IP, USAGE


class CommandError(ValueError):
    """Raised when the arguments are not a valid plug command."""


class PlugAction(StrEnum):
    ON = "on"
    OFF = "off"


@dataclass(frozen=True)
class PlugCommand:
    username: str
    password: str
    ip: str
    action: PlugAction


def parse_args(args: Sequence[str]) -> PlugCommand:
    """Build a PlugCommand from USERNAME PASSWORD IP on|off (without the program name)."""
    if len(args) != ARG_COUNT:
        raise CommandError(USAGE)
    username, password, ip, action = args

    # cmd.exe passes single quotes literally; strip them so 'pw' works like "pw"
    if len(password) > 1 and password[0] == password[-1] == "'":
        password = password[1:-1]

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise CommandError(INVALID_IP.format(ip=ip)) from None

    try:
        plug_action = PlugAction(action)
    except ValueError:
        raise CommandError(INVALID_ACTION.format(action=action)) from None

    return PlugCommand(username, password, ip, plug_action)
