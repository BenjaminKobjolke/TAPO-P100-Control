"""User-facing strings and logger names shared across the CLI."""

USAGE = "usage: tapo USERNAME PASSWORD IP on|off"
ARG_COUNT = 4

APP_LOGGER_NAME = "tapo"
PYP100_LOGGER_NAME = "PyP100"

INVALID_IP = 'Invalid IP "{ip}". ' + USAGE
INVALID_ACTION = 'Invalid action "{action}", use on or off. ' + USAGE
SWITCH_FAILED = (
    "Failed to switch plug {ip} {action}: {error}\n"
    'Check IP, username/password, and "Third-Party Compatibility" in the Tapo app.'
)
