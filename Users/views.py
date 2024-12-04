from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework.generics import ListAPIView

from Users.forms import UserLoginForm, UserProfileForm, UserChangeProfileForm, UserRegForm
from Users.serializers import UserProfileSerializer
from Users.models import User


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


class UserProfileView(View):
    context = {
        'title': 'Личный кабинет'
    }

    def get(self, request):
        form = UserProfileForm
        self.context['form'] = form
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


class UserLogoutView(View):
    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def post(self, request):
        if self.is_ajax():
            response = HttpResponseRedirect(reverse('main:index'))
            response.delete_cookie('auth-token')
            return response
        return HttpResponse(status=500)


class UserAccountsListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
