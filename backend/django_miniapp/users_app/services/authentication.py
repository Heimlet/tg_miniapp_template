import hashlib
import hmac

from django.http import JsonResponse
from django.middleware import csrf
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from tg_miniapp import settings
from users_app.models import User
from users_app.serializers import UserProfileSerializer


def validate_tg_init_data(received_data):
    received_hash = received_data.get('hash')

    data_check_string = '\n'.join(f'{key}={value}' for key, value in sorted(received_data.items()) if key != 'hash')

    bot_token = settings.BOT.get('BOT_API_KEY')
    secret_key = hmac.new(str.encode('WebAppData'), str.encode(bot_token), hashlib.sha256).digest()

    expected_hash = hmac.new(secret_key, str.encode(data_check_string), hashlib.sha256).hexdigest()

    return expected_hash == received_hash, received_hash, expected_hash


def prepare_set_cookie_response(user: User):
    serialized_user_data = UserProfileSerializer(user)
    response = JsonResponse({"status": "success", "user": serialized_user_data.data},
                            status=status.HTTP_200_OK)
    access_token = AccessToken.for_user(user)
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=access_token,
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    response.status = status.HTTP_200_OK

    return response
