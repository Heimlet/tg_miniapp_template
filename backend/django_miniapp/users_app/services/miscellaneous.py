import random
import string

import phonenumbers
from phonenumber_field.phonenumber import PhoneNumber

from users_app.models import User


def filter_fields_by_model(fields: dict, model):
    valid_fields = {field.name for field in model._meta.get_fields()}
    return {key: fields[key] for key in fields if key in valid_fields}


def generate_random_username(prefix, length=8):
    characters = string.ascii_letters + string.digits

    username = ''.join(random.choice(characters) for _ in range(length))

    if User.objects.filter(username=f"{prefix}{username}").exists():
        return generate_random_username(prefix, length)

    return f"{prefix}{username}"


def format_e164_phone_from_string(phone):
    """ Returns correct format for a phone number from given string. """
    try:
        number = PhoneNumber.from_string(phone, region="RU")

        if number.is_valid():
            phone_as_e164 = number.as_e164
            return phone_as_e164, True
        else:
            return None, False
    except (phonenumbers.phonenumberutil.NumberParseException, ) as e:
        return None, False

