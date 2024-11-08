import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from loguru import logger
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users_app.models import User, Profile
from users_app.permissions import IsUserProfileOwner
from users_app.serializers import UserProfileSerializer, FullProfileUserSerializer

from users_app.services.authentication import prepare_set_cookie_response
from users_app.services.user_creation import create_user_from_telegram
from users_app.services.authentication import validate_tg_init_data

logger.add("log/loguru_debug.log", format="{time} {level} {message}", level="DEBUG")
logger.add("log/loguru_info.log", format="{time} {level} {message}", level="INFO")


#  ====  Authentication  ====

@csrf_exempt
@require_POST
def validate_telegram_data_view(request):
    received_data = request.POST
    success, received_hash, expected_hash = validate_tg_init_data(received_data)
    print(f"req post data: {request.POST}")

    if not success:
        return JsonResponse({"status": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    user_info_str = received_data["user"]
    print('!!!!!!!', user_info_str)
    user_info = json.loads(user_info_str)
    tg_id = user_info['id']
    firstname = user_info['first_name']
    lastname = user_info.get('last_name')
    tg_login = user_info.get('username')
    cleaned_user_data = {
        "tg_id": tg_id,
        "firstname": firstname,
        "lastname": lastname if lastname is not None and lastname != '' else None,
        "tg_login": tg_login if tg_login is not None and tg_login != '' else None,
    }
    # user = User.objects.get(tg_id=tg_id)

    if User.objects.filter(tg_id=tg_id).exists():
        user = User.objects.get(tg_id=tg_id)
    else:
        user = create_user_from_telegram(
            tg_id=tg_id,
            firstname=cleaned_user_data.get('firstname'),
            lastname=cleaned_user_data.get('lastname'),
            tg_login=cleaned_user_data.get('tg_login'),
        )

    if user.is_active:
        return prepare_set_cookie_response(user)  # todo: take data higher
    else:
        return JsonResponse({"status": "success", "message": "user not active", "access": str('nope')},
                            status=status.HTTP_403_FORBIDDEN)


#  ====  Permissions  ====

class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        permissions = request.user.get_all_permissions()
        return Response({'permissions': list(permissions)})


#  ====  User  ====
class CurrentUserProfileByUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # profile = get_profile_by_user(request.user)
        user = User.objects.get(pk=request.user.pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


#  ====  Profile  ====


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsUserProfileOwner]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsUserProfileOwner]
        elif self.action == 'me':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'update':
            return FullProfileUserSerializer
        elif self.action == 'retrieve':
            # if self.get_object().user == self.request.user:
            return FullProfileUserSerializer
            # return ProfileIsVerifiedSerializer
        elif self.action == 'me':
            return FullProfileUserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        updated_fields = []
        for field, value in serializer.validated_data.items():
            if getattr(instance, field) != value:
                updated_fields.append(field)

        self.perform_update(serializer)

        return Response({
            "modified": updated_fields,
            **serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get', 'patch', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        """
        Either retrieve or update the profile of the current authenticated user.
        The action taken depends on the HTTP method used in the request.
        """
        user = request.user
        profile = get_object_or_404(Profile, user=user)

        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        elif request.method in ['PATCH', 'PUT']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(profile, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            updated_fields = []
            for field, value in serializer.validated_data.items():
                if getattr(profile, field) != value:
                    updated_fields.append(field)

            self.perform_update(serializer)

            return Response({
                "modified": updated_fields,
                **serializer.data
            }, status=status.HTTP_200_OK)

        else:
            return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Creating profiles is not allowed."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Deleting profiles is not allowed."}, status=status.HTTP_403_FORBIDDEN)
