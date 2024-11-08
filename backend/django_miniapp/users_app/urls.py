from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users_app import views
from users_app.views import *

from rest_framework import routers

router = SimpleRouter()
router.register(r'profile', views.ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/v2/', include(router.urls)),
    path('api/v2/miniapp_login/', validate_telegram_data_view, name="miniapp_login"),

    #
    # path('api/v2/login/', LoginView.as_view(), name="login"),
    # path('api/v2/check_authenticated/', CheckAuthenticatedView.as_view(), name='token_verify'),
    # path('api/v2/logout/', logout_view, name='logout'),
    # # path('api/v2/token/', login_view, name='login'),
    # # path('api/v2/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v2/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v2/user/me/', CurrentUserProfileByUserView.as_view(), name='user_me'),
    #
    # # telegram bot instance auth and methods
    # path('api/v2/auth/telegram_user/', get_token_for_telegram_user, name="api_tg_auth"),
    # path('api/v2/auth/telegram_user/existed_user/', take_and_update_existed_user_from_telegram,
    #      name="api_tg_auth_existed"),

    # permissions
    path('api/v2/user/me/permissions/', UserPermissionsView.as_view(), name='permissions_list'),

    # media auth
    # path('media_auth/', FileAuthView.as_view(), name='media_auth'),  # expects `?original_uri=/media/file_path` from NGINX
]
