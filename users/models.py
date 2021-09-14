from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, domain, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        domain = extra_fields.get('domain')
        if not domain:
            raise ValueError('The given domain must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(domain + settings.SEPARATE_CHARACTER + username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_User(self, username, domain, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.USER)
        extra_fields.setdefault('is_confirmed', False)
        extra_fields.setdefault('domain', domain)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.ADMIN)
        extra_fields.setdefault('is_confirmed', True)
        extra_fields.setdefault('domain', settings.DOMAIN_SUPERUSER)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):

    class Role(models.TextChoices):
        USER = 'user', _('User')
        ADMIN = 'admin', _('Admin')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username = models.CharField(max_length=settings.LEN, unique=True, verbose_name=_('username'))
    domain = models.CharField(max_length=settings.SHORT_LEN, verbose_name=_('domain'))

    first_name = models.CharField(
        max_length=settings.SHORT_LEN, blank=True, verbose_name=_('first name'))
    last_name = models.CharField(
        max_length=settings.SHORT_LEN, blank=True, verbose_name=_('last name'))
    email = models.EmailField(blank=True)

    role = models.CharField(
        max_length=settings.SHORT_LEN, choices=Role.choices,
        default=Role.USER, verbose_name=_('role')
    )
    is_confirmed = models.BooleanField(default=False, verbose_name=_('is confirmed'))

    created_at = models.DateTimeField(auto_now_add=timezone.now)

    objects = UserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return '\\'.join(self.username.split(settings.SEPARATE_CHARACTER))

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_user(self):
        return self.role == self.Role.USER

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, *args, **kwargs):
        return self.is_staff

    def has_module_perms(self, *args, **kwargs):
        return self.is_staff

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = (
            '-created_at',
        )
