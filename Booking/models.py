from django.db import models

from Main.models import Address


class BookingInformation(models.Model):
    TIME_CHOICE = [
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
    ]
    date = models.DateField(verbose_name='Дата посещения')
    time = models.CharField(choices=TIME_CHOICE, max_length=5, verbose_name='Время посещения')
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE, verbose_name='Адресс кафе')
    cost = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name="Стандартная стоимость посещения")
    duration_of_the_visit = models.PositiveSmallIntegerField(verbose_name="Продолжительность посещения")
    number_of_places = models.PositiveSmallIntegerField(verbose_name="Количество мест")

    def __str__(self):
        return f'Дата: {self.date}, время: {self.time}, места: {self.number_of_places}'

    def available_places(self):
        pass

    class Meta:
        db_table = 'Booking information'
        verbose_name = 'Информация о посещении'
        verbose_name_plural = 'Информацию о посещении'


class Booking(models.Model):
    inf_about_booking = models.ForeignKey(to=BookingInformation, on_delete=models.CASCADE, verbose_name="Информация о бронировании")
    cost = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name="Стоимость посещения")

    def __str__(self):
        return f'Дата: {self.inf_about_booking.date}, время: {self.inf_about_booking.time}'

    class Meta:
        db_table = 'Booking'
        verbose_name = 'Информация о брони'
        verbose_name_plural = 'Информацию о брони'