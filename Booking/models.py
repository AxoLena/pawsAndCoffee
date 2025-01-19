import datetime

from django.db import models

from Main.models import Address


class Schedule(models.Model):
    TIME_CHOICE = [
        ('0', '10:00'),
        ('1', '11:00'),
        ('2', '12:00'),
        ('3', '13:00'),
        ('4', '15:00'),
        ('5', '16:00'),
        ('6', '17:00'),
        ('7', '18:00'),
    ]
    date = models.DateField(verbose_name='Дата посещения')
    time = models.CharField(choices=TIME_CHOICE, max_length=5, verbose_name='Время посещения')
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE, verbose_name='Адресс кафе', default=1)
    cost = models.DecimalField(default=400.00, max_digits=5, decimal_places=2, verbose_name="Стандартная стоимость посещения")
    # duration_of_the_visit = models.TimeField(verbose_name="Продолжительность посещения", default=datetime.time(1, 00))
    number_of_places = models.PositiveSmallIntegerField(verbose_name="Количество мест", default=5)

    def __str__(self):
        return f'Дата: {self.date}, время: {self.time}, места: {self.number_of_places}'

    def available_places(self):
        pass

    class Meta:
        db_table = 'Booking information'
        verbose_name = 'Информация о посещении'
        verbose_name_plural = 'Информация о посещених'


class Booking(models.Model):
    date = models.DateField(verbose_name='Дата посещения')
    time = models.TimeField(verbose_name='Время посещения')
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE, verbose_name='Адресс кафе', default=1)
    cost = models.DecimalField(default=400.00, max_digits=5, decimal_places=2, verbose_name="Cтоимость посещения")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество человек')
    session_key = models.CharField(max_length=32, blank=True, null=True)
    user_pk = models.PositiveIntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False, verbose_name='Статус оплаты')

    class Meta:
        db_table = 'Booking'
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'