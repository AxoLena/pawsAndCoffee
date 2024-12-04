from django.contrib import admin

from Main.models import InfAboutCafe, Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'street', 'house_number']


@admin.register(InfAboutCafe)
class InfAboutCafe(admin.ModelAdmin):
    list_display = ['address', 'phone', 'cost']