import datetime
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import re_path

from Booking.models import Schedule, Booking


@admin.register(Schedule)
class BookingInformationAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'number_of_places']
    change_list_template = "admin/Booking_change_list.html"

    def get_urls(self):
        urls = super(BookingInformationAdmin, self).get_urls()
        custom_urls = [
            re_path('^import/delete/$', self.delete_schedule, name='delete_schedule'),
            re_path('^import/create/$', self.create_schedule, name='create_schedule'),
        ]
        return custom_urls + urls

    def delete_schedule(self, request):
        s = Schedule.objects.all()
        s.delete()
        self.message_user(request, "все записи были удалены")
        return HttpResponseRedirect("../")

    def create_schedule(self, request):
        today = datetime.date.today()
        extrayear, month = divmod(today.month, 12)
        next_month = datetime.datetime(year=today.year + extrayear, month=month + 1, day=1)
        last_day_month = next_month - datetime.timedelta(days=1)
        dates = last_day_month.day - today.day
        count = 0
        if dates > 0:
            for i in range(int(today.day)-1, dates+int(today.day)):
                for k in range(8):
                    Schedule.objects.create(
                        date=datetime.datetime.strptime(f'{today.year}-{today.month}-{i + 1}', '%Y-%m-%d').date(),
                        time=f'{k}',
                    )
                    count += 1
        self.message_user(request, f"создано {count} новых записей")
        return HttpResponseRedirect("../")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'user', 'session_key']