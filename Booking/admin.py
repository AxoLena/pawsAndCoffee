from django.contrib import admin

from Booking.models import BookingInformation


@admin.register(BookingInformation)
class BookingInformationAdmin(admin.ModelAdmin):
    list_display = ['date', 'number_of_places']
