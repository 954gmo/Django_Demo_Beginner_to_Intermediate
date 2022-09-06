# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['example.com', '*']
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ORIGIN_WHITELIST = (
# )

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


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

QR_CODE = os.getenv('QR_CODE')
CUSTOMER_IMG = os.getenv('CUSTOMER_IMG')
CUSTOMER_ID = os.getenv('CUSTOMER_ID')

LOGO_URL = os.getenv('LOGO_URL')
QR_BASEURL = os.getenv('QR_BASEURL')
IMG_BASEURL = os.getenv('IMG_BASEURL')

SMS_ACCT = os.getenv('SMS_ACCT')
SMS_TOKEN = os.getenv('SMS_TOKEN')
SMS_FROM_NUMBER = os.getenv('SMS_FROM_NUMBER')
SMS_ADMIN_NUMBER = os.getenv('SMS_ADMIN_NUMBER')
SMS_MGMT_NUMBER = os.getenv('SMS_MGMT_NUMBER').split(',')
SMS_IMG = os.getenv('SMS_IMG')
SMS_IMG_URL = os.getenv('SMS_IMG_URL')



