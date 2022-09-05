# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django.conf import settings

if settings.DASHBOARD:
    from . import dashboard_sample_data
if settings.BLOG:
    from . import blog_sample_data