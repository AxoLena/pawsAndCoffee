from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from Bonuses.models import Coin


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email, username, password=None, birthday=None):
        if not phone:
            raise ValueError('User must have an phone')
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError("User must have a password")
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            birthday=birthday,
        )
        user.username = username
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, username, password=None, birthday=None, **kwargs):
        if not phone:
            raise ValueError('User must have an phone')
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            birthday=birthday,
            is_superuser=True,
            **kwargs
        )
        user.username = username
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, email, username, password=None, birthday=None, **kwargs):
        if not phone:
            raise ValueError('User must have an phone')
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            birthday=birthday,
            **kwargs
        )
        user.username = username
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, PermissionsMixin):
    ADMIN = 'admin'
    STAFF = 'staff'
    STATUS = [
        (ADMIN, 'Admin User'),
        (STAFF, 'Staff User'),
    ]

    username = models.CharField(unique=False, verbose_name='Имя пользователя', max_length=30)
    phone = models.CharField(unique=True, verbose_name='номер телефона', db_index=True)
    email = models.EmailField(max_length=254, unique=True, verbose_name='Эл. почта')
    coins = models.OneToOneField(to=Coin, on_delete=models.CASCADE, verbose_name='Мяукоины', null=True, blank=True, related_name='customuser')
    birthday = models.DateField(blank=True, null=True, verbose_name='дата рождения')
    session_key = models.CharField(max_length=32, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'username']

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f'{self.username}'

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
