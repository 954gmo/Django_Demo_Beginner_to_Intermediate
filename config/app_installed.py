# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from config.base import INSTALLED_APPS

INSTALLED_APPS += [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    'accounts.apps.AccountsConfig',
    'api.apps.ApiConfig',
    'sites.apps.SitesConfig',
]

AUTH_USER_MODEL = 'accounts.Operator'