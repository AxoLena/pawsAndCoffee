from django.urls import path

from Cats.views import OurCatsView, CatsListAPIView, AdoptView, GiveView, GuardianshipView, AdopAPIView, GiveAPIView, \
    GuardianshipAPIView

app_name = 'cats'


urlpatterns = [
    path('our-cats/', OurCatsView.as_view(), name='our_cats'),
    path('adopt/', AdoptView.as_view(), name='adopt'),
    path('api/adopt/', AdopAPIView.as_view()),
    path('give/', GiveView.as_view(), name='give'),
    path('api/give/', GiveAPIView.as_view()),
    path('guardianship/', GuardianshipView.as_view(), name='guardianship'),
    path('api/guardianship/', GuardianshipAPIView.as_view()),
    path('api/cats/', CatsListAPIView.as_view(), name='cats-list'),
]