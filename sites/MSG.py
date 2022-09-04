# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

from django.conf import settings
from twilio.rest import Client
import logging
from sites import qrcode_util as QR

info_logger = logging.getLogger('info')
err_logger = logging.getLogger('error')


class MSG:
    client = Client(settings.SMS_ACCT, settings.SMS_TOKEN)

    @staticmethod
    def send_msg(phone, body, media_urls=None):
        if media_urls:
            MSG.send_msg_with_img(phone, body, media_urls)
        else:
            message = MSG.client.messages.create(
                body=body,
                from_=settings.SMS_FROM_NUMBER,
                to=phone,
            )
            info_logger.info(f"TEXT message sent to {phone}")

    @staticmethod
    def send_msg_with_img(phone, body, media_urls):
        message = MSG.client.messages.create(
            body=body,
            from_=settings.SMS_FROM_NUMBER,
            media_url=media_urls,
            to=phone,
        )
        info_logger.info(f'TEXT message with image sent to {phone}')

    @staticmethod
    def send_qr_code(first_name, last_name, phone):
        qr = QR.qr_string(first_name, last_name, phone)
        qr_img_url = settings.QR_BASEURL + qr + ".png"
        info_logger.info(f'send qr_code: {phone}:{qr_img_url}')
        MSG.send_msg_with_img(phone,
                     f"Hello {first_name} {last_name}! Attached is your QR code",
                     qr_img_url)