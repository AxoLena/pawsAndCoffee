from django.urls import path

from Booking.views import ScheduleView, ScheduleDayAPIView, ScheduleTimeAPIView, BookingAPIView, BookingAPIDelete

app_name = 'booking'

urlpatterns = [
    path('', ScheduleView.as_view(), name='schedule'),
    path('api/schedule/day/', ScheduleDayAPIView.as_view()),
    path('api/schedule/time/', ScheduleTimeAPIView.as_view()),
    path('api/booking/', BookingAPIView.as_view()),
    path('api/booking/<int:pk>', BookingAPIDelete.as_view()),
]
