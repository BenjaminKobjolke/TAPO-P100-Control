#!/usr/bin/python

import ipaddress
import logging
import sys
from PyP100 import PyP100

USAGE = 'usage: tapo USERNAME PASSWORD IP on|off'

if len(sys.argv) != 5:
    sys.exit(USAGE)

username, password, ip, action = sys.argv[1:]

# cmd.exe passes single quotes literally; strip them so 'pw' works like "pw"
if len(password) > 1 and password[0] == password[-1] == "'":
    password = password[1:-1]

try:
    ipaddress.ip_address(ip)
except ValueError:
    sys.exit(f'Invalid IP "{ip}". {USAGE}')

if action not in ('on', 'off'):
    sys.exit(f'Invalid action "{action}", use on or off. {USAGE}')

# PyP100 logs a full traceback per failed protocol; we report one clean line instead
logging.getLogger('PyP100').setLevel(logging.CRITICAL)

try:
    p100 = PyP100.P100(ip, username, password)
    p100.handshake()
    p100.login()
    p100.turnOn() if action == 'on' else p100.turnOff()
except Exception as e:
    sys.exit(f'Failed to switch plug {ip} {action}: {e}\n'
             'Check IP, username/password, and "Third-Party Compatibility" in the Tapo app.')
