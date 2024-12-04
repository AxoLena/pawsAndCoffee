from django.db import models


class Address(models.Model):
    city = models.CharField(verbose_name="Город")
    street = models.CharField(verbose_name="Улица")
    house_number = models.CharField(verbose_name="Номер строения")

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house_number}'

    class Meta:
        db_table = 'Address'
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class InfAboutCafe(models.Model):
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE, default=None, verbose_name="Адрес кафе")
    phone = models.CharField(unique=True, verbose_name="Номер телефона")
    working_hours = models.CharField(verbose_name="Часы работы")
    count_of_cats = models.PositiveIntegerField(verbose_name="Количество котов")
    cost = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name="Стоимость посещения")
    duration_of_the_visit = models.PositiveSmallIntegerField(verbose_name="Продолжительность посещения")

    def __str__(self):
        return f'{self.address}'

    class Meta:
        db_table = 'Information'
        verbose_name = 'Информаци о кафе'
        verbose_name_plural = 'Информацию о кафе'
