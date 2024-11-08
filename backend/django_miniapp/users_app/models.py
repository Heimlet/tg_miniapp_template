from __future__ import unicode_literals

import os

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


def get_user_avatar_directory_path(instance, filename):
    file_name, file_extension = os.path.splitext(filename)
    return 'user_{0}/profile_{1}/avatar_{2}_{3}{4}'.format(instance.user.pk,
                                                           instance.pk,
                                                           instance.user.username,
                                                           file_name[:10],
                                                           file_extension)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255, unique=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True, default=None)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    phone = PhoneNumberField(unique=True, null=True, blank=True, verbose_name="Телефон")
    tg_id = models.BigIntegerField(verbose_name="TG_ID", unique=True, null=True, blank=True, default=None)
    tg_login = models.CharField(max_length=50, null=True, default=None, verbose_name="Логин в тг")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        unique_together = ('username', 'email', 'phone')

    def __str__(self):
        try:
            profile = self.profile
            fio = self.profile.get_fio()
        except Profile.DoesNotExist:
            profile = None
            fio = None
        if fio:
            return profile.__str__()
        elif self.username:
            return self.username
        elif self.email:
            return f"email: {self.email}"
        else:
            return f"phone: {self.phone}"


def validate_file_size(value: InMemoryUploadedFile):
    max_size = 2 * 1024 * 1024  # 2MB
    if value.size > max_size:
        raise ValidationError("Размер файла слишком большой. Размер должен быть не более 2MB.")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    firstname = models.CharField(_('Firstname'), max_length=100)
    lastname = models.CharField(_('Lastname'), blank=True, null=True, max_length=100)
    birthdate = models.DateField(null=True, blank=True, default=None, verbose_name="Дата рождения")
    nickname = models.CharField(max_length=50, null=True, blank=True, default=None, verbose_name="Ник")
    social = models.CharField(max_length=100, null=True, blank=True, default=None, verbose_name="Соц. сети")
    avatar = models.ImageField(upload_to=get_user_avatar_directory_path,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                           validate_file_size],
                               verbose_name="Аватар",
                               null=True,
                               blank=True,
                               default=None)

    def __str__(self):
        if self.user.is_verified is True:
            verified_str = ' ✅'
        else:
            verified_str = ''

        if self.firstname:
            return f"{self.firstname}{verified_str}"
        elif self.nickname:
            return f"nickname: {self.nickname}{verified_str}"
        else:
            return f"user instance: {self.user}{verified_str}"

    def is_verified(self):
        return self.user.is_verified

    def get_fio(self):
        return "{0} {1}".format(self.firstname, self.lastname).strip()

    class Meta:
        ordering = ['firstname', 'lastname']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
