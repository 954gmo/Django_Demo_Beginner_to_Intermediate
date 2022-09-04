# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import sys

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.conf import settings

from accounts.models import Operator
from sites.models import Store
from .dashboard import DashboardMixin
from ..forms import AddUserForm


import logging
err_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class MgmtOperator(LoginRequiredMixin, DashboardMixin, ListView):
    login_url = 'login'
    template_name = 'sites/operator.html'

    model = Operator

    context_object_name = 'operators'
    paginate_by = settings.ENTRIES_PER_PAGE
    object_list = model.objects.all()

    def __init__(self):
        self.get_action = {
            'add': self.add_op,
            'edit': self.edit,
        }

        self.post_action = {
            'add': self.add_op,
            'save': self.save,
            'change_password': self.change_password,
        }

    def get_context_data(self, **kwargs):
        # operator have no permission to these information
        # if user is store manager, display store_manager and operators of the store only
        # if user is admin, display all operators, including all store_manager, all operators at different store
        # otherwise, user is superuser, display all users

        if self.request.user.user_type == 'store_manager':
            self.object_list = self.object_list.filter(
                store=self.request.user.store).filter(user_type__in=['store_manager', 'operator'])
        elif self.request.user.user_type == 'admin':
            self.object_list = self.object_list.filter(user_type__in=['store_manager', 'admin', 'operator'])

        context = super(MgmtOperator, self).get_context_data(**kwargs)

        self.pagination_context(context, len(self.object_list))

        return context

    def add_op(self):
        try:
            # dynamically check if user exists before submission
            if n := self.request.GET.get('n', None):
                r = self.model.objects.filter(username=n)
                if r.count():
                    return JsonResponse({'status': 201})
                else:
                    return JsonResponse({'status': 200})

            # handle submission
            if self.request.method == 'POST':
                form = AddUserForm(self.request.POST)
                if form.is_valid():
                    # commit=False, means we don't want to save the form yet,
                    # we need to make some changes to the forms value before saving
                    # this model form to database
                    user = form.save(commit=False)
                    user.set_password(
                        form.cleaned_data['password']
                    )
                    user.save()
                    Token.objects.create(user=user)
                    messages.success(self.request, message="New User Added!")

                    return render(self.request, 'sites/operator_add_done.html')

            # display an empty form
            form = AddUserForm()

            if self.request.user.user_type != 'superuser':
                #
                # create a form for adding User/Operator
                #
                # superuser can add admin, store_manager, operators
                # admin can add store_manager, operators for all stores
                # store_manger can add operators for his/her store
                # operators have no permission to this function
                #

                roles = {
                    'admin': Operator.USER_TYPES[0:2],
                    'store_manager': [Operator.USER_TYPES[0], ],
                }
                # dict compression for the stores
                store_dic = {i[0]: i[1] for i in Store.STORES}
                stores = {
                    'admin': Store.STORES,
                    'store_manager': [(self.request.user.store, store_dic[self.request.user.store])]
                }

                form.fields['user_type'].choices = roles.get(self.request.user.user_type)
                form.fields['store'].choices = stores.get(self.request.user.user_type)

            return render(self.request, 'sites/operator_add.html', {'form': form})
        except Exception as e:
            err_logger.error(e, exc_info=sys.exc_info())

    def edit(self):
        context = {}
        try:
            context['operator'] = self.model.objects.get(id=self.request.GET.get('id', None))
            if self.request.user.user_type == 'admin' or self.request.user.user_type == 'superuser':
                context['admin_enabled'] = True
        except ObjectDoesNotExist:
            return render(self.request, 'sites/operator_edit.html',
                          context={'no_exist': True, 'pk': self.request.GET.get('id', None)})

        return render(self.request, 'sites/operator_edit.html', context=context)

    def save(self):
        try:
            r = self.model.objects.get(id=self.request.POST.get('id'))
            if r.first_name != self.request.POST.get('first_name'):
                r.first_name = self.request.POST.get('first_name')
                r.save(update_fields=['first_name'])

            if r.last_name != self.request.POST.get('last_name'):
                r.last_name = self.request.POST.get('last_name')
                r.save(update_fields=['last_name'])

            if r.email != self.request.POST.get('email'):
                r.email = self.request.POST.get('email')
                r.save(update_fields=['email'])

            if r.user_type != self.request.POST.get('user_type'):
                r.user_type = self.request.POST.get('user_type')
                r.save(update_fields=['user_type'])

            is_acitve = False if self.request.POST.get('is_active') == 'false' else True
            if r.is_active != is_acitve:
                r.is_active = is_acitve
                r.save(update_fields=['is_active'])

        except Exception as e:
            err_logger.error(e, exc_info=sys.exc_info())
            return JsonResponse({'status': 205})

        return JsonResponse({'status': 200})

    def change_password(self):
        op = self.model.objects.get(id=self.request.POST.get('id'))
        op.set_password(self.request.POST.get('new'))
        op.save()
        t = Token.objects.filter(user=op)
        n = t[0].generate_key()
        t.update(key=n)

        return JsonResponse({'status': 200})
