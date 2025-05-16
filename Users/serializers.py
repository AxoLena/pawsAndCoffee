import re
from datetime import date

from rest_framework import serializers

from Users.models import CustomUser
from Booking.serializers import BookingSerializer
from Cats.serializers import GuardianshipSerializer
from Bonuses.serializers import CoinSerializer


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
        model = CustomUser
        fields = ['username', 'email', 'phone', 'birthday', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password2'] != attrs['password']:
            raise serializers.ValidationError({'password2': 'Пароли не совпадают'})
        if CustomUser.objects.filter(phone=attrs['phone']):
            raise serializers.ValidationError({'phone': 'Пользователь с таким телефон уже существует'})
        return attrs

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            birthday=validated_data['birthday'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_validate])
    birthday = serializers.DateField(validators=[birthday_validate], required=False, default=None, allow_null=True)
    booking = BookingSerializer(many=True, required=False)
    guardianship = GuardianshipSerializer(many=True, required=False)
    coins = CoinSerializer()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'birthday', 'coins', 'booking', 'guardianship', 'id']

    def validate(self, attrs):
        user = self.context['request'].user
        if CustomUser.objects.filter(phone=attrs['phone']) and not (user.phone == attrs['phone']):
            raise serializers.ValidationError({'phone': 'Пользователь с таким телефон уже существует'})
        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.save()
        return instance
