# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def sites_url(value, field_name, url_encode=None):
    url = f'?{field_name}={value}'
    if url_encode:
        query_str = url_encode.split('&')
        filtered_query_str = filter(lambda p: p.split('=')[0] != field_name, query_str)
        encoded_query_str = '&'.join(filtered_query_str)
        url = f'{url}&{encoded_query_str}'
    return url


@register.simple_tag
def ajax_pagination_url(page, url_encode=None):
    url = f'search?page={page}'
    if url_encode:
        query_str = url_encode.split('&')
        filtered_query_str = filter(lambda p: p.split('=')[0] != 'page', query_str)
        encoded_query_str = '&'.join(filtered_query_str)
        url = f'{url}&{encoded_query_str}'
    return url


@register.filter
def status(t):
    return 'Active' if t else 'Inactive'

@register.filter
def shifts(shift):
    return settings.SHIFTS.get(shift)
