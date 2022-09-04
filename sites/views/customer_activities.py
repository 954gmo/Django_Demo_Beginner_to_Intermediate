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
from sites.models import CustomerActivities, Customer, Store, Operator
from .. import sig_utils


class ViewCustomerActivities(LoginRequiredMixin, DashboardMixin, ListView):
    login_url = 'login'
    template_name = 'sites/customer_activities.html'

    model = CustomerActivities

    context_object_name = 'customers'
    paginate_by = settings.ENTRIES_PER_PAGE
    object_list = model.objects.all()

    def __init__(self):
        self.get_action = {
            'search': self.search,
            'export': self.export,
        }

    def get_context_data(self, **kwargs):
        if self.request.user.user_type == 'store_manager':
            self.object_list = self.object_list.filter(store=self.request.user.store)
        elif self.request.user.user_type == 'operator':
            self.object_list = self.model.objects.operator_view(Operator.objects.get(username=self.request.user))

        context = super(ViewCustomerActivities, self).get_context_data(**kwargs)

        if self.request.user.user_type == 'admin' or self.request.user.user_type == 'superuser':
            context['store_enabled'] = True
            context['stores'] = Store.objects.all()

        context['shift_enabled'] = True
        context['shifts'] = settings.SHIFTS

        self.pagination_context(context, len(self.object_list))

        return context

    def export(self):
        fields = ['customer__first_name', 'customer__last_name', 'customer__phone',
                  'check_in_time', 'shift', 'operator__username', 'store__name']
        return sig_utils.export(request=self.request, data_set=CustomerActivities.objects,
                                fields=fields, file='customer_activities', obj='customer_activities')

    def search(self):

        if self.request.user.user_type == 'operator':
            data_set = CustomerActivities.objects.operator_view(Operator.objects.get(username=self.request.user))
        else:
            data_set = CustomerActivities.objects

        res = sig_utils.searching_result(self.request, data_set, 'customer_activities')
        context = {}
        sig_utils.pagination(request=self.request, data_list=res.order_by('-check_in_time'),
                             context=context, context_obj='customers')
        html = render_to_string('sites/customer_activities_search_result.html', context)
        return HttpResponse(html)