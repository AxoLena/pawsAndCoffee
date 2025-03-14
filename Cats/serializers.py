import re
from datetime import date
from rest_framework import serializers

from Cats.models import Cats, FormForGuardianship, FormForGive, FormForAdopt


def russian_validator(value):
    allowed_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЪЫЭЮЯабвгдеёжзийклмнопрстуфхцчшщьъыэюя- "
    code = 'russian'
    if not (set(value) <= set(allowed_chars)):
        raise serializers.ValidationError("Поле должно состоять только из русских символов, дефис и пробел.", code=code)


def phone_validate(value):
    if not value.isdigit():
        raise serializers.ValidationError('Номер телефона должен состоять только из цифр')
    pattern = re.compile(r'^\d{12}$')
    if not pattern.match(value):
        raise serializers.ValidationError('Неверный формат')


class CatsSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    cat_age = serializers.SerializerMethodField()

    class Meta:
        model = Cats
        fields = '__all__'
        depth = 1

    def get_cat_age(self, obj):
        return obj.cat_age()


class AdoptSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_validate])
    name = serializers.CharField(validators=[russian_validator])

    class Meta:
        model = FormForAdopt
        fields = '__all__'

    def create(self, validated_data):
        adopt = FormForAdopt.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            social=validated_data['social'],
            cat_name=validated_data['cat_name'],
            why_this_cat=validated_data['why_this_cat'],
            children=validated_data['children'],
            has_pet=validated_data['has_pet'],
            pets=validated_data['pets']
        )
        return adopt


class GiveSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_validate])
    name = serializers.CharField(validators=[russian_validator])
    cat_name = serializers.CharField(validators=[russian_validator])

    class Meta:
        model = FormForGive
        fields = '__all__'

    def validate(self, attrs):
        birthday = attrs['birthday']
        if birthday > date.today():
            raise serializers.ValidationError({'birthday': 'Нельзя указывать еще ненаступившую дату'})
        last_date = date(2014, 1, 1)
        if birthday < last_date:
            raise serializers.ValidationError({'birthday': 'Нельзя указать дату, которой больше 20 лет'})
        return attrs

    def create(self, validated_data):
        give = FormForGive.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            social=validated_data['social'],
            cat_name=validated_data['cat_name'],
            birthday=validated_data['birthday'],
            character=validated_data['character'],
            features=validated_data['features'],
            gender=validated_data['gender'],
            type_of_help=validated_data['type_of_help'],
            reason=validated_data['reason'],
            image=validated_data['image']
        )
        return give


class GuardianshipSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_validate])
    name = serializers.CharField(validators=[russian_validator])
    user = serializers.CharField(source='user.id', default=None)
    plan = serializers.CharField(required=False)
    cat_name = serializers.CharField(source='cat_name.name')

    class Meta:
        model = FormForGuardianship
        fields = '__all__'
        # depth = 1

    def create(self, validated_data):
        guardianship = FormForGuardianship.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            social=validated_data['social'],
            cat_name=validated_data['cat_name'],
            amount_of_money=validated_data['amount_of_money'],
            interval=validated_data['interval'],
            user=validated_data['user'],
            session_key=validated_data['session_key']
        )
        return guardianship

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.session_key = validated_data.get('session_key', instance.session_key)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
