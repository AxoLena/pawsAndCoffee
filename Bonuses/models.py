from django.db import models


class Coin(models.Model):
    count = models.PositiveIntegerField(verbose_name='Количество', default=0)

    def increased(self, discount, payment_amount, description):
        cost = (discount/100) * payment_amount
        self.count += cost
        History.objects.create(
            description=description,
            count=f'+{cost}',
            coin=self
        )
        return self.count

    def reducing(self, c):
        self.count -= c
        History.objects.create(
            description=f'Списание за бронь',
            count=f'-{c}',
            coin=self
        )
        return self.count

    def __str__(self):
        return f'{self.count}'

    class Meta:
        db_table = 'Bonuses'
        verbose_name = 'Мяукоин'
        verbose_name_plural = 'Мяукоины'


class History(models.Model):
    description = models.CharField(verbose_name='описание')
    count = models.CharField(verbose_name="Сумма начисления/списания")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата начисления')
    coin = models.ForeignKey(to=Coin, on_delete=models.CASCADE, verbose_name='Мяукоины пользователя',
                             blank=True, null=True, related_name='histories')

    class Meta:
        db_table = 'History'
        verbose_name = 'История'


class Coupon(models.Model):
    discount = models.PositiveIntegerField(verbose_name='Процент скидки')
    description = models.CharField(verbose_name='Описание')
    code = models.CharField(max_length=15, verbose_name='Код купона')

    def __str__(self):
        return f'{self.discount} - {self.description}'

    class Meta:
        db_table = 'Coupon'
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'