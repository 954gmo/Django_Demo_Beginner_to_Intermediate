# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'sites/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class DashboardMixin:

    def pagination_context(self, context, total):

        if not context.get('is_paginated', False):
            context['total'] = total
            return context

        paginator = context.get('paginator')
        page_obj = paginator.get_page(self.request.GET.get('page', 1))
        page_obj.adjusted_elided_pages = paginator.get_elided_page_range(self.request.GET.get('page', 1))
        context['page_obj'] = page_obj
        context['total'] = paginator.count

    def get(self, request, *args, **kwargs):
        action = kwargs.get('action', 'default')
        return self.get_action.get(action, self.default)()

    def post(self, request, *args, **kwargs):
        action = kwargs.get('action', 'default')
        return self.post_action.get(action, self.default)()

    def default(self):
        context = self.get_context_data()
        return render(request=self.request, template_name=self.template_name,
                      context=context)
