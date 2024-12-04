import requests
from django.views.generic import TemplateView
from rest_framework import generics

from Main.models import InfAboutCafe, Address
from Main.serializers import InfAboutCafeSerializer, AddressSerializer


class AddressListAPIView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class InfAboutCafeViewSet(generics.ListAPIView):
    queryset = InfAboutCafe.objects.all()
    serializer_class = InfAboutCafeSerializer


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Лапки&Кофе'
        return context

    def get(self, request, *args, **kwargs):
        url_cats = "http://localhost:8000/cats/api/cats/"
        url_inf = "http://localhost:8000/api/information/"
        response = requests.get(url_cats)
        cats = response.json()
        response = requests.get(url_inf)
        inf = response.json()
        context = self.get_context_data(**kwargs)
        context['cats'] = cats
        context['information'] = inf
        return self.render_to_response(context)
