from rest_framework import serializers

from Bonuses.serializers import CouponSerializer
from Booking.models import Schedule, Booking
from Cats.serializers import phone_validate, russian_validator
from Main.models import Address
from Main.serializers import AddressSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    time = serializers.CharField(source='get_time_display')

    class Meta:
        model = Schedule
        fields = '__all__'

    def create(self, validated_data):
        schedule = Schedule.objects.create(
            date=validated_data['date'],
            time=validated_data['time'],
        )
        return schedule


class BookingSerializer(serializers.ModelSerializer):
    address_id = serializers.IntegerField()
    is_paid = serializers.SerializerMethodField()
    is_inactive = serializers.SerializerMethodField()
    phone = serializers.CharField(validators=[phone_validate])
    name = serializers.CharField(validators=[russian_validator])
    coupon = serializers.CharField(source='coupon.code', required=False)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'session_key']
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key in ['user', 'address_id']:
            representation.pop(key, None)
        return representation

    def validate(self, attrs):
        cost = attrs['cost']
        quantity = attrs['quantity']
        coupon = attrs['coupon']
        bonuses = attrs['bonuses']
        if coupon:
            coupon_serializer = CouponSerializer(data=coupon)
            if coupon_serializer.is_valid(raise_exception=True):
                attrs['coupon'] = coupon_serializer.validated_data
        if ((float(cost) * int(quantity)) - int(bonuses)) < 1:
            raise serializers.ValidationError({'coins': 'Сумма оплаты не должна быть меньше 1 рубля!'})
        if coupon and bonuses != 0:
            raise serializers.ValidationError({
                'code': 'Невозможно использовать промокод и бонусы вместе, необходимо использовать что-то одно!',
                'coins': 'Невозможно использовать промокод и бонусы вместе, необходимо использовать что-то одно!',
            })
        return attrs

    def get_is_inactive(self, obj):
        return obj.is_inactive()

    def address_create(self, obj):
        return Address.objects.get(id=obj.address_id)

    def get_is_paid(self, obj):
        return 'оплачен' if obj.is_paid else 'ожидание'

    def create(self, validated_data):
        booking = Booking.objects.create(
            date=validated_data['date'],
            time=validated_data['time'],
            quantity=validated_data['quantity'],
            cost=validated_data['cost'],
            address_id=validated_data['address_id'],
            user=validated_data['user'],
            session_key=validated_data['session_key'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            name=validated_data['name'],
            bonuses=validated_data['bonuses'],
            coupon=validated_data['coupon']
        )
        booking.address = self.address_create(booking)
        return booking
