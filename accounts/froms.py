# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(max_length=25,
                               widget=forms.TextInput(attrs={
                                                                'class': 'form-control form-control-lg',
                                                                'id': 'username',
                                                                'type': 'text',
                                                                'placeholder': 'Enter User Name',
                                                            }
                                                    )
                            )

    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                    'class': 'form-control form-control-lg',
                                                                    'id': 'password',
                                                                    'placeholder': 'Enter Password',
                                                                }

                                                          )
                               )