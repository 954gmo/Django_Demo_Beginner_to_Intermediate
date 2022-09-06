# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import traceback

"""
Django settings for the project
"""
import importlib # https://docs.python.org/3/library/importlib.html
# Begin: Custom per-env settings
import socket

HOST = socket.gethostname()
CONFIGS = {
    'DESKTOP-0UV5SFP': 'local',  # change 'DESKTOP-0UV5SFP' to your machine name
    'Tutorial': 'prod',  # change 'Tutorial' to your machine name
}
config = f'config.blog.{CONFIGS[HOST]}'

setting_module_files = [
    'config.blog.base',  # setup base settings that are common to all profile, local, production or other env
    config,  # Automatically Determine which configuration file to setup with, by the hostname
]

try:
    for module_file in setting_module_files:
        module_settings = importlib.import_module(module_file)
        for setting in dir(module_settings):
            # Only fully-uppercase variables are supposed to be settings
            if setting == setting.upper():
                locals()[setting] = getattr(module_settings, setting)
except Exception as e:
    # could be ignore, the print is for debugging purposes
    traceback.print_exception(e)

