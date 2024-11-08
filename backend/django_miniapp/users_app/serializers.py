from datetime import date

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users_app.models import User, Profile
from users_app.services.miscellaneous import format_e164_phone_from_string


# from users_app.services.permissions import get_user_permissions


# ==== Model Serializers ====

class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'tg_id', 'tg_login', 'is_verified', 'is_superuser', 'is_staff', ]
        read_only_fields = ['id', 'username', 'phone', 'tg_id', 'tg_login', 'is_verified', 'is_superuser', 'is_staff' ]


class UserIsVerifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_verified']
        read_only_fields = ['id', 'is_verified']


class ProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'birthdate', 'firstname', 'lastname', 'fullname', 'nickname', 'social', 'user',]
        read_only_fields = ['user',]

    def get_fullname(self, instance):
        return instance.get_fio()


class SlimProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'firstname', 'lastname', 'nickname', 'social', 'user', ]
        read_only_fields = ['user',]


class SlimProfileIsVerifiedSerializer(serializers.ModelSerializer):
    user = UserIsVerifiedSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'firstname', 'lastname', 'nickname', 'social', 'user', ]
        read_only_fields = ['id', 'user',]


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, required=False)
    # permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tg_id', 'tg_login', 'phone', 'is_verified', 'is_staff', 'is_superuser', 'profile',]
        read_only_fields = ['id', 'username', 'email', 'tg_id', 'tg_login', 'phone', 'is_verified', 'is_staff', 'is_superuser', 'profile',]

    # def get_permissions(self, instance):
    #     print('perms', get_user_permissions(instance))
    #     return get_user_permissions(instance)


class SlimUserProfileSerializer(serializers.ModelSerializer):
    profile = SlimProfileSerializer(read_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile', 'is_verified', ]
        read_only_fields = ['id', 'username', 'profile', 'is_verified', ]


class FullProfileUserSerializer(serializers.ModelSerializer):
    user = FullUserSerializer(read_only=True)
    # permissions = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'birthdate', 'firstname', 'lastname', 'nickname', 'social', 'user', 'avatar', ]  # 'permissions',
        read_only_fields = ['user',]  #, permissions

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.social = validated_data.get('social', instance.social)

        instance.save()
        return instance

    # def get_permissions(self, instance):
    #     return instance.user and get_user_permissions(instance.user)

    def validate_birthdate(self, value):
        if value is not None and value > date.today():
            raise serializers.ValidationError("Кажется, вы ещё не родились.")
        return value


class ProfileIsVerifiedSerializer(serializers.ModelSerializer):
    user = UserIsVerifiedSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'birthdate', 'firstname', 'lastname', 'nickname', 'social', 'user',]
        read_only_fields = ['user',]


# ==== Scripts serializers ====

class TelegramUserUpdateSerializer(serializers.Serializer):
    tg_id = serializers.IntegerField(required=True)
    existed_profile_id = serializers.IntegerField(required=False)
    phone = serializers.CharField(allow_null=True, required=False)
    username = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False)
    birthdate = serializers.DateField(required=False)
    tg_login = serializers.CharField(required=False)
    firstname = serializers.CharField(required=False)
    lastname = serializers.CharField(required=False)

    def validate_existed_profile_id(self, value):
        if not value:
            return value

        if not Profile.objects.filter(user__is_verified=False, pk=value).exists():
            raise serializers.ValidationError("Указанный профиль не найден в системе.")
        return value

    def validate_phone(self, value):
        if not value:
            return value

        phone, success = format_e164_phone_from_string(value)
        if not success:
            raise serializers.ValidationError("Введите корректный номер телефона.")

        return phone
