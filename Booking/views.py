from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework import views, status, generics
from rest_framework.response import Response
from datetime import datetime

from Booking.models import Schedule, Booking
from Booking.serializers import ScheduleSerializer, BookingSerializer
from Booking.forms import BookingForm
from mixins.mixins import GetCacheMixin


class ScheduleView(GetCacheMixin, TemplateView):
    template_name = 'booking/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Онлайн-запись'
        user = self.request.user
        if user.is_authenticated:
            data = {'name': user.username, 'phone': user.phone}
            form = BookingForm(data)
            context['form'] = form
        else:
            context['form'] = BookingForm
        inf = self.get_cache_for_context(cache_name=settings.MAIN_INFORMATION_CACHE_NAME,
                                         url=(reverse('main:information')), time=60*60)
        context['inf'] = inf
        return context


class ScheduleDayAPIView(views.APIView):
    def get(self, request):
        day = request.GET['day']
        today = datetime.today()
        date = datetime.strptime(f'{today.year}-{today.month}-{day}', '%Y-%m-%d').date()
        queryset = Schedule.objects.filter(date=date)
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)


class ScheduleTimeAPIView(views.APIView):
    def get(self, request):
        day = request.GET['day']
        time = request.GET['time']
        today = datetime.today()
        date = datetime.strptime(f'{today.year}-{today.month}-{day}', '%Y-%m-%d').date()
        queryset = Schedule.objects.filter(date=date, time=time)
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)


class BookingAPIDelete(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingAPIView(views.APIView):

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if not request.session.session_key:
            request.session.create()
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.validated_data['user'] = request.user
                serializer.validated_data['session_key'] = None
                serializer.validated_data['birthday'] = request.user.birthday
            else:
                serializer.validated_data['user'] = None
                serializer.validated_data['session_key'] = request.session.session_key
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        booking = Booking.objects.all()
        return Response(BookingSerializer(booking, many=True).data)
