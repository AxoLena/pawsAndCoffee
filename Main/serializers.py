from rest_framework import serializers

from Main.models import InfAboutCafe, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        depth = 1


class InfAboutCafeSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = InfAboutCafe
        fields = '__all__'