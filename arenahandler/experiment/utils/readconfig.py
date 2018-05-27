import os
import json
#from arenahandler import version as app_ver

config_example = \
"""
{
    "serialport":"COM5",
    "baudrate":"57600"
}
"""

config = json.loads(open('config/config.json').read())