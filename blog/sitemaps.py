# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django.contrib.sitemaps import Sitemap
from blog.models import Post


#
# create a custom sitemap by inheriting the Sitemap class of the sitemaps module
#
class PostSitemap(Sitemap):
    change_freq = 'monthly'
    priority = 0.7

    def items(self):
        return Post.published.all()

    # receives each object returned by items() and returns the last time
    # the object was modified.
    def lastmod(self, obj):
        return obj.updated