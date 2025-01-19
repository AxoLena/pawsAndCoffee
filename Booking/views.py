from django.views.generic import TemplateView
from rest_framework import views, status
from rest_framework.response import Response
from datetime import datetime

from Booking.models import Schedule, Booking
from Booking.serializers import ScheduleSerializer, BookingSerializer
from Booking.forms import BookingForm


class ScheduleView(TemplateView):
    template_name = 'booking/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Онлайн-запись'
        context['form'] = BookingForm
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


class BookingAPIView(views.APIView):

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['cost'] = 400
            if request.user.is_authenticated:
                serializer.validated_data['user_pk'] = request.user.pk
                serializer.validated_data['session_key'] = None
            else:
                serializer.validated_data['user_pk'] = None
                serializer.validated_data['session_key'] = request.session.session_key
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        booking = Booking.objects.all()
        return Response({'posts': BookingSerializer(booking, many=True).data})
