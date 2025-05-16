from django.contrib import admin

from Cats.models import Cats, FormForGuardianship, FormForGive, FormForAdopt


@admin.register(Cats)
class CatAdmin(admin.ModelAdmin):
    list_display = ['name', 'birthday', 'gender', 'breed', 'id']
    search_fields = ['gender']


@admin.register(FormForGuardianship)
class GuardianshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'cat_name', 'plan']


@admin.register(FormForGive)
class GiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'cat_name', 'birthday', 'gender']


@admin.register(FormForAdopt)
class AdoptAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'cat_name']