import json

import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from rest_framework import viewsets, generics, views, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from Cats.forms import AdoptForm, GiveForm, GuardianshipForm
from Cats.models import Cats, FormForGuardianship, FormForAdopt, FormForGive
from Cats.serializers import CatsSerializer, GuardianshipSerializer, AdoptSerializer, GiveSerializer


class CatsListAPIView(generics.ListAPIView):
    queryset = Cats.objects.all()
    serializer_class = CatsSerializer


class OurCatsView(TemplateView):
    template_name = 'cats/our_cats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Наши коты'
        return context

    def get(self, request, *args, **kwargs):
        url = "http://localhost:8000/cats/api/cats/"
        response = requests.get(url)
        cats = response.json()
        context = self.get_context_data(**kwargs)
        context['cats'] = cats
        return self.render_to_response(context)


class AdopAPIView(views.APIView):
    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def post(self, request):
        serializer = AdoptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if self.is_ajax():
                valid_data = []
                for field in serializer.validated_data:
                    valid_data.append(field)
                response_data = {
                    'message': 'Заявка была принята',
                    'valid_data': json.dumps(valid_data),
                }
                return JsonResponse(response_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            if self.is_ajax():
                errors = {}
                for field in serializer.errors:
                    errors[field] = serializer.errors[field][0].title()
                valid_data = []
                for field in serializer.data:
                    if field not in errors:
                        valid_data.append(field)
                response_data = {
                    'result': 'error',
                    'errors': json.dumps(errors),
                    'valid_data': json.dumps(valid_data),
                    'message': 'Заявка не была отправлена! Проверьте правильность заполнения полей'
                }
                return JsonResponse(response_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        adopt = FormForAdopt.objects.all()
        return Response({'post': AdoptSerializer(adopt, many=True).data})


class AdoptView(View):
    context = {
        'title': 'Приютить котика',
    }

    def get(self, request):
        form = AdoptForm
        self.context['form'] = form
        return render(request, 'cats/adopt.html', context=self.context)


class GiveAPIView(views.APIView):
    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def post(self, request):
        serializer = GiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if self.is_ajax():
                valid_data = []
                for field in serializer.validated_data:
                    valid_data.append(field)
                response_data = {
                    'message': 'Заявка была принята',
                    'valid_data': json.dumps(valid_data),
                }
                return JsonResponse(response_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            if self.is_ajax():
                errors = {}
                for field in serializer.errors:
                    errors[field] = serializer.errors[field][0].title()
                valid_data = []
                for field in serializer.data:
                    if field not in errors:
                        valid_data.append(field)
                response_data = {
                    'result': 'error',
                    'errors': json.dumps(errors),
                    'valid_data': json.dumps(valid_data),
                    'message': 'Заявка не была отправлена! Проверьте правильность заполнения полей'
                }
                return JsonResponse(response_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        give = FormForGive.objects.all()
        return Response({'post': GiveSerializer(give, many=True).data})


class GiveView(View):
    context = {
        'title': 'Отдать котика',
    }

    def get(self, request):
        form = GiveForm
        self.context['form'] = form
        return render(request, 'cats/give.html', context=self.context)


class GuardianshipView(View):
    context = {
        'title': 'Опекунство',
    }

    def get(self, request):
        form = GuardianshipForm
        self.context['form'] = form
        return render(request, 'cats/guardianship.html', context=self.context)


class GuardianshipAPIView(views.APIView):
    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def post(self, request):
        serializer = GuardianshipSerializer(data=request.data)
        request.session.save()
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.validated_data['user'] = request.user
                serializer.validated_data['session_key'] = None
            else:
                serializer.validated_data['user'] = None
                serializer.validated_data['session_key'] = request.session.session_key
            serializer.save()
            if self.is_ajax():
                valid_data = []
                for field in serializer.validated_data:
                    valid_data.append(field)
                response_data = {
                    'message': 'Заявка была принята',
                    'valid_data': json.dumps(valid_data),
                }
                return JsonResponse(response_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            if self.is_ajax():
                errors = {}
                for field in serializer.errors:
                    errors[field] = serializer.errors[field][0].title()
                valid_data = []
                for field in serializer.data:
                    if field not in errors:
                        valid_data.append(field)
                response_data = {
                    'result': 'error',
                    'errors': json.dumps(errors),
                    'valid_data': json.dumps(valid_data),
                    'message': 'Заявка не была отправлена! Проверьте правильность заполнения полей'
                }
                return JsonResponse(response_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        guardianship = FormForGuardianship.objects.all()
        return Response({'post': GuardianshipSerializer(guardianship, many=True).data})
