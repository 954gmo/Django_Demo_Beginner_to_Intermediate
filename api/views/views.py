import json
import os
import datetime

import pytz
from django.conf import settings

import PIL.Image as Image

import twilio.base.exceptions
from django.utils import timezone

from rest_framework.decorators import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from sites.models import Customer, CustomerActivities, OperatorActivities

import sites.qrcode_util as QR
from sites.MSG import MSG

import logging
err_logger = logging.getLogger('error')
logger = logging.getLogger('info')


class Operators(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, )

    def __init__(self):
        self.reqs = {
            'NC': self.handle_new_customer,
            'LF': self.handle_lost_and_found,
            'CK': self.check_in_existing_customer,
            'VQR': self.validate_customer,
        }

    def post(self, request):
        return self.reqs[request.data['req_type']]()

    def handle_new_customer(self):
        """
            handle request of registering new customer
            :return:
                    302 if customer already exists
                    200 registered new customer successfully
                    406 failed to send text message, because the phone#
                    409 other kind of exception raised, need to check info.log
        """
        try:
            op = Token.objects.get(key=self.request.headers.get('Authorization').split()[1]).user
            first_name = self.request.data['first_name']
            last_name = self.request.data['last_name']
            phone = self.request.data['number']
            qr = QR.qr_string(first_name, last_name, phone)

            # if customer already exists.
            if Customer.objects.filter(qr_code=qr):
                logger.info(f"operator: {op}"
                            f"::customer already exists: {first_name}-{last_name}-{phone}")
                return Response(status=status.HTTP_302_FOUND)
            #
            # register new customer
            #

            # save customer real person image, for in-person validation when customer check in
            cust_img_path = os.path.join(settings.CUSTOMER_IMG, qr + ".jpg")
            image = self.request.FILES['cust_img']
            img = Image.open(image)
            img.save(cust_img_path)
            logger.info(f"saved {cust_img_path}  size: {os.path.getsize(cust_img_path) / (1024 * 1024.0):.2f} MB")
            # save customer ID image, store for future use
            cust_id_path = os.path.join(settings.CUSTOMER_ID, qr + ".jpg")
            image = self.request.FILES['cust_id']
            img = Image.open(image)
            img.save(cust_id_path)
            logger.info(f"saved {cust_id_path} size: {os.path.getsize(cust_id_path) / (1024 * 1024.0):.2f} MB")
            # SMS QR code to customer
            qr_img_path, img_name = QR.generate_QRCODE(qr)
            img_url = [os.path.join(settings.QR_BASEURL, img_name), settings.LOGO_URL]
            MSG.send_msg(phone, f"Enjoy your Day and Good Luck, {first_name} {last_name} !", img_url)
            # save customer information to database
            Customer(operator_id=op.id, first_name=first_name, last_name=last_name,
                         phone=phone, qr_code=qr, store=op.store).save()
            logger.info("CustomerInfo saved to database")
            self.log_op_activities(activity="Registered New Customer: ", op=op)

            customer_info = Customer.objects.get(qr_code=qr)
            CustomerActivities(customer_id=customer_info.id, check_in_time=customer_info.last_check_in,
                               operator_id=op.id,
                               shift=self.shift(customer_info.last_check_in), store=op.store).save()
            logger.info("Customer Activities saved to database ")
            return Response(status=status.HTTP_200_OK)
        except twilio.base.exceptions.TwilioException:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def shift(self, check_in_time):
        """
        determine what shift it belongs to
        :param check_in_time:
        :return: shift string
        """
        zero = datetime.time(0, 0, 0)
        shift_A = datetime.time(8, 59, 59)
        shift_B = datetime.time(15, 59, 59)
        shift_C = datetime.time(23, 59, 59)

        t = timezone.localtime(check_in_time + timezone.localtime(check_in_time).dst()).time()
        if zero <= t <= shift_A:
            return settings.SHIFTS['shift_a']
        elif shift_A < t <= shift_B:
            return settings.SHIFTS['shift_b']
        elif shift_B < t <= shift_C:
            return settings.SHIFTS['shift_c']

    def log_op_activities(self, activity, op):
        """
        log operator activities
        :param activity:
        :param op:
        :return:
        """
        activities = activity + " " + self.request.data['first_name'] + " " + self.request.data['last_name'] + " " + self.request.data[
            'number']
        OperatorActivities(operator_id=op.id, activities=activities).save()

    def handle_lost_and_found(self):
        try:
            first_name = self.request.data['first_name']
            last_name = self.request.data['last_name']
            phone = self.request.data['number']

            if self.is_valid_customer(first_name, last_name, phone):
                qr = QR.qr_string(first_name, last_name, phone)
                qr_img_url = settings.QR_BASEURL + qr + ".png"
                MSG.send_msg(phone, f"Hello {first_name} {last_name}! Attached is your QR code", qr_img_url)
                op = Token.objects.get(key=self.request.headers.get('Authorization').split()[1]).user
                self.log_op_activities(op=op, activity="Lost and Found for ")
                logger.info("SMS QR to customer")
                return Response(status=status.HTTP_200_OK)

            logger.info("customer not found")
            return Response(status.HTTP_404_NOT_FOUND)
        except Exception as e:
            err_logger.info(f"exception raised in handle_lost_and_found: {e}")
            return Response(status.HTTP_409_CONFLICT)

    def is_valid_customer(self, first_name, last_name, phone):
        """
        check if the customer exist in the system
        :param first_name:
        :param last_name:
        :param phone:
        :return: Ture: qr_code found, valid customer;
                False: qr_code not found, invalid customer
        """
        qr = QR.qr_string(first_name, last_name, phone)
        if Customer.objects.filter(qr_code=qr):
            return True
        return False

    def check_in_existing_customer(self):
        try:
            customer_info = Customer.objects.get(qr_code=self.request.data['QRcode'])
            op = Token.objects.get(key=self.request.headers.get('Authorization').split()[1]).user
            return self.checkin_response(customer_info, op)
        except Customer.DoesNotExist:
            err_logger.info(
                ": Failed to get customer information CustomerInfo.objects.get(qr_code=self.request.data['QRcode']): "
                                      "QRcode: %s" % (self.request.data['QRcode']))
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Customer.MultipleObjectsReturned:
            customer_info = Customer.objects.first(qr_code=self.request.data['QRcode'])
            op = Token.objects.get(key=self.request.headers.get('Authorization').split()[1]).user
            err_logger.info(
                f"{customer_info.store} : multiple customer linked to one qr_code"
                f" {customer_info.id} - {self.request.data['QRcode']}")

            body = f"{customer_info.store} : exception raise: multipleObjectsReturned:"\
                   f" {customer_info.id} - {self.request.data['QRcode']}"

            MSG.send_msg(settings.SMS_ADMIN_NUMBER, body)
            return self.checkin_response(customer_info, op)

        except Exception as e:
            err_logger.info(f"exception raised in check_in_existing_customer\n {e}")
            return Response(status=status.HTTP_409_CONFLICT)

    def checkin_response(self, customer_info, op):
        last_check_in = customer_info.last_check_in
        check_in_time = timezone.now()

        # gama
        gama_local_time = check_in_time.astimezone(timezone.get_current_timezone())
        gama_last_check_in = last_check_in.astimezone(timezone.get_current_timezone())
        td = gama_local_time.date()
        gama_time_bound = datetime.datetime(td.year, td.month, td.day, 8, 0, 0, tzinfo=gama_local_time.tzinfo)

        gama_same_date = (gama_local_time.date() == gama_last_check_in.date())
        gama_after_8_criteria = (gama_local_time > gama_time_bound > gama_last_check_in)
        gama_before_8_criteria = ((not gama_same_date) and (gama_time_bound > gama_local_time > gama_last_check_in))
        # gama_criteria = ((customer_info.store == 'gama') and (gama_before_8_criteria or gama_after_8_criteria))
        gama_criteria = ((op.store == 'gama') and (gama_before_8_criteria or gama_after_8_criteria))
        # eta
        # eta_criteria = ((customer_info.store == 'eta') and (check_in_time - last_check_in > settings.TIME_DELTA))
        # eta_criteria = ((op.store == 'eta') and check_in_time - last_check_in > settings.TIME_DELTA)

        eta_criteria = ((op.store == 'eta') and (gama_before_8_criteria or gama_after_8_criteria))
        expiration = customer_info.expiration_date

        if expiration and (check_in_time.astimezone(utc=pytz.timezone('UTC')) > expiration):
            customer_info.expiration_date = None
            customer_info.save(update_fields=['expiration_date'])

        if customer_info.expiration_date:
            fl_time = timezone.localtime(last_check_in).strftime("%m/%d/%Y %H:%M:%S")
            data = {'last_check_in': fl_time,
                    'time_delta': f"Your are inactivated until {customer_info.expiration_date}"}
            return Response(data=json.dumps(data), status=status.HTTP_208_ALREADY_REPORTED)
        elif gama_criteria or eta_criteria:
            CustomerActivities(customer_id=customer_info.id, check_in_time=check_in_time,
                               operator_id=op.id, shift=self.shift(check_in_time), store=op.store).save()
            logger.info(customer_info.store + f": Customer Activities saved to database, ::{customer_info.id}")
            Customer.objects.filter(id=customer_info.id).update(last_check_in=check_in_time)
            logger.info(
                customer_info.store + f": Updated last_check_in time in CustomerInfo, ::{check_in_time} :: last_check_in :: {last_check_in}")
            return Response(status=status.HTTP_200_OK)
        #
        # doesn't meet requirement
        #
        data = {}
        fl_time = timezone.localtime(last_check_in).strftime("%m/%d/%Y %H:%M:%S")
        if customer_info.store == 'gama':
            data = {'last_check_in': fl_time, 'time_delta': "until 8:00 am next day"}
            logger.info(customer_info.store + ": Should wait" + "until 8:00 am next day")
        if customer_info.store == 'eta':
            # data = {'last_check_in': fl_time, 'time_delta': settings.DELTA_TIME}
            data = {'last_check_in': fl_time, 'time_delta': 'until 8:00 am next day'}
            # logger.info(customer_info.store + ": Should wait" + settings.DELTA_TIME + " hours")
            logger.info(customer_info.store + ": Should wait" + "until 8:00 am next day")
        return Response(data=json.dumps(data), status=status.HTTP_208_ALREADY_REPORTED)

    def validate_customer(self):
        if Customer.objects.filter(qr_code=self.request.data['QRcode']):
            data = {'img_url': settings.IMG_BASEURL + self.request.data['QRcode'] + '.jpg'}
            data = json.dumps(data)
            return Response(data=data, status=status.HTTP_200_OK)
        # invalid qrcode
        logger.info("invalid qr: %s" % (self.request.data['QRcode']))
        return Response(status=status.HTTP_404_NOT_FOUND)

