"""Central logger: the only module that touches the `logging` package."""

import logging
import sys

from tapo_control.constants import APP_LOGGER_NAME, PYP100_LOGGER_NAME


class AppLogger:
    """Writes plain messages to stderr; one place to change level or sink."""

    def __init__(self, level: int = logging.INFO) -> None:
        self._logger = logging.getLogger(APP_LOGGER_NAME)
        self._logger.setLevel(level)
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(logging.Formatter("%(message)s"))
            self._logger.addHandler(handler)
        self._logger.propagate = False
        # PyP100 logs a full traceback per failed protocol; we report one clean line instead
        logging.getLogger(PYP100_LOGGER_NAME).setLevel(logging.CRITICAL)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def error(self, message: str) -> None:
        self._logger.error(message)
