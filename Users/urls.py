from django.urls import path, re_path, include
from rest_framework import routers

from Users.views import (UserProfileView, UserChangeProfileView, UserLoginRegView, UserAccountViewSet, UserLogoutView,
                         UserResetPasswordView, UserResetNewPasswordView, UserUpdateInfAboutPaymentsView)

app_name = 'users'

router = routers.SimpleRouter()
router.register(r'inf', UserAccountViewSet, basename='account')

urlpatterns = [
    path('login/', UserLoginRegView.as_view(), name='page_login'),
    path('update/', UserUpdateInfAboutPaymentsView.as_view(), name='update'),
    path('email/reset/', UserResetPasswordView.as_view(), name='reset_password'),
    path('password/reset/confirm/<str:uid>/<str:token>/', UserResetNewPasswordView.as_view(), name='new_password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/change/', UserChangeProfileView.as_view(), name='change_profile'),
    path('logout/', UserLogoutView.as_view(), name='logout_delToken'),
    path('api/auth/profile/<int:pk>/', include(router.urls), name='inf_about_user_profile'),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^api/auth/', include('djoser.urls.authtoken')),
]
