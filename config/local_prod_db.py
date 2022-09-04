# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import configparser
import os
from django.conf import settings

config = configparser.ConfigParser()
config.read(os.path.join(settings.BASE_DIR, 'config/config.ini'))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['KEY']['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'SITES_APP': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config['DATABASE']['DB_NAME'],
        'USER': config['DATABASE']['DB_USER'],
        'PASSWORD': config['DATABASE']['DB_PASS'],
        'HOST': config['DATABASE']['DB_HOST'],
        'PORT': config['DATABASE']['DB_PORT'],
    }
}

QR_CODE = config['SITES_APP']['QR_CODE']
CUSTOMER_IMG = config['SITES_APP']['CUSTOMER_IMG']
CUSTOMER_ID = config['SITES_APP']['CUSTOMER_ID']

LOGO_URL = config['SITES_APP']['LOGO_URL']
QR_BASEURL = config['SITES_APP']['QR_BASEURL']
IMG_BASEURL = config['SITES_APP']['IMG_BASEURL']

SMS_ACCT = config['SITES_APP']['SMS_ACCT']
SMS_TOKEN = config['SITES_APP']['SMS_TOKEN']
SMS_FROM_NUMBER = config['SITES_APP']['SMS_FROM_NUMBER']
SMS_ADMIN_NUMBER = config['SITES_APP']['SMS_ADMIN_NUMBER']
SMS_MGMT_NUMBER = config['SITES_APP']['SMS_MGMT_NUMBER'].split(',')
SMS_IMG = config['SITES_APP']['SMS_IMG']
SMS_IMG_URL = config['SITES_APP']['SMS_IMG_URL']

LOG_DIR = config['SITES_APP']['LOG_DIR']


