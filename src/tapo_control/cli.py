"""CLI entry point with the central error handler."""

from collections.abc import Sequence

from tapo_control.app_logger import AppLogger
from tapo_control.command import CommandError, parse_args
from tapo_control.plug import DEFAULT_PLUG_FACTORY, PlugError, PlugFactory, switch_plug


def main(args: Sequence[str], plug_factory: PlugFactory = DEFAULT_PLUG_FACTORY) -> int:
    """Run the command; return the process exit code."""
    logger = AppLogger()
    try:
        command = parse_args(args)
        switch_plug(command, plug_factory)
    except (CommandError, PlugError) as e:
        logger.error(str(e))
        return 1
    return 0
