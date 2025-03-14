import requests
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework import viewsets

from Users.forms import UserLoginForm, UserChangeProfileForm, UserRegForm, UserResetForm, UserSetPasswordForm
from Users.serializers import UserProfileSerializer
from Users.models import CustomUser
from Booking.models import Booking
from Cats.models import FormForGuardianship


class UserLoginRegView(View):
    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    context = {
        'title': 'Авторизация'
    }

    def get(self, request):
        form = UserRegForm
        form1 = UserLoginForm
        self.context['form1'] = form1
        self.context['form'] = form
        return render(request, 'users/login.html', context=self.context)

    def post(self, request):
        if self.is_ajax():
            token = request.POST.get('auth-token')
            response = render(request, 'users/login.html', context=self.context)
            response.set_cookie('auth-token', token)
            return response
        return HttpResponse(status=500)


class UserResetPasswordView(View):
    context = {
        'title': 'Восстановаление пароля'
    }

    def get(self, request):
        form = UserResetForm
        self.context['form'] = form
        return render(request, 'users/reset_password.html', context=self.context)


class UserResetNewPasswordView(View):
    context = {
        'title': 'Установка нового пароля'
    }

    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def get(self, request, **kwargs):
        user = request.user
        form = UserSetPasswordForm(user=user)
        self.context['form'] = form
        self.context['uid'] = kwargs.get('uid')
        self.context['token'] = kwargs.get('token')
        return render(request, 'users/reset_new_password.html', context=self.context)


class UserProfileView(View):
    context = {
        'title': 'Личный кабинет'
    }

    def get(self, request, *args, **kwargs):
        user_pk = request.user.pk
        url = f'http://127.0.0.1:8000/user/api/auth/profile/{user_pk}/inf/'
        response = requests.get(url)
        user = response.json()
        url = 'http://127.0.0.1:8000/bonus/api/coupon/list/'
        response = requests.get(url)
        coupons = response.json()
        self.context['user'] = user
        self.context['coupons'] = coupons
        return render(request, 'users/profile.html', context=self.context)


class UserChangeProfileView(View):
    context = {
        'title': 'Изменить профиль'
    }

    def get(self, request):
        user = request.user
        form = UserChangeProfileForm(instance=user)
        self.context['form'] = form
        return render(request, 'users/change_profile.html', context=self.context)


class UserUpdateInfAboutPaymentsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            booking = Booking.objects.filter(phone=user.phone)
            guardianship = FormForGuardianship.objects.filter(phone=user.phone)
            if booking:
                for data in booking:
                    if data.is_paid:
                        data.user = user
            if guardianship:
                for data in guardianship:
                    if data.is_paid:
                        data.user = user
            return redirect(reverse('users:profile'))
        else:
            messages.warning(request, 'На сервере произошла ошибка!\n Попробуйте авторизоваться еще раз')
            return redirect(reverse('users:page_login'))


class UserLogoutView(View):
    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def post(self, request):
        if self.is_ajax():
            response = HttpResponseRedirect(reverse('main:index'))
            response.delete_cookie('auth-token')
            return response
        return HttpResponse(status=500)


class UserAccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.kwargs['pk'])
