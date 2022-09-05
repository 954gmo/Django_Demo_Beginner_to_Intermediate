# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import os
from django.conf import settings
import docs

modules = {}

if settings.DASHBOARD:
    modules['dashboard'] = docs.DB_sample_data.dashboard_sample_data
if settings.BLOG:
    modules['blog'] = docs.DB_sample_data.blog_sample_data

apps = {
    'dashboard': ['accounts', 'api', 'sites'],
    'blog': ['blog', ]
}


def clean_migrations_and_database(demo):
    # clean migrations and database
    migrations = []
    for app in apps[demo]:
        migrations.append(os.path.join(settings.BASE_DIR, app, 'migrations'))

    sqlite3_db = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    if os.path.exists(sqlite3_db):
        os.remove(sqlite3_db)
        print(f'{sqlite3_db} removed')

    for m in migrations:
        for f in os.listdir(m):
            if f.startswith('0'):
                p = os.path.join(m, f)
                if os.path.exists(p):
                    os.remove(p)
                    print(f"{p} removed")


def makemigration_and_migrate(demo):
    print("start making migrations")
    os.system(f'python manage.py makemigrations {" ".join(apps[demo])}')
    print("start migration")
    os.system(f'python manage.py migrate')


def populate_sample_database(demo):
    if demo in modules:
        clean_migrations_and_database(demo)
        makemigration_and_migrate(demo)
        print("start populating database")
        getattr(modules[demo], 'populate_database')()
        print("finished populating database. ")
    else:
        print(f"No demo installed: {demo}")
    return


if __name__ == "__main__":
    # populate_sample_database('dashboard')
    pass