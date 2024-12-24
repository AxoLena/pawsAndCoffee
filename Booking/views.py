from django.shortcuts import render
from django.views.generic import TemplateView


class ScheduleView(TemplateView):
    template_name = 'booking/schedule.html'