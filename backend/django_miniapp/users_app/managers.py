from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password=None, user_fields=None, pk=None):
        from users_app.services.miscellaneous import filter_fields_by_model
        user_fields = filter_fields_by_model(user_fields, self.model)

        if not user_fields.get('username'):
            raise ValueError('The given username must be set')

        with transaction.atomic():
            user = self.model(**user_fields)

            if pk:
                user.pk = pk

            if password:
                user.set_password(password)
            user.save(using=self._db)

        return user

    def create_user(self, pk=None, username=None, password=None, tg_login=None, email=None, phone=None, tg_id=None):
        """ For creating non-admin and non-staff users. """
        from users_app.services.miscellaneous import generate_random_username

        user_fields = {
            'username': username or generate_random_username('AUTO_'),
            'tg_login': tg_login,
            'email': email,
            'phone': phone,
            'tg_id': tg_id or None,
            'is_superuser': False,
            'is_staff': False,
            'is_active': True
        }

        return self._create_user(password=password, user_fields=user_fields, pk=pk)

    def create_superuser(self, username, password, email=None, **extra_fields):
        user_fields = {
            'username': username,
            'password': password,
            'email': email,
            'is_superuser': True,
            'is_staff': True,
            'is_active': True
        }

        return self._create_user(password=password, user_fields=user_fields)
