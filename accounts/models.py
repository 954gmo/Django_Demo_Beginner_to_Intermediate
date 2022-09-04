from django.db import models
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.db.models import UniqueConstraint
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class OperatorManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_operator(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'operator')
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("user_type", 'superuser')
        if not email:
            email = 'superuser@sixdigit.net'
        return self._create_user(username, email, password, **extra_fields)


# extending the Django User Model
# by using AbstractUser, Django create the Operator model without creating User table.
# need to adjust AUTH_USER_MODEL = 'sites.Operators' in `config/base.py`
class Operator(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username', 'email']

    class Meta:
        constraints = [
            UniqueConstraint(fields=['email', 'username'], name='unique_operator_account')
        ]
        ordering = ['-last_login', 'id']

    # `operator` is limited to use only the mobile app or login to web-end for simple business operations,
    # `store_manager` is limited to see only the store info under their management
    # `super_admin` is has almost all permission of the system, such as creating user, assigning permission, etc.
    USER_TYPES = (
        ('operator', 'Operator'),
        ('store_manager', 'Store Manager'),
        ('admin', 'Administrator'),
        ('superuser', 'Superuser'),
    )

    STORES = {
        ('eta', 'eta'),
        ('gama', 'gama'),
    }

    is_active = models.BooleanField(verbose_name='is_active', default=True)
    store = models.CharField(verbose_name="work at", choices=STORES,  max_length=50, default='eta')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='operator')

    email = models.EmailField(
        _('email'),
        unique=True,
        help_text=_(
            'Required. Email'
        ),
        max_length=255,
        blank=False,
    )

    # these fields declarations are copied as-is from `AbstractUser`
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        unique=True,
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    objects = OperatorManager()




