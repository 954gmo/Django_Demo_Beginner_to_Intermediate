# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django import forms
from .models import Operator, CustomerActivationLog


class AddUserForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = (
            'username', 'first_name',
            'last_name', 'email', 'is_active',
            'store', 'user_type'
        )

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)


class CustomerActivationForm(forms.ModelForm):
    class Meta:
        model = CustomerActivationLog
        fields = '__all__'
        widgets = {
            'reason': forms.Textarea(
                attrs={'rows': 3,
                       'cols': 40,
                       'id': 'reason',
                       'class': 'form-control',
                       'placeholder': 'Reason for dis-activation'}),
            'periods': forms.Select(
                attrs={'id': 'periods', }
            )
        }

    PERIODS = (
        ('', 'Select a Period'),
        (1, 'De-activate'),
        (7, 'Seven Days'),
        (15, 'Fifteen Days'),
        (30, 'Thirty Days'),
        (0, 'Reactivate'),
    )
    periods = forms.ChoiceField(choices=PERIODS)
