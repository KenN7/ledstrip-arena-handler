import os
import json
#from arenahandler import version as app_ver

config_example = \
"""
{
    "serialport":"/dev/ttyS5",
    "baudrate": 57600,
    "loglevel":"INFO",
    "logformat":"%(asctime)s %(name)s [%(levelname)s] %(message)s"
}
"""

config = json.loads(open('config/config.json').read())