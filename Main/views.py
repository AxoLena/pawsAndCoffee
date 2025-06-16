import requests
from django.conf import settings
from django.urls import reverse
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
        context = self.get_context_data(**kwargs)
        context['contacts'] = {
            'github': ('AxoLena', 'https://github.com/AxoLena'),
            'telegram': ('@hiiirch', 'https://t.me/hiiirch'),
            'email': ('alena.sukhar333@gmail.com', 'mailto:alena.sukhar333@gmail.com')
        }
        return self.render_to_response(context)
