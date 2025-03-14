from django.contrib import admin

from Users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['booked', 'birthday']
    list_display = ['username', 'phone', 'email']
