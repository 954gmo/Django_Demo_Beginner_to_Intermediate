# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"


from ..froms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, template_name='sites/dashboard.html', context={})
                else:
                    return render(request, template_name='accounts/login.html',
                                  context={'msg': 'Please enter correct username and password'})
            else:
                return render(request, template_name='accounts/login.html',
                              context={
                                  'msg': 'Please enter correct username and password',
                                  'form': form})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
