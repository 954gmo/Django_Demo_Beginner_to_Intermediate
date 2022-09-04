# -*- encoding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__ENTITY_author__ = "SIX DIGIT INVESTMENT GROUP"
__author__ = "GWONGZAN"

import hashlib
import os
import qrcode
from django.conf import settings


def qr_string(first_name, last_name, ph):
    """
    generate a string for generating QR code
    :param first_name: of customer
    :param last_name: of customer
    :param ph: of customer
    :return: sha1 encoded string
    """
    return hashlib.sha1(bytes(first_name + last_name + ph, 'utf-8')).hexdigest()


def generate_QRCODE(qr_str):
    """
    generate QR code image for the qt_str
    :param qr_str:
    :return: img_path : image path of the QR code
            filename: image filename
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_str)
    qr.make(fit=True)
    filename = qr_str + '.png'
    img = qr.make_image(fill='black', back_color='white')
    img_path = os.path.join(settings.QR_CODE, filename)
    img.save(img_path)
    return img_path, filename
