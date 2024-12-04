from django.urls import path

from Main.views import IndexView, InfAboutCafeViewSet, AddressListAPIView

app_name = 'main'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/address/', AddressListAPIView.as_view()),
    path('api/information/', InfAboutCafeViewSet.as_view(), name='information'),
]