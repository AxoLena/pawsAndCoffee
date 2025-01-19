from django import forms

from Booking.models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
         model = Booking
         fields = ['quantity']
         widgets = {
             'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
         }
