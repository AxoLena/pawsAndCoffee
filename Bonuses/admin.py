from django.contrib import admin

from Bonuses.models import Coin, Coupon, History


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ['customuser', 'count']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['coin', 'created_timestamp', 'count', 'description']
