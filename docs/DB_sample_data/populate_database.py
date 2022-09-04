# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import os

from django.conf import settings

from . import dashboard_sample_data

modules = {
    'dashboard': dashboard_sample_data,
}


def clean_migrations_and_database():
    # clean migrations and database
    acct_migrations = os.path.join(settings.BASE_DIR, 'accounts', 'migrations')
    sites_migrations = os.path.join(settings.BASE_DIR, 'sites', 'migrations')
    sqlite3_db = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    if os.path.exists(sqlite3_db):
        os.remove(sqlite3_db)

    for f in os.listdir(acct_migrations):
        if f.startswith('0'):
            p = os.path.join(acct_migrations, f)
            if os.path.exists(p):
                os.remove(p)

    for f in os.listdir(sites_migrations):
        if f.startswith('0'):
            p = os.path.join(sites_migrations, f)
            if os.path.exists(p):
                os.remove(p)


def makemigration_and_migrate():
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')


def populate_sample_database(demo):
    clean_migrations_and_database()
    makemigration_and_migrate()
    getattr(modules[demo], 'populate_database')()


if __name__ == "__main__":
    populate_sample_database('dashboard')