import requests
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import generics

from Main.models import InfAboutCafe, Address
from Main.serializers import InfAboutCafeSerializer, AddressSerializer
from mixins.mixins import GetCacheMixin


class AddressListAPIView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class InfAboutCafeViewSet(generics.ListAPIView):
    queryset = InfAboutCafe.objects.all()
    serializer_class = InfAboutCafeSerializer


class IndexView(GetCacheMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Лапки&Кофе'
        return context

    def get(self, request, *args, **kwargs):
        cats = self.get_cache_for_context(cache_name=settings.CATS_CACHE_NAME,
                                          url=reverse('cats:cats-list'), time=60*60)
        inf = self.get_cache_for_context(cache_name=settings.MAIN_INFORMATION_CACHE_NAME,
                                         url=reverse('main:information'), time=60*60)
        context = self.get_context_data(**kwargs)
        context['contacts'] = {
            'github': 'https://github.com/AxoLena',
            'telegram': '@hiiirch',
            'email': 'alena.sukhar333@gmail.com'
        }
        context['cats'] = cats
        context['information'] = inf
        return self.render_to_response(context)
