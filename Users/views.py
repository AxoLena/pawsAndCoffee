from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from djoser.email import BaseDjoserEmail
from rest_framework import viewsets
from rest_framework.decorators import action

from Users.forms import UserLoginForm, UserChangeProfileForm, UserRegForm, UserResetForm, UserSetPasswordForm
from Users.serializers import UserProfileSerializer
from Users.models import CustomUser
from Booking.models import Booking
from Cats.models import FormForGuardianship
from mixins.mixins import GetCacheMixin, GetAuthTokenMixin
from permissions.permissions import IsAdminOrAuthenticatedReadOnly
from Users.tasks import custom_reset_password


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


class CustomPasswordResetEmail(BaseDjoserEmail):
    template_name = "email/password_reset.html"

    def get_context_data(self, request):
        email = request.GET.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'email': 'Пользователя с такой почтой не найдено'})

        reset_email_context = custom_reset_password.delay(user=user, request=request)
        new_values = {key: value for (key, value) in reset_email_context.items()}

        context = super().get_context_data()
        context.update(new_values)

        return context


class UserProfileView(LoginRequiredMixin, GetCacheMixin, GetAuthTokenMixin, View):
    context = {
        'title': 'Личный кабинет'
    }

    def get(self, request, *args, **kwargs):
        user_pk = request.user.pk

        user = self.get_cache_for_context(cache_name=f'user_profile_cache_{user_pk}',
                                          url=request.build_absolute_uri(reverse(
                                              'users:inf_about_user_profile', args=[user_pk]
                                          )),
                                          headers=self.get_auth_token(request), time=60 * 60)
        coupons = self.get_cache_for_context(cache_name=settings.COUPONS_CACHE_NAME,
                                             url=request.build_absolute_uri(reverse('bonuses:coupon-list')), time=60 * 60)
        self.context['user'] = user
        self.context['coupons'] = coupons
        return render(request, 'users/profile.html', context=self.context)


class UserChangeProfileView(LoginRequiredMixin, View):
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

    @action(detail=True, methods=['get'], permission_classes=[IsAdminOrAuthenticatedReadOnly])
    def get_queryset(self):
        return CustomUser.objects.filter(id=self.kwargs['pk'])
