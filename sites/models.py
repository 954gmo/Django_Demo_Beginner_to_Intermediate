from django.db import models
from accounts.models import Operator
from django.utils import timezone
from config.dashboard.sitewide_conf import SHIFTS


class Store(models.Model):
    class Meta:
        verbose_name = "Store Information"

    STORES = (
        ('eta', 'eta'),
        ('gama', 'gama'),
    )
    name = models.CharField(max_length=255, choices=STORES)
    address = models.CharField(max_length=1024, default='')
    phone = models.CharField(max_length=15, default='')
    administrator = models.CharField(max_length=150, default='')

    def __str__(self):
        return self.name


class Customer(models.Model):
    class Meta:
        verbose_name = "Customer Information"
        ordering = ['id']

    # management information
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)  # register operator
    enabled = models.BooleanField(default=True)     # disable instead of delete
    expiration_date = models.DateTimeField(null=True, blank=True)   # dis-activation

    # customer information
    first_name = models.CharField(max_length=150, default='')
    last_name = models.CharField(max_length=150, default='')
    phone = models.CharField(max_length=15, default='')
    qr_code = models.CharField(max_length=128, default='')

    # meta activities information
    since = models.DateTimeField(default=timezone.now)
    last_check_in = models.DateTimeField(default=timezone.now)


class CustomerActivitiesManager(models.Manager):
    def operator_view(self, operator):
        return self.filter(operator=operator)


class CustomerActivities(models.Model):
    class Meta:
        verbose_name = "Customer Activities"
        ordering = ['-check_in_time']

    SHIFTS_CHOICE = ((k, v) for k, v in SHIFTS.items())

    # management information
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="check in at ")
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE) # handle operator, different than the register operator

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=timezone.now)
    shift = models.CharField(max_length=25, choices=SHIFTS_CHOICE)

    objects = CustomerActivitiesManager()


class OperatorActivitiesManager(models.Manager):
    def operator_view(self, operator):
        return self.filter(operator=operator)


class OperatorActivities(models.Model):
    class Meta:
        verbose_name = "Operator Activities"
        ordering = ['-log_time']

    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    log_time = models.DateTimeField(verbose_name='operate at', default=timezone.now)
    activities = models.CharField(max_length=255, default='')

    objects = OperatorActivitiesManager()


class CustomerActivationLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    log_time = models.DateTimeField(default=timezone.now)   # time of the dis-activation
    reason = models.TextField(null=True, blank=True)    # reason of dis-activation
    expiration_date = models.DateTimeField(null=True, blank=True)   # expiration of this dis-activation


class AdminHistory(models.Model):
    class Meta:
        verbose_name = 'Admin History'
    ACTIONS = (
        ('disable_customer', 'Disable Customer'),
        ('enable_customer', 'Enable Customer'),
        ('disable_operator', 'Disable Operator'),
        ('enable_operator', 'Enable Operator'),
    )
    action = models.CharField(max_length=15, default='disable_customer')
    reason = models.TextField()
    action_time = models.DateTimeField(default=timezone.now)