# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import importlib
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

apps = {
    'dashboard': ['accounts', 'api', 'sites'],
    'blog': ['blog', ]
}


def clean_migrations(demo):
    # clean migrations and database
    migrations = []
    for app in apps[demo]:
        migrations.append(os.path.join(BASE_DIR, app, 'migrations'))

    for m in migrations:
        for f in os.listdir(m):
            if f.startswith('0'):
                p = os.path.join(m, f)
                if os.path.exists(p):
                    os.remove(p)
                    print(f"{p} removed")


def clean_database(demo):
    sqlite3_db = os.path.join(BASE_DIR, 'config', demo, 'db.sqlite3')
    if os.path.exists(sqlite3_db):
        os.remove(sqlite3_db)
        print(f'{sqlite3_db} removed')


def clean_migrations_and_database(demo):
    clean_migrations(demo)
    clean_database(demo)


def makemigration_and_migrate(demo):
    print("start making migrations")
    os.system(f'python manage.py makemigrations {" ".join(apps[demo])}')
    print("start migration")
    os.system(f'python manage.py migrate')


def populate_sample_database(demo):
    try:
        modules = importlib.import_module('docs.DB_sample_data.' + demo)
        clean_migrations_and_database(demo)
        makemigration_and_migrate(demo)
        print("start populating database")

        getattr(modules, 'populate_database')()
        print("finished populating database. ")
    except Exception as e :
        print(e)
        # print(f"No demo installed: {demo}")

    return


if __name__ == "__main__":
    pass