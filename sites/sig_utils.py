# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import re
import pytz
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator
import datetime
from django.db.models import Q
from django.http import HttpResponse
import csv
import os
from sites import MSG
import time
from random import seed
import random
import twilio
import logging
import unicodedata

from sites.models import Store

info_logger = logging.getLogger('info')
err_logger = logging.getLogger('error')
msg_logger = logging.getLogger('message_sender')


def url_action(path_info):
    pat = re.compile(r'/(\w+)\?')
    res = pat.search(path_info)
    if res:
        return res.group(1)
    res = path_info.rsplit('/', 1)[-1]
    if res:
        return res
    return 'default'


def url_action(path_info):
    pat = re.compile(r'/(\w+)\?')
    res = pat.search(path_info)
    if res:
        return res.group(1)
    res = path_info.rsplit('/', 1)[-1]
    if res:
        return res
    return 'default'


def searching_result(request, data_set, obj):
    if request.method == 'GET':
        q = request.GET.get('q', None)
        f = request.GET.get('f', None)
        t = request.GET.get('t', None)
        s = request.GET.get('s', None)
        st = request.GET.get('st', None)
    elif request.method == 'POST':
        q = request.POST.get('q', None)
        f = request.POST.get('f', None)
        t = request.POST.get('t', None)
        s = request.POST.get('s', None)
        st = request.POST.get('st', None)

    dt_fmt = '%Y-%m-%d'
    utc = pytz.timezone('UTC')
    local_timezone = pytz.timezone(timezone.get_current_timezone().key)

    res = data_set
    if s:
        res = res.filter(store__in=Store.objects.filter(name__in=s.split(',')))  # all
    if q:
        if obj == 'customer_info':
            res = res.filter(Q(first_name__icontains=q) | Q(phone__icontains=q))
        elif obj == 'customer_activities':
            res = res.filter(Q(customer__first_name__icontains=q) | Q(customer__phone__icontains=q))
        elif obj == 'operator_activities':
            res = res.filter(operator__username__icontains=q)
    if f:
        f = local_timezone.localize(datetime.datetime.strptime(f, dt_fmt))
        f = f.astimezone(utc)
        if obj == 'customer_activities':
            res = res.filter(check_in_time__gte=f)
        if obj == 'customer_info':
            res = res.filter(last_check_in__gte=f)
        if obj == 'operator_activities':
            res = res.filter(log_time__gte=f)
    if t:
        t = local_timezone.localize(datetime.datetime.strptime(t, dt_fmt))
        t = t.astimezone(utc)
        if obj == 'customer_activities':
            res = res.filter(check_in_time__lte=t)
        if obj == 'customer_info':
            res = res.filter(last_check_in__lte=t)
        if obj == 'operator_activitiies':
            res = res.filter(log_time__lte=t)
    if st:
        res = res.filter(shift__in=st.split(','))

    return res


def pagination(request, data_list, context, context_obj):
    """
    :param request:
    :param data_list:
    :param context:
    :param context_obj: customers, operators
    :return:
    """
    paginator = Paginator(data_list, settings.ENTRIES_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(request.GET.get('page', 1))
    context['page_obj'] = page_obj
    context[context_obj] = page_obj
    context['is_paginated'] = True
    context['urlencode'] = request.GET.urlencode
    if paginator.count:
        context['total'] = paginator.count
    else:
        context['total'] = len(data_list)


def export(request, data_set, fields, file, obj):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f"attachment; filename={datetime.datetime.now().strftime('%m_%d_%Y')}_{file}.csv"}
    )
    ids = request.GET.get('ids', None)
    writer = csv.DictWriter(response, fields)
    writer.writeheader()
    if ids:
        # handle selected export
        rows = data_set.filter(id__in=ids.split(','))
    else:
        rows = searching_result(request, data_set, obj)

    for row in rows.values(*fields):
        # mgmt_customer_info, view_customer_activities
        if obj == 'customer_activities':
            row['check_in_time'] = row['check_in_time'].astimezone(timezone.get_current_timezone())
        if obj == 'customer_info':
            row['last_check_in'] = row['last_check_in'].astimezone(timezone.get_current_timezone())
            row['since'] = row['since'].astimezone(timezone.get_current_timezone())
        if obj == 'operator_activities':
            row['log_time'] = row['log_time'].astimezone(timezone.get_current_timezone())
        writer.writerow(row)

    return response


def msg_sender(rows, msg, img_files):
    msg_counter = {'current_id': 0, 'total': len(rows), 'sent': 1}
    img_urls = []
    for img in img_files:
        img_urls.append(os.path.join(settings.SMS_IMG_URL, img))

    for phone in settings.SMS_MGMT_NUMBER:
        MSG.send_msg(phone, 'System started Sending Messages to customers', img_urls)

    msg_logger.info(f'System started sending messages to customers: {msg_counter["total"]}')

    morning = datetime.time(hour=9, minute=30)
    evening = datetime.time(hour=20, minute=30)
    morning_sec = morning.hour * 3600 + morning.minute * 60
    evening_sec = evening.hour * 3600 + evening.minute * 60
    duration = evening_sec - morning_sec
    one_day = 24 * 3600
    idle_duration = one_day - duration

    for row in rows:
        msg_counter['current_id'] = row.id
        cur_time = datetime.datetime.now().time()
        cur_sec = cur_time.hour * 3600 + cur_time.minute * 60 + cur_time.second

        if (cur_time < morning) or (cur_time > evening):
            MSG.send_msg(settings.SMS_ADMIN_NUMBER, f"Long sleeping sending message at id:{row.id} ")
            if cur_time < morning:
                sleep_duration = morning_sec - cur_sec
            elif cur_time > evening:
                sleep_duration = idle_duration - cur_time + evening_sec
            hr = sleep_duration % 3600
            minute = (sleep_duration - hr * 3600) / 60
            msg_logger.info(f'long pause sending message at id: {row.id} for {hr} hours, {minute} minutes')
            time.sleep(sleep_duration)
            msg_logger.info(f'starting sending message again at id : {row.id}')
            MSG.send_msg(settings.SMS_ADMIN_NUMBER, f"start sending message again at id: {row.id}")

        if msg_counter['sent'] % 10 == 0:
            seed(datetime.datetime.now())
            t = random.randint(1, 5)
            msg_logger.info("pause every 10 entries for {0} minutes".format(t))
            time.sleep(t * 60)

        # start sending msg
        content = f"Hello {row.first_name} {row.last_name} {msg}"
        try:
            MSG.send_msg(row.phone, content, img_urls)
            msg_logger.info(f" #{msg_counter} : msg sent to {row.phone}")
            msg_counter['sent'] += 1
            seed(datetime.datetime.now())
            start = random.randint(5, 15)
            end = random.randint(35, 45)
            t = random.randint(start, end)
            time.sleep(t)

        except twilio.base.exceptions.TwilioRestException as e:
            err_logger.info(f"exception occur when sending to  cust_id: {row.id}, phone: {row.phone}\n {e}")
            MSG.send_msg(settings.SMS_ADMIN_NUMBER,
                         f"check the scripts and log, exceptions happened:: customer_id: {row.id}; phone#: {row.phone}")

    msg_logger.info("finished sending msg")
    for phone in settings.SMS_MGMT_NUMBER:
        MSG.send_msg(phone, 'Finished sending text messages customers')


def clean_filename(filename):
    file, ext = os.path.splitext(filename.lower())
    file = unicodedata.normalize('NFKD', file).encode('ascii', 'ignore').decode('ascii')
    file = re.sub(r'[^\w\s-]', '', file)
    file = re.sub(r'[-\s]+', '', file)
    return file + ext