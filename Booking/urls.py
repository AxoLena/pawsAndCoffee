from django.urls import path

from Booking.views import ScheduleView

app_name = 'booking'

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
]