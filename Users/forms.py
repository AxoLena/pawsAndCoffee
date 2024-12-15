from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.core.exceptions import ValidationError

from Users.models import User


def validate_password(pas, re_pas):
    if re_pas != pas:
        raise ValidationError("Пароли не совпадают")
    else:
        return re_pas


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


class UserChangeProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'birthday', 'current_password', 'new_password', 're_new_password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый логин'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(000) 000-0000', 'id': 'id_phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый адрес эл. почты'}),
        }

    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': "form-control", 'type': 'date'}), required=False)
    current_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                  'placeholder': 'Введите текущий пароль'}))
    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                                 'placeholder': 'Введите новый пароль'}))
    re_new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                  'placeholder': 'Подтвердите пароль'}))


class UserResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес эл. почты'}))


class UserSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password', 're_new_password']

    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                                     'placeholder': 'Введите новый пароль'}))
    re_new_password = forms.CharField(required=False, validators=[validate_password],
                                      widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Подтвердите новый пароль'}))