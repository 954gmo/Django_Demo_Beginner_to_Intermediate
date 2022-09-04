# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.shortcuts import render

from .dashboard import DashboardMixin
from sites.models import CustomerActivities, Customer, OperatorActivities, Operator
from .. import sig_utils


class ViewOperatorActivities(LoginRequiredMixin, DashboardMixin, ListView):
    login_url = 'login'
    template_name = 'sites/operator_activities.html'

    model = OperatorActivities

    context_object_name = 'operators'
    paginate_by = settings.ENTRIES_PER_PAGE
    object_list = model.objects.all()

    def __init__(self):
        self.get_action = {
            'search': self.search,
            'export': self.export,
        }

    def get_context_data(self, **kwargs):
        if self.request.user.user_type == 'store_manager':
            self.object_list = self.model.objects.filter(store=self.request.user.store)
        elif self.request.user.user_type == 'operator':
            self.object_list = self.model.objects.operator_view(Operator.objects.get(username=self.request.user))

        context = super(ViewOperatorActivities, self).get_context_data(**kwargs)

        self.pagination_context(context, len(self.object_list))

        return context

    def export(self):
        fields = ['operator__username', 'log_time', 'activities', 'operator__store']
        return sig_utils.export(request=self.request, data_set=self.object_list,
                                fields=fields, file='operator_activities', obj='operator_activities')

    def search(self):
        if self.request.user.user_type == 'operator':
            data_set = CustomerActivities.objects.operator_view(Operator.objects.get(username=self.request.user))
        else:
            data_set = CustomerActivities.objects
        res = sig_utils.searching_result(self.request, data_set, 'operator_activities')
        context = {}
        sig_utils.pagination(request=self.request, data_list=res.order_by('-last_check_in'),
                             context=context, context_obj='operators')
        html = render_to_string('sites/operator_activities_search_result.html', context)
        return HttpResponse(html)