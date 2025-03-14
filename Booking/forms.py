from django import forms

from Booking.models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
         model = Booking
         fields = ['quantity', 'name', 'phone']
         widgets = {
             'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5', 'value': '1', 'id': 'quantity'}),
             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
             'phone': forms.TextInput(
                 attrs={'class': 'form-control', 'placeholder': '(000) 000-0000', 'id': 'id_phone'})
         }
