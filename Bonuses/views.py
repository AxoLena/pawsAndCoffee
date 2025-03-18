from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from Bonuses.models import Coin, Coupon
from Bonuses.serializers import CoinSerializer, CouponCompareSerializer, CouponSerializer


class CoinUpdateAPIView(generics.UpdateAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.count = instance.reducing(request.data['coins'])
        instance.save()
        return super().update(request, *args, **kwargs)


class CouponAPIView(views.APIView):
    def get(self, request):
        coupons = Coupon.objects.all()
        return Response(CouponSerializer(coupons, many=True).data)


class CouponCompareAPIView(generics.GenericAPIView):
    serializer_class = CouponCompareSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if request.user.is_authenticated:
            serializer.birthday = request.user.birthday
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
