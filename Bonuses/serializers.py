import datetime

from rest_framework import serializers

from Bonuses.models import Coin, Coupon, History
from Booking.models import Booking


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'description', 'count', 'created_timestamp']


class CoinSerializer(serializers.ModelSerializer):
    histories = HistorySerializer(many=True, required=False)

    class Meta:
        model = Coin
        fields = '__all__'
        depth = 1


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CouponCompareSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    quantity = serializers.IntegerField()
    birthday = serializers.DateTimeField(required=False, default=None)

    class Meta:
        model = Coupon
        fields = ['code', 'birthday', 'phone', 'quantity']

    def validate(self, attrs):
        code = attrs['code']
        phone = attrs['phone']
        quantity = attrs['quantity']
        birthday = attrs['birthday']
        booking = Booking.objects.filter(phone=phone)
        match code:
            case 'FULLOFROMANTIC':
                if quantity != 2:
                    raise serializers.ValidationError({'code': 'Этот промокод можно использовать только на компанию из двоих человек!'})
            case 'CATINPARTYHAD':
                if not birthday or birthday != datetime.date.today():
                    raise serializers.ValidationError({'code': 'Этот промокод можно использовать только в ваш день рождения! '
                                                               'Укажите вашу дату рождения при регистраци, чтобы мы могли подтвердить информацию.'})
            case 'FIRSTMEOW':
                if booking:
                    raise serializers.ValidationError({'code': 'Этот промокод можно использовать только на первый заказ!'})
            case 'MEOWX2':
                if booking.count() > 1 and booking:
                    raise serializers.ValidationError(
                        {'code': 'Этот промокод можно использовать только на второй заказ!'})
            case _:
                raise serializers.ValidationError({'code': 'Промокод не найден'})
        return {'code': code}
