from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from Bonuses.models import Coupon
from Bonuses.serializers import CouponSerializer


class CouponAPIViewTestCase(APITestCase):
    def test_get(self):
        test_coupon = Coupon.objects.create(discount=12, description='test coupon', code='TEST!1')
        url = reverse('bonuses:coupon-list')
        print(url)
        response = self.client.get(url)
        serializer_data = CouponSerializer(test_coupon).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        print(response)

