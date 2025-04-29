from datetime import date as d
from django.db import models
from django.db.models import Q

from Users.models import CustomUser
from Payment.models import ProductStripe, PriceStripe, CheckoutSessionStripe
from Cats.tasks import create_product


class Cats(models.Model):
    FEM = 'FEMALE'
    MAN = 'MALE'
    GENDER_CHOICE = [
        (FEM, 'кошечка'),
        (MAN, 'кот'),
    ]
    name = models.CharField(max_length=100, unique=True, verbose_name='Кличка')
    birthday = models.DateField(default=d.today, verbose_name='Дата рождения')
    gender = models.CharField(max_length=7, choices=GENDER_CHOICE, default=FEM, verbose_name='Пол')
    description = models.TextField(max_length=500, verbose_name='Описание')
    breed = models.CharField(blank=True, null=True, verbose_name='Порода')
    image = models.ImageField(upload_to='cats_images', blank=True, null=True, verbose_name='Фотография котика')

    def cat_age(self):
        today = d.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def save(self, *args, **kwargs):
        name = self.name
        product_is_exists = ProductStripe.objects.filter(name=name).exists()
        if not product_is_exists:
            description = f'Подписка на поддержание котика {name}'
            product = ProductStripe.objects.create(name=name, description=description)
            create_product.delay(name=name, description=description, id=product.id)
        super(Cats, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        product = ProductStripe.objects.get(name=self.name).delete()
        super(Cats, self).delete(*args, **kwargs)

    def __str__(self):
        return f'Котик {self.name}'

    class Meta:
        db_table = 'Cats'
        verbose_name = 'Котик'
        verbose_name_plural = 'Котики'


class FormForAdopt(models.Model):
    name = models.CharField(verbose_name='Имя')
    phone = models.CharField(verbose_name='Номер телефона')
    email = models.EmailField(max_length=254, verbose_name='Адресс эл. почты')
    social = models.URLField(blank=True, null=True, verbose_name='Ссылка на соц. сети')
    cat_name = models.ForeignKey(to=Cats, on_delete=models.CASCADE, verbose_name='Имя котика')
    why_this_cat = models.TextField(verbose_name='Причины взять котика')
    children = models.BooleanField(default=False, verbose_name='Есть дети?')
    has_pet = models.BooleanField(default=False, verbose_name='Есть другие животные?')
    pets = models.TextField(blank=True, null=True, verbose_name='Какие питомцы еще есть')

    class Meta:
        db_table = 'Adopt'
        verbose_name = f" Анкета 'Взять в семью'"
        verbose_name_plural = f" Анкета 'Взять в семью'"

    def __str__(self):
        return f'Имя котика: {self.cat_name}, кто забирает: {self.name}'


class FormForGuardianship(models.Model):
    AMOUNT_OF_MONEY = [
        ('400', '400'),
        ('800', '800'),
        ('1000', '1000'),
        ('1500', '1500'),
    ]
    INTERVAL = [
        ('month', 'Месяц'),
        ('year', 'Год'),
    ]
    name = models.CharField(verbose_name='Имя')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='дата создания заказа')
    phone = models.CharField(verbose_name='Номер телефона')
    email = models.EmailField(max_length=254, verbose_name='Адресс эл. почты')
    social = models.URLField(blank=True, null=True, verbose_name='Ссылка на соц. сети')
    cat_name = models.ForeignKey(to=ProductStripe, on_delete=models.CASCADE, verbose_name='Имя котика')
    plan = models.ForeignKey(to=PriceStripe, on_delete=models.CASCADE, verbose_name='План подписки', default=None)
    amount_of_money = models.CharField(max_length=4, choices=AMOUNT_OF_MONEY, default='400', verbose_name='Сумма на опекунство')
    interval = models.CharField(max_length=11, choices=INTERVAL, default='month', verbose_name='Интервал')
    session_key = models.CharField(max_length=32, blank=True, null=True)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             null=True, blank=True, related_name='guardianship', db_index=True)
    is_paid = models.BooleanField(default=False, verbose_name='Статус оплаты')
    pay_session = models.ForeignKey(to=CheckoutSessionStripe, on_delete=models.CASCADE, null=True, blank=True, default=None)
    payment_method = models.CharField(null=True, blank=True)

    class Meta:
        db_table = 'Guardianship'
        verbose_name = f" Анкета 'Оформить опекунство'"
        verbose_name_plural = f" Анкета 'Оформить опекунство'"
        indexes = [
            models.Index(fields=['session_key'], condition=Q(session_key__isnull=False),
                         name='guardian_session_key_not_null')
        ]

    def save(self, *args, **kwargs):
        plan = PriceStripe.objects.filter(unit_amount=self.amount_of_money, interval=self.interval, product=self.cat_name)
        if plan:
            self.plan = plan.first()
        else:
            self.plan = PriceStripe.objects.create(product=self.cat_name, name=f'Price for {self.cat_name.name}',
                                                   unit_amount=self.amount_of_money, interval=self.interval)
        super(FormForGuardianship, self).save(*args, **kwargs)

    def __str__(self):
        return f'Имя котика: {self.cat_name}, кто оформил опекунство: {self.name}'


class FormForGive(models.Model):
    CURATOR = 'CURATOR'
    HELPER = 'HELPER'
    TYPE_OF_HELP = [
        (CURATOR, 'Я куратор, хочу с вами сотрудничать'),
        (HELPER, 'Я хочу разово помочь одному животному')
    ]
    FEM = 'FEMALE'
    MAN = 'MALE'
    GENDER_CHOICE = [
        (FEM, 'кошечка'),
        (MAN, 'кот'),
    ]
    name = models.CharField(verbose_name='Имя')
    phone = models.CharField(verbose_name='Номер телефона')
    email = models.EmailField(max_length=254, verbose_name='Адресс эл. почты')
    social = models.URLField(blank=True, null=True, verbose_name='Ссылка на соц. сети')
    cat_name = models.CharField(max_length=100, verbose_name='Кличка')
    birthday = models.DateField(verbose_name='Дата рождения')
    character = models.TextField(verbose_name='Характер коткика')
    features = models.TextField(verbose_name='Особенности котика')
    gender = models.CharField(max_length=7, choices=GENDER_CHOICE, default=FEM, verbose_name='Пол')
    type_of_help = models.CharField(max_length=37, choices=TYPE_OF_HELP, default=HELPER, verbose_name='Тип помощи')
    reason = models.TextField(verbose_name='Причина передачить котика')
    image = models.ImageField(upload_to='give_cats', default=None, blank=True, null=True, verbose_name='Фотография котика')

    class Meta:
        db_table = 'Given'
        verbose_name = f" Анкета 'Передать кота в кафе'"
        verbose_name_plural = f" Анкета 'Передать кота в кафе'"

    def __str__(self):
        return f'ФИО: {self.name}, прчина передачи: {self.reason}'
