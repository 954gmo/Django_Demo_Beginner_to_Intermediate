# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def sample(demo, name):
    globals()[f'dir_{demo}'](name)


def dir_content(folder):
    res = os.listdir(os.path.join(BASE_DIR, folder))
    for f in res:
        print(f"`{f}` : \n")


if __name__ == "__main__":
    # locals()['dir_content']('config')
    # globals()['dir_content']('api')
    sample('content', 'Django')

