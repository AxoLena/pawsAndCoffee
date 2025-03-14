from django.contrib import admin

from Payment.models import ProductStripe, PriceStripe, CheckoutSessionStripe


@admin.register(ProductStripe)
class ProductStripeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(PriceStripe)
class PriceStripeAdmin(admin.ModelAdmin):
    list_display = ['name', 'product']


@admin.register(CheckoutSessionStripe)
class CheckoutSessionStripe(admin.ModelAdmin):
    list_display = ['created_timestamp', 'is_completed']
