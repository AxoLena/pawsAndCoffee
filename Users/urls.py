from django.urls import path, re_path, include

from Users.views import UserProfileView, UserChangeProfileView, UserLoginRegView, UserAccountsListView, UserLogoutView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginRegView.as_view(), name='page_login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/change/', UserChangeProfileView.as_view(), name='change_profile'),
    path('logout/', UserLogoutView.as_view(), name='logout_delToken'),
    path('api/auth/users/inf/', UserAccountsListView.as_view()),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^api/auth/', include('djoser.urls.authtoken')),
]
