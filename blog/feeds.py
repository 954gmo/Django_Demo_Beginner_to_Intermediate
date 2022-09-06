# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

#
# Django has a built-in syndication feed framework that you can use to
# dynamically generate RSS or Atom feeds in a similar manner to creating
# sitemaps using the site's framework

# a web fee is a data format(usually XML) that provides users with
# the most recently updated content.
# Users will be able to subscribe to your feed using a feed aggregator

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from blog.models import Post


class LatestPostsFeed(Feed):
    title = 'Blog'
    link = reverse_lazy('blog:post_list')
    description = "New Posts of Blog"

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)

