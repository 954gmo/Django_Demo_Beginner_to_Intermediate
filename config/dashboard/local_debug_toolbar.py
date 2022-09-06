# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from .base import MIDDLEWARE, INSTALLED_APPS
import importlib

try:
    settings = importlib.import_module('config.local')
    for setting in dir(settings):
        # Only fully-uppercase variables are supposed to be settings
        if setting == setting.upper():
            locals()[setting] = getattr(settings, setting)
except Exception as e:
    # could be ignore, the print is for debugging purposes
    print(e)

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]
INTERNAL_IPS = ('127.0.0.1',)

