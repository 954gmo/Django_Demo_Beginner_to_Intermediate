# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import os
from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-caebb+zs_ai6pc5g-kb&jlt626l4sgi*fjwhn5k8+9)vlznx+mg9ubl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

QR_CODE = os.getenv('QR_CODE')
CUSTOMER_IMG = os.getenv('CUSTOMER_IMG')
CUSTOMER_ID = os.getenv('CUSTOMER_ID')

LOGO_URL = os.getenv('LOGO_URL')
QR_BASEURL = os.getenv('QR_BASEURL')
IMG_BASEURL = os.getenv('IMG_BASEURL')

# SMS_ACCT = os.getenv('SMS_ACCT')
# SMS_TOKEN = os.getenv('SMS_TOKEN')
SMS_ACCT = 'lksjdklf'
SMS_TOKEN = 'sjdlkfjsad'
SMS_FROM_NUMBER = os.getenv('SMS_FROM_NUMBER')
SMS_ADMIN_NUMBER = os.getenv('SMS_ADMIN_NUMBER')
SMS_MGMT_NUMBER = os.getenv('SMS_MGMT_NUMBER', '').split(',')
SMS_IMG = os.getenv('SMS_IMG')
SMS_IMG_URL = os.getenv('SMS_IMG_URL')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
