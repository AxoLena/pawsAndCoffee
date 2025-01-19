from rest_framework import serializers

from Booking.models import Schedule, Booking
from Main.serializers import AddressSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
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
    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        booking = Booking.objects.create(
            date=validated_data['date'],
            time=validated_data['time'],
            address=validated_data['address'],
            quantity=validated_data['quantity'],
            cost=validated_data['cost'],
            user_pk=validated_data['user_pk'],
            session_key=validated_data['session_key'],
        )
        return booking
