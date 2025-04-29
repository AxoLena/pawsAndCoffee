import stripe
from currency_converter import CurrencyConverter
from django.core.exceptions import ValidationError
from django.db import models


class ProductStripe(models.Model):
    name = models.CharField(verbose_name='Название')
    description = models.CharField(verbose_name='Описание')
    product_id = models.CharField(unique=True)

    class Meta:
        db_table = 'Products'
        verbose_name = f"Продукт для подписки"
        verbose_name_plural = f"Продукты для подписки"

    def __str__(self):
        return f'Котик {self.name}'

    def delete(self, *args, **kwargs):
        try:
            stripe.Product.delete(self.product_id)
            super(ProductStripe, self).delete(*args, **kwargs)
        except Exception as e:
            raise ValidationError(str(e))


class PriceStripe(models.Model):
    product = models.ForeignKey(to=ProductStripe, on_delete=models.CASCADE, verbose_name='Продукт')
    name = models.CharField(verbose_name='Название')
    unit_amount = models.CharField(verbose_name='Сумма на опекунство')
    interval = models.CharField(verbose_name='Интервал')
    currency = models.CharField(verbose_name='Валюта', default='usd')
    price_id = models.CharField(unique=True, null=True, blank=True)

    def format_amount_to_stripe(self):
        c = CurrencyConverter()
        return int(c.convert(float(self.unit_amount), 'RUB', 'USD') * 100)

    def save(self, *args, **kwargs):
        is_exists = False
        prices = stripe.Price.list()
        for price in prices.data:
            if (price.nickname == self.name
                    and price.unit_amount == self.format_amount_to_stripe()
                    and price.recurring.interval == self.interval):
                if not PriceStripe.objects.filter(unit_amount=self.unit_amount, interval=self.interval, product=self.product).exists():
                    self.price_id = price.id
                    is_exists = True
        if not is_exists:
            try:
                price = stripe.Price.create(
                    nickname=self.name,
                    currency=self.currency,
                    recurring={'interval': self.interval},
                    unit_amount=self.format_amount_to_stripe(),
                    product=self.product.id
                )
                self.price_id = price.id
            except Exception as e:
                raise ValidationError(str(e))
        super(PriceStripe, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Price'
        verbose_name = f"Цена подписки"
        verbose_name_plural = f"Цены подписок"


class CheckoutSessionStripe(models.Model):
    checkout_session_id = models.CharField(unique=True)
    customer_id = models.CharField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    price_id = models.ForeignKey(to=PriceStripe, on_delete=models.CASCADE)
    subscription_id = models.CharField(blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    class Meta:
        db_table = 'CheckoutSessionStripe'
        verbose_name = f"Информация о сесссии"
        verbose_name_plural = f"Информация о сесссиях"
