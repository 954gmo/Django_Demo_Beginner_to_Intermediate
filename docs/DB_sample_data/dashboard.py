import datetime
import random
from django.conf import settings
from django.utils import timezone

from accounts.models import Operator
from django.contrib.auth.hashers import make_password
import sites.qrcode_util as QR
from sites.models import (Store, Customer, CustomerActivities,
                          CustomerActivationLog, OperatorActivities)


def populate_database():

    # populate database
    Store.objects.create(name=Store.STORES[0][0], address='eta address', phone='9541234564', administrator='eta admin')
    Store.objects.create(name=Store.STORES[1][0], address='gama address', phone='7866478596', administrator='gama admin')

    password = 'etk786lkl@*'

    Operator.objects.create(username='SUPERUSER', is_active=True, store=Store.STORES[0][0],
                            user_type=Operator.USER_TYPES[3][0], email='SUPERUSER@exampl.com',
                            first_name='SUPER', last_name='USER', password=make_password(password))

    Operator.objects.create(username='ADMIN', is_active=True, store=Store.STORES[0][0],
                            user_type=Operator.USER_TYPES[2][0], email='ADMIN@exampl.com',
                            first_name='ADMIN', last_name='USER', password=make_password(password))

    Operator.objects.create(username='TEST_STORE_MANAGER1', is_active=True, store=Store.STORES[0][0],
                            user_type=Operator.USER_TYPES[1][0], email='TEST_MANAGER_1@exampl.com',
                            first_name='TEST_STORE', last_name='MANAGER 1', password=make_password(password))

    Operator.objects.create(username='TEST_STORE_MANAGER2', is_active=True, store=Store.STORES[1][0],
                            user_type=Operator.USER_TYPES[1][0], email='TEST_MANAGER_2@exampl.com',
                            first_name='TEST_STORE', last_name='MANAGER 2', password=make_password(password))

    Operator.objects.create(username='TEST_OP1', is_active=True, store=Store.STORES[0][0],
                            user_type=Operator.USER_TYPES[0][0], email='TEST_OP1@exampl.com',
                            first_name='TEST', last_name='OP1', password=make_password(password))

    Operator.objects.create(username='TEST_OP2', is_active=True, store=Store.STORES[1][0],
                            user_type=Operator.USER_TYPES[0][0], email='TEST_OP2@exampl.com',
                            first_name='TEST', last_name='OP2', password=make_password(password))

    first_names = ["Chanorika", "Cindy", "Marcus", "Lawrence", "Paul", "Darlene", "Theresa", "Melissa", "Beaucher", "Chi", "Pierrie", "Derrick", "Ross marie","Pamela", "Tiffany", "Shameika", "Steven", "Joel", "Vincent ","Teresa", "Eric", "Morales", "Shakeera", "Nicole", "Kathy ","Ashley", "Tation", "Deandra", "Donairus", "Thomas", "Beverly", "Christopher", "Regina", "Muir", "Nieves", "Michael", "Tierra", "Irma", "Vutthapoom", "Rochelle", "Todd", "Juan", "Lewis", "Aheimeka", "Willie", "Mike", "Garett", "Jason", "Cindy linn", "Li yun"]
    last_names = ["Pullen", "Scopa", "Johnson", "Irving", "Quarantello", "Barber", "Laviolette", "Defrancesco", "Erica lynn","Wu", "Romulus", "Eddings", "Ting", "Chaves", "Gonsalves", "Northern", "Northrup", "Rivera", "Snider", "Fogarty", "Tartaglia", "Gabby", "Beyer", "Nester", "Smith", "Lott", "Brown", "Parker", "Johnson", "Parrish", "Wyche", "Healy", "Ginn", "Adam", "Cruz", "Fitzgerald", "Taylor", "Mendez", "Srichalerm", "Elliott", "Parish", "Nann", "Vincent", "Dinley", "Robinson", "Zito", "Walters", "Thompson", "Johnson", "kang"]

    # generate random phone number
    def random_phone_number():
        area = str(random.randint(100, 999))
        mid = str(random.randint(0, 999)).zfill(3)
        tail = str(random.randint(0, 9999)).zfill(4)
        return f'{area}{mid}{tail}'

    phones = []

    for i in range(0, len(first_names)):
        phones.append(random_phone_number())

    stores = Store.objects.all()
    operators = Operator.objects.all()
    check_in_time = timezone.now()

    for k in range(0, len(first_names)):
        Customer.objects.create(store=random.choice(stores), operator=random.choice(operators),
                                first_name=first_names[k], last_name=last_names[k], phone=phones[k],
                                qr_code=QR.qr_string(first_names[k], last_names[k], phones[k]),
                                since=check_in_time + datetime.timedelta(
                                              days=random.choice(range(10, -11, -1)),
                                              hours=random.choice(range(29, -27, -1)),
                                              minutes=random.choice(range(134, -46, -1))
                                          ),
                                last_check_in=check_in_time + datetime.timedelta(
                                              days=random.choice(range(10, -11, -1)),
                                              hours=random.choice(range(29, -27, -1)),
                                              minutes=random.choice(range(134, -46, -1))
                                          )
                                )

    customers = Customer.objects.all()
    check_in_time = timezone.now()
    shifts = [k for k in settings.SHIFTS]
    for k in range(0, len(first_names) * 3):
        CustomerActivities.objects.create(store=random.choice(stores), operator=random.choice(operators),
                                          customer=random.choice(customers),
                                          check_in_time=check_in_time + datetime.timedelta(
                                              days=random.choice(range(10, -11, -1)),
                                              hours=random.choice(range(29, -27, -1)),
                                              minutes=random.choice(range(134, -46, -1))
                                          ),
                                          shift=random.choice(shifts))

    activities = ['Register new Customer', 'Lost and Found', 'Check in Customer', 'Disable Customer', 'Deactivate Customer']
    for k in range(0, len(first_names) * 2):
        OperatorActivities.objects.create(operator=random.choice(operators),
                                          log_time=check_in_time + datetime.timedelta(
                                              days=random.choice(range(10, -11, -1)),
                                              hours=random.choice(range(29, -27, -1)),
                                              minutes=random.choice(range(134, -46, -1))
                                          ),
                                          activities=random.choice(activities))


if __name__ == '__main__':
    pass
