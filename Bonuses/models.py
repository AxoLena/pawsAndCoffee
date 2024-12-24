from django.db import models


class Coin(models.Model):
    count = models.PositiveIntegerField(default=0, verbose_name='Количество')
    description = models.CharField(verbose_name='История', blank=True, null=True)

    def increased(self, c):
        self.count += c
        self.description = ''
        return self.count

    def reducing(self, c):
        self.count -= c
        self.description = ''
        return self.count

    def __str__(self):
        return f'{self.count}'

    class Meta:
        db_table = 'Bonuses'
        verbose_name = 'Мяукоин'
        verbose_name_plural = 'Мяукоины'


class Discount(models.Model):
    percent = models.PositiveIntegerField(verbose_name='Процент скидки')
    description = models.CharField(verbose_name='Описание')

    def __str__(self):
        return f'{self.percent} - {self.description}'

    class Meta:
        db_table = 'Discount'
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'