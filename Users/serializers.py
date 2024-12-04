import re
from datetime import date

from rest_framework import serializers

from Users.models import User


def phone_validate(value):
    if not value.isdigit():
        raise serializers.ValidationError('Номер телефона должен состоять только из цифр')
    pattern = re.compile(r'^\d{11}$')
    if not pattern.match(value):
        raise serializers.ValidationError('Неверный формат')


def birthday_validate(value):
    if value > date.today():
        raise serializers.ValidationError('Нельзя указывать еще ненаступившую дату')
    last_date = date(1924, 1, 1)
    if value < last_date:
        raise serializers.ValidationError('Нельзя указать дату, которой более 100 лет')


class UserRegSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_validate])
    password2 = serializers.CharField(write_only=True)
    birthday = serializers.DateField(validators=[birthday_validate], required=False, default=None)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'birthday', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password2'] != attrs['password']:
            raise serializers.ValidationError({'password2': 'Пароли не совпадают'})
        if User.objects.filter(phone=attrs['phone']):
            raise serializers.ValidationError({'phone': 'Пользователь с таким телефон уже существует'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            birthday=validated_data['birthday'],
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
