from django.urls import path

from Bonuses.views import CoinUpdateAPIView, CouponCompareAPIView, CouponAPIView

app_name = 'bonuses'

urlpatterns = [
    path('api/bonus/update/<int:pk>/', CoinUpdateAPIView.as_view()),
    path('api/coupon/compare/', CouponCompareAPIView.as_view()),
    path('api/coupon/list/', CouponAPIView.as_view(), name='coupon-list'),
]
