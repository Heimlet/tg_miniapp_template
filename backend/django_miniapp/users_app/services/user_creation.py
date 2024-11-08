from django.db import transaction

from users_app.models import User, Profile
from users_app.services.miscellaneous import generate_random_username, filter_fields_by_model


def create_user_with_profile(pk=None, username=None, password=None, tg_id=None, tg_login=None, profile_fields=None, ):
    profile_fields = filter_fields_by_model(profile_fields, Profile)

    with transaction.atomic():
        user = User.objects.create_user(pk=pk, username=username, password=password, tg_login=tg_login, tg_id=tg_id)

        Profile.objects.create(user=user, **profile_fields)

    return user


def create_user_from_telegram(
        tg_id,
        firstname,
        lastname=None,
        tg_login=None,
        nickname=None,
        birthdate=None,
):
    with transaction.atomic():
        username = generate_random_username('TG_')
        profile_fields = {
            'firstname': firstname,
            'lastname': lastname,
        }

        user = create_user_with_profile(username=username, tg_id=tg_id, tg_login=tg_login, profile_fields=profile_fields)

        return user
