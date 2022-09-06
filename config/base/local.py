# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import os
from pathlib import Path
from django.conf import settings
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-caebb+zs_ai6pc5g-kb&jlt626l4sgi*fjwhn5k8+9)vlznx+mg9ubl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# multiple database settings.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': settings.BASE_DIR / 'db.sqlite3',
#     },
#     'remote': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME':
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}