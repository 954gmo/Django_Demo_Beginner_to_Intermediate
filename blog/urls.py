# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django.urls import path
from blog.views import post
from blog.feeds import LatestPostsFeed

# application namespace
# this allows you to organize URLs by application and use the name when referring to them
# the application namespace can be set in two ways
# 1. in `urls.py` using `app_name` as here does,
#       Django will use this  `app_name` as the application namespace
#       only if we are included the patterns with module reference.
# 2. in `include(pattern, app_namespace

app_name = 'blog'

urlpatterns = [
    path('', post.post_list, name='post_list'),
    # path('', post.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', post.post_list, name='post_list_by_tag'),
    # use angle brackets to capture the values from the URL
    # any value specified in the URL patterns as <param> is captured as a string
    # you use path converters, such as <int:year>, to specifically match and return an integer
    # https://docs.djangoproject.com/en/4.1/topics/http/urls/#path-converters
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', post.post_detail, name='post_detail'),
    path('<int:post_id>/share/', post.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', post.post_search, name='post_search'),
]