# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django.urls import path
from .views import Dashboard, MgmtCustomers, MgmtOperator, ViewOperatorActivities, ViewCustomerActivities
urlpatterns = [
    path('', Dashboard.as_view(), name='index'),

    path('customer/', MgmtCustomers.as_view(), name='customer'),
    path('customer/<str:action>', MgmtCustomers.as_view(), name='customer_actions'),

    path('activities/', ViewCustomerActivities.as_view(), name='customer_activities'),
    path('activities/<str:action>', ViewCustomerActivities.as_view(), name='customer_activities_actions'),

    path('operator/', MgmtOperator.as_view(), name='operator'),
    path('operator/<str:action>', MgmtOperator.as_view(), name='operator_actions'),

    path('op_activities/', ViewOperatorActivities.as_view(), name='operator_activities'),
    path('op_activities/<str:action>', ViewOperatorActivities.as_view(), name='operator_activities_actions'),
]
