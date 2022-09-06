# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django import forms
from blog.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        # indicate which model to use to build the form
        # Django introspects the model and builds the form dynamically for you.
        model = Comment
        # by default, Django builds a form field for each field contained in the model
        # you can explicitly tell Django which fields you want to include in your form
        # using a fields list
        fields = ('name', 'email', 'body', )


class SearchForm(forms.Form):
    query = forms.CharField()