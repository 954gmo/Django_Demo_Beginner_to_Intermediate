# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import datetime
import logging
import os
import threading

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render
from django.conf import settings

from ..models import Customer, Store, CustomerActivationLog
from .dashboard import DashboardMixin
from ..forms import CustomerActivationForm
from sites import sig_utils
import sites.qrcode_util as QR
from sites.MSG import MSG
err_logger = logging.getLogger('error')
msg_logger = logging.getLogger('message_sender')


class MgmtCustomers(LoginRequiredMixin, DashboardMixin, ListView):
    login_url = 'login'
    template_name = 'sites/customer.html'

    model = Customer

    context_object_name = 'customers'
    paginate_by = settings.ENTRIES_PER_PAGE
    object_list = model.objects.all().filter(enabled=True)

    def __init__(self):
        self.get_action = {
            'search': self.search,
            'export': self.export,
            'edit': self.edit,
        }
        self.post_action = {
            'send_msg': self.send_msg,
            'del': self.disable_customer,
            'save': self.save_customer,
        }

    def get_context_data(self, **kwargs):
        context = super(MgmtCustomers, self).get_context_data(**kwargs)

        if self.request.user.user_type in ['admin', 'superuser']:
            context['msg_enabled'] = True
            context['store_enabled'] = True
            context['stores'] = Store.objects.all()

        self.pagination_context(context, len(self.object_list))

        return context

    def edit(self):
        # display customer profile if exist
        # otherwise show info "not exist"
        template = 'sites/customer_edit.html'

        context = self.get_context_data()
        try:
            customer_id = self.request.GET.get('id', None)
            customer = Customer.objects.get(id=customer_id)
            context['customer'] = customer
            context['img'] = customer.qr_code
            context['disable'] = CustomerActivationForm()
            context['disable_history'] = CustomerActivationLog.objects.filter(
                customer_id=customer_id).order_by('-log_time')
            if customer.expiration_date:
                context['status'] = f"Customer is disabled until {timezone.localtime(customer.expiration_date).strftime('%m/%d/%Y %H:%M:%S')}"
            else:
                context['status'] = 'Customer is active'
        except ObjectDoesNotExist:
            return render(self.request, template,
                          context={'no_exist': True, 'pk': self.request.GET.get('id', None)})
        return render(self.request, template, context=context)

    def disable_customer(self):
        try:
            id = self.request.POST.get('id')
            self.admin_log(msg=serializers.serialize('jsonl', [self.model.objects.get(id=id)])).save()
            customer = Customer.objects.get(id=id)
            # QRCODE = os.path.join(settings.QR_CODE, customer.qr_code + '.png')
            # IMG = os.path.join(settings.CUSTOMER_IMG, customer.qr_code + '.jpg')
            # ID = os.path.join(settings.CUSTOMER_ID, customer.qr_code + '.jpg')

            # if os.path.exists(QRCODE):
            #     os.remove(QRCODE)
            #
            # if os.path.exists(IMG):
            #     os.remove(IMG)
            #
            # if os.path.exists(ID):
            #     os.remove(ID)
            customer.enabled = False
            customer.save(update_fields=['enabled'])

            return JsonResponse({'status': 200})
        except Exception as e:
            err_logger(e)
            return JsonResponse({'status': 205})

    def save_customer(self):
        """
            after editing customer profile,
            if there any change to the first name, last name, and phone number
                update the field that changed,
                generate a new QR code,
                message the customer with the new QR code
                delete the old QR code,
                rename the customer img and ID with the new QR code
                update customerinfo with new qr_code
            update the qr_code in the customerinfo;
        :return:
        """
        try:
            first_name = self.request.POST.get('first_name')
            last_name = self.request.POST.get('last_name')
            phone = self.request.POST.get('phone')
            msg = self.request.POST.get('msg', None)
            periods = self.request.POST.get('periods', None)
            customer_id = self.request.POST.get('id', None)

            r = Customer.objects.get(id=customer_id)

            utc = pytz.timezone('UTC')
            if periods:
                if periods == '0':
                    r.expiration_date = None
                    r.save(update_fields=['expiration_date'])
                    CustomerActivationLog.objects.create(customer=customer_id,
                                                            log_time=datetime.datetime.now().astimezone(utc),
                                                            expiration_date=None,
                                                            reason=msg)
                    MSG.send_msg(phone,
                                 f'Hi, {first_name} {last_name}, your account is activated')
                elif periods == '1':
                    expiration = datetime.datetime(2200, 12, 20, 0, 0, 0, tzinfo=utc)
                    r.expiration_date = expiration
                    r.save(update_fields=['expiration_date'])
                    CustomerActivationLog.objects.create(customer=customer_id,
                                                            log_time=datetime.datetime.now().astimezone(utc),
                                                            expiration_date=r.expiration_date,
                                                            reason=msg)
                    MSG.send_msg(phone,
                                 f'Hi, {first_name} {last_name}, your account is deactivated for the reason of {msg}')

                else:
                    expiration = datetime.datetime.now() + datetime.timedelta(days=int(periods))
                    r.expiration_date = expiration.astimezone(utc)
                    r.save(update_fields=['expiration_date'])
                    CustomerActivationLog.objects.create(customer=customer_id,
                                                            log_time=datetime.datetime.now().astimezone(utc),
                                                            expiration_date=r.expiration_date,
                                                            reason=msg)
                    MSG.send_msg(phone,
                                 f'Hi, {first_name} {last_name}, your account is deactivated until {r.expiration_date} for the reason of {msg}')

            qr = QR.qr_string(first_name, last_name, phone)

            # log dis-activation to CustomerDisactivationLog
            # add expiration date to self.customer_objs
            # send msg to customer "xxx, you are dis-activated for 'reason' until 'date'/'datetime'
            #
            if qr != r.qr_code:
                self.admin_log(action='save_customer',
                               msg=serializers.serialize('jsonl', [r, ])).save()

                if first_name != r.first_name:
                    r.first_name = first_name
                    r.save(update_fields=['first_name'])
                if last_name != r.last_name:
                    r.last_name = last_name
                    r.save(update_fields=['last_name'])
                if phone != r.phone:
                    r.phone = phone
                    r.save(update_fields=['phone'])

                # Send new QR code to customer
                body = f'Enjoy Your Day and Good Luck, {first_name} {last_name} ! Attached is your new QR code'
                # generate a new QR code
                img_path, new_qr_code = QR.generate_QRCODE(qr)
                qr_url = os.path.join(settings.QR_BASEURL, new_qr_code)
                img_files = [qr_url, settings.LOGO_URL]
                # message the new QR code to customer
                t = threading.Thread(target=MSG.send_msg_with_img, args=[phone, body, img_files], daemon=True)
                t.start()
                # remove the old QR code
                QRCODE = os.path.join(settings.QR_CODE, r.qr_code + '.png')
                IMG = os.path.join(settings.CUSTOMER_IMG, r.qr_code + '.jpg')
                ID = os.path.join(settings.CUSTOMER_ID, r.qr_code + '.jpg')
                if os.path.exists(QRCODE):
                    os.remove(QRCODE)
                # change IMG and ID name to new qr_code
                if os.path.exists(IMG):
                    os.rename(IMG, os.path.join(settings.CUSTOMER_IMG, qr + '.jpg'))
                if os.path.exists(ID):
                    os.rename(ID, os.path.join(settings.CUSTOMER_ID, qr + '.jpg'))
                # update customerinfo with new qr
                r.qr_code = qr
                r.save(update_fields=['qr_code'])
            return JsonResponse({'status': 200})

        except Exception as e:
            err_logger.error(e)
            return JsonResponse({'status': 205})

    def export(self):
        fields = ['id', 'first_name', 'last_name', 'phone', 'last_check_in', 'since']
        return sig_utils.export(request=self.request, data_set=self.object_list,
                                fields=fields, file='customer_info', obj='customer_info')

    def search(self):
        res = sig_utils.searching_result(self.request, self.object_list, 'customer_info')
        context = {}
        sig_utils.pagination(request=self.request, data_list=res.order_by('-last_check_in'),
                             context=context, context_obj='customers')
        html = render_to_string('sites/customer_search_result.html', context)
        return HttpResponse(html)

    def send_msg(self):
        msg = self.request.POST.get('msg')
        img_files = self.handle_upload_file()
        ids = self.request.POST.get('ids', None)

        if ids:
            rows = Customer.objects.filter(id__in=ids.split(','))
        else:
            rows = sig_utils.searching_result(self.request, Customer.objects, 'customer_info')

        if rows:
            t = threading.Thread(target=sig_utils.msg_sender,
                                 args=[rows.only('id', 'first_name', 'last_name', 'phone'), msg, img_files],
                                 daemon=True)
            t.start()

        data = [{'status': 200, 'msg': 'start sending message to selected customers'}]
        return JsonResponse(data, safe=False)

    def handle_upload_file(self):
        # clean the SMS_IMG dir
        for file in os.listdir(settings.SMS_IMG):
            os.remove(os.path.join(settings.SMS_IMG, file))
        # save new uploaded file to SMS_IMG dir
        fs = FileSystemStorage()
        files = []
        for file in self.request.FILES.getlist('files'):
            f = sig_utils.clean_filename(file.name)
            filename = os.path.join(settings.SMS_IMG, f)
            fs.save(filename, file)
            files.append(f)

        return files