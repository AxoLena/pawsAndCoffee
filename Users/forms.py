from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms

from Users.models import User


class UserRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'birthday', 'password', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control inpt', 'placeholder': 'Введите ваш логин'}),
            'phone': forms.TextInput(attrs={'class': 'form-control inpt', 'placeholder': '(000) 000-0000', 'id': 'id_phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control inpt', 'placeholder': 'Введите ваш адрес эл. почты'}),
        }

    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': "form-control inpt", 'type': 'date'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control inpt",
                                                                  'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control inpt", 'placeholder': 'Повторите пароль'}))


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control inpt', 'placeholder': 'Введите ваш адрес эл. почты'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control inpt", 'placeholder': 'Введите пароль'}))


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'birthday', 'coins', 'booking']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый логин'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(000) 000-0000', 'id': 'id_phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый адрес эл. почты'}),
        }

    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': "form-control", 'type': 'date'}), required=False)


class UserChangeProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'birthday', 'password', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый логин'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(000) 000-0000', 'id': 'id_phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый адрес эл. почты'}),
        }

    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': "form-control", 'type': 'date'}), required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                  'placeholder': 'Введите новый пароль'}))
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Повторите пароль'}))
