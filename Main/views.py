from django.views.generic import TemplateView
from rest_framework import generics

from Main.models import InfAboutCafe, Address
from Main.serializers import InfAboutCafeSerializer, AddressSerializer
from mixins.mixins import RequestsGETMixin


class AddressListAPIView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class InfAboutCafeViewSet(generics.ListAPIView):
    queryset = InfAboutCafe.objects.all()
    serializer_class = InfAboutCafeSerializer


class IndexView(RequestsGETMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Лапки&Кофе'
        return context

    def get(self, request, *args, **kwargs):
        cats = self.get_dict(url="http://localhost:8000/cats/api/cats/")
        inf = self.get_dict(url="http://localhost:8000/api/information/")
        context = self.get_context_data(**kwargs)
        context['cats'] = cats
        context['information'] = inf
        return self.render_to_response(context)
