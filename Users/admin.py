from django.contrib import admin

from Users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['booked', 'birthday']
    list_display = ['username', 'phone', 'email']
